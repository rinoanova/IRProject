import score
import utils

class ZHeap:
    def __init__(self, item=[], id=[]):
        # 初始化。item为数组
        self.items = item
        self.ids = id
        self.heapsize = len(self.items)

    def LEFT(self, i):
        return 2 * i + 1

    def RIGHT(self, i):
        return 2 * i + 2

    def PARENT(self, i):
        return int((i - 1) / 2)

    def MIN_HEAPIFY(self, i):
        # 最小堆化：使以i为根的子树成为最小堆
        l = self.LEFT(i)
        r = self.RIGHT(i)
        if l < self.heapsize and self.items[l] < self.items[i]:
            smallest = l
        else:
            smallest = i

        if r < self.heapsize and self.items[r] < self.items[smallest]:
            smallest = r

        if smallest != i:
            self.items[i], self.items[smallest] = self.items[smallest], self.items[i]
            self.ids[i], self.ids[smallest] = self.ids[smallest], self.ids[i]
            self.MIN_HEAPIFY(smallest)

    def INSERT(self, val,id):
        # 插入一个值val，并且调整使满足堆结构
        self.items.append(val)
        self.ids.append(id)
        idx = len(self.items) - 1
        parIdx = int(self.PARENT(idx))
        while parIdx >= 0:
            if self.items[parIdx] > self.items[idx]:
                self.items[parIdx], self.items[idx] = self.items[idx], self.items[parIdx]
                self.ids[parIdx], self.ids[idx] = self.ids[idx], self.ids[parIdx]
                idx = parIdx
                parIdx = self.PARENT(parIdx)
            else:
                break
        self.heapsize += 1

    def DELETE(self):
        last = len(self.items) - 1
        if last < 0:
            # 堆为空
            return None
        # else:
        self.items[0], self.items[last] = self.items[last], self.items[0]
        self.ids[0], self.ids[last] = self.ids[last], self.ids[0]
        val = self.items.pop()
        id = self.ids.pop()
        self.heapsize -= 1
        self.MIN_HEAPIFY(0)
        return id


    def BUILD_MIN_HEAP(self):
        # 建立最小堆, O(nlog(n))
        i = self.PARENT(len(self.items) - 1)
        while i >= 0:
            self.MIN_HEAPIFY(i)
            i -= 1

    def SHOW(self):
        print(self.items)


class ZPriorityQ(ZHeap):
    def __init__(self, item=[]):
        ZHeap.__init__(self, item)

    def enQ(self, val, id):
        ZHeap.INSERT(self, val, id)

    def deQ(self):
        val = ZHeap.DELETE(self)
        return val

def topK(wordlist, docID, K):

    print("here is topK")
    VSM_sum = utils.get_from_file('VSM_sum')
    pq = ZPriorityQ()
    if len(docID) < K:
        K = len(docID)
    for doc in docID:
        #calculate the score of cos(q,d)
        value = score.cosinescore(wordlist, doc)
        #print(value)
        #get the tf-idf
        doc_score = VSM_sum[str(doc)]+value
        pq.enQ(doc_score, doc)
    result = []
    for i in range(K):
        docID = pq.deQ()
        print(docID)
        result.append(docID)
    return result