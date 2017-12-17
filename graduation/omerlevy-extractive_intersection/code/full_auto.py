import sys
from os.path import join
from os import listdir

from ds.alignment2entailment import generate_potential_extractions, generate_potential_entailments
from ds.entailment import create_entailments_dictionary
from ds.intersection import intersection
from ds.io import read_file, parse_entailments
from ds.sentence_tree import DynamicTree
from ds.nlg import generate_natural_language

sys.path.append('auto_aligner')
from aligner import align

import pdb

def main():
    path = sys.argv[1]
    with open(path + 'system.out', 'w') as fout:
        entailment_out = open(path + '_entailment.out', 'w')
        for sentence1, sentence2 in load_candidates(path):
            output = generate_natural_language(sentence1) + '\t' + generate_natural_language(sentence2) + '|||'

            try:
                alignments = linear_align(generate_natural_language(sentence1), generate_natural_language(sentence2))
            except Exception as e:
                print e
                print >>fout, output + '\t'
                continue

            extraction1, extraction2 = generate_potential_extractions(sentence1, sentence2, alignments)
            extractions = [assign_slots(extraction1[0].replace('?', '>'), extraction1[4], extraction1[5]),
                           assign_slots(extraction2[0].replace('?', '<'), extraction2[5], extraction2[4])]
            extractions = parse_entailments(extractions, sentence1, sentence2, 's1:', 's2:')
            sentence1 = extract_sentence(sentence1, extractions, '>')
            sentence2 = extract_sentence(sentence2, extractions, '<')

            entailments = generate_potential_entailments(sentence1, sentence2, alignments)
            entailments = [assign_slots(entailment[0].replace('?', '>'), entailment[4], entailment[5]) for entailment in entailments] + \
                          [assign_slots(entailment[0].replace('?', '<'), entailment[5], entailment[4]) for entailment in entailments]

            entailments = parse_entailments(entailments, sentence1, sentence2, 's1:', 's2:')
            entailments, edge_entailments = create_entailments_dictionary(sentence1, sentence2, entailments)

            intersections = intersection(sentence1, sentence2, entailments)
            intersections = sorted(set([generate_natural_language(s, edge_entailments=edge_entailments) for s in intersections]))
            output += '\t'.join(intersections)
            print >>entailment_out, entailments
            print >>entailment_out, edge_entailments
            print >>fout, output


def load_candidates(path):
    files = [join(path, f) for f in listdir(path)]
    for f in files:
        if ('msr_' in f) or ('kapil_' in f) or ('org_' in f):
            sentence1, sentence2, entailments = read_file(f)
            yield sentence1, sentence2


def linear_align(s1, s2):
    tokens1 = s1.split(' ')
    tokens2 = s2.split(' ')
    alignments = sorted([(a1-1, a2-1) for a1, a2 in align(s1, s2)[0]])
    equals = set([(a1, a2) for a1, a2 in alignments  if(a1<len(tokens1) and a2<len(tokens2) and tokens1[a1] == tokens2[a2])])

    new_alignments = []
    current = []
    for a1, a2 in alignments:
        if ((a1, a2) in equals) and (len(current) == 0 or current[-1] == (a1-1, a2-1)):
            current.append((a1, a2))
        else:
            if len(current) > 0:
                seq1, seq2 = zip(*current)
                new_alignments.append((tuple(map(str, seq1)), tuple(map(str, seq2))))
            new_alignments.append(((str(a1),), (str(a2),)))
            current = []
    if len(current) > 0:
        seq1, seq2 = zip(*current)
        new_alignments.append((tuple(map(str, seq1)), tuple(map(str, seq2))))

    return new_alignments


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


def assign_slots(entailment, p_args, h_args):
    forward = '>' in entailment
    if forward:
        lhs, rhs = entailment.split(' > ')
    else:
        lhs, rhs = entailment.split(' < ')

    slots = []
    for slot_i, (h_slot, h_arg, h_aligned) in enumerate(h_args):
        aligned_p_args = [(p_slot, p_arg) for p_slot, p_arg, p_aligned in p_args if p_aligned == h_slot]
        if len(aligned_p_args) > 1:
            raise Exception('Double alignment. BUG!')
        if len(aligned_p_args) == 1:
            p_slot, p_arg = aligned_p_args[0]
            slots.append((p_slot, h_slot))
        else:
            slots.append(('*thing', h_slot))

    if len(slots) > 0:
        p_slots, h_slots = zip(*slots)
        if forward:
            lhs += ' : ' + ' '.join(map(str, p_slots))
            rhs += ' : ' + ' '.join(map(str, h_slots))
            entailment = lhs + ' > ' + rhs
        else:
            lhs += ' : ' + ' '.join(map(str, h_slots))
            rhs += ' : ' + ' '.join(map(str, p_slots))
            entailment = lhs + ' < ' + rhs
    return entailment


if __name__ == '__main__':
    main()

