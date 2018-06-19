# !/usr/bin/env python
import os
import utils
import InvertedIndex

# ------------
# 构建索引/VSM
# ------------
# 跑一遍来构建文件，第二遍就可以注释掉了
# print('Creating Index...')
## 构建倒排索引和每篇文档的词数
# index, doc_size = InvertedIndex.create_index()
## 用倒排索引生成词表
# print('Creating Wordlist...')
# wordlist = InvertedIndex.get_wordlist(index)
## 生成 VSM
# print('Creating VSM...')
# VSM = InvertedIndex.create_VSM(index, doc_size, wordlist)
## 将文件存档
# print('Saving Files...')
# utils.write_to_file(index, utils.ppath+'index.json')
# utils.write_to_file(wordlist, utils.ppath+'wordlist.json')
# utils.write_to_file(doc_size, utils.ppath+'doc_size.json')
# utils.write_to_file(VSM, utils.ppath+'VSM.json')

## 从 JSON 读取数据， JSON 文件默认放在 IRProject 下
# print('Getting Data from Files...')
# index = utils.get_from_file('index')
# wordlist = utils.get_from_file('wordlist')
# doc_size = utils.get_from_file('doc_size')
# VSM = utils.get_from_file('VSM')

# ------------
# 搜索 etc.
# ------------