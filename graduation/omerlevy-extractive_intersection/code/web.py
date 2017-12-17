from cgi import escape
from collections import defaultdict
import hashlib
from itertools import groupby
from os import listdir
import datetime
import re
from threading import Lock
from os.path import join

import cherrypy
import docopt

from ds.alignment2entailment import generate_potential_entailments, generate_potential_extractions
from ds.alignment_validation import validate_alignments
from ds.entailment import create_entailments_dictionary
from ds.intersection import intersection
from ds.io import read_file, parse_entailments
from ds.nlg import generate_natural_language
from ds.sentence_tree import DynamicTree
from ds.sentences2alignment import generate_groups


class AlignmentEntailmentTask:

    def __init__(self, candidates_dir):
        self.lock = Lock()
        self.user_id_counter = 1000

        self.candidates = self.load_candidates(candidates_dir)
        print 'Loaded all candidates:'
        print '\n'.join(self.candidates.keys())

        self.LOGIN_HTML = self.load_html('web/html/login.html')
        self.ALIGNMENT_HTML = self.load_html('web/html/alignment.html')
        self.EXTRACTION_HTML = self.load_html('web/html/extraction.html')
        self.ENTAILMENT_HTML = self.load_html('web/html/entailment.html')
        self.GRAMMATICAL_HTML = self.load_html('web/html/grammatical.html')
        self.THANKS_HTML = self.load_html('web/html/thanks.html')
        self.NOTHANKS_HTML = self.load_html('web/html/nothanks.html')

    @staticmethod
    def load_candidates(path):
        candidates = []
        files = [join(path, f) for f in listdir(path)]
        for f in files:
            sentence1, sentence2, entailments = read_file(f)
            h = hashlib.new('sha1')
            h.update(generate_natural_language(sentence1) + ' ' + generate_natural_language(sentence2))
            candidates.append((h.hexdigest(), (sentence1, sentence2)))
        return dict(candidates)

    @staticmethod
    def load_html(path):
        with open(path) as fin:
            html = fin.read()
        with open('web/html/style.css') as fin:
            css = fin.read()
        with open(path[:-5] + '.js') as fin:
            javascript = fin.read()
        return html.replace('CSS', css).replace('SCRIPT', javascript)

    @cherrypy.expose
    def index(self):
        with self.lock:
            html = self.LOGIN_HTML
            candidate_options = [(candidate_id, ''.join((generate_natural_language(sentence1)[:20], '... | ', generate_natural_language(sentence2)[:20], '...')))
                                 for candidate_id, (sentence1, sentence2) in self.candidates.iteritems()]
            candidate_options = [CANDIDATE_HTML.replace('CANDIDATE_ID', candidate_id).replace('CANDIDATE', candidate)
                                 for candidate_id, candidate in candidate_options]
            html = html.replace('CANDIDATES', ''.join(candidate_options))
        return html

    @cherrypy.expose
    def alignment(self, **kwargs):
        with self.lock:
            html = self.ALIGNMENT_HTML

            if 'user_id' in kwargs:
                html = html.replace('USER_ID', kwargs['user_id'])
            else:
                html = html.replace('USER_ID', str(self.user_id_counter))
                self.user_id_counter += 1

            candidate_id = kwargs['candidate_id']
            html = html.replace('CANDIDATE_ID', candidate_id)

            sentence1, sentence2 = self.candidates[candidate_id]
            html = html.replace('SENTENCE1', self.generate_sentence_html(sentence1, 0))
            html = html.replace('SENTENCE2', self.generate_sentence_html(sentence2, 1))
            html = html.replace('GROUPS', str(generate_groups(sentence1, sentence2)))

        return html

    @staticmethod
    def generate_sentence_html(sentence, si):
        return ' '.join([TOKEN_HTML.replace('SINDEX', str(si+1)).replace('TINDEX', str(ti)).replace('TOKEN', t)
                         for ti, t in enumerate(generate_natural_language(sentence).split(' '))])

    @cherrypy.expose
    def extraction(self, **kwargs):
        with self.lock:
            user_id = kwargs['user_id']
            candidate_id = kwargs['candidate_id']
            alignments = kwargs['alignments']
            if self.validate_alignments(candidate_id, alignments):
                html = self.EXTRACTION_HTML
                html = html.replace('USER_ID', user_id)
                html = html.replace('CANDIDATE_ID', candidate_id)
                html = html.replace('ALIGNMENTS', alignments)
                prerequisites, equals, questionnaire = self.generate_extraction_questionnaire(candidate_id, alignments)
                html = html.replace('PREREQUISITES', str(dict(prerequisites)))
                html = html.replace('EQUALS', str(equals))
                html = html.replace('QUESTIONNAIRE', questionnaire)
            else:
                html = self.NOTHANKS_HTML
        return html

    def validate_alignments(self, candidate_id, alignments_str):
        sentence1, sentence2 = self.candidates[candidate_id]
        alignments = self.parse_alignments(alignments_str)
        return validate_alignments(sentence1, sentence2, alignments)

    def generate_extraction_questionnaire(self, candidate_id, alignments_str):
        sentence1, sentence2 = self.candidates[candidate_id]
        alignments = self.parse_alignments(alignments_str)
        extraction1, extraction2 = generate_potential_extractions(sentence1, sentence2, alignments)

        prerequisites = defaultdict(list)
        equals = []
        questions = []

        entailment, prerequisite, premise1, premise2, args1, args2, template1, template2 = extraction1
        entailment1 = entailment.replace('?', '>')
        hypothesis1 = self.generate_hypothesis(args1, args2, template2)
        question1 = ENTAILMENT_QUESTION_HTML.replace('HYPOTHESIS', hypothesis1).replace('PREMISE', premise1).replace('ENTAILMENT', escape(entailment1, True))
        questions.append(question1)
        if self.equal_string(premise1, hypothesis1):
            equals.append(entailment1)

        entailment, prerequisite, premise1, premise2, args1, args2, template1, template2 = extraction2
        entailment2 = entailment.replace('?', '<')
        hypothesis2 = self.generate_hypothesis(args2, args1, template1)
        question2 = ENTAILMENT_QUESTION_HTML.replace('HYPOTHESIS', hypothesis2).replace('PREMISE', premise2).replace('ENTAILMENT', escape(entailment2, True))
        questions.append(question2)
        if self.equal_string(premise2, hypothesis2):
            equals.append(entailment2)

        return prerequisites, equals, ''.join(questions)

    @cherrypy.expose
    def entailment(self, **kwargs):
        with self.lock:
            candidate_id = kwargs['candidate_id']
            alignments = kwargs['alignments']
            extractions_str = self.parse_entailments(kwargs)
            sentence1, sentence2 = self.extract_sentences(candidate_id, extractions_str)

            html = self.ENTAILMENT_HTML
            html = html.replace('USER_ID', kwargs['user_id'])
            html = html.replace('CANDIDATE_ID', candidate_id)
            html = html.replace('ALIGNMENTS', alignments)
            html = html.replace('EXTRACTIONS', extractions_str)
            prerequisites, equals, questionnaire = self.generate_entailment_questionnaire(sentence1, sentence2, alignments)
            html = html.replace('PREREQUISITES', str(dict(prerequisites)))
            html = html.replace('EQUALS', str(equals))
            html = html.replace('QUESTIONNAIRE', questionnaire)
        return html

    def extract_sentences(self, candidate_id, extractions_str):
        sentence1, sentence2 = self.candidates[candidate_id]
        entailments = self.get_real_entailments(sentence1, sentence2, extractions_str)
        sentence1 = self.extract_sentence(sentence1, entailments, '>')
        sentence2 = self.extract_sentence(sentence2, entailments, '<')
        return sentence1, sentence2

    @staticmethod
    def extract_sentence(sentence, entailments, direction):
        extractions = [entailment for entailment in entailments if entailment.type_ == direction]
        if len(extractions) == 0:
            new_root = sentence.root.children[0].modifier
        elif len(extractions) == 1:
            extraction = extractions[0]
            new_root = extraction.edges1[0].modifier if direction == '>' else extraction.edges2[0].modifier
        else:
            raise Exception('HORRIBLE BUG!!! More than one extraction per sentence!')
        return DynamicTree(None, new_root)

    def generate_entailment_questionnaire(self, sentence1, sentence2, alignments_str):
        alignments = self.parse_alignments(alignments_str)
        potential_entailments = generate_potential_entailments(sentence1, sentence2, alignments)

        prerequisites = defaultdict(list)
        equals = []
        questions = []
        for entailment, prerequisite, premise1, premise2, args1, args2, template1, template2 in potential_entailments:
            prerequisites[prerequisite].append(entailment)

            entailment1 = entailment.replace('?', '>')
            hypothesis1 = self.generate_hypothesis(args1, args2, template2)
            question1 = ENTAILMENT_QUESTION_HTML.replace('HYPOTHESIS', hypothesis1).replace('PREMISE', premise1).replace('ENTAILMENT', escape(entailment1, True))
            questions.append(question1)
            if self.equal_string(premise1, hypothesis1):
                equals.append(entailment1)

            entailment2 = entailment.replace('?', '<')
            hypothesis2 = self.generate_hypothesis(args2, args1, template1)
            question2 = ENTAILMENT_QUESTION_HTML.replace('HYPOTHESIS', hypothesis2).replace('PREMISE', premise2).replace('ENTAILMENT', escape(entailment2, True))
            questions.append(question2)
            if self.equal_string(premise2, hypothesis2):
                equals.append(entailment2)

        return prerequisites, equals, ''.join(questions)

    def generate_hypothesis(self, p_args, h_args, h_template):
        for slot_i, (h_slot, h_arg, h_aligned) in enumerate(h_args):
            aligned_p_args = [(p_slot, p_arg) for p_slot, p_arg, p_aligned in p_args if p_aligned == h_slot]
            if len(aligned_p_args) > 1:
                raise Exception('Double alignment. BUG!')
            elif len(aligned_p_args) == 1:
                p_slot, p_arg = aligned_p_args[0]
                argument_select = ALIGNED_ARGUMENT_SELECT_HTML.replace('P_SLOT', p_slot).replace('H_SLOT', h_slot).replace('ARGUMENT', p_arg)
            else:
                arguments = ''.join([ARGUMENT_HTML.replace('P_SLOT', p_slot).replace('ARGUMENT', p_arg) for p_slot, p_arg, p_aligned in p_args])
                argument_select = ARGUMENT_SELECT_HTML.replace('H_SLOT', h_slot).replace('ARGUMENTS', arguments)
            h_template = h_template.replace('SLOT' + str(slot_i) + '!', argument_select)
        return self.remove_initial_spaces(h_template)

    @staticmethod
    def remove_initial_spaces(s):
        s = s.strip()
        while s.startswith('&nbsp;'):
            s = s[6:].strip()
        return s

    @staticmethod
    def parse_alignments(alignments_str):
        nice_alignments = []
        ugly_alignments = [alignment.split(',')[:-1] for alignment in alignments_str.split(';')[:-1]]
        for alignment in ugly_alignments:
            tokens = [(int(t[1]), t.split(':')[1]) for t in alignment]
            nice_alignment = tuple([tuple(zip(*g)[1]) for k, g in groupby(sorted(tokens), lambda t: t[0])])
            nice_alignments.append(nice_alignment)
        return nice_alignments

    @staticmethod
    def equal_string(premise, hypothesis):
        if '<option value="*">' in hypothesis:
            return False

        hypothesis = re.sub(r'(&nbsp;)?<select', 'START', hypothesis)
        hypothesis = re.sub(r'/select>(&nbsp;)?', 'END', hypothesis)

        start = hypothesis.find('START', 0)
        while start > -1:
            end = hypothesis.find('END', start)
            hypothesis = hypothesis[:start] + hypothesis[end + 3:]
            start = hypothesis.find('START', 0)

        return premise.strip().split() == hypothesis.strip().split()

    @cherrypy.expose
    def grammatical(self, **kwargs):
        with self.lock:
            candidate_id = kwargs['candidate_id']
            extractions_str = kwargs['extractions']
            entailments_str = self.parse_entailments(kwargs)
            sentence1, sentence2 = self.extract_sentences(candidate_id, extractions_str)
            intersection_sentences = self.intersection(sentence1, sentence2, entailments_str)

            html = self.GRAMMATICAL_HTML
            html = html.replace('USER_ID', kwargs['user_id'])
            html = html.replace('CANDIDATE_ID', candidate_id)
            html = html.replace('ALIGNMENTS', kwargs['alignments'])
            html = html.replace('EXTRACTIONS', extractions_str)
            html = html.replace('ENTAILMENTS', entailments_str)
            html = html.replace('QUESTIONNAIRE', ''.join([GRAMMAR_QUESTION_HTML.replace('SENTENCE', escape(sentence, True)) for sentence in intersection_sentences]))
        return html

    @staticmethod
    def parse_entailments(kwargs):
        annotations = [(k, v) for k, v in kwargs.items() if k not in ('user_id', 'candidate_id', 'alignments', 'extractions', 'finito')]

        entailments = dict([(k, ([], [])) for k, v in annotations if ':' not in k and v == 'True'])
        slot_alignments = [k.split(' : ') + [v] for k, v in annotations if ':' in k]

        for entailment, h_slot, p_slot in slot_alignments:
            if entailment in entailments:
                if '>' in entailment:
                    entailments[entailment][0].append(p_slot)
                    entailments[entailment][1].append(h_slot)
                else:
                    entailments[entailment][0].append(h_slot)
                    entailments[entailment][1].append(p_slot)

        entailment_strs = []
        for entailment, (slots1, slots2) in entailments.items():
            direction = ' > ' if '>' in entailment else ' < '
            subtree1, subtree2 = entailment.split(direction)
            if len(slots1) > 0:
                slots1, slots2 = tuple(zip(*sorted(zip(slots1, slots2))))
                subtree1 = ' : '.join((subtree1, ' '.join(slots1)))
                subtree2 = ' : '.join((subtree2, ' '.join(slots2)))
            entailment_strs.append(direction.join((subtree1, subtree2)))
        positive_entailments_str = ';'.join(entailment_strs)
        negative_entailments_str = ';'.join(sorted(set([k for k, v in annotations if ':' not in k and v == 'False'])))
        return '|||'.join((positive_entailments_str, negative_entailments_str))

    def intersection(self, sentence1, sentence2, entailments_str):
        entailments = self.get_real_entailments(sentence1, sentence2, entailments_str)
        entailments, edge_entailments = create_entailments_dictionary(sentence1, sentence2, entailments)
        intersections = intersection(sentence1, sentence2, entailments)
        return sorted(set([generate_natural_language(s, edge_entailments=edge_entailments) for s in intersections]))

    @staticmethod
    def get_real_entailments(sentence1, sentence2, entailments_str):
        if len(entailments_str) <= 3:
            return []
        positive_entailments_str = entailments_str.split('|||')[0]
        if len(positive_entailments_str) == 0:
            return []
        return parse_entailments(positive_entailments_str.split(';'), sentence1, sentence2, 's1:', 's2:')

    @cherrypy.expose
    def thanks(self, **kwargs):
        with self.lock:
            now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_id = kwargs['user_id']
            candidate_id = kwargs['candidate_id']
            alignments = kwargs['alignments']
            extractions = kwargs['extractions']
            entailments = kwargs['entailments']
            intersections = self.parse_intersections(kwargs)

            h = hashlib.new('sha1')
            h.update(''.join(('Lagi', user_id, candidate_id, 'Leshami')))
            code = ''.join((user_id, 'X', candidate_id, 'X', h.hexdigest()))

            annotation = '\t'.join([now, user_id, candidate_id, code, alignments, extractions, entailments] + intersections)
            with open('web/annotations', 'a') as fout:
                print >>fout, annotation
                print annotation
            with open('../vsbkp/annotations', 'a') as fout:
                print >>fout, annotation
                print annotation

            html = self.THANKS_HTML.replace('CODE', code)
            sentence1, sentence2 = self.candidates[candidate_id]
            html = html.replace('SENTENCE1', generate_natural_language(sentence1))
            html = html.replace('SENTENCE2', generate_natural_language(sentence2))
            html = html.replace('INTERSECTIONS', '</br>'.join(self.clean_intersections(intersections)))
        return html

    @staticmethod
    def parse_intersections(kwargs):
        sentences = [k for k in kwargs.keys() if k not in ('user_id', 'candidate_id', 'alignments', 'extractions', 'entailments', 'finito') and k[-5:] != '|||TF']
        return ['|||'.join((s, kwargs[s + '|||TF'], kwargs[s])) for s in sentences]

    @staticmethod
    def clean_intersections(intersections):
        intersections = [sentence.split('|||') for sentence in intersections]
        return [sentence[2] for sentence in intersections if sentence[1] == 'True']


