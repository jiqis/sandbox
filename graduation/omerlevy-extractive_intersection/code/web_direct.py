from cgi import escape
import hashlib
from os import listdir
import datetime
from threading import Lock
from os.path import join

import cherrypy
import docopt

from ds.io import read_file
from ds.nlg import generate_natural_language


class AlignmentEntailmentTask:

    def __init__(self, candidates_dir):
        self.lock = Lock()
        self.user_id_counter = 6000

        self.candidates = self.load_candidates(candidates_dir)
        print 'Loaded all candidates:'
        print '\n'.join(self.candidates.keys())

        self.LOGIN_HTML = self.load_html('web/html/login_direct.html')
        self.DIRECT_HTML = self.load_html('web/html/direct.html')
        self.GRAMMATICAL_HTML = self.load_html('web/html/grammatical_direct.html')
        self.THANKS_HTML = self.load_html('web/html/thanks_direct.html')

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
    def direct(self, **kwargs):
        with self.lock:
            html = self.DIRECT_HTML

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

        return html

    @staticmethod
    def generate_sentence_html(sentence, si):
        return ' '.join([TOKEN_HTML.replace('SINDEX', str(si+1)).replace('TINDEX', str(ti)).replace('TOKEN', t)
                         for ti, t in enumerate(generate_natural_language(sentence).split(' '))])

    @cherrypy.expose
    def grammatical(self, **kwargs):
        with self.lock:
            intersections_token_str = kwargs['intersections_token_str']
            intersections_sentence_str = kwargs['intersections_sentence_str']
            intersection_sentences = set(intersections_sentence_str.split('|||')[:-1])
            html = self.GRAMMATICAL_HTML
            html = html.replace('USER_ID', kwargs['user_id'])
            html = html.replace('CANDIDATE_ID', kwargs['candidate_id'])
            html = html.replace('INTERSECTIONS_TOKEN_STR', intersections_token_str)
            html = html.replace('INTERSECTIONS_SENTENCE_STR', intersections_sentence_str)
            html = html.replace('QUESTIONNAIRE', ''.join([GRAMMAR_QUESTION_HTML.replace('SENTENCE', escape(sentence, True)) for sentence in intersection_sentences]))
        return html

    @cherrypy.expose
    def thanks(self, **kwargs):
        with self.lock:
            now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_id = kwargs['user_id']
            candidate_id = kwargs['candidate_id']
            intersections_token_str = kwargs['intersections_token_str']
            intersections = self.parse_intersections(kwargs)

            h = hashlib.new('sha1')
            h.update(''.join(('Aglo', user_id, candidate_id, 'Leshlaab')))
            code = ''.join((user_id, 'X', candidate_id, 'X', h.hexdigest()))

            annotation = '\t'.join([now, user_id, candidate_id, code, intersections_token_str] + intersections)
            with open('web/annotations_direct', 'a') as fout:
                print >>fout, annotation
                print annotation
            with open('../vsbkp/annotations_direct', 'a') as fout:
                print >>fout, annotation
                print annotation

        html = self.THANKS_HTML.replace('CODE', code)
        return html

    @staticmethod
    def parse_intersections(kwargs):
        sentences = [k for k in kwargs.keys() if k not in ('user_id', 'candidate_id', 'intersections_token_str', 'finito') and k[-5:] != '|||TF']
        return ['|||'.join((s, kwargs[s + '|||TF'], kwargs[s])) for s in sentences]



# CONSTANTS (HTML) #

CANDIDATE_HTML = """
<option value="CANDIDATE_ID">CANDIDATE</option>
"""

TOKEN_HTML = """<span class="token" id="sSINDEX:TINDEX" onclick="selectWord(this)">TOKEN</span>"""

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
            web_direct.py [options] <candidates_dir>

        Options:
            --port NUM  [default: 17171]
    """)
    print "port is:", args['--port']
    print args

    cherrypy.config.update({"server.socket_port" : int(args["--port"])})
    cherrypy.config.update({"server.socket_host" : "0.0.0.0"})
    cherrypy.quickstart(AlignmentEntailmentTask(args['<candidates_dir>']))
