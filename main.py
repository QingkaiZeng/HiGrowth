########################################################
# Data-Driven Data Science Syllabus Generation         #
#  Given a text corpus of data science publications,   #
#  construt a faceted concept hierarchy of             #
#  data science in lightly-supervised way.             #
# Author: Meng Jiang (mjiang2@nd.edu)                  #
# Version:                                             #
#  v1.0 - March 10, 2018: Hearst Pattern matching      #
########################################################

import sys

MAXINF = 999999
MAXDIST = 10

# This function prepares the following input files:
#  (1) vocabulary.txt
#      Each line is a concept word/phrase.
#      If the concept is in lower case, we assume it is case insensitive;
#      if the concept has at least one upper case, we assume it is case sensitiive.
#      Concepts in the text corpus will be recognized if they are in this list.
#  (2) patterns.txt
#      Each line has multiple columns.
#      Column 1: textual pattern (Hearst pattern, etc.)
#       $: concept
#       <pl>: plural "-s"
#      Column 2-: each column is a relation.
#       <synonym/ancestor/sibling> <order of left entity> <order of right entity> <if has context>
#       synonym(left,right): symmetric
#       ancestor(left,right): asymmetric
#       sibling(left,right): symmetric
def step0():
    # Given syllabus.txt, which is
    #  ground truth of the data science syllabus (faceted concept hierarchy),
    # output the vocabulary of data science concepts.
    fw = open('input/vocabulary.txt','w')
    fr = open('input/syllabus.txt','r')
    for line in fr:
        text = line.strip('\r\n')
        pos = text.rfind('-->')
        entity = text[0:pos]
        if '_' in entity:
            pos = entity.find('_')
            entity = entity[pos+1:]
        fw.write(entity+'\n')
    fr.close()
    fw.close()

    # Output textual patterns and their corresponding relations.
    #  The biggest number of $ is 5.
    fw = open('input/patterns.txt','w')
    # '$ ( $ )' --> synonym(1,2,F)
    fw.write('$ ( $ )' \
            +'\t'+'synonym_1_2_F' \
            +'\n')
    # '$ and/or $ <pl>' --> sibling(1,2,T)
    for head in ['$']:
        for body in ['and','or']:
            for tail in ['$ <pl>']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'sibling_1_2_T' \
                        +'\n')
    # '<pl> {,} such as/including/especially $ {,/and/or $}*' --> sibling(1,2,T)
    for head in ['<pl>','<pl> ,']:
        for body in ['such as','including','especially']:
            for tail in ['$ , $','$ and $','$ or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'sibling_1_2_T' \
                        +'\n')
            for tail in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'sibling_1_2_T' \
                        +'\t'+'sibling_1_3_T' \
                        +'\t'+'sibling_2_3_T' \
                        +'\n')
            for tail in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'sibling_1_2_T' \
                        +'\t'+'sibling_1_3_T' \
                        +'\t'+'sibling_1_4_T' \
                        +'\t'+'sibling_2_3_T' \
                        +'\t'+'sibling_2_4_T' \
                        +'\t'+'sibling_3_4_T' \
                        +'\n')
    # 'such as/including/especially $ {,/and/or $}*' --> sibling(1,2,F)
    for body in ['such as','including','especially']:
        for tail in ['$ , $','$ and $','$ or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_F' \
                    +'\n')
        for tail in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_F' \
                    +'\t'+'sibling_1_3_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\n')
        for tail in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_F' \
                    +'\t'+'sibling_1_3_F' \
                    +'\t'+'sibling_1_4_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\t'+'sibling_2_4_F' \
                    +'\t'+'sibling_3_4_F' \
                    +'\n')
    # 'such <pl> as $ {,/and/or $}*' --> sibling(1,2,T)
    for body in ['such <pl> as']:
        for tail in ['$ , $','$ and $','$ or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_T' \
                    +'\n')
        for tail in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_T' \
                    +'\t'+'sibling_1_3_T' \
                    +'\t'+'sibling_2_3_T' \
                    +'\n')
        for tail in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_T' \
                    +'\t'+'sibling_1_3_T' \
                    +'\t'+'sibling_1_4_T' \
                    +'\t'+'sibling_2_3_T' \
                    +'\t'+'sibling_2_4_T' \
                    +'\t'+'sibling_3_4_T' \
                    +'\n')
    # '$ <pl> {,} such as/including/especially $ {,/and/or $}*' --> ancestor(1,2,T) sibling(2,3,T)
    for head in ['$ <pl>','$ <pl> ,']:
        for body in ['such as','including','especially']:
            for tail in ['$']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_T'+'\n')
            for tail in ['$ , $','$ and $','$ or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_T' \
                        +'\t'+'ancestor_1_3_T' \
                        +'\t'+'sibling_2_3_T' \
                        +'\n')
            for tail in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_T' \
                        +'\t'+'ancestor_1_3_T' \
                        +'\t'+'ancestor_1_4_T' \
                        +'\t'+'sibling_2_3_T' \
                        +'\t'+'sibling_2_4_T' \
                        +'\t'+'sibling_3_4_T' \
                        +'\n')
            for tail in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_T' \
                        +'\t'+'ancestor_1_3_T' \
                        +'\t'+'ancestor_1_4_T' \
                        +'\t'+'ancestor_1_5_T' \
                        +'\t'+'sibling_2_3_T' \
                        +'\t'+'sibling_2_4_T' \
                        +'\t'+'sibling_2_5_T' \
                        +'\t'+'sibling_3_4_T' \
                        +'\t'+'sibling_3_5_T' \
                        +'\t'+'sibling_4_5_T' \
                        +'\n')
    # '$ {,} such as/including/especially $ {,/and/or $}*' --> ancestor(1,2,F) sibling(2,3,F)
    for head in ['$','$ ,']:
        for body in ['such as','including','especially']:
            for tail in ['$']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_F'+'\n')
            for tail in ['$ , $','$ and $','$ or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_F' \
                        +'\t'+'ancestor_1_3_F' \
                        +'\t'+'sibling_2_3_F' \
                        +'\n')
            for tail in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_F' \
                        +'\t'+'ancestor_1_3_F' \
                        +'\t'+'ancestor_1_4_F' \
                        +'\t'+'sibling_2_3_F' \
                        +'\t'+'sibling_2_4_F' \
                        +'\t'+'sibling_3_4_F' \
                        +'\n')
            for tail in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
                fw.write(head+' '+body+' '+tail \
                        +'\t'+'ancestor_1_2_F' \
                        +'\t'+'ancestor_1_3_F' \
                        +'\t'+'ancestor_1_4_F' \
                        +'\t'+'ancestor_1_5_F' \
                        +'\t'+'sibling_2_3_F' \
                        +'\t'+'sibling_2_4_F' \
                        +'\t'+'sibling_2_5_F' \
                        +'\t'+'sibling_3_4_F' \
                        +'\t'+'sibling_3_5_F' \
                        +'\t'+'sibling_4_5_F' \
                        +'\n')
    # 'such $ as $ {,/and/or $}*' --> ancestor(1,2,F) sibling(2,3,F)                
    for body in ['such $ as']:
        for tail in ['$']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_2_F'+'\n')
        for tail in ['$ , $','$ and $','$ or $']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_2_F' \
                    +'\t'+'ancestor_1_3_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\n')
        for tail in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_2_F' \
                    +'\t'+'ancestor_1_3_F' \
                    +'\t'+'ancestor_1_4_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\t'+'sibling_2_4_F' \
                    +'\t'+'sibling_3_4_F' \
                    +'\n')
        for tail in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_2_F' \
                    +'\t'+'ancestor_1_3_F' \
                    +'\t'+'ancestor_1_4_F' \
                    +'\t'+'ancestor_1_5_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\t'+'sibling_2_4_F' \
                    +'\t'+'sibling_2_5_F' \
                    +'\t'+'sibling_3_4_F' \
                    +'\t'+'sibling_3_5_F' \
                    +'\t'+'sibling_4_5_F' \
                    +'\n')
    # '$ {,/and/or $}* {,} and/or other $' --> ancestor(-1,1,F) sibling(1,2,F)                
    for tail in ['and other $','or other $',', and other $',', or other $']:
        for body in ['$']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_2_F'+'\n')
        for body in ['$ , $','$ and $','$ or $']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_3_F' \
                    +'\t'+'ancestor_2_3_F' \
                    +'\t'+'sibling_1_2_F' \
                    +'\n')
        for body in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_4_F' \
                    +'\t'+'ancestor_2_4_F' \
                    +'\t'+'ancestor_3_4_F' \
                    +'\t'+'sibling_1_2_F' \
                    +'\t'+'sibling_1_3_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\n')
        for body in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'ancestor_1_5_F' \
                    +'\t'+'ancestor_2_5_F' \
                    +'\t'+'ancestor_3_5_F' \
                    +'\t'+'ancestor_4_5_F' \
                    +'\t'+'sibling_1_2_F' \
                    +'\t'+'sibling_1_3_F' \
                    +'\t'+'sibling_1_4_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\t'+'sibling_2_4_F' \
                    +'\t'+'sibling_3_4_F' \
                    +'\n')
    # '$ {,/and/or $}* {,} and/or other <pl>' --> sibling(1,2,T)                
    for tail in ['and other <pl>','or other <pl>',', and other <pl>',', or other <pl>']:
        for body in ['$ , $','$ and $','$ or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_F' \
                    +'\n')
        for body in ['$ , $ , $','$ , $ and $','$ , $ , and $','$ , $ or $','$ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_F' \
                    +'\t'+'sibling_1_3_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\n')
        for body in ['$ , $ , $ , $','$ , $ , $ and $','$ , $ , $ , and $','$ , $ , $ or $','$ , $ , $ , or $']:
            fw.write(body+' '+tail \
                    +'\t'+'sibling_1_2_F' \
                    +'\t'+'sibling_1_3_F' \
                    +'\t'+'sibling_1_4_F' \
                    +'\t'+'sibling_2_3_F' \
                    +'\t'+'sibling_2_4_F' \
                    +'\t'+'sibling_3_4_F' \
                    +'\n')
    fw.close()

# This function removes REFERENCE(S) section and citations ([x,y,z]) from a document
def rmref(text):
    ret = ''    
    if 'REFERENCE' in text:
        pos = text.find('REFERENCE')
        text = text[0:pos]
    while '[' in text:
        pos1 = text.find('[')
        ret += text[0:pos1]
        text = text[pos1+1:]
        if not ']' in text:
            return ret+text
        pos2 = text.find(']')
        text = text[pos2+1:]
    return ret+text

