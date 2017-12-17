from itertools import chain
from ds.nlg import generate_natural_language


def validate_alignments(sentence1, sentence2, actual_alignments):
    actual_alignments = [(map(int, seq1), map(int, seq2)) for seq1, seq2 in actual_alignments]
    sentence1 = generate_natural_language(sentence1).split(' ')
    sentence2 = generate_natural_language(sentence2).split(' ')
    high_prob_alignments = aligned_unigrams(sentence1, sentence2, 3)
    covered_alignments = sum(1 if covers_alignment(expected_alignment, actual_alignments) else 0 for expected_alignment in high_prob_alignments)
    print
    print actual_alignments
    print covered_alignments
    print len(high_prob_alignments)
    print
    return ((float(covered_alignments) + 2) / (len(high_prob_alignments) + 3)) > 0.66


def aligned_unigrams(s1, s2, n):
    ngrams1 = get_ngrams(s1, n)
    ngrams2 = get_ngrams(s2, n)
    ngrams = set(ngrams1).intersection(set(ngrams2))
    indices1 = [ngrams1.index(ngram) for ngram in ngrams]
    indices2 = [ngrams2.index(ngram) for ngram in ngrams]
    alignments = [zip(range(i1, i1 + n), range(i2, i2 + n)) for i1, i2 in zip(indices1, indices2)]
    return set(chain(*alignments))


def get_ngrams(s, n):
    return [tuple(s[i:i+n]) for i in xrange(0, len(s) - n)]


def covers_alignment(expected_alignment, actual_alignments):
    return any(contains_alignment(expected_alignment, actual_alignment) for actual_alignment in actual_alignments)


def contains_alignment(expected_alignment, actual_alignment):
    return (expected_alignment[0] in actual_alignment[0]) and (expected_alignment[1] in actual_alignment[1])
