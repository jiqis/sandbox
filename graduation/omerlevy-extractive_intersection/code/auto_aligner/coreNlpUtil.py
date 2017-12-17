import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib




from config import *


import pdb

from stanford_corenlp_pywrapper import CoreNLP

class StanfordNLP:
    def __init__(self):
        #self.server = ServerProxy(JsonRpc20(),
        #                         TransportTcpIp(addr=("127.0.0.1", 8080)))
        corenlp_dir="/usr/local/lib/stanford-corenlp-full-2017-06-09/*"

        self.server = CoreNLP(configdict={'annotators': 'tokenize,ssplit,pos,depparse,lemma,ner','depparse.model':'edu/stanford/nlp/models/parser/nndep/english_SD.gz'}, corenlp_jars=[corenlp_dir])

    def parse(self, text):
        return self.server.parse_doc(text)


##############################################################################################################################
def parseText(sentences):
    parseResult = nlp.parse(sentences)
    if len(parseResult['sentences']) == 1:
        return parseResult
    wordOffset = 0
    try:
        for i in xrange(len(parseResult['sentences'])):
            if i>0:
                for j in xrange(len(parseResult['sentences'][i]['deps_basic'])):

                    for k in xrange(1,3):
                        #tokens = parseResult['sentences'][i]['dependencies'][j][k].split('-')
                        tokens = parseResult['sentences'][i]['deps_basic'][j][k]
                        if tokens == -1:
                            newWordIndex = 0
                        else:
                        #if not tokens[len(tokens)-1].isdigit(): # forced to do this because of entries like u"lost-8'" in parseResult
                           #continue
                            newWordIndex = tokens+wordOffset
                    """
                    if len(tokens) == 2:
                          parseResult['sentences'][i]['deps-cc'][j][k] = tokens[0]+ '-' + str(newWordIndex)
                    else:
                        w = ''
                        for l in xrange(len(tokens)-1):
                            w += tokens[l]
                            if l<len(tokens)-2:
                                w += '-'
                        parseResult['sentences'][i]['deps-cc'][j][k] = w + '-' + str(newWordIndex)
                    """
                    parseResult['sentences'][i]['deps_basic'][j][k]=newWordIndex
            wordOffset +=  len(parseResult['sentences'][i]['tokens'])

            if i>0:
                for j in xrange(len(parseResult['sentences'][i]['deps_cc'])):

                    for k in xrange(1,3):
                        #tokens = parseResult['sentences'][i]['dependencies'][j][k].split('-')
                        tokens = parseResult['sentences'][i]['deps_cc'][j][k]
                        if tokens == -1:
                            newWordIndex = 0
                        else:
                        #if not tokens[len(tokens)-1].isdigit(): # forced to do this because of entries like u"lost-8'" in parseResult
                           #continue
                            newWordIndex = tokens+wordOffset
                parseResult['sentences'][i]['deps_cc'][j][k]=newWordIndex
            wordOffset +=  len(parseResult['sentences'][i]['tokens'])
    except Exception as e:
        print e
        print sentences[0]
        raise e
    # merge information of all sentences into one
    for i in xrange(1,len(parseResult['sentences'])):
        #parseResult['sentences'][0]['text'] += ' ' + parseResult['sentences'][i]['text']
        for jtem in parseResult['sentences'][i]['deps_basic']:
            parseResult['sentences'][0]['deps_basic'].append(jtem)
        for jtem in parseResult['sentences'][i]['deps_cc']:
            parseResult['sentences'][0]['deps_cc'].append(jtem)
        for jtem in parseResult['sentences'][i]['tokens']:
            parseResult['sentences'][0]['tokens'].append(jtem)
        for jtem in parseResult['sentences'][i]['pos']:
            parseResult['sentences'][0]['pos'].append(jtem)
        for jtem in parseResult['sentences'][i]['ner']:
            parseResult['sentences'][0]['ner'].append(jtem)
        for jtem in parseResult['sentences'][i]['lemmas']:
            parseResult['sentences'][0]['lemmas'].append(jtem)
        for jtem in parseResult['sentences'][i]['normner']:
            parseResult['sentences'][0]['normner'].append(jtem)
        for jtem in parseResult['sentences'][i]['char_offsets']:
            parseResult['sentences'][0]['char_offsets'].append(jtem)
    # remove all but the first entry
    parseResult['sentences'] = parseResult['sentences'][0:1]

    return parseResult
