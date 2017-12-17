from stanford_corenlp_pywrapper import CoreNLP
proc = CoreNLP(configdict={'annotators': 'tokenize,ssplit,pos,depparse','depparse.model': 'edu/stanford/nlp/models/parser/nndep/english_SD.gz'}, corenlp_jars=["/usr/local/lib/stanford-corenlp-full-2017-06-09/*"])
import pdb
#pdb.set_trace()

def readLines(filename):
	f=open(filename,'r')
	for i in f:
		yield i

f=open('./org_sentences.out','w')

def parse(sentence,outfile,parser):
	dict = parser.parse_doc(sentence)
	print(dict)
	#print(deps)
	
	tokens = dict['sentences'][0]['tokens']
	deps = sorted(dict['sentences'][0]['deps_basic'],key = lambda x: x[2])
	for i in xrange(len(tokens)):
		outfile.write(str(i)+'\t'+tokens[i]+'\t'+str(deps[i][1])+'\t'+deps[i][0]+'\n')
	outfile.write('\n')

for i in readLines('test.txt'):
	parse(i,f,proc)

f.close()
