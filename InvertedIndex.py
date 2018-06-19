import os
import utils
import math

# 构建倒排索引(Reuters 的默认路径在上级目录)
def create_index():
    index = {}
    doc_size = [0 for d in range(1, utils.D*2+2)] # 21576
    print(len(doc_size))
    files = os.listdir(utils.rpath)
    for file in files:
        content = utils.process_doc_content(utils.rpath+file)
        docID = utils.get_doc_ID(file)

        num = 0 # word 在文档中的位置
        for word in content:
            if word not in index:
                doclist = {}
                doclist[docID] = [num]
                index[word] = doclist
            else:
                if docID not in index[word]:
                    index[word][docID] = [num]
                else:
                    index[word][docID].append(num)
            num += 1
        doc_size[docID]=num
    
    return index, doc_size

# 用倒排索引生成词表
def get_wordlist(index):
    wordlist = []
    for word in index.keys():
        wordlist.append(word)
    
    return wordlist

# 生成 VSM
# TF_word_i = len(index[word][article_i])/doc_size[article_i]
# IDF = log_2(D/len(index[word])), D=10788
# TF-IDF_word_i = TF*IDF
def create_VSM(index, doc_size, wordlist):
    VSM = {}
    for d in range(1, utils.D*2+1): # 21576
        if d%1000==0:
            print('Processing:'+str(d))
        # 不考虑文件夹内不存在的篇目
        if doc_size[d]==0:
            continue
        tf_idf_list = []
        num = 0
        for word in wordlist:
            # 简单的索引压缩
            if str(d) not in index[word]:
                num += 1
                continue
            else:
                if num > 0:
                    tf_idf_list.append(str(num))
                tf = float(len(index[word][str(d)])/doc_size[d])
                idf = math.log2(utils.D/len(index[word]))
                tf_idf = '%.3f' % float(tf*idf) # 保留三位小数
                tf_idf_list.append(tf_idf)
                num = 0
        VSM[d] = tf_idf_list

    return VSM