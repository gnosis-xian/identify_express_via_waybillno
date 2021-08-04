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
    # 开始计算词频
    log.info('开始计算词频')
    frequency = defaultdict(int)
    for text in texts:
        for word in text:
            frequency[word] += 1
    texts = [[word for word in text if frequency[word] > 1] for text in texts]
    return texts


def create_dirctionary(texts):
    log.info('创建字典 单词 - 编号')
    dictionary = corpora.Dictionary(texts)
    log.info(dictionary)
    log.info(dictionary.token2id)

    log.info('开始建立语料')
    corpus = [dictionary.doc2bow(text) for text in texts]
    log.info(corpus)

    log.info('model init...')
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    log.info('create index...')
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
