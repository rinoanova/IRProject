
import json
import utils
import chardet
import tokenize
import html

#input word and return the inverted index of the word
def boolquery(query):
    all_doc = utils.get_doc_list()
    all_doc.sort()

    isAnd = False
    isOr = False
    isNot = False
    query_words = []
    result = []
    result_2 = []
    word = ''
    word_last = ''

    i=0
    while i<len(query):
        if(query[i]=='('): #when we meet ()
            lcount = 1
            rcount = 0
            isclose = False
            i += 1
            while(i<len(query)):
                if(query[i]=='('):
                    lcount += 1
                if(query[i]==')'):
                    rcount += 1
                    if(rcount<lcount):
                        word += ')'
                        i += 1
                        continue
                    isclose=True
                    break
                else:
                    word += query[i]
                i = i+1
            if(isclose==False): #the () is not closed
                print("Bad Search! Only has '('!")
                return []
            else:
                if isAnd: #() is after AND
                    if isNot: #like: AND NOT ()
                        result_2 = handle_not(boolquery(word), all_doc)
                        isNot = False
                    else:
                        result_2 = boolquery(word)
                    result = handle_and(result, result_2)
                    isAnd = False
                elif isOr: #() is after OR
                    if isNot: #like: OR NOT ()
                        isNot = False
                        result_2 = handle_not(boolquery(word), all_doc)
                    else:
                        result_2 = boolquery(word)
                    result = handle_or(result, result_2)
                    isOr = False
                else: #() is in the front
                    if isNot:# like: NOT ()
                        isNot = False
                        result = handle_not(boolquery(word), all_doc)
                    else:
                        result = boolquery(word)

        elif(query[i]=='A'):
            if(i+2<len(query) and i-1>0):
                if(query[i+1]=='N' and query[i+2] == 'D' and query[i-1]==' '):
                    isAnd = True
                    i+=2
                else:
                    word+='a'
            else:
                word+='a'

        elif(query[i]=='O'):
            if(i+1<len(query) and i-1>0):
                if(query[i+1]=='R' and query[i-1]==' '):
                    isOr = True
                    i+=1
                else:
                    word+='o'
            else:
                word+='o'

        elif(query[i]=='N'):
            if(i+2<len(query) and word==''):
                if(query[i+1]=='O' and query[i+2]=='T'):
                    isNot = True
                    i+=2
                else:
                    word+='n'
            else:
                word+='n'

        elif(query[i]==' '):
            if(word!=''):
                word = word.lower()
                query_words.append(word)
                if isAnd: #() is after AND
                    if(word_last==''):
                        print("Bad Query! Meet AND First!")
                        return []
                    if isNot: #like: AND NOT ()
                        result_2 = handle_not(utils.loadIndex(word), all_doc)
                        isNot = False
                    else:
                        result_2 = utils.loadIndex(word)
                    result = handle_and(result, result_2)
                    isAnd = False
                elif isOr: #() is after OR
                    if (word_last == ''):
                        print("Bad Query! Meet AND First!")
                        return []
                    if isNot: #like: OR NOT ()
                        isNot = False
                        result_2 = handle_not(utils.loadIndex(word), all_doc)
                    else:
                        result_2 = utils.loadIndex(word)
                    result = handle_or(result, result_2)
                    isOr = False
                else: #() is in the front
                    if isNot:# like: NOT ()
                        isNot = False
                        result = handle_not(utils.loadIndex(word), all_doc)
                    else:
                        result = utils.loadIndex(word)
                word_last = word
                word=''

        else:
            word+=query[i]
            if i==len(query)-1: #at the end of the query
                word = word.lower()
                query_words.append(word)
                if isAnd:  # () is after AND
                    if (word_last == ''):
                        print("Bad Query! Meet AND First!")
                        return []
                    if isNot:  # like: AND NOT ()
                        result_2 = handle_not(utils.loadIndex(word), all_doc)
                        isNot = False
                    else:
                        result_2 = utils.loadIndex(word)
                    result = handle_and(result, result_2)
                    isAnd = False
                elif isOr:  # () is after OR
                    if (word_last == ''):
                        print("Bad Query! Meet OR First!")
                        return []
                    if isNot:  # like: OR NOT ()
                        isNot = False
                        result_2 = handle_not(utils.loadIndex(word), all_doc)
                    else:
                        result_2 = utils.loadIndex(word)
                    result = handle_or(result, result_2)
                    isOr = False
                else:  # () is in the front
                    if isNot:  # like: NOT ()
                        isNot = False
                        result = handle_not(utils.loadIndex(word), all_doc)
                    else:
                        result = utils.loadIndex(word)
                word_last = word
                word = ''
        i = i+1
    return result



#get user input and judge the boolean word
def controller(query):
    index = boolquery(query)
    query.replace('NOT','')
    query.replace('AND','')
    query.replace('OR','')
    query.replace('(','')
    query.replace(')','')
    query.replace('  ',' ')
    wordlist = []
    wordlist = query.split(' ')
    #print(index)
    utils.printtext(wordlist,index)

#for each boolean word, do something to the index(notice ( and ) )
#and
def handle_and(index1, index2):
    index1.sort()
    index2.sort()
    i = 0
    j = 0
    result = []
    while(i<len(index1) and j<len(index2)):
        if index1[i]==index2[j]:
            result.append(index1[i])
            i+=1
            j+=1
        elif index1[i]<index2[j]:
            i+=1
        else:
            j+=1
    return result

#or
def handle_or(index1, index2):
    index1.sort()
    index2.sort()
    i = 0
    j = 0
    result = []
    while(i<len(index1) and j<len(index2)):
        if index1[i]==index2[j]:
            result.append(index1[i])
            i+=1
            j+=1
        elif index1[i]<index2[j]:
            result.append(index1[i])
            i+=1
        else:
            result.append(index2[j])
            j+=1
    if(i==len(index1)):
        while j<len(index2):
            result.append(index2[j])
            j+=1
    else:
        while i<len(index1):
            result.append(index1[i])
            i+=1
    return result

#not
def handle_not(index, all_doc):
    index.sort()
    i = 0
    j = 0
    result = []
    while(i<len(index) and j<len(all_doc)):
        if index[i]==all_doc[j]:
            i+=1
            j+=1
        elif all_doc[j]<index[i]:
            result.append(all_doc[j])
            j+=1
    while j<len(all_doc):
        result.append(all_doc[j])
        j+=1
    return result

#main
# t = utils.loadIndex('shoppers')
#
# print("*********INDEX********")
# print(t)
#
# query = input("Input your query:\n")
# index = boolquery(query)
# print(index)