# This function recognizes concepts of the vocabulary in the documents,
#  and compress the documents for only concepts and their significant contexts
#  - non-contextual parts are represented as "#<number of words skipped>".
def step1():
    # How many neighboring words around a concept will be shown? When <= SIZE_NEIGHBOR.
    SIZE_NEIGHBOR = 5
    # How many consecutive non-contextual words between concepts will be skipped? When > SIZE_WINDOW.
    SIZE_WINDOW = 20

    indexI,nindexI = [{}],1 # Insensitive entity/concept name's word index
    indexS,nindexS = [{}],1 # Sensitive entity/concept name's word index

    # Build case-(in)sensitive word indices (Trie trees) for concepts
    fr = open('input/vocabulary.txt','r')
    for line in fr:
        entity = line.strip('\r\n')
        words = entity.split(' ')
        n = len(words)
        if entity.lower() == entity: # When case insensitive
            if n > nindexI:
                for i in range(nindexI,n):
                    indexI.append({})
                nindexI = n
            temp = indexI[n-1]
            if n > 1:
                for i in range(n-1):
                    word = words[i]
                    if not word in temp:
                        temp[word] = {}
                    temp = temp[word]
                word = words[n-1]
            else:
                word = words[0]
            temp[word] = entity.replace(' ','_')
        else: # When case sensitive
            if n > nindexS:
                for i in range(nindexS,n):
                    indexS.append({})
                nindexS = n
            temp = indexS[n-1]
            if n > 1:
                for i in range(n-1):
                    word = words[i]
                    if not word in temp:
                        temp[word] = {}
                    temp = temp[word]
                word = words[n-1]
            else:
                word = words[0]
            temp[word] = entity.replace(' ','_')
    fr.close()

    # Count the number of docs for progress bar
    ndoc = 0
    fr = open('input/data.txt','r')
    for line in fr:
        ndoc += 1
    fr.close()

    # Given documents, recognize concepts and compress for significant contexts
    #  data.txt
    #  Column 1: document id
    #  Column 2: document's tokenized text
    fw = open('output/step1.txt','w')
    fr = open('input/data.txt','r')
    idoc = 0    
    for line in fr:
        # Show progress bar
        idoc += 1
        if idoc % 10 == 0 or idoc == ndoc:
            sys.stdout.write('\r\tProgress: '+str(0.01*int(10000.0*idoc/ndoc))+'%'+' Doc. '+str(idoc)+' / '+str(ndoc)+'                    ')
            sys.stdout.flush()
        # Recognize concepts by DFS tree branch search
        output = ''
        entityset = set()
        pid,text = line.strip('\r\n').split('\t')
        text = rmref(text)
        words = text.split(' ')
        wordsS = []
        for word in words:
            if word == '': continue
            wordsS.append(word)
        wordsI = [word.lower() for word in wordsS]
        l = len(wordsS)
        i = 0
        while i < l:
            isvalid = False
            for j in range(min(nindexI,l-i),0,-1): # Priority for longest phrases
                temp = indexI[j-1]
                k = 0
                while k < j and i+k < l:
                    tempword = wordsI[i+k]
                    if not tempword in temp: break
                    temp = temp[tempword]
                    k += 1
                if k == j:
                    entity = temp
                    surface = ''
                    for _k in range(0,j):
                        surface += '_'+wordsS[i+_k]
                    output += ' $e:'+surface[1:]+':'+entity
                    isvalid = True
                    break
            if isvalid:
                i += k
                continue
            for j in range(min(nindexS,l-i),0,-1):
                temp = indexS[j-1]
                k = 0
                while k < j and i+k < l:
                    tempword = wordsS[i+k]
                    if not tempword in temp: break
                    temp = temp[tempword]
                    k += 1
                if k == j:
                    entity = temp
                    surface = ''
                    for _k in range(0,j):
                        surface += '_'+wordsS[i+_k]
                    output += ' $e:'+surface[1:]+':'+entity # Label the concept as "$e:<Surface>:<Entity>"
                    isvalid = True
                    break
            if isvalid:
                i += k
                continue
            if not wordsS[i] == '':
                output += ' '+wordsS[i]
            i += 1
        text = output[1:]
        # Compress documents by skipping non-significant contexts
        output = ''
        words = text.split(' ')
        l = len(words)
        i = 0
        wordsInterm = []
        while i < l:
            if words[i].startswith('$e:'):
                nInterm = len(wordsInterm)
                if nInterm > SIZE_WINDOW:
                    for k in range(SIZE_NEIGHBOR):
                        output += ' '+wordsInterm[k]
                    output += ' #'+str(nInterm-2*SIZE_NEIGHBOR)                 
                    for k in range(nInterm-SIZE_NEIGHBOR,nInterm):
                        output += ' '+wordsInterm[k]
                else:
                    for word in wordsInterm:
                        output += ' '+word
                output += ' '+words[i]
                i += 1
                wordsInterm = []
                continue
            wordsInterm.append(words[i])
            i += 1
        nInterm = len(wordsInterm)
        if nInterm > SIZE_WINDOW:
            for k in range(SIZE_NEIGHBOR):
                output += ' '+wordsInterm[k]
            output += ' #'+str(nInterm-SIZE_NEIGHBOR)
        else:
            for word in wordsInterm:
                output += ' '+word
        text = output[1:]
        # Output document id along with compressed concept-recognized text
        fw.write(pid+'\t'+text+'\n')
    fr.close()
    fw.close()

