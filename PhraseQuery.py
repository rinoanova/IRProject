
import utils
import json
import chardet
import html

def phrasequery_wordlist(wordlist):
    docID = []
    docID_storage = []
    judge_index = []
    docID_index = []
    for word in wordlist:
        index = utils.loadLocationIndex(word)
        if index is None:
            print("No such word!")
            return None
        result = []
        for item in index:
            result.append(int(item))
        result.sort()
        storage = {}
        for i in range(len(result)):
            storage.setdefault(i, result[i])
        docID_storage.append(storage)
        docID_index.append(index)
        judge_index.append(0)

    #get common docID
    while True:
        IsSame = True
        IsOver = False
        temp = -1
        max = -1
        for i in range(len(wordlist)):
            if (judge_index[i] >= len(docID_storage[i])):
                IsOver = True
                isSame = False
                break
            if docID_storage[i][judge_index[i]]>max:
                temp = i
                max = docID_storage[i][judge_index[i]]
            if i>0 and IsSame:
                if docID_storage[i][judge_index[i]]!=docID_storage[i-1][judge_index[i-1]]:
                    IsSame=False
        if IsSame:
            if (judge_index[0] >= len(docID_storage[0])):
                break
            docID.append(docID_storage[0][judge_index[0]])
            for i in range(len(wordlist)):
                judge_index[i]+=1
                if(judge_index[i]>=len(docID_storage[i])):
                    IsOver = True
                    break
        else:
            for i in range(len(wordlist)):
                if i!=temp:
                    judge_index[i]+=1
                    if (judge_index[i] >= len(docID_storage[i])):
                        IsOver = True
                        break
        if IsOver:
            break

    #for these docID, judge the location
    result = getPhraseDoc(docID_index, docID)
    return result


def getPhraseDoc(docID_index, docID):
    result = [] #result_docID
    judge_onedoc = [] #wordindex of query words in one doc
    for j in range(len(docID)):
        judge_onedoc = []
        for i in range(len(docID_index)):
            word_index = docID_index[i][str(docID[j])]
            judge_onedoc.append(word_index)
        if(isPhrase(judge_onedoc)):
            result.append(docID[j])
    return result

    #对每个docID，选出这些词的wordindex，判断是否有短语部分

def isPhrase(judge_onedoc):
    for i in range(len(judge_onedoc)):
        judge_onedoc[i].sort()
    index = 1
    wordlist1 = judge_onedoc[0]
    temp_result = []
    while index<len(judge_onedoc):
        wordlist2 = judge_onedoc[index]
        p1 = 0
        p2 = 0
        while p1<len(wordlist1) and p2<len(wordlist2):
            if(wordlist1[p1]==wordlist2[p2]-1):
                temp_result.append(wordlist2[p2])
                p1+=1
                p2+=1
            elif wordlist1[p1]>wordlist2[p2]:
                p2+=1
            elif wordlist1[p1]<wordlist2[p2]:
                p1+=1
        wordlist1 = temp_result
        index+=1
        if len(wordlist1)==0:
            return False
    if(len(wordlist1)>0):
        return True
    return False

def phrasequery(query):
    query = query.lower()
    wordlist = query.split(' ')
    docID = phrasequery_wordlist(wordlist)
    if docID is not None:
        printquery = [query]
        printtext(printquery, docID)

def printtext(wordlist, doclist):
    directory = "./Reuters"
    highlights = []
    for word in wordlist:
        highlights.append(word)
        highlights.append(word.upper())
        highlights.append(word.title())
    for docid in doclist:
        with open(directory + '/' + str(docid) + '.html', 'rb') as htmlfile:
            rawdata = htmlfile.read()
            encoding = chardet.detect(
                rawdata)['encoding']
            text = rawdata.decode(encoding)
            text = html.unescape(text)
        #find title
        #find body
        print("************** Boolean Query Result **************")
        print("\033[1;33;40m"+str(docid)+".html"+"\033[0m")
        for word in highlights:
            text = text.replace(word, "\033[1;31;40m" + word + "\033[0m")
        print(text)

#query = input("Input your query:\n")
#phrasequery(query)