# CONSTANTS (HTML) #

CANDIDATE_HTML = """
<option value="CANDIDATE_ID">CANDIDATE</option>
"""

TOKEN_HTML = """<span class="token" id="sSINDEX:TINDEX" onclick="selectWord(this)">TOKEN</span>"""

ENTAILMENT_QUESTION_HTML = """
<table id="ENTAILMENT" width="100%">
<tr>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="irregular"><span class="small">&nbsp;</span></td>
<td class="pad"><span class="small">&nbsp;</span></td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<b><i>Given that this is true:</i></b>&nbsp;&nbsp;</td>
<td class="irregular">PREMISE</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="irregular"><span class="small">&nbsp;</span></td>
<td class="pad"><span class="small">&nbsp;</span></td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<b><i>Is this true too?</i></b>&nbsp&nbsp;</td>
<td class="irregular">HYPOTHESIS</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<input type="radio" name="ENTAILMENT" value="True" onclick="annotate(this, true)"> <span class="blue" id="ENTAILMENT:True">Yes</span>&nbsp;&nbsp;</td>
<td class="irregular">&nbsp;</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<input type="radio" name="ENTAILMENT" value="False" onclick="annotate(this, false)"> <span class="red" id="ENTAILMENT:False">No</span>&nbsp;&nbsp;</td>
<td class="irregular">&nbsp;</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<input type="radio" name="ENTAILMENT" value="NA" onclick="annotate(this, null)"> <span class="gray" id="ENTAILMENT:NA">It's not a sentence</span>&nbsp;&nbsp;</td>
<td class="irregular">&nbsp;</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="irregular"><span class="small">&nbsp;</span></td>
<td class="pad"><span class="small">&nbsp;</span></td>
</tr>
</table>
"""

