import json
import logging as log
import threading

import constants
import file_funcs
import import_dataset
import lock_util
import reload_util
import utils

log.basicConfig(format=constants.log_format, level=constants.log_level)

tfidf = None
index = None
documents = None
dictionary = None
file_content_map = None

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
    current_lock = 'obj_persistence.lock'
    try:
        if lock_util.locked(current_lock):
            return
        lock_util.create_lock(current_lock)
        tfidf, index, documents, dictionary, file_content_map = file_funcs.load_persistence_objs()
    except FileNotFoundError as fnfe:
        import_dataset.main()
        tfidf, index, documents, dictionary, file_content_map = file_funcs.load_persistence_objs()
    finally:
        lock_util.remove_lock(current_lock)

def calc_result_without_threshold(waybill_no, new_text, dictionary, index, tfidf, documents):
    log.info('转化向量')
    new_vec = dictionary.doc2bow(new_text)

    log.info('相似度分析并返回最大文本')
    new_vec_tfidf = tfidf[new_vec]
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
    log.info('转化向量')
    new_vec = dictionary.doc2bow(new_text)

    log.info('相似度分析并返回最大文本')
    new_vec_tfidf = tfidf[new_vec]
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
    constants.reload = False

def regc(waybill_no):
    new_text = identify_waybill_express(waybill_no)
    if dictionary is None or index is None or tfidf is None or documents is None or file_content_map is None:
        load_persistence_obj()
    if constants.reload:
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
