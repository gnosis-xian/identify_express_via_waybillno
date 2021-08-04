import json
import logging as log
import threading

import constants
import file_funcs
import import_dataset
import utils

log.basicConfig(format=constants.log_format, level=constants.log_level)

tfidf = None
index = None
documents = None
dictionary = None
file_content_map = None

reload = False


def identify_waybill_express(waybill_no):
    # 文档预处理
    pre_waybillno_str = utils.parse_waybillno(waybill_no)
    new_text = utils.participles(pre_waybillno_str)
    log.info(new_text)
    return new_text


def load_persistence_obj():
    global tfidf
    global index
    global documents
    global dictionary
    global file_content_map
    try:
        tfidf, index, documents, dictionary, file_content_map = file_funcs.load_persistence_objs()
    except FileNotFoundError as fnfe:
        import_dataset.main()
        tfidf, index, documents, dictionary, file_content_map = file_funcs.load_persistence_objs()

def calc_result_without_threshold(waybill_no, new_text, dictionary, index, tfidf, documents):
    # 4.将待比较的文档转换为向量（词袋表示方法）
    log.info('4.将待比较的文档转换为向量（词袋表示方法）')
    # 使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
    new_vec = dictionary.doc2bow(new_text)

    # 8.相似度计算并返回相似度最大的文本
    log.info('# 8.相似度计算并返回相似度最大的文本')
    new_vec_tfidf = tfidf[new_vec]  # 将待比较文档转换为tfidf表示方法
    # 计算要比较的文档与语料库中每篇文档的相似度
    sims = index[new_vec_tfidf]
    log.info(sims)
    sims_list = sims.tolist()
    # log.info(sims_list.index(max(sims_list)))  # 返回最大值
    log.info("待判断的运单号为：{}".format(waybill_no))

    result_list = []
    file_content_map_keys = file_content_map.keys()
    for sim in sims_list:
        if sim > 0:
            express_code = list(file_content_map_keys)[sims_list.index(sim)]
            result_list.append({"express_code": express_code, "prob_percentage": sim})
    return result_list

def calc_result(waybill_no, new_text, dictionary, index, tfidf, documents):
    # 4.将待比较的文档转换为向量（词袋表示方法）
    log.info('4.将待比较的文档转换为向量（词袋表示方法）')
    # 使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
    new_vec = dictionary.doc2bow(new_text)

    # 8.相似度计算并返回相似度最大的文本
    log.info('# 8.相似度计算并返回相似度最大的文本')
    new_vec_tfidf = tfidf[new_vec]  # 将待比较文档转换为tfidf表示方法
    # 计算要比较的文档与语料库中每篇文档的相似度
    sims = index[new_vec_tfidf]
    log.info(sims)
    sims_list = sims.tolist()
    # log.info(sims_list.index(max(sims_list)))  # 返回最大值
    log.info("待判断的运单号为：{}".format(waybill_no))

    result_list = []
    file_content_map_keys = file_content_map.keys()
    for sim in sims_list:
        express_code = list(file_content_map_keys)[sims_list.index(sim)]
        threshold_express_map = file_funcs.read_express_threshold()
        threshold = threshold_express_map.get(express_code)
        if threshold is not None and sim > threshold:
            result_list.append({"express_code": express_code, "prob_percentage": sim})
    return result_list


def reload_objs():
    load_persistence_obj()
    global reload
    reload = False


def regc(waybill_no):
    new_text = identify_waybill_express(waybill_no)
    if dictionary is None or index is None or tfidf is None or documents is None or file_content_map is None:
        load_persistence_obj()
    global reload
    if reload:
        t1 = threading.Thread(target=reload_objs)
        t1.start()
    result_list = calc_result(waybill_no, new_text, dictionary, index, tfidf, documents)
    # 持久化未识别运单数据
    # if result_list == []:
    #     file_funcs.append_line(constants.error_waybill_save_file, waybill_no)
    log.info("运单号：{} 判断结果：{}".format(waybill_no, json.dumps(result_list)))
    return result_list

def regc_without_threshold(waybill_no):
    new_text = identify_waybill_express(waybill_no)
    return calc_result_without_threshold(waybill_no, new_text, dictionary, index, tfidf, documents)

def main():
    waybill_no = 'JT5045023079024'
    regc(waybill_no)


if __name__ == '__main__':
    main()
