# !/usr/bin/env python
import os
import utils
import InvertedIndex
import BooleanQuery
import PhraseQuery
import GlobbingQuery

# ------------
# 构建索引/VSM
# ------------
# # 跑一遍来构建文件，第二遍就可以注释掉了
# print('Creating Index...')
# # 构建倒排索引和每篇文档的词数
# index, doc_size = InvertedIndex.create_index()
# # 用倒排索引生成词表
# print('Creating Wordlist...')
# wordlist = InvertedIndex.get_wordlist(index)
# # 生成 VSM
# print('Creating VSM...')
# VSM = InvertedIndex.create_VSM(index, doc_size, wordlist)
# # 为 Top K 暴力查表做计算
# VSM_sum = InvertedIndex.VSM_sum(VSM)
# # 将文件存档
# print('Saving Files...')
# utils.write_to_file(index, utils.ppath+'index.json')
# utils.write_to_file(wordlist, utils.ppath+'wordlist.json')
# utils.write_to_file(doc_size, utils.ppath+'doc_size.json')
# utils.write_to_file(VSM, utils.ppath+'VSM.json')
# utils.write_to_file(VSM_sum, utils.ppath+'VSM_sum.json')
#
# 从 JSON 读取数据， JSON 文件默认放在 IRProject 下
print('Getting Data from Files...')
index = utils.get_from_file('index')
wordlist = utils.get_from_file('wordlist')
doc_size = utils.get_from_file('doc_size')
VSM = utils.get_from_file('VSM')
btree, btree_rev = GlobbingQuery.BuildTree(wordlist)

# ------------
# 搜索 etc.
# ------------
def main():
    while True:
        print("\n", "*"*50)
        number = input("Choose the way to query:\n  1.Boolean Query\n  2.Phrase Query\n  3.Wildcard Query\n  4.Fuzzy Query\nInput 0 to quit\n")
        if int(number)==0:
            break
        if int(number) > 4 or int(number) < 0:
            print("ERROR: WRONG INPUT!")
            continue
        query = input("Input your query:\n")
        #boolean query
        if(int(number)==1):
            BooleanQuery.controller(query)
        #phrase query
        if(int(number)==2):
            PhraseQuery.phrasequery(query)
        #wildcard query
        if(int(number)==3):
            GlobbingQuery.controller(query, btree, btree_rev,wordlist)
        #Fuzzy Query
        if(int(number)==4):
            SpellingCorrect.spelling_correct(query)

        #merge
        #if query.find('*')!=-1:
            #GlobbingQuery.controller(query, btree, btree_rev, wordlist)


if __name__ == "__main__":
    main()
