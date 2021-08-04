# -*- coding: utf-8 -*-

import logging as log
from collections import defaultdict
import pickle

from gensim import corpora, models, similarities


log.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)

# 初始数据
documents = [
    "圆通,YT9526461127919,YT3152106024925,YT3152106024925,YT9524007949484,YT5367929986231,YT5367929986231,YT3152108281015,YT3152136828938,YT3152203412211,YT5368465871546,YT5366159234528,YT5367737239799,YT5367737239799,YT9523523613205,YT5366702808708,YT9524134332840,YT5368335691509,YT9524134332840,YT5368335691509,YT3152234659232,YT5364048347426,YT5365190319631,YT5369668794964",
    "中通,73151851564226,73151851564226,75451536660386,75451536660386,75451536660386,75453204167122,75453204167122,73151924400438,73151924400438,75453013986304,75453026860348,75453021427473,75453013986304,75453026860348,75453021427473,75453261072966,75453261072966,75453329687513,",
    "百世,557048108035375,552040384064621,552040384064621,552040421989667,557048126682745,552039919600318,557048071464776,557047939057905,557048022558627,557047989329527,557047939057905,550013167747733,552040421755913,557048132378734,552039813403260,552039813403260,557048103864142,557048098923036,557047863446314,550013115980087,557048176292312,",
    "韵达,4313667952799,4313634566107,6000106491277,4313667952799,4313644459546,4313642167951,4313684512722,4607791994244,4313648722660,4313648585566,4313614794618,4313661544004,4313693234455,4313684758627,4313683775310,4313673780458,4607797611222,4313661913726,4607794643359,4313643154951,4313688814602,4313683754368,4313690639906,",
]
# 待判断运单
new_doc = "YT5462646061400"

# 分词
texts = []
for line in documents:
    splited_list = line.split(",")
    words = []
    for split in splited_list:
        words.append(split[0:2])
        words.append(split[0:3])
        words.append(split[0:4])
        words.append(split[0:5])
    texts.append(words)
for line in texts:
    log.info(line)

# 文档预处理
words = [new_doc]
new_text = []
for word in words:
    new_text.append(new_doc[0:2])
    new_text.append(new_doc[0:3])
    new_text.append(new_doc[0:4])
    new_text.append(new_doc[0:5])
log.info(new_text)

# 2.计算词频
log.info('2.计算词频')
frequency = defaultdict(int)  # 构建一个字典对象
# 遍历分词后的结果集，计算每个词出现的频率
for text in texts:
    for word in text:
        frequency[word] += 1
# 选择频率大于1的词(根据实际需求确定)
texts = [[word for word in text if frequency[word] > 1] for text in texts]
for line in texts:
    log.info(line)

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
for doc in corpus_tfidf:
    log.info(doc)

# 7.创建索引
log.info('7.创建索引')
# 使用上一步得到的带有tfidf值的语料库建立索引
index = similarities.MatrixSimilarity(corpus_tfidf)

# 序列化对象
dictionary_file = open("dictionary" + ".bin", "wb")
index_file = open("index" + ".bin", "wb")
tfidf_file = open("tfidf" + ".bin", "wb")
documents_file = open("documents" + ".bin", "wb")

pickle.dump(dictionary, dictionary_file)
pickle.dump(index, index_file)
pickle.dump(tfidf, tfidf_file)
pickle.dump(documents, documents_file)


# 4.将待比较的文档转换为向量（词袋表示方法）
log.info('4.将待比较的文档转换为向量（词袋表示方法）')
# 使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
new_vec = dictionary.doc2bow(new_text)
log.info(new_vec)



# 8.相似度计算并返回相似度最大的文本
log.info('# 8.相似度计算并返回相似度最大的文本')
new_vec_tfidf = tfidf[new_vec]  # 将待比较文档转换为tfidf表示方法
log.info(new_vec_tfidf)
# 计算要比较的文档与语料库中每篇文档的相似度
sims = index[new_vec_tfidf]
log.info(sims)
sims_list = sims.tolist()
# log.info(sims_list.index(max(sims_list)))  # 返回最大值
log.info("待判断的运单号为：{}".format(new_doc))
for sim in sims_list:
    if sim > 0:
        log.info("相似的文本为：{} {} {}".format(sims_list.index(sim), documents[sims_list.index(sim)], sim))  # 返回相似度最大的文本

if __name__ == "__main__":
    pass
