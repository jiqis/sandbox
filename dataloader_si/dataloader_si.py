#dataloader

#format:
# <sentence1>\t<sentence2>|||<intersection>

import sys

def sentenceDivide(line):
    inout=line.split('|||')
    sentences=inout[0].split('\t')
    return (sentences[0],sentences[1],inout[1])

def readfromFile(filename):
    try:
        f=open(filename,'r')
        for lines in f:
            yield lines
    except:
        print 'Failed to open file "%s"' % filename
        raise

if(len(sys.argv)<2):
   print 'No input file. Quit.'
else:
    data=[]
    data_fail=[]
    try:
       
       filename=sys.argv[1]
       for lines in readfromFile(filename):
           sentences=sentenceDivide(lines)
           if len(sentences[2].split())<1:
               data_fail.append(sentences)
           else:
               data.append(sentences)

    except:
       print 'Failed to read data. Ensure that input file exists.'
       raise
    if(len(data)>0):
    	out_suc=open('./data_success.txt','w')
    	for i in data:
    		out_suc.write(i[0] + '\n')
    		out_suc.write(i[1] + '\n\n')
    		out_suc.write(i[2].split('\t')[len(i[2].split('\t'))-1] + '\n\n')
    	out_suc.close()
    if(len(data_fail)>0):
    	out_fail=open('./data_failed.txt','w')
    	for i in data_fail:
    		out_fail.write(i[0] + '\n')
    		out_fail.write(i[1] + '\n\n')
    		
    	out_fail.close()