##############################################################################################################################



##############################################################################################################################
def nerWordAnnotator(parseResult):

    res = []

    wordIndex = 1
    for i in xrange(len(parseResult['sentences'][0]['tokens'])):
        tag = [parseResult['sentences'][0]['char_offsets'][i], wordIndex, parseResult['sentences'][0]['tokens'][i], parseResult['sentences'][0]['ner'][i]]
        wordIndex += 1

        if tag[3] <> 'O':
            res.append(tag)


    return res
##############################################################################################################################


##############################################################################################################################
def ner(parseResult):

    nerWordAnnotations = nerWordAnnotator(parseResult)

    namedEntities = []
    currentNE = []
    currentCharacterOffsets = []
    currentWordOffsets = []

    for i in xrange(len(nerWordAnnotations)):


        if i == 0:
            currentNE.append(nerWordAnnotations[i][2])
            currentCharacterOffsets.append(nerWordAnnotations[i][0])
            currentWordOffsets.append(nerWordAnnotations[i][1])
            if len(nerWordAnnotations) == 1:
                namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i-1][3]])
                break
            continue

        if nerWordAnnotations[i][3] == nerWordAnnotations[i-1][3] and nerWordAnnotations[i][1] == nerWordAnnotations[i-1][1]+1:
            currentNE.append(nerWordAnnotations[i][2])
            currentCharacterOffsets.append(nerWordAnnotations[i][0])
            currentWordOffsets.append(nerWordAnnotations[i][1])
            if i == len(nerWordAnnotations)-1:
                namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i][3]])
        else:
            namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i-1][3]])
            currentNE = [nerWordAnnotations[i][2]]
            currentCharacterOffsets = []
            currentCharacterOffsets.append(nerWordAnnotations[i][0])
            currentWordOffsets = []
            currentWordOffsets.append(nerWordAnnotations[i][1])
            if i == len(nerWordAnnotations)-1:
                namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i][3]])

    #print namedEntities

    return namedEntities
##############################################################################################################################


##############################################################################################################################
def posTag(parseResult):

    res = []

    wordIndex = 1
    for i in xrange(len(parseResult['sentences'][0]['tokens'])):
        tag = [parseResult['sentences'][0]['char_offsets'][i], wordIndex, parseResult['sentences'][0]['tokens'][i], parseResult['sentences'][0]['pos'][i]]
        wordIndex += 1
        res.append(tag)


    return res
##############################################################################################################################




##############################################################################################################################
def lemmatize(parseResult):

    res = []
    wordIndex = 1
    for i in xrange(len(parseResult['sentences'][0]['tokens'])):
        tag = [parseResult['sentences'][0]['char_offsets'][i], wordIndex, parseResult['sentences'][0]['tokens'][i], parseResult['sentences'][0]['lemmas'][i]]
        wordIndex += 1
        res.append(tag)


    return res
##############################################################################################################################





##############################################################################################################################
def dependencyParseAndPutOffsets(parseResult):
# returns dependency parse of the sentence whhere each item is of the form (rel, left{charStartOffset, charEndOffset, wordNumber}, right{charStartOffset, charEndOffset, wordNumber})

    dParse = parseResult['sentences'][0]['deps_cc']
    words = parseResult['sentences'][0]['tokens']

    #for item in dParse:
        #print item

    result = []

    for item in dParse:
        newItem = []

        # copy 'rel'
        newItem.append(item[0])

        # construct and append entry for 'left'
        if item[1]==-1:
            left='ROOT'
        else:
            left = words[item[1]]
        left += '-'
        wordNumber = str(item[1]+1)
        if wordNumber.isdigit() == False:
            continue
        left += '{' + str(parseResult['sentences'][0]['char_offsets'][int(wordNumber)-1][0]) + ' ' + str(parseResult['sentences'][0]['char_offsets'][int(wordNumber)-1][1]) + ' ' + wordNumber + '}'
        newItem.append(left)

        # construct and append entry for 'right'
        if item[2]==-1:
            right='ROOT'
        else:
            right = words[item[2]]
        right += '-'
        wordNumber = str(item[2]+1)
        if wordNumber.isdigit() == False:
            continue
        right += '{' + str(parseResult['sentences'][0]['char_offsets'][int(wordNumber)-1][0]) + ' ' + str(parseResult['sentences'][0]['char_offsets'][int(wordNumber)-1][1]) + ' ' + wordNumber + '}'
        newItem.append(right)

        result.append(newItem)

    return result
