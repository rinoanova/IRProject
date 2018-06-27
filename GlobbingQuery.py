import BooleanQuery
import utils
import topk

#globbing query
#using * to match all character

class Node(object):
    def __init__(self, key):
        self.key1 = key
        self.key2 = None
        self.left = None
        self.middle = None
        self.right = None

    def isLeaf(self):
        return self.left is None and self.middle is None and self.right is None

    def isFull(self):
        return self.key2 is not None

    def hasKey(self, key):
        if (self.key1 == key) or (self.key2 is not None and self.key2 == key):
            return True
        else:
            return False

    def getChild(self, key):
        if key < self.key1:
            return self.left
        elif self.key2 is None:
            return self.middle
        elif key < self.key2:
            return self.middle
        else:
            return self.right

    def findkey(self, key1, key2):
        result = []
        if key2 <= self.key1:
            if self.left is not None:
                temp = self.left.findkey(key1, key2)
                for word in temp:
                    result.append(word)
        if key2 > self.key1 >= key1:
            if self.left is not None and self.key1 > key1:
                temp = self.left.findkey(key1, key2)
                for word in temp:
                    result.append(word)
            result.append(self.key1)
        if self.key2 is not None:
            if key2 <= self.key2:
                if self.middle is not None:
                    temp = (self.middle.findkey(key1, key2))
                    for word in temp:
                        result.append(word)
            if key2 > self.key2 >= key1:
                if self.middle is not None and self.key2 > key1:
                    temp = (self.middle.findkey(key1, key2))
                    for word in temp:
                        result.append(word)
                result.append(self.key2)
            if key1 > self.key2 or key2 > self.key2:
                if self.right is not None:
                    temp = (self.right.findkey(key1, key2))
                    for word in temp:
                        result.append(word)
        else:
            if key1 > self.key1 or key2 >= self.key1:
                if self.middle is not None:
                    temp = (self.middle.findkey(key1, key2))
                    for word in temp:
                        result.append(word)

        return result


class Tree(object):
    def __init__(self):
        self.root = None

    def get(self, key):
        if self.root is None:
            return None
        else:
            return self._get(self.root, key)

    def _get(self, node, key):
        if node is None:
            return None
        elif node.hasKey(key):
            return node
        else:
            child = node.getChild(key)
            return self._get(child, key)

    def put(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            pKey, pRef = self._put(self.root, key)
            if pKey is not None:
                newnode = Node(pKey)
                newnode.left = self.root
                newnode.middle = pRef
                self.root = newnode

    def _put(self, node, key):
        if node.hasKey(key):
            return None, None
        elif node.isLeaf():
            return self._addtoNode(node, key, None)
        else:
            child = node.getChild(key)
            pKey, pRef = self._put(child, key)
            if pKey is None:
                return None, None
            else:
                return self._addtoNode(node, pKey, pRef)

    def _addtoNode(self, node, key, pRef):
        if node.isFull():
            return self._splitNode(node, key, pRef)
        else:
            if key < node.key1:
                node.key2 = node.key1
                node.key1 = key
                if pRef is not None:
                    node.right = node.middle
                    node.middle = pRef
            else:
                node.key2 = key
                if pRef is not None:
                    node.right = pRef
            return None, None

    def _splitNode(self, node, key, pRef):
        newnode = Node(None)
        if key < node.key1:
            pKey = node.key1
            node.key1 = key
            newnode.key1 = node.key2
            if pRef is not None:
                newnode.left = node.middle
                newnode.middle = node.right
                node.middle = pRef
        elif key < node.key2:
            pKey = key
            newnode.key1 = node.key2
            if pRef is not None:
                newnode.left = pRef
                newnode.middle = node.right
        else:
            pKey = node.key2
            newnode.key1 = key
            if pRef is not None:
                newnode.left = node.right
                newnode.middle = pRef
        node.key2 = None
        return pKey, newnode

    def find(self, key1, key2):
        result = []
        if self.root is not None:
            result = (self.root.findkey(key1, key2))
        return result

#to build a btree of using all words and build a btree_rev of reverse words
def BuildTree(wordlist):
    print("building B tree...")
    btree = Tree()
    btree_rev = Tree()
    for word in wordlist:
        btree.put(word)
        btree_rev.put(word[::-1])
    print(btree.root.key1)
    print(btree_rev.root.key1)
    print("building B tree finished")
    return btree, btree_rev

#do globbing query.
def globbingquery(query, btree, btree_rev, wordlist):
    if query == '*':
        return wordlist
    count = query.count('*')

    #when query only contains one '*', do search
    if count == 1:
        if query[0] == '*':
            #use btree_rev
            #print("first *")
            word = query[1::]
            #print(word)
            word2 = nextword(word[::-1])[::-1]
            #print(word2)
            result_rev = btree_rev.find(word[::-1], word2[::-1])
            result = []
            for word in result_rev:
                result.append(word[::-1])
            return result
        elif query[len(query)-1] == '*':
            #use btree
            #print("last *")
            words_list = query.split('*')
            word = words_list[0]
            #print(word)
            word2 = nextword(word)
            #print(word, word2)
            result = btree.find(word, word2)
            return result
        else:
            words = query.split('*')
            result1 = globbingquery(words[0]+'*', btree, btree_rev, wordlist)
            #print(result1)
            result2 = globbingquery('*'+words[1],btree, btree_rev, wordlist)
            #print(result2)
            result = []
            if result1 is None or result2 is None:
                return None
            for word in result1:
                if word in result2:
                    result.append(word)
            return result

    #when query contains more than one *, split it and then search
    else:
        if query[0]!='*' and query[len(query)-1]!='*':
            words_list = query.split('*')
            newquery = words_list[0]+'*'+words_list[len(words_list)-1]
        elif query[0]!='*':
            words_list = query.split('*')
            newquery = words_list[0]+'*'
        elif query[len(query)-1]!='*':
            words_list = query.split('*')
            newquery = '*'+words_list[len(words_list)-1]
        else:
            words_list = query.split('*')
            newquery = '*'
        print(newquery)
        result = globbingquery(newquery, btree, btree_rev, wordlist)
        j = 0
        while True:
            if j>=len(result):
                break
            word = result[j]
            for i in range(1, len(words_list)-1):
                if word.find(words_list[i]) == -1:
                    result.remove(word)
                    j -= 1
                    break
            j += 1
        return result


#find the word that is a little bigger than input
def nextword(word):
    if(word[len(word)-1]<'z'):
        number = ord(word[len(word)-1])
        newword = word[0:len(word)-1]
        word = newword + chr(number+1)
    else:
        newword = word[0:len(word)-1]
        word = nextword(newword)+word[len(word)-1]
    return word

def controller(query, btree, btree_rev, words):
    wordlist = globbingquery(query, btree, btree_rev, words)
    if len(wordlist) == 0:
        print("no such word!")
        return False

    print("You maybe want to search the words below: \n", wordlist)
    answer = ''
    while answer!='y' and answer!='n':
        answer = input("Do you want to see the articles of these words? It may cost some times. [y/n]\n")
    if answer == 'n':
        return False

    docIDlist = []
    for word in wordlist:
        docID = utils.loadIndex(word)
        docIDlist.append(docID)

    result = docIDlist[0]
    for i in range(1,len(docIDlist)):
        result = BooleanQuery.handle_or(result,docIDlist[i])

    docID = topk.topK(wordlist, result)
    utils.printtext(wordlist, docID)
    #utils.printtext(wordlist, result)
    return True
