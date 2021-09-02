import logging

log_format = '%(asctime)s : %(levelname)s : %(message)s'
log_level = logging.INFO

dir_path = './data_set'

objs_sub_dir = './data_objs'

error_waybill_save_file = './error_regc.txt'

threshold_file = './express_threshold.txt'

wait_integrate_file = './wait_integrate.txt'
train_waybill_token = '7ZBF4Hn4n5hJLcYk'
train_waybill_size_limit = 20

DEFAULT_REGC_THRESHOLD = 0.1

split_str = '==='

reload = False