ARGUMENT_SELECT_HTML = """
&nbsp;<select name="ENTAILMENT : H_SLOT">
<option value="*thing" selected>[something]</option>
<option value="*one">[someone]</option>
<option value="*where">[somewhere]</option>
<option value="*time">[sometime]</option>
ARGUMENTS
</select>&nbsp;
"""

ARGUMENT_HTML = """
<option value="P_SLOT">ARGUMENT</option>
"""

ALIGNED_ARGUMENT_SELECT_HTML = """
ARGUMENT<select class="aligned" name="ENTAILMENT : H_SLOT">
<option value="P_SLOT" selected>ARGUMENT</option>
</select>
"""

GRAMMAR_QUESTION_HTML = """
<table id="SENTENCE" width="100%">
<tr>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="irregular"><span class="small">&nbsp;</span></td>
<td class="pad"><span class="small">&nbsp;</span></td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<b><i>Make this grammatical:</i></b>&nbsp;&nbsp;</td>
<td class="irregular"><input type="text" class="sentence" name="SENTENCE" value="SENTENCE"></td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<input type="radio" name="SENTENCE|||TF" value="True" onclick="annotate(this, true)"> <span class="blue" id="SENTENCE:True">It's good now</span>&nbsp;&nbsp;</td>
<td class="irregular">&nbsp;</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular">&nbsp;</td>
<td class="regular">&nbsp;<input type="radio" name="SENTENCE|||TF" value="False" onclick="annotate(this, false)"> <span class="red" id="SENTENCE:False">Impossible</span>&nbsp;&nbsp;</td>
<td class="irregular">&nbsp;</td>
<td class="pad">&nbsp;</td>
</tr>
<tr>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="regular"><span class="small">&nbsp;</span></td>
<td class="irregular"><span class="small">&nbsp;</span></td>
<td class="pad"><span class="small">&nbsp;</span></td>
</tr>
</table>
"""


# MAIN #

if __name__ == '__main__':
    args = docopt.docopt("""
        Usage:
            web.py [options] <candidates_dir>

        Options:
            --port NUM  [default: 17171]
    """)
    print "port is:", args['--port']
    print args

    cherrypy.config.update({"server.socket_port" : int(args["--port"])})
    cherrypy.config.update({"server.socket_host" : "0.0.0.0"})
    cherrypy.quickstart(AlignmentEntailmentTask(args['<candidates_dir>']))
