import constants
import file_funcs
import logging as log

import utils

log.basicConfig(format=constants.log_format, level=constants.log_level)

def append_waybill(waybill_no, express_code):
    content = waybill_no + constants.split_str + express_code
    file_funcs.append_line(constants.wait_integrate_file, content)


def judge_out_of_limit():
    file_lines = []
    try:
        file_lines = file_funcs.readline_with_file(constants.wait_integrate_file)
    except Exception as e:
        log.warning(e)
    if len(file_lines) < constants.train_waybill_size_limit:
        return
    file_funcs.empty_file_content(constants.wait_integrate_file)
    for line in file_lines:
        if utils.is_blank(line):
            continue
        line = line.replace("\n", "")
        if utils.is_blank(line):
            continue
        result = line.split(constants.split_str)
        if result is None or len(result) != 2:
            continue
        waybill_no = result[0]
        express_code = result[1]
        file_name = "{}/{}.csv".format(constants.dir_path, express_code)
        file_funcs.append_line(file_name, waybill_no)