##############################################################################################################################



##############################################################################################################################
def findParents(dependencyParse, wordIndex, word):
# word index assumed to be starting at 1
# the third parameter is needed because of the collapsed representation of the dependencies...

    wordsWithIndices = ((int(item[2].split('{')[1].split('}')[0].split(' ')[2]), item[2].split('{')[0]) for item in dependencyParse)
    wordsWithIndices = list(set(wordsWithIndices))
    wordsWithIndices = sorted(wordsWithIndices, key=lambda item: item[0])
    #print wordsWithIndices

    wordIndexPresentInTheList = False
    for item in wordsWithIndices:
        if item[0] == wordIndex:
            wordIndexPresentInTheList = True
            break

    parentsWithRelation = []

    if wordIndexPresentInTheList:
        for item in dependencyParse:
            currentIndex = int(item[2].split('{')[1].split('}')[0].split(' ')[2])
            if currentIndex == wordIndex:
                parentsWithRelation.append([int(item[1].split('{')[1].split('}')[0].split(' ')[2]), item[1].split('{')[0], item[0]])
    else:
        # find the closest following word index which is in the list
        nextIndex = 0
        for i in xrange(len(wordsWithIndices)):
            if wordsWithIndices[i][0] > wordIndex:
                nextIndex = wordsWithIndices[i][0]
                break
        if nextIndex == 0:
            return [] #?
        for i in xrange(len(dependencyParse)):
            if int(dependencyParse[i][2].split('{')[1].split('}')[0].split(' ')[2]) == nextIndex:
                   pos = i
                   break
        for i in xrange(pos, len(dependencyParse)):
            if '_' in dependencyParse[i][0] and word in dependencyParse[i][0]:
                parent = [int(dependencyParse[i][1].split('{')[1].split('}')[0].split(' ')[2]), dependencyParse[i][1].split('{')[0], dependencyParse[i][0]]
                parentsWithRelation.append(parent)
                break

    return parentsWithRelation
##############################################################################################################################




##############################################################################################################################
def findChildren(dependencyParse, wordIndex, word):
# word index assumed to be starting at 1
# the third parameter is needed because of the collapsed representation of the dependencies...

    wordsWithIndices = ((int(item[2].split('{')[1].split('}')[0].split(' ')[2]), item[2].split('{')[0]) for item in dependencyParse)
    wordsWithIndices = list(set(wordsWithIndices))
    wordsWithIndices = sorted(wordsWithIndices, key=lambda item: item[0])

    wordIndexPresentInTheList = False
    for item in wordsWithIndices:
        if item[0] == wordIndex:
            wordIndexPresentInTheList = True
            break

    childrenWithRelation = []

    if wordIndexPresentInTheList:
        #print True
        for item in dependencyParse:
            currentIndex = int(item[1].split('{')[1].split('}')[0].split(' ')[2])
            if currentIndex == wordIndex:
                childrenWithRelation.append([int(item[2].split('{')[1].split('}')[0].split(' ')[2]), item[2].split('{')[0], item[0]])
    else:
        # find the closest following word index which is in the list
        nextIndex = 0
        for i in xrange(len(wordsWithIndices)):
            if wordsWithIndices[i][0] > wordIndex:
                nextIndex = wordsWithIndices[i][0]
                break

        if nextIndex == 0:
            return []
        for i in xrange(len(dependencyParse)):
            if int(dependencyParse[i][2].split('{')[1].split('}')[0].split(' ')[2]) == nextIndex:
                   pos = i
                   break
        for i in xrange(pos, len(dependencyParse)):
            if '_' in dependencyParse[i][0] and word in dependencyParse[i][0]:
                child = [int(dependencyParse[i][2].split('{')[1].split('}')[0].split(' ')[2]), dependencyParse[i][2].split('{')[0], dependencyParse[i][0]]
                childrenWithRelation.append(child)
                break

    return childrenWithRelation
##############################################################################################################################


nlp = StanfordNLP()
