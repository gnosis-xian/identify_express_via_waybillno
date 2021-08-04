import logging as log
from collections import defaultdict

from gensim import corpora, models, similarities

import constants
import file_funcs
import utils

log.basicConfig(format=constants.log_format, level=constants.log_level)

documents = []


def participles(file_content_map):
    # 分词
    texts = []
    for key in file_content_map.keys():
        line = file_content_map[key]['data_list']
        documents.append(line)
        splited_list = line.split(",")
        words = []
        for split in splited_list:
            words += utils.participles(split)
        texts.append(words)
    return texts


def calc_words_frequency(texts):
    # 2.计算词频
    log.info('2.计算词频')
    frequency = defaultdict(int)  # 构建一个字典对象
    # 遍历分词后的结果集，计算每个词出现的频率
    for text in texts:
        for word in text:
            frequency[word] += 1
    # 选择频率大于1的词(根据实际需求确定)
    texts = [[word for word in text if frequency[word] > 1] for text in texts]
    return texts


def create_dirctionary(texts):
    # 3.创建字典（单词与编号之间的映射）
    log.info('3.创建字典（单词与编号之间的映射）')
    dictionary = corpora.Dictionary(texts)
    log.info(dictionary)
    # 打印字典，key为单词，value为单词的编号
    log.info(dictionary.token2id)

    # 5.建立语料库
    log.info('5.建立语料库')
    # 将每一篇文档转换为向量
    corpus = [dictionary.doc2bow(text) for text in texts]
    log.info(corpus)

    # 6.初始化模型
    log.info('6.初始化模型')
    # 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数），表示方法为新的表示方法（Tfidf 实数权重）
    tfidf = models.TfidfModel(corpus)
    # 将整个语料库转为tfidf表示方法
    corpus_tfidf = tfidf[corpus]

    # 7.创建索引
    log.info('7.创建索引')
    # 使用上一步得到的带有tfidf值的语料库建立索引
    index = similarities.MatrixSimilarity(corpus_tfidf)
    return dictionary, index, tfidf


def main():
    file_content_map = file_funcs.read_data_set_from_file()
    texts = participles(file_content_map)
    texts = calc_words_frequency(texts)
    dictionary, index, tfidf = create_dirctionary(texts)
    file_funcs.persistence(file_content_map, dictionary, index, tfidf, documents)
    log.warning("重新加载数据源完成")


if __name__ == '__main__':
    main()
