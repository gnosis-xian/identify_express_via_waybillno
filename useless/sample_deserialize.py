import logging as log
import pickle

log.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)

# 待判断运单
new_doc = "4608248893574"

# 文档预处理
words = [new_doc]
new_text = []
for word in words:
    new_text.append(new_doc[0:2])
    new_text.append(new_doc[0:3])
    new_text.append(new_doc[0:4])
    new_text.append(new_doc[0:5])
log.info(new_text)

index_file = open("index" + ".bin", "rb")
tfidf_file = open("tfidf" + ".bin", "rb")
documents_file = open("documents" + ".bin", "rb")
dictionary_file = open("dictionary" + ".bin", "rb")

tfidf = pickle.load(tfidf_file)
index = pickle.load(index_file)
documents = pickle.load(documents_file)
dictionary = pickle.load(dictionary_file)

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
