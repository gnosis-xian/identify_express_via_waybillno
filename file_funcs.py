import logging as log
import os
import pickle

import constants
import utils

import lock_util

log.basicConfig(format=constants.log_format, level=constants.log_level)


def read_express_threshold():
    result = {}
    try:
        with open(constants.threshold_file, 'r') as f:
            file_content = f.read()
            if file_content is not None:
                split_lines = file_content.split('\n')
                for line in split_lines:
                    l = line.split('==')
                    result[l[0]] = float(l[1])
    except Exception as ignored:
        log.warn("阈值文件处理失败")
    return result


def append_line(file_path, content):
    try:
        with open(file_path, mode='a') as filename:
            filename.write(content)
            filename.write('\n')
    except FileNotFoundError:
        with open(file_path, mode='w') as filename:
            filename.write(content)
            filename.write('\n')
    except Exception as ignored:
        log.warn("写入文件出错")


def read_file_content(file_path):
    result = ''
    with open(file_path, 'r') as f:
        file_content = f.read()
        lines = file_content.split('\n')
        for line in lines:
            waybill_no = line.replace('"', '').replace('\n', '')
            result += utils.parse_waybillno(waybill_no) + ','
    return result.replace('waybill_no,', '')


def read_data_set_from_file():
    file_list = os.listdir(constants.dir_path)
    file_map = {}
    for file in file_list:
        file_path = constants.dir_path + '/' + file
        file_map[file.replace(".csv", '')] = {
            "file_path": file_path,
            "data_list": read_file_content(file_path)
        }
    return file_map


def persistence(file_content_map, dictionary, index, tfidf, documents):
    # 序列化对象
    current_lock = 'persistence_objs.lock'
    try:
        if lock_util.locked(current_lock):
            log.warning("序列化对象正在运行...")
            return
        lock_util.create_lock(current_lock)
        if not os.path.exists(constants.objs_sub_dir):
            os.makedirs(constants.objs_sub_dir)
        file_content_map_file = open(get_persistence_obj_filepath("file_content_map"), "wb")
        dictionary_file = open(get_persistence_obj_filepath("dictionary"), "wb")
        index_file = open(get_persistence_obj_filepath("index"), "wb")
        tfidf_file = open(get_persistence_obj_filepath("tfidf"), "wb")
        documents_file = open(get_persistence_obj_filepath("documents"), "wb")

        pickle.dump(file_content_map, file_content_map_file)
        pickle.dump(dictionary, dictionary_file)
        pickle.dump(index, index_file)
        pickle.dump(tfidf, tfidf_file)
        pickle.dump(documents, documents_file)
    except Exception as e:
        log.error("持久化对象发生错误")
    finally:
        lock_util.remove_lock(current_lock)


def load_persistence_objs():
    index_file = open(get_persistence_obj_filepath("index"), "rb")
    tfidf_file = open(get_persistence_obj_filepath("tfidf"), "rb")
    documents_file = open(get_persistence_obj_filepath("documents"), "rb")
    dictionary_file = open(get_persistence_obj_filepath("dictionary"), "rb")
    file_content_map_file = open(get_persistence_obj_filepath("file_content_map"), "rb")

    tfidf = pickle.load(tfidf_file)
    index = pickle.load(index_file)
    documents = pickle.load(documents_file)
    dictionary = pickle.load(dictionary_file)
    file_content_map = pickle.load(file_content_map_file)

    return tfidf, index, documents, dictionary, file_content_map


def get_persistence_obj_filepath(filename):
    return constants.objs_sub_dir + "/" + filename + ".bin"


def readline_with_file(filename):
    return open(filename, 'rU').readlines()

def caculate_file_length(filename):
    return len(readline_with_file(filename))


def empty_file_content(wait_integrate_file):
    with open(wait_integrate_file, 'r+') as file:
        file.truncate(0)