# This function types the entities into four categories:
#  (1) PROBLEM: a research problem or an application;
#  (2) METHOD: a methodology or a computational model;
#  (3) CONCEPT: a concept/term used in some method;
#  (4) METRIC: an evaluation metric for some problem.
# The typing algorithm is based on majority voting with neighboring trigger words,
#  so called MajVote-Trigger
def step2():
    # Read list of stopwords
    stopwordset = set()
    fr = open('input/stopwords.txt','r')
    for line in fr:
        stopwordset.add(line.strip('\r\n'))
    fr.close()

    # Count the number of docs for progress bar
    ndoc = 0
    fr = open('output/step1.txt','r')
    for line in fr:
        ndoc += 1
    fr.close()

    # Count left/right neighbor words of concepts (lower case)
    entity2count = {}
    entity2neighbor2count = {} # Left neighbors and right neighbors
    fr = open('output/step1.txt','r')
    idoc = 0    
    for line in fr:
        # Show progress bar
        idoc += 1
        if idoc % 10 == 0 or idoc == ndoc:
            sys.stdout.write('\r\tProgress: '+str(0.01*int(10000.0*idoc/ndoc))+'%'+' Doc. '+str(idoc)+' / '+str(ndoc)+'                    ')
            sys.stdout.flush()
        # Read through the document and count neighbor words
        pid,text = line.strip('\r\n').split('\t')
        words = text.split(' ')
        l = len(words)
        for i in range(l):
            if not words[i].startswith('$e:'): continue
            pos = words[i].rfind(':')
            entity = words[i][pos+1:]
            if not entity in entity2count:
                entity2count[entity] = 0
            entity2count[entity] += 1
            for j in range(i-1,-1,-1): # Left neighbors
                if words[j].startswith('#') or words[j].startswith('$e:') or (len(words[j]) == 1 and not words[j].isalpha()): break
                neighbor = words[j].lower()               
                if neighbor in stopwordset: continue
                if neighbor.isalpha():
                    if not entity in entity2neighbor2count:
                        entity2neighbor2count[entity] = [{},{}]
                    if not neighbor in entity2neighbor2count[entity][0]:
                        entity2neighbor2count[entity][0][neighbor] = 0
                    entity2neighbor2count[entity][0][neighbor] += 1
            for j in range(i+1,l): # Right neighbors
                if words[j].startswith('#') or words[j].startswith('$e:') \
                    or (len(words[j]) == 1 and not words[j].isalpha()): break
                neighbor = words[j].lower()                
                if neighbor in stopwordset: continue
                if neighbor.isalpha():                
                    if not entity in entity2neighbor2count:
                        entity2neighbor2count[entity] = [{},{}]
                    if not neighbor in entity2neighbor2count[entity][1]:
                        entity2neighbor2count[entity][1][neighbor] = 0
                    entity2neighbor2count[entity][1][neighbor] += 1
    fr.close()

    fw = open('output/step2-support.txt','w')
    for [entity,count] in sorted(entity2count.items(),key=lambda x:-x[1]):
        fw.write(entity+'\t'+str(count)+'\n')
    fw.close()

    # Output left/right neighbor words of concepts and their counts
    fw = open('output/step2-neighbor.txt','w')
    for [entity,[neighbor2countLeft,neighbor2countRight]] in sorted(entity2neighbor2count.items(),key=lambda x:x[0]):
        outputLeft = ''
        for [neighbor,count] in sorted(neighbor2countLeft.items(),key=lambda x:-x[1]):
            outputLeft += ' '+neighbor+'|'+str(count)
        if outputLeft == '':
            outputLeft = 'NA'
        else:
            outputLeft = outputLeft[1:]
        outputRight = ''
        for [neighbor,count] in sorted(neighbor2countRight.items(),key=lambda x:-x[1]):
            outputRight += ' '+neighbor+'|'+str(count)
        if outputRight == '':
            outputRight = 'NA'
        else:
            outputRight = outputRight[1:]
        fw.write(entity+'\t'+outputLeft+'\t'+outputRight+'\n')
    fw.close()

    # Read the neighbor words and counts
    entity2neighbors = {}
    fr = open('output/step2-neighbor.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        entity = arr[0]
        entity2neighbors[entity] = [[],[]] # left, right
        if not arr[1] == 'NA':
            for neighborcount in arr[1].split(' '):
                neighbor,strcount = neighborcount.split('|')
                count = int(strcount)
                entity2neighbors[entity][0].append([neighbor,count])
        if not arr[2] == 'NA':
            for neighborcount in arr[2].split(' '):
                neighbor,strcount = neighborcount.split('|')
                count = int(strcount)
                entity2neighbors[entity][1].append([neighbor,count])
    fr.close()

    # Read trigger words and their mapping to the type category from
    #  triggers.txt
    #  Column 1: trigger word (lower case)
    #  Column 2: L(eft) or R(ight) neighbor
    #  Column 3: type category to vote for
    tag_pos_tp = []
    fr = open('input/triggers.txt','r')
    for line in fr:
        tag_pos_tp.append(line.strip('\r\n').split('\t'))
    fr.close()

    # MajVote-Trigger: Predict concept type given neighbor words
    entity2tppredict = {}
    fw = open('output/step2-typing.txt','w')
    fr = open('input/vocabulary.txt','r')
    for line in fr:
        entity = line.strip('\r\n')
        entity = entity.replace(' ','_')
        tp2count = {}
        if entity in entity2neighbors:
            for [tag,pos,tp] in tag_pos_tp:
                if pos == 'L':
                    for [neighbor,count] in entity2neighbors[entity][0]:
                        if tag == neighbor:
                            if not tp in tp2count:
                                tp2count[tp] = 0
                            tp2count[tp] += count
                elif pos == 'R':
                    for [neighbor,count] in entity2neighbors[entity][1]:
                        if tag == neighbor:
                            if not tp in tp2count:
                                tp2count[tp] = 0
                            tp2count[tp] += count
        tp_count = sorted(tp2count.items(),key=lambda x:-x[1])
        tpstr = ''
        for [tp,count] in tp_count:
            tpstr += ' '+tp+'|'+str(count)
        tppredict = 'CONCEPT' # The default type is CONCEPT
        if not tpstr == '':
            tpstr = tpstr[1:]
            tppredict = tp_count[0][0] # Predicted as the most voted type
        fw.write(entity+'\t'+tppredict+'\t'+tpstr+'\n')
        entity2tppredict[entity] = tppredict
    fr.close()
    fw.close()

    # Evaluate concept typing based on the ground truth "syllabus"
    flag2count = {}
    fw = open('output/step2-typing-evaluate.txt','w')
    fr = open('input/syllabus.txt','r')
    for line in fr:
        text = line.strip('\r\n')
        pos = text.rfind('-->')
        tptruth = text[pos+3:]
        entity = text[0:pos]
        if '_' in entity:
            pos = entity.find('_')
            entity = entity[pos+1:]
        entity = entity.replace(' ','_')
        tppredict = entity2tppredict[entity]
        flag = 'F'
        if tppredict == tptruth:
            flag = 'T'
        if not flag in flag2count:
            flag2count[flag] = 0
        flag2count[flag] += 1
        fw.write(entity+'\t'+tptruth+'\t'+tppredict+'\t'+flag+'\n')
    fr.close()
    s = '#'
    nT,nAll = 0,0
    for [flag,count] in sorted(flag2count.items(),key=lambda x:x[0]):
        s += ' '+flag+'|'+str(count)
        if flag == 'T':
            nT += count
        nAll += count
    accuracy = 1.0*nT/nAll
    fw.write(s+'\t'+str(accuracy)+'\n')
    fw.close()

    print('\n\tTyping accuracy (MajVote-Trigger): '+str(accuracy))

    # Replace "e" as the type for each concept in the compressed corpus 
    fw = open('output/step2.txt','w')
    fr = open('output/step1.txt','r')
    for line in fr:
        output = ''
        pid,text = line.strip('\r\n').split('\t')
        words = text.split(' ')
        l = len(words)
        for i in range(l):
            if words[i].startswith('$e:'):
                pos = words[i].rfind(':')
                entity = words[i][pos+1:]
                tp = entity2tppredict[entity]
                pos = words[i].find(':')
                output += ' $'+tp+words[i][pos:]
            else:
                output += ' '+words[i]
        fw.write(pid+'\t'+output[1:]+'\n')
    fr.close()
    fw.close()

# This function extracts relations of three types:
#  (1) synonym(left,right): symmetric
#  (2) ancestor(left,right): asymmetric
#  (3) sibling(left,right): symmetric
# by Hearst (Hearst Pattern Matching)
def step3():
    index,nindex = [{}],1 # textual pattern's element index

    # Build pattern element index (Trie tree) for pattern matching    
    fr = open('input/patterns.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        pattern = arr[0]
        mapping = []
        for i in range(1,len(arr)):
            _arr = arr[i].split('_')
            reltype = _arr[0]
            ordleft = int(_arr[1])
            ordright = int(_arr[2])
            enablepl = _arr[3]
            mapping.append([reltype,ordleft,ordright,enablepl])
        words = pattern.split(' ')
        n = len(words)
        if n > nindex:
            for i in range(nindex,n):
                index.append({})
            nindex = n
        temp = index[n-1]
        if n > 1:
            for i in range(n-1):
                word = words[i]
                if not word in temp:
                    temp[word] = {}
                temp = temp[word]
            word = words[n-1]
        else:
            word = words[0]
        temp[word] = [pattern,pattern.split(' '),mapping]
    fr.close()

    # Count the number of docs for progress bar
    ndoc = 0
    fr = open('output/step2.txt','r')
    for line in fr:
        ndoc += 1
    fr.close()

    # Relation extraction using pattern matching
    # Output pattern matching
    #  Column 1: Hearst pattern
    #  Column 2: Matched segment in the document
    relation2count = {}
    fw = open('output/step3-pattern.txt','w')
    fr = open('output/step2.txt','r')
    idoc = 0
    for line in fr:
        # Show progress bar
        idoc += 1
        if idoc % 10 == 0 or idoc == ndoc:        
            sys.stdout.write('\r\tProgress: '+str(0.01*int(10000.0*idoc/ndoc))+'%'+' Doc. '+str(idoc)+' / '+str(ndoc)+'                    ')
            sys.stdout.flush()
        # Pattern matching using Trie tree search
        words = line.strip('\r\n').split(' ')
        l = len(words)
        i = 0
        while i < l:
            isvalid = False
            for j in range(min(nindex,l-i),0,-1):
                temp = index[j-1]
                k = 0
                while k < j and i+k < l:
                    tempword = words[i+k]
                    if tempword == '$':
                        tempword = 'USD'
                    elif tempword.startswith('$'):
                        tempword = '$'
                    elif len(tempword) > 3 and tempword.endswith('s') and '<pl>' in temp:
                        tempword = '<pl>'
                    if not tempword in temp: break
                    temp = temp[tempword]
                    k += 1
                if k == j:
                    pattern,elems,mapping = temp
                    for [reltype,ordleft,ordright,enablepl] in mapping:
                        posleft,posright,pospls = -1,-1,[]
                        _ord = 0
                        for _i in range(0,len(elems)):
                            if elems[_i] == '$':
                                _ord += 1
                                if _ord == ordleft:
                                    posleft = _i
                                if _ord == ordright:
                                    posright = _i
                            if enablepl == 'T' and elems[_i] == '<pl>':
                                pospls.append(_i)
                        if posleft < 0 or posright < 0: continue
                        relation = ''
                        _posleft = words[i+posleft].rfind(':')
                        _posright = words[i+posright].rfind(':')
                        _posleft_ = words[i+posleft].find(':')
                        _posright_ = words[i+posright].find(':')
                        surfaceleft = words[i+posleft][_posleft_+1:_posleft]
                        surfaceright = words[i+posright][_posright_+1:_posright]
                        entityleft = words[i+posleft][_posleft+1:]
                        entityright = words[i+posright][_posright+1:]
                        if entityleft == entityright: continue
                        context = ''
                        if len(pospls) > 0:
                            for pospl in pospls:
                                context += ' '+words[i+pospl]
                            context = context[1:]
                        relation = reltype+'\t'+entityleft+'\t'+entityright # +'\t'+context # context ignored
                        if not relation in relation2count:
                            relation2count[relation] = 0
                        relation2count[relation] += 1
                    surface = ''
                    for _k in range(0,j):
                        surface += ' '+words[i+_k]
                    fw.write(pattern+'\t'+surface[1:]+'\n')
                    isvalid = True
                    break
            if isvalid:
                i += k
                continue
            i += 1
    fr.close()
    fw.close()

    # Output relations
    #  Column 1: relation type
    #  Column 2: left entity
    #  Column 3: right entity
    #  (context ignored)
    #  Column 4: count
    fw = open('output/step3-relation.txt','w')
    for [relation,count] in sorted(relation2count.items(),key=lambda x:-x[1]):
        fw.write(relation+'\t'+str(count)+'\n')
    fw.close()

# This function conducts the following tasks:
#  (1) Synonym clustering: group synonym concepts into a cluster;
#  (2) Sibling clustering: group sibling concept clusters into a level cluster;
#  (3) Re-typing: assume that synonym/sibling concepts have the same type;
#  (4) Typing evaluation: re-evaluate the refined typing results.
def step4():
    # parameter: trust the sibling relation if count >= MIN_COUNT_SIBLING
    MIN_COUNT_SIBLING = 3

    # Relation: (relation type, left entity, right entity, count)
    relation_count = []
    # Synonym amended
    fr = open('input/domainknowledge.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        concept1,concept2,reltype = arr[0],arr[1],arr[2]
        relation_count.append([reltype,concept1,concept2,MAXINF])
    fr.close()
    concepts = []
    fr = open('output/step2-typing.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        concept = arr[0]
        concepts.append(concept)
    fr.close()
    concepts = sorted(concepts)
    nConcept = len(concepts)
    for i in range(0,nConcept-1):
        if concepts[i]+'s' == concepts[i+1] or \
            concepts[i].replace('-','_') == concepts[i+1].replace('-','_') or \
            (concepts[i+1].count('_') == concepts[i].count('_')+1 and concepts[i+1].startswith(concepts[i]+'_')):
            relation_count.append(['synonym',concepts[i],concepts[i+1],MAXINF])
    # Read relation
    fr = open('output/step3-relation.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        reltype = arr[0]
        entityleft = arr[1]
        entityright = arr[2]
        count = int(arr[3])
        relation_count.append([reltype,entityleft,entityright,count])
    fr.close()

    # Group synonym concepts/entities into clusters
    entity2clustername = {} # entity -> cluster
    clustername2entityset = {} # entity cluster -> set of entities
    entity2nonsynonymset = {} # if not synonyms...
    for [reltype,entityleft,entityright,count] in relation_count:
        if count < 2: break
        if not reltype == 'synonym':
            if not entityleft in entity2nonsynonymset:
                entity2nonsynonymset[entityleft] = set()
            entity2nonsynonymset[entityleft].add(entityright)
            if not entityright in entity2nonsynonymset:
                entity2nonsynonymset[entityright] = set()
            entity2nonsynonymset[entityright].add(entityleft)
    for [reltype,entityleft,entityright,count] in relation_count:
        if not reltype == 'synonym': continue
        if (entityleft in entity2nonsynonymset and entityright in entity2nonsynonymset[entityleft]) \
            or (entityright in entity2nonsynonymset and entityleft in entity2nonsynonymset[entityright]):
            continue
        if entityleft[0].isalpha() and entityright[0].isalpha() \
            and not entityleft[0].lower() == entityright[0].lower():
            continue
        if entityleft in entity2clustername and entityright in entity2clustername:
            clusterleft = entity2clustername[entityleft]
            clusterright = entity2clustername[entityright]
            if not clusterleft == clusterright:
                entityset = set()
                entityset = entityset | clustername2entityset[clusterleft]
                entityset = entityset | clustername2entityset[clusterright]
                entitylist = sorted(entityset,key=lambda x:-len(x))
                clustername = entitylist[0]
                del clustername2entityset[clusterleft]
                del clustername2entityset[clusterright]
                for entity in entityset:
                    entity2clustername[entity] = clustername
                clustername2entityset[clustername] = entityset
        elif entityleft in entity2clustername and not entityright in entity2clustername:
            clustername = entity2clustername[entityleft]
            entity2clustername[entityright] = clustername
            clustername2entityset[clustername].add(entityright)
        elif not entityleft in entity2clustername and entityright in entity2clustername:
            clustername = entity2clustername[entityright]
            entity2clustername[entityleft] = clustername
            clustername2entityset[clustername].add(entityleft)
        else:
            entityset = set([entityleft,entityright])
            entitylist = sorted(entityset,key=lambda x:-len(x))
            clustername = entitylist[0]
            entity2clustername[entityleft] = clustername
            entity2clustername[entityright] = clustername
            clustername2entityset[clustername] = entityset
    # Make single-concept/entity clusters (optional)
    for [reltype,entityleft,entityright,count] in relation_count:
        if not entityleft in entity2clustername:
            entity2clustername[entityleft] = entityleft
            clustername2entityset[entityleft] = set([entityleft])
        if not entityright in entity2clustername:
            entity2clustername[entityright] = entityright
            clustername2entityset[entityright] = set([entityright])

    # Read ancestor relationship 
    cluster2ancestorset = {}
    for [reltype,entityleft,entityright,count] in relation_count:
        if reltype == 'ancestor':
            if entityleft in entity2clustername and entityright in entity2clustername:
                clusterleft = entity2clustername[entityleft]
                clusterright = entity2clustername[entityright]
                if not clusterleft in cluster2ancestorset:
                    cluster2ancestorset[clusterleft] = set()
                cluster2ancestorset[clusterleft].add(clusterright)
                if not clusterright in cluster2ancestorset:
                    cluster2ancestorset[clusterright] = set()
                cluster2ancestorset[clusterright].add(clusterleft)

    # Group sibling concept/entity clusters as a "level" cluster
    cluster2level = {}
    level2clusterset = {}
    for [reltype,entityleft,entityright,count] in relation_count:
        if not (reltype == 'sibling' and entityleft in entity2clustername and entityright in entity2clustername):
            continue
        if count < MIN_COUNT_SIBLING:
                continue        
        clusterleft = entity2clustername[entityleft]
        clusterright = entity2clustername[entityright]
        if (clusterleft in cluster2ancestorset and clusterright in cluster2ancestorset[clusterleft]) \
            or (clusterright in cluster2ancestorset and clusterleft in cluster2ancestorset[clusterright]):
            continue
        if clusterleft in cluster2level and clusterright in cluster2level:
            levelleft = cluster2level[clusterleft]
            levelright = cluster2level[clusterright]
            if not levelleft == levelright:
                clusterset = set()
                clusterset = clusterset | level2clusterset[levelleft]
                clusterset = clusterset | level2clusterset[levelright]
                clusterlist = sorted(clusterset,key=lambda x:-len(x))
                level = clusterlist[0]
                del level2clusterset[levelleft]
                del level2clusterset[levelright]
                for cluster in clusterset:
                    cluster2level[cluster] = level
                level2clusterset[level] = clusterset
        elif clusterleft in cluster2level and not clusterright in cluster2level:
            level = cluster2level[clusterleft]
            cluster2level[clusterright] = level
            level2clusterset[level].add(clusterright)
        elif not clusterleft in cluster2level and clusterright in cluster2level:
            level = cluster2level[clusterright]
            cluster2level[clusterleft] = level
            level2clusterset[level].add(clusterleft)
        else:
            clusterset = set([clusterleft,clusterright])
            clusterlist = sorted(clusterset,key=lambda x:-len(x))
            level = clusterlist[0]
            cluster2level[clusterleft] = level
            cluster2level[clusterright] = level
            level2clusterset[level] = clusterset

    # Output synonym/sibling concept clusters
    fw = open('output/step4-cluster.txt','w')
    for [clustername,entityset] in sorted(clustername2entityset.items(),key=lambda x:x[0]):
        if len(entityset) == 1: continue
        s = ''
        for entity in sorted(entityset):
            s += '|'+entity
        fw.write('synonym'+'\t'+clustername+'\t'+s[1:]+'\n')
    for [level,clusterset] in sorted(level2clusterset.items(),key=lambda x:x[0]):
        s = ''
        for cluster in sorted(clusterset):
            s += '|'+cluster
        fw.write('sibling'+'\t'+level+'\t'+s[1:]+'\n')
    fw.close()

    # Read synonym/sibling concept clusters
    entity2cluster = {}
    cluster2entityset = {}
    cluster2level = {}
    level2clusterset = {}
    fr = open('output/step4-cluster.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        reltype = arr[0]
        if reltype == 'synonym':
            cluster = arr[1]
            cluster2entityset[cluster] = set()
            for entity in arr[2].split('|'):
                entity2cluster[entity] = cluster
                cluster2entityset[cluster].add(entity)
        if reltype == 'sibling':
            level = arr[1]
            level2clusterset[level] = set()
            for cluster in arr[2].split('|'):
                cluster2level[cluster] = level
                level2clusterset[level].add(cluster)
                if not cluster in entity2cluster:
                    entity = cluster
                    entity2cluster[entity] = cluster
                    cluster2entityset[cluster] = set([entity])
    fr.close()

    # Merge synonym/sibling concept clusters into "type groups", assuming that
    #  (1) synonyms have the same concept type;
    #  (2) siblings have the same concept type.
    entity2typegroup = {}
    typegroup = 0
    allclusterset = set()
    for [level,clusterset] in level2clusterset.items():
        typegroup += 1
        allclusterset = allclusterset | clusterset
        for cluster in clusterset:
            for entity in cluster2entityset[cluster]:
                entity2typegroup[entity] = typegroup
    for [cluster,entityset] in cluster2entityset.items():
        if cluster in allclusterset: continue
        typegroup += 1
        for entity in cluster2entityset[cluster]:
            entity2typegroup[entity] = typegroup

    # Read neighbor words of concepts, and then have neighbor words of "type groups"
    entity2neighbors = {}
    typegroup2neighbors = {}
    fr = open('output/step2-neighbor.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        entity = arr[0]
        if entity in entity2typegroup: # in type groups
            typegroup = entity2typegroup[entity]
            if not typegroup in typegroup2neighbors:
                typegroup2neighbors[typegroup] = [{},{}] # left, right
            if not arr[1] == 'NA':
                for neighborcount in arr[1].split(' '):
                    neighbor,strcount = neighborcount.split('|')
                    count = int(strcount)
                    if not neighbor in typegroup2neighbors[typegroup][0]:
                        typegroup2neighbors[typegroup][0][neighbor] = 0
                    typegroup2neighbors[typegroup][0][neighbor] += count
            if not arr[2] == 'NA':
                for neighborcount in arr[2].split(' '):
                    neighbor,strcount = neighborcount.split('|')
                    count = int(strcount)
                    if not neighbor in typegroup2neighbors[typegroup][1]:
                        typegroup2neighbors[typegroup][1][neighbor] = 0
                    typegroup2neighbors[typegroup][1][neighbor] += count
        else: # not in type groups
            entity2neighbors[entity] = [[],[]] # left, right
            if not arr[1] == 'NA':
                for neighborcount in arr[1].split(' '):
                    neighbor,strcount = neighborcount.split('|')
                    count = int(strcount)
                    entity2neighbors[entity][0].append([neighbor,count])
            if not arr[2] == 'NA':
                for neighborcount in arr[2].split(' '):
                    neighbor,strcount = neighborcount.split('|')
                    count = int(strcount)
                    entity2neighbors[entity][1].append([neighbor,count])
    fr.close()

    # Read trigger words for typing
    tag_pos_tp = []
    fr = open('input/triggers.txt','r')
    for line in fr:
        tag_pos_tp.append(line.strip('\r\n').split('\t'))
    fr.close()

    # Re-predict the concept type
    entity2tppredict = {}
    fw = open('output/step4-typing.txt','w')
    fr = open('input/vocabulary.txt','r')
    for line in fr:
        entity = line.strip('\r\n')
        entity = entity.replace(' ','_')
        tp2count = {}
        if entity in entity2typegroup:
            typegroup = entity2typegroup[entity]
            for [tag,pos,tp] in tag_pos_tp:
                if pos == 'L':
                    for [neighbor,count] in typegroup2neighbors[typegroup][0].items():
                        if tag == neighbor:
                            if not tp in tp2count:
                                tp2count[tp] = 0
                            tp2count[tp] += count
                elif pos == 'R':
                    for [neighbor,count] in typegroup2neighbors[typegroup][1].items():
                        if tag == neighbor:
                            if not tp in tp2count:
                                tp2count[tp] = 0
                            tp2count[tp] += count
        elif entity in entity2neighbors:
            for [tag,pos,tp] in tag_pos_tp:
                if pos == 'L':
                    for [neighbor,count] in entity2neighbors[entity][0]:
                        if tag == neighbor:
                            if not tp in tp2count:
                                tp2count[tp] = 0
                            tp2count[tp] += count
                elif pos == 'R':
                    for [neighbor,count] in entity2neighbors[entity][1]:
                        if tag == neighbor:
                            if not tp in tp2count:
                                tp2count[tp] = 0
                            tp2count[tp] += count
        tp_count = sorted(tp2count.items(),key=lambda x:-x[1])
        tpstr = ''
        for [tp,count] in tp_count:
            tpstr += ' '+tp+'|'+str(count)
        tppredict = 'CONCEPT'
        if not tpstr == '':
            tpstr = tpstr[1:]
            tppredict = tp_count[0][0]
        fw.write(entity+'\t'+tppredict+'\t'+tpstr+'\n')
        entity2tppredict[entity] = tppredict
    fr.close()
    fw.close()

    # Re-evaluate the concept type
    flag2count = {}
    fw = open('output/step4-typing-evaluate.txt','w')
    fr = open('input/syllabus.txt','r')
    for line in fr:
        text = line.strip('\r\n')
        pos = text.rfind('-->')
        tptruth = text[pos+3:]
        entity = text[0:pos]
        if '_' in entity:
            pos = entity.find('_')
            entity = entity[pos+1:]
        entity = entity.replace(' ','_')
        tppredict = entity2tppredict[entity]
        flag = 'F'
        if tppredict == tptruth:
            flag = 'T'
        if not flag in flag2count:
            flag2count[flag] = 0
        flag2count[flag] += 1
        fw.write(entity+'\t'+tptruth+'\t'+tppredict+'\t'+flag+'\n')
    fr.close()
    s = '#'
    nT,nAll = 0,0
    for [flag,count] in sorted(flag2count.items(),key=lambda x:x[0]):
        s += ' '+flag+'|'+str(count)
        if flag == 'T':
            nT += count
        nAll += count
    accuracy = 1.0*nT/nAll
    fw.write(s+'\t'+str(accuracy)+'\n')
    fw.close()

    print('\tRe-typing accuracy (MajVote-cluster): '+str(accuracy))

    # Count the number of docs for progress bar
    ndoc = 0
    fr = open('output/step2.txt','r')
    for line in fr:
        ndoc += 1
    fr.close()

    fw = open('output/step4.txt','w')
    fr = open('output/step1.txt','r')
    idoc = 0    
    for line in fr:
        # Show progress bar
        idoc += 1
        if idoc % 10 == 0 or idoc == ndoc:        
            sys.stdout.write('\r\tProgress: '+str(0.01*int(10000.0*idoc/ndoc))+'%'+' Doc. '+str(idoc)+' / '+str(ndoc)+'                    ')
            sys.stdout.flush()
        # Update concept types with retyping results
        output = ''
        pid,text = line.strip('\r\n').split('\t')
        words = text.split(' ')
        l = len(words)
        for i in range(l):
            if words[i].startswith('$e:'):
                pos = words[i].rfind(':')
                entity = words[i][pos+1:]
                tp = entity2tppredict[entity]
                pos = words[i].find(':')
                output += ' $'+tp+words[i][pos:]
            else:
                output += ' '+words[i]
        fw.write(pid+'\t'+output[1:]+'\n')
    fr.close()
    fw.close()

# This function conducts second-round relation extraction using pattern matching
def step5():
    index,nindex = [{}],1 # textual pattern's element index

    # Build pattern element index (Trie tree) for pattern matching
    fr = open('input/patterns.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        pattern = arr[0]
        mapping = []
        for i in range(1,len(arr)):
            _arr = arr[i].split('_')
            reltype = _arr[0]
            ordleft = int(_arr[1])
            ordright = int(_arr[2])
            enablepl = _arr[3]
            mapping.append([reltype,ordleft,ordright,enablepl])
        words = pattern.split(' ')
        n = len(words)
        if n > nindex:
            for i in range(nindex,n):
                index.append({})
            nindex = n
        temp = index[n-1]
        if n > 1:
            for i in range(n-1):
                word = words[i]
                if not word in temp:
                    temp[word] = {}
                temp = temp[word]
            word = words[n-1]
        else:
            word = words[0]
        temp[word] = [pattern,pattern.split(' '),mapping]
    fr.close()

    # Count the number of docs for progress bar
    ndoc = 0
    fr = open('output/step2.txt','r')
    for line in fr:
        ndoc += 1
    fr.close()

    # Second-round relation extraction using pattern matching
    # Output:
    #  Column 1: relation type
    #  Column 2: left element ($TYPE:<surface>:<entity>)
    #  Column 3: right element ($TYPE:<surface>:<entity>)
    #  Column 4: context
    #  Column 5: textual pattern (hearst pattern, etc.)
    #  Column 6: left entity $ order in pattern
    #  Column 7: right entity $ order in pattern
    fw = open('output/step5-extraction.txt','w')
    fr = open('output/step4.txt','r')
    idoc = 0    
    for line in fr:
        # Show progress bar
        idoc += 1
        if idoc % 10 == 0 or idoc == ndoc:        
            sys.stdout.write('\r\tProgress: '+str(0.01*int(10000.0*idoc/ndoc))+'%'+' Doc. '+str(idoc)+' / '+str(ndoc)+'                    ')
            sys.stdout.flush()
        # Pattern matching by Trie tree search
        words = line.strip('\r\n').split(' ')
        l = len(words)
        i = 0
        while i < l:
            isvalid = False
            for j in range(min(nindex,l-i),0,-1):
                temp = index[j-1]
                k = 0
                while k < j and i+k < l:
                    tempword = words[i+k]
                    if tempword == '$':
                        tempword = 'USD'
                    elif tempword.startswith('$'):
                        tempword = '$'
                    elif len(tempword) > 3 and tempword.endswith('s') and '<pl>' in temp:
                        tempword = '<pl>'
                    if not tempword in temp: break
                    temp = temp[tempword]
                    k += 1
                if k == j:
                    pattern,elems,mapping = temp
                    for [reltype,ordleft,ordright,enablepl] in mapping:
                        posleft,posright,pospls = -1,-1,[]
                        _ord = 0
                        for _i in range(0,len(elems)):
                            if elems[_i] == '$':
                                _ord += 1
                                if _ord == ordleft:
                                    posleft = _i
                                if _ord == ordright:
                                    posright = _i
                            if enablepl == 'T' and elems[_i] == '<pl>':
                                pospls.append(_i)
                        if posleft < 0 or posright < 0: continue
                        relation = ''
                        _posleft = words[i+posleft].rfind(':')
                        _posright = words[i+posright].rfind(':')
                        entityleft = words[i+posleft][_posleft+1:]
                        entityright = words[i+posright][_posright+1:]
                        if entityleft == entityright: continue
                        context = ''
                        if len(pospls) > 0:
                            for pospl in pospls:
                                context += ' '+words[i+pospl]
                            context = context[1:]
                        fw.write(reltype+'\t'+words[i+posleft]+'\t'+words[i+posright]+'\t'+context+'\t'+pattern+'\t'+str(ordleft)+'\t'+str(ordright)+'\n')
                    isvalid = True
                    break
            if isvalid:
                i += k
                continue
            i += 1
    fr.close()
    fw.close()

# This function infers concept hierarchies (min_sup = 10,5,3,2,1)
def step6():
    # from graphviz import Digraph

    MAXATTR = 3
    conceptset = set()
    conceptpair2reltype2count = {}
    concept2concepttype = {}
    fr = open('output/step5-extraction.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        reltype = arr[0]
        pos = arr[1].rfind(':')
        concept_left = arr[1][pos+1:]
        pos = arr[1].find(':')
        concepttype_left = arr[1][0:pos]
        pos = arr[2].rfind(':')
        concept_right = arr[2][pos+1:]
        pos = arr[2].find(':')
        concepttype_right = arr[2][0:pos]
        context = arr[3]
        conceptset.add(concept_left+' '+concepttype_left)
        conceptset.add(concept_right+' '+concepttype_right)
        concept2concepttype[concept_left] = concepttype_left
        concept2concepttype[concept_right] = concepttype_right
        if reltype == 'synonym':
            if not concept_left[0].lower() == concept_right[0].lower(): continue
        if reltype == 'ancestor': # asymmetric
            conceptpair = concept_left+'\t'+concept_right+'\t'+concepttype_left+'\t'+concepttype_right
        else: # symmetric (sorted)
            if not concepttype_left == concepttype_right: continue
            concept_type = sorted([[concept_left,concepttype_left], \
                    [concept_right,concepttype_right]],key=lambda x:x[0])
            conceptpair = concept_type[0][0]+'\t'+concept_type[1][0]+'\t'+concept_type[0][1]+'\t'+concept_type[1][1]
        if not conceptpair in conceptpair2reltype2count:
            conceptpair2reltype2count[conceptpair] = ['NA',-1,{}] # best reltype
        if not reltype in conceptpair2reltype2count[conceptpair][2]:
            conceptpair2reltype2count[conceptpair][2][reltype] = [0,{}]
        conceptpair2reltype2count[conceptpair][2][reltype][0] += 1
        if not context == '':
            if not context in conceptpair2reltype2count[conceptpair][2][reltype][1]:
                conceptpair2reltype2count[conceptpair][2][reltype][1][context] = 0
            conceptpair2reltype2count[conceptpair][2][reltype][1][context] += 1
    fr.close()
    for conceptpair in conceptpair2reltype2count:
        reltype_count = sorted(conceptpair2reltype2count[conceptpair][2].items(),key=lambda x:-x[1][0])
        conceptpair2reltype2count[conceptpair][0] = reltype_count[0][0]
        conceptpair2reltype2count[conceptpair][1] = reltype_count[0][1][0]
        if len(reltype_count) > 1 and reltype_count[0][1][0] == reltype_count[1][1][0]:
            conceptpair2reltype2count[conceptpair][1] = -1

    # load domain knowledge
    domainknowledge = []
    fr = open('input/domainknowledge.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        concept1,concept2,reltype = arr[0],arr[1],arr[2]
        if concept1 in concept2concepttype and concept2 in concept2concepttype:
            domainknowledge.append([concept1,concept2,concept2concepttype[concept1],concept2concepttype[concept2],reltype])
    fr.close()

    # output relations
    fw = open('output/step6-samplelinks.txt','w')
    # domain knowledge: ancestor/sibling/synonym
    for [concept1,concept2,concepttype1,concepttype2,reltype] in domainknowledge:
        fw.write(concept1+'\t'+concept2+'\t'+concepttype1+'\t'+concepttype2+'\t'+reltype+'\t'+str(MAXINF)+'\t'+''+'\n')
    # prior knowledge: prefix -> synonym
    conceptlist = sorted(conceptset)
    concepts = []
    for concept in conceptlist:
        pos = concept.find(' ')
        concepts.append([concept[0:pos],concept[pos+1:]])
    nConcept = len(concepts)
    for i in range(0,nConcept-1):
        if concepts[i][0]+'s' == concepts[i+1][0] or \
            concepts[i][0].replace('-','_') == concepts[i+1][0].replace('-','_') or \
            (concepts[i+1][0].count('_') == concepts[i][0].count('_')+1 and concepts[i+1][0].startswith(concepts[i][0]+'_')):
            fw.write(concepts[i][0]+'\t'+concepts[i+1][0]+'\t'+concepts[i][1]+'\t'+concepts[i+1][1]+'\t'+'synonym'+'\t'+str(MAXINF)+'\t'+''+'\n')
    # prior knowledge: postfix -> ancestor
    conceptlist = sorted([concept[::-1] for concept in conceptset])
    concepts = []
    for concept in conceptlist:
        pos = concept.find(' ')
        concepts.append([concept[pos+1:][::-1],concept[0:pos][::-1]])
    nConcept = len(concepts)
    for i in range(0,nConcept-1):
        if '_' in concepts[i][0] and concepts[i+1][0].endswith('_'+concepts[i][0]):
            fw.write(concepts[i][0]+'\t'+concepts[i+1][0]+'\t'+concepts[i][1]+'\t'+concepts[i+1][1]+'\t'+'ancestor'+'\t'+str(MAXINF)+'\t'+''+'\n')
    # relations from data
    for [conceptpair,[bestreltype,bestcount,reltype2count]] in \
        sorted(conceptpair2reltype2count.items(),key=lambda x:-x[1][1]):
        if bestcount < 0: break
        s0 = ''
        for [context,count] in sorted(reltype2count[bestreltype][1].items(),key=lambda x:-x[1]):
            s0 += '|'+context+':'+str(count)
        if not s0 == '':
            s0 = s0[1:]
        s1 = ''
        for [reltype,[count,context2count]] in sorted(reltype2count.items(),key=lambda x:-x[1][0]):
            s1 += '|'+reltype+':'+str(count)
        if not s1 == '':
            s1 = s1[1:]
        if bestreltype == 'ancestor':
            fw.write(conceptpair+'\t'+bestreltype+'\t'+str(bestcount)+'\t'+s0+'\n')
        else:
            fw.write(conceptpair+'\t'+bestreltype+'\t'+str(bestcount)+'\t'+''+'\n')
    fw.close()

    # reload the relations
    freq2reltype2conceptpairs = {}
    conceptpair_context_count = []
    concept2concepttype = {}    
    fr = open('output/step6-samplelinks.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        concept1,concept2 = arr[0],arr[1]
        concepttype1,concepttype2 = arr[2],arr[3]
        reltype,freq = arr[4],int(arr[5])
        context_count = []
        if not arr[6] == '':
            for elem in arr[6].split('|'):
                _arr = elem.split(':')
                context_count.append([_arr[0],int(_arr[1])])
        if not freq in freq2reltype2conceptpairs:
            freq2reltype2conceptpairs[freq] = {}
        if not reltype in freq2reltype2conceptpairs[freq]:
            freq2reltype2conceptpairs[freq][reltype] = []
        freq2reltype2conceptpairs[freq][reltype].append([concept1,concept2,concepttype1,concepttype2,context_count])
        conceptpair_context_count.append([concept1,concept2,concepttype1,concepttype2,context_count])
        concept2concepttype[concept1] = concepttype1
        concept2concepttype[concept2] = concepttype2
    fr.close()

    for MINFREQ in [10,5,3,2,1]:

        nodes = [] # node: ENABLED, SET OF CONCEPT NAMES (or 'N/A'), ATTRIBUTES (parent, child, ancestor, descendant)
        name2nodeid = {}
        for [freq,reltype2conceptpairs] in sorted(freq2reltype2conceptpairs.items(),key=lambda x:-x[0]):
            if freq < MINFREQ: break
            for [reltype,conceptpairs] in sorted(reltype2conceptpairs.items(),key=lambda x:x[0]):
                for [concept1,concept2,concepttype1,concepttype2,context_count] in sorted(conceptpairs,key=lambda x:-len(x[4])):
                    # generate nodes
                    if not concept1 in name2nodeid:
                        nodeid = len(nodes)
                        node = [True,set(),{}]
                        node[1].add(concept1)
                        nodes.append(node)
                        name2nodeid[concept1] = nodeid
                    if not concept2 in name2nodeid:
                        nodeid = len(nodes)
                        node = [True,set(),{}]
                        node[1].add(concept2)
                        nodes.append(node)
                        name2nodeid[concept2] = nodeid
                    nodeid1 = name2nodeid[concept1]
                    nodeid2 = name2nodeid[concept2]
                    # synonym(node1,node2): symmetric
                    if reltype == 'synonym':
                        nodeid = len(nodes)
                        node = [True,set(),{}]
                        for concept in nodes[nodeid1][1]:
                            node[1].add(concept)
                            name2nodeid[concept] = nodeid
                        for concept in nodes[nodeid2][1]:
                            node[1].add(concept)
                            name2nodeid[concept] = nodeid
                        value2attributeset = {}
                        for [value,attribute] in nodes[nodeid1][2].items():
                            if not value in value2attributeset:
                                value2attributeset[value] = set()
                            value2attributeset[value].add(attribute)
                        for [value,attribute] in nodes[nodeid2][2].items():
                            if not value in value2attributeset:
                                value2attributeset[value] = set()
                            value2attributeset[value].add(attribute)
                        for [value,attributeset] in value2attributeset.items():
                            if 'child' in attributeset and 'descendant' in attributeset:
                                attributeset.remove('descendant')
                            if 'parent' in attributeset and 'ancestor' in attributeset:
                                attributeset.remove('ancestor')
                            attributes = list(attributeset)
                            if not len(attributes) == 1: continue
                            attribute = attributes[0]
                            node[2][value] = attribute
                            if attribute == 'child':
                                nodes[value][2][nodeid] = 'parent'
                            elif attribute == 'descendant':
                                nodes[value][2][nodeid] = 'ancestor'
                            elif attribute == 'parent':
                                nodes[value][2][nodeid] = 'child'
                            elif attribute == 'ancestor':
                                nodes[value][2][nodeid] = 'descendant'
                        nodes.append(node)
                        nodes[nodeid1][0] = False
                        nodes[nodeid2][0] = False
                    # sibling(node1,node2): symmetric
                    elif reltype == 'sibling':
                        parentset1 = set()
                        for [value,attribute] in nodes[nodeid1][2].items():
                            if attribute == 'parent':
                                parentset1.add(value)
                        parentset2 = set()
                        for [value,attribute] in nodes[nodeid2][2].items():
                            if attribute == 'parent':
                                parentset2.add(value)
                        if len(parentset1 & parentset2) == 0:
                            connectedset1 = set()
                            cands = [nodeid1]
                            while len(cands) > 0:
                                newcands = []
                                for cand in cands:
                                    for [value,attribute] in nodes[cand][2].items():
                                        if not value in connectedset1:
                                            connectedset1.add(value)
                                            newcands.append(value)
                                cands = newcands
                            if nodeid2 in connectedset1: continue
                        ancestorset1 = set()
                        for [value,attribute] in nodes[nodeid1][2].items():
                            if attribute == 'parent' or attribute == 'ancestor':
                                ancestorset1.add(value)
                        ancestorset2 = set()
                        for [value,attribute] in nodes[nodeid2][2].items():
                            if attribute == 'parent' or attribute == 'ancestor':
                                ancestorset2.add(value)
                        if len(ancestorset1 & ancestorset2) > 0: continue
                        parentset = parentset1 | parentset2
                        childset = set()
                        for parent in parentset:
                            for [value,attribute] in nodes[parent][2].items():
                                if attribute == 'child':
                                    childset.add(value)
                        childset.add(nodeid1)
                        childset.add(nodeid2)
                        parentNonNAset = set()
                        parentNAset = set()
                        for parent in parentset:
                            names = list(nodes[parent][1])
                            if len(names) == 1 and names[0] == 'N/A':
                                parentNAset.add(parent)
                            else:
                                parentNonNAset.add(parent)
                        if len(parentNonNAset) == 0:
                            nodeid = len(nodes)
                            node = [True,set(),{}]
                            node[1].add('N/A')
                            nodes.append(node)
                            parentNonNAset.add(nodeid)
                        for parent in parentNAset:
                            nodes[parent][0] = False
                        for parent in parentNonNAset:
                            for child in childset:
                                nodes[parent][2][child] = 'child'
                                nodes[child][2][parent] = 'parent'
                    # ancestor(node1,node2): asymmetric
                    elif reltype == 'ancestor':
                        ancestorset1 = set()
                        cands = [nodeid1]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in ancestorset1 and (attribute == 'parent' or attribute == 'ancestor'):
                                        ancestorset1.add(value)
                                        newcands.append(value)
                            cands = newcands
                        ancestorset2 = set()
                        cands = [nodeid2]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in ancestorset2 and (attribute == 'parent' or attribute == 'ancestor'):
                                        ancestorset2.add(value)
                                        newcands.append(value)
                            cands = newcands
                        descendantset1 = set()
                        cands = [nodeid1]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in descendantset1 and (attribute == 'child' or attribute == 'descendant'):
                                        descendantset1.add(value)
                                        newcands.append(value)
                            cands = newcands
                        descendantset2 = set()
                        cands = [nodeid2]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in descendantset2 and (attribute == 'child' or attribute == 'descendant'):
                                        descendantset2.add(value)
                                        newcands.append(value)
                            cands = newcands
                        parentset1 = set()
                        cands = [nodeid1]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in parentset1 and (attribute == 'parent'):
                                        parentset1.add(value)
                                        newcands.append(value)
                            cands = newcands
                        parentset2 = set()
                        cands = [nodeid2]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in parentset2 and (attribute == 'parent'):
                                        parentset2.add(value)
                                        newcands.append(value)
                            cands = newcands
                        childset1 = set()
                        cands = [nodeid1]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in childset1 and (attribute == 'child'):
                                        childset1.add(value)
                                        newcands.append(value)
                            cands = newcands
                        childset2 = set()
                        cands = [nodeid2]
                        while len(cands) > 0:
                            newcands = []
                            for cand in cands:
                                for [value,attribute] in nodes[cand][2].items():
                                    if not value in childset2 and (attribute == 'child'):
                                        childset2.add(value)
                                        newcands.append(value)
                            cands = newcands
                        if len(parentset1 & parentset2) > 0: continue
                        if nodeid1 in ancestorset2 | descendantset2: continue
                        if nodeid2 in ancestorset1 | descendantset1: continue
                        children = list(childset1 & childset2)
                        if len(children) > 0:
                            for child in children:
                                del nodes[child][2][nodeid1]
                                del nodes[nodeid1][2][child]
                        nodes[nodeid1][2][nodeid2] = 'descendant'
                        nodes[nodeid2][2][nodeid1] = 'ancestor'

            # eliminate N/A
            nNode = len(nodes)
            for nodeid in range(0,nNode):
                if not nodes[nodeid][0]: continue
                names = list(nodes[nodeid][1])
                if not (len(names) == 1 and names[0] == 'N/A'): continue
                childset = set()
                for [value,attribute] in nodes[nodeid][2].items():
                    if attribute == 'child':
                        childset.add(value)
                ancestor2count = {}
                for child in childset:
                    for [value,attribute] in nodes[child][2].items():
                        if not value == nodeid and nodes[value][0] and (attribute == 'parent' or attribute == 'ancestor'):
                            if not value in ancestor2count:
                                ancestor2count[value] = 0
                            ancestor2count[value] += 1
                nAncestor = len(ancestor2count)
                ancestors = []
                if nAncestor == 0:
                    continue
                elif nAncestor == 1:
                    for ancestor in ancestor2count:
                        ancestors.append(ancestor)
                else:
                    for [ancestor,count] in ancestor2count.items():
                        if count >= 2:
                            ancestors.append(ancestor)
                for ancestor in ancestors:
                    for [value,attribute] in nodes[nodeid][2].items():
                        if attribute == 'child':
                            nodes[ancestor][2][value] = 'child'
                            nodes[value][2][ancestor] = 'parent'
                        elif attribute == 'descendant':
                            nodes[ancestor][2][value] = 'descendant'
                            nodes[value][2][ancestor] = 'ancestor'
                        elif attribute == 'parent':
                            nodes[ancestor][2][value] = 'parent'
                            nodes[value][2][ancestor] = 'child'
                        elif attribute == 'ancestor':
                            nodes[ancestor][2][value] = 'ancestor'
                            nodes[value][2][ancestor] = 'descendant'
                nodes[nodeid][0] = False

        # only ancestor and no parent -> parent
        nNode = len(nodes)
        for nodeid in range(0,nNode):
            if not nodes[nodeid][0]: continue
            parentset = set()        
            ancestorset = set()
            for [value,attribute] in nodes[nodeid][2].items():
                if attribute == 'parent':
                    parentset.add(value)
                elif attribute == 'ancestor':
                    ancestorset.add(value)
            if len(parentset) == 0 and len(ancestorset) > 0:
                for ancestor in ancestorset:
                    nodes[ancestor][2][nodeid] = 'child'            
                    nodes[nodeid][2][ancestor] = 'parent'

        # attribute name clustering
        parentid2childtype2context2count = {}
        for [concept1,concept2,concepttype1,concepttype2,context_count] in conceptpair_context_count:
            if not concept1 in name2nodeid: continue
            if not concept2 in name2nodeid: continue
            nodeid1 = name2nodeid[concept1]
            nodeid2 = name2nodeid[concept2]
            if nodeid2 in nodes[nodeid1][2]:
                attribute = nodes[nodeid1][2][nodeid2]
                if attribute == 'child' or attribute == 'descendant':                
                    parentid = nodeid1
                    childtype = concepttype2
                    if not parentid in parentid2childtype2context2count:
                        parentid2childtype2context2count[parentid] = {}
                    if not childtype in parentid2childtype2context2count[parentid]:
                        parentid2childtype2context2count[parentid][childtype] = {}
                    for [context,count] in context_count:
                        if not context in parentid2childtype2context2count[parentid][childtype]:
                            parentid2childtype2context2count[parentid][childtype][context] = 0
                        parentid2childtype2context2count[parentid][childtype][context] += count
            else:
                parentset1 = set()
                parentset2 = set()
                for [value,attribute] in nodes[nodeid1][2].items():
                    if attribute == 'parent':
                        parentset1.add(value)
                for [value,attribute] in nodes[nodeid2][2].items():
                    if attribute == 'parent':
                        parentset2.add(value)
                parentset = parentset1 & parentset2
                for parentid in parentset:
                    childtype = concepttype2
                    if not parentid in parentid2childtype2context2count:
                        parentid2childtype2context2count[parentid] = {}
                    if not childtype in parentid2childtype2context2count[parentid]:
                        parentid2childtype2context2count[parentid][childtype] = {}
                    for [context,count] in context_count:
                        if not context in parentid2childtype2context2count[parentid][childtype]:
                            parentid2childtype2context2count[parentid][childtype][context] = 0
                        parentid2childtype2context2count[parentid][childtype][context] += count

        # select the best context for (parent node, child node type)
        parentid2childtype2contextstr = {}
        for [parentid,childtype2context2count] in parentid2childtype2context2count.items():
            for [childtype,context2count] in childtype2context2count.items():
                if len(context2count) == 0: continue
                context_count = sorted(context2count.items(),key=lambda x:-x[1])
                count2contextset = {}
                for [context,count] in context_count:
                    if not count in count2contextset:
                        count2contextset[count] = set()
                    count2contextset[count].add(context)
                count_contextset = sorted(count2contextset.items(),key=lambda x:-x[0])
                contexts = sorted(count_contextset[0][1])
                contextstr = contexts[0]
                if not parentid in parentid2childtype2contextstr:
                    parentid2childtype2contextstr[parentid] = {}
                parentid2childtype2contextstr[parentid][childtype] = contextstr
        for nodeid in range(0,nNode):
            if not nodes[nodeid][0]: continue
            value_contextstr = []
            for [value,attribute] in nodes[nodeid][2].items():
                if attribute == 'child' or attribute == 'descendant':
                    parentid = nodeid
                    childconcepts = list(nodes[value][1])
                    childtype = concept2concepttype[childconcepts[0]]
                    if parentid in parentid2childtype2contextstr and childtype in parentid2childtype2contextstr[parentid]:
                        contextstr = parentid2childtype2contextstr[parentid][childtype]
                        value_contextstr.append([value,contextstr])
            for [value,contextstr] in value_contextstr:
                nodes[nodeid][2][value] = contextstr

        # node placement
        nNode = len(nodes)
        nodeids = []
        nodeid2level = {}
        for nodeid in range(0,nNode):
            node = nodes[nodeid]
            if not node[0]: continue
            nodeid2level[nodeid] = [0,0] # level, #child/descendant
            for [value,attribute] in node[2].items():
                if not nodes[value][0]: continue
                if attribute == 'child' or attribute == 'descendant':
                    nodeid2level[nodeid][1] += 1
        while True:
            ifchanged = False
            for nodeid in nodeid2level:
                node = nodes[nodeid]            
                for [value,attribute] in node[2].items():
                    if not nodes[value][0]: continue
                    level = nodeid2level[nodeid][0]+1                
                    if attribute == 'child' or attribute == 'descendant':
                        if value in nodeid2level:
                            if nodeid2level[value][0] < level:
                                nodeid2level[value][0] = level
                                ifchanged = True
            if not ifchanged: break
        nodeid_level = sorted(nodeid2level.items(),key=lambda x:MAXINF*x[1][0]-x[1][1])

        # output into .md (Typora mermaid)
        fw = open('output/step6-hierarchy-minfreq-'+str(MINFREQ)+'.md','w')
        fw.write('```mermaid\ngraph LR\n')
        for [nodeid,level] in nodeid_level:
            node = nodes[nodeid]        
            nodename = 'N'+str(nodeid)
            nodeconcept = ''
            for concept in sorted(node[1]):
                nodeconcept += ','+concept
            nodeconcept = nodeconcept[1:]
            fw.write(nodename+'['+nodeconcept+']\n')
        for [nodeid,level] in nodeid_level:
            node = nodes[nodeid]        
            nodename = 'N'+str(nodeid)
            for [value,attribute] in node[2].items():
                if not value in nodeid2level: continue
                if not (attribute == 'parent' or attribute == 'ancestor'):
                    childnodename = 'N'+str(value)
                    fw.write(nodename+' --> |'+attribute+'| '+childnodename+'\n')             
        fw.write('```\n')
        fw.close()

        # output into graphviz
        # dot = Digraph()
        # dot.graph_attr['rankdir'] = 'LR'
        # dot.graph_attr['ratio'] = 'compress'
        # for [nodeid,level] in nodeid_level:
        #     node = nodes[nodeid]        
        #     nodename = 'N'+str(nodeid)
        #     nodeconcept = ''
        #     for concept in sorted(node[1]):
        #         nodeconcept += ','+concept
        #     nodeconcept = nodeconcept[1:]
        #     dot.node(nodename,nodeconcept)
        # for [nodeid,level] in nodeid_level:
        #     node = nodes[nodeid]        
        #     nodename = 'N'+str(nodeid)
        #     for [value,attribute] in node[2].items():
        #         if not value in nodeid2level: continue
        #         if not (attribute == 'parent' or attribute == 'ancestor'):
        #             _color = 'black'
        #             if attribute == 'child' or attribute == 'descendant':
        #                 attribute = 'child'
        #             else:
        #                 _color = 'blue'
        #             childnodename = 'N'+str(value)
        #             dot.edge(nodename,childnodename,label=attribute,fontcolor=_color,color=_color)
        # dot.render('output/step6-hierarchy-minfreq-'+str(MINFREQ),view=False)

def figure_item_support():
    reltype2counts = {}
    fr = open('output/step6-samplelinks.txt','r')
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        reltype,count = arr[4],int(arr[5])
        if count == MAXINF: continue
        if not reltype in reltype2counts:
            reltype2counts[reltype] = []
        reltype2counts[reltype].append(count)
    fr.close()
    for [reltype,counts] in reltype2counts.items():
        fw = open('output/item_support_'+reltype+'.txt','w')
        fw.write(reltype+'(X,Y)\tsupport\n')
        for i in range(0,len(counts)):
            fw.write(str(i+1)+'\t'+str(counts[i])+'\n')
        fw.close()

def table_evaluation():
    # load ground truth
    namea2nameb2hopTruth = {}
    name2synonymsTruth = {}
    name2facetTruth = {}
    fr = open('input/syllabus.txt','r')
    namepath = []
    line = fr.readline()
    pos = line.find('-->')
    name = line[0:pos].replace(' ','_')
    namepath.append(name)
    name2synonymsTruth[name] = set()
    name2synonymsTruth[name].add(name)
    for line in fr:
        pos = line.find('-->')
        text = line[0:pos]
        n = len(text)
        level = 0
        for i in range(n):
            if not text[i] == ' ': break
            level += 1
        facet_name = text[level:]
        pos = facet_name.find('_')
        facet = facet_name[0:pos]
        nameb = facet_name[pos+1:].replace(' ','_')
        name2synonymsTruth[nameb] = set()
        name2synonymsTruth[nameb].add(nameb)
        curlevel = len(namepath)
        if level == curlevel-1:
            namepath = namepath[:-1]
        elif not level == curlevel:
            namepath = namepath[0:level]
        namea = namepath[-1]
        if not namea in namea2nameb2hopTruth:
            namea2nameb2hopTruth[namea] = {}
        if not nameb in namea2nameb2hopTruth:
            namea2nameb2hopTruth[nameb] = {}
        if facet == 'synonym':
            name2synonymsTruth[namea].add(nameb)
        else:
            namea2nameb2hopTruth[namea][nameb] = 1
            namea2nameb2hopTruth[nameb][namea] = -1
            name2facetTruth[nameb] = facet
        namepath.append(nameb)
    fr.close()
    for [name,synonyms] in name2synonymsTruth.items():
        if not name in name2facetTruth: continue
        for synonym in synonyms:
            name2facetTruth[synonym] = name2facetTruth[name]
    # compute ground truth distance matrix
    namea2nameb2distTruth = {}
    for [namea,nameb2hop] in namea2nameb2hopTruth.items():
        nameb2dist = {}
        candnames = []        
        for [nameb,hop] in nameb2hop.items():
            nameb2dist[nameb] = abs(hop)
            candnames.append(nameb)
        while True:
            newnames = []
            for nameb in candnames:
                if not nameb in namea2nameb2hopTruth: continue
                for [name,hop] in namea2nameb2hopTruth[nameb].items():
                    if name in nameb2dist or name == namea: continue
                    nameb2dist[name] = nameb2dist[nameb]+abs(hop)
                    newnames.append(name)
            if len(newnames) == 0: break
            candnames = [name for name in newnames]
        namea2nameb2distTruth[namea] = nameb2dist
    for name in name2synonymsTruth:
        for synonyma in name2synonymsTruth[name]:
            for synonymb in name2synonymsTruth[name]:
                if synonyma == synonymb: continue
                if not synonyma in namea2nameb2distTruth:
                    namea2nameb2distTruth[synonyma] = {}
                if not synonymb in namea2nameb2distTruth:
                    namea2nameb2distTruth[synonymb] = {}
                namea2nameb2distTruth[synonyma][synonymb] = 0
                namea2nameb2distTruth[synonymb][synonyma] = 0
    namepair = []
    for namea in namea2nameb2distTruth:
        for nameb in namea2nameb2distTruth[namea]:
            namepair.append([namea,nameb])
    for [namea,nameb] in namepair:
        for synonyma in name2synonymsTruth[namea]:
            if not synonyma in namea2nameb2distTruth:
                namea2nameb2distTruth[synonyma] = {}
            for synonymb in name2synonymsTruth[nameb]:
                namea2nameb2distTruth[synonyma][synonymb] = namea2nameb2distTruth[namea][nameb]

    relationmap = {}
    relationmap['descendant'] = 'child'
    for relation in ['algorithms','approaches','methods','models','techniques']:
        relationmap[relation] = 'model'
    for relation in ['applications','problems','tasks']:
        relationmap[relation] = 'task'        
    for relation in ['measures','metrics']:
        relationmap[relation] = 'measure'

    fw = open('evaluation.txt','w')
    fw.write('MINFREQ\tDIST\tMAE\tRMSE\tPRECISION\tRECALL\tF1\tN\tHIT\tPRED\tTRUTH\n')
    for minfreq in [1,2,3,5,10]:
        # load prediction
        node2names = {}
        nodea2nodeb2hop = {}
        node2facet = {}
        name2facet = {}
        fr = open('output/step6-hierarchy-minfreq-'+str(minfreq)+'.md','r')
        fr.readline()
        fr.readline()
        for line in fr:
            text = line.strip('\r\n')
            if text == '```': break
            if '-->' in text:
                # link
                arr = text.split(' ')
                nodea,nodeb = arr[0],arr[-1]
                if not nodea in nodea2nodeb2hop:
                    nodea2nodeb2hop[nodea] = {}
                if not nodeb in nodea2nodeb2hop:
                    nodea2nodeb2hop[nodeb] = {}
                nodea2nodeb2hop[nodea][nodeb] = 1
                nodea2nodeb2hop[nodeb][nodea] = -1
                node2facet[nodea] = arr[2][1:-1]
            else:
                # node
                pos = text.find('[')
                node = text[0:pos]
                node2names[node] = []
                for name in text[pos+1:-1].split(','):
                    node2names[node].append(name)
        fr.close()
        for [node,facet] in node2facet.items():
            if not node in node2names: continue
            for name in node2names[node]:
                name2facet[name] = facet
        # compute prediction distance matrix
        nodea2nodeb2dist = {}
        namea2nameb2dist = {}
        for [nodea,nodeb2hop] in nodea2nodeb2hop.items():
            nodeb2dist = {}
            candnodes = []        
            for [nodeb,hop] in nodeb2hop.items():
                nodeb2dist[nodeb] = abs(hop)
                candnodes.append(nodeb)
            while True:
                newnodes = []
                for nodeb in candnodes:
                    if not nodeb in nodea2nodeb2hop: continue
                    for [node,hop] in nodea2nodeb2hop[nodeb].items():
                        if node in nodeb2dist or node == nodea: continue
                        nodeb2dist[node] = nodeb2dist[nodeb]+abs(hop)
                        newnodes.append(node)
                if len(newnodes) == 0: break
                candnodes = [node for node in newnodes]
            nodea2nodeb2dist[nodea] = nodeb2dist
        for [nodea,nodeb2dist] in nodea2nodeb2dist.items():
            for [nodeb,dist] in nodeb2dist.items():
                for namea in node2names[nodea]:
                    if not namea in namea2nameb2dist:
                        namea2nameb2dist[namea] = {}
                    for nameb in node2names[nodeb]:
                        namea2nameb2dist[namea][nameb] = dist
        for node in node2names:
            for namea in node2names[node]:
                for nameb in node2names[node]:
                    if namea == nameb: continue
                    if not namea in namea2nameb2dist:
                        namea2nameb2dist[namea] = {}
                    namea2nameb2dist[namea][nameb] = 0
        # evaluate
        namea2namebset = {}
        for [namea,nameb2distTruth] in namea2nameb2distTruth.items():
            if not namea in namea2namebset:
                namea2namebset[namea] = set()
            for nameb in nameb2distTruth:
                namea2namebset[namea].add(nameb)
        for [namea,nameb2dist] in namea2nameb2dist.items():
            if not namea in namea2namebset:
                namea2namebset[namea] = set()
            for nameb in nameb2dist:
                namea2namebset[namea].add(nameb)
        n = [0 for i in range(MAXDIST)]
        mae = [0.0 for i in range(MAXDIST)]
        rmse = [0.0 for i in range(MAXDIST)]
        hit = [0 for i in range(MAXDIST)]
        pred = [0 for i in range(MAXDIST)]
        truth = [0 for i in range(MAXDIST)]
        prec = [0.0 for i in range(MAXDIST)]
        recall = [0.0 for i in range(MAXDIST)]
        f1 = [0.0 for i in range(MAXDIST)]
        for [namea,namebset] in sorted(namea2namebset.items(),key=lambda x:x[0]):
            for nameb in sorted(namebset):
                distTruth,dist = -1,-1
                if namea in namea2nameb2distTruth and nameb in namea2nameb2distTruth[namea]:
                    distTruth = namea2nameb2distTruth[namea][nameb]
                if namea in namea2nameb2dist and nameb in namea2nameb2dist[namea]:
                    dist = namea2nameb2dist[namea][nameb]
                if distTruth < 0 and dist < 0: continue                    
                for i in range(MAXDIST):
                    if distTruth < 0 and dist <= i:
                        n[i] += 1
                        mae[i] += 1.0*dist
                        rmse[i] += 1.0*dist*dist
                        pred[i] += 1
                    elif dist < 0 and distTruth <= i:
                        n[i] += 1
                        mae[i] += 1.0*distTruth
                        rmse[i] += 1.0*distTruth*distTruth
                        truth[i] += 1
                    elif distTruth <= i:
                        n[i] += 1
                        mae[i] += 1.0*abs(distTruth-dist)
                        rmse[i] += 1.0*(distTruth-dist)*(distTruth-dist)
                        hit[i] += 1
                        pred[i] += 1
                        truth[i] += 1
        for i in range(MAXDIST):
            mae[i] = mae[i]/n[i]
            rmse[i] = (rmse[i]/n[i])**0.5
            prec[i] = 1.0*hit[i]/pred[i]
            recall[i] = 1.0*hit[i]/truth[i]
            if prec[i]+recall[i] > 0:
                f1[i] = 2.0*prec[i]*recall[i]/(prec[i]+recall[i])
        for i in range(MAXDIST):            
            fw.write(str(minfreq)+'\t'+str(i)+'\t'+str(mae[i])+'\t'+str(rmse[i]) \
                    +'\t'+str(prec[i])+'\t'+str(recall[i])+'\t'+str(f1[i]) \
                    +'\t'+str(n[i])+'\t'+str(hit[i])+'\t'+str(pred[i])+'\t'+str(truth[i])+'\n')
    fw.close()

if __name__ == '__main__':
    # Prepare vocabulary and textual patterns
    # print('Step 0: Prepare vocabulary and textual patterns...')
    # step0()
    # print('\tConcept vocabulary and patterns are ready!')

    # # Recognize concepts and compress documents
    # print('Step 1: Recognize concepts and compress documents...')
    # step1()
    # print('\n\tConcepts recognized and documents compressed!')

    # # Type concepts using MajVote-Trigger and evaluate typing results
    # print('Step 2: Type concepts using MajVote-Trigger and evaluate typing results...')
    # step2()
    # print('\tConcept types ready!')

    # # First-round relation extraction using Hearst (Hearst Pattern Matching)
    # print('Step 3: First-round relation extraction using Hearst (Hearst Pattern Matching)...')
    # step3()
    # print('\n\tFirst-round relations ready!')

    # # Synonym clustering, sibling clustering, re-typing, and evaluation
    # print('Step 4: Synonym clustering, sibling clustering, re-typing, and evaluation...')
    # step4()
    # print('\n\tRe-typed concept types ready!')

    # # Second-round relation extraction
    # print('Step 5: Second-round relation extraction...')
    # step5()
    # print('\n\tSecond-round relations ready!')

    # Concept hierarchy construction
    print('Step 6: Concept hierarchy construction...')
    step6()
    print('\tHierarchies in (.md) on min_sup (10,5,3,2,1) are ready!')
    print('\tYou can open with Typora or any flowchart visualization tools.')

    figure_item_support()

    table_evaluation()

