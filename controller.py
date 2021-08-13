import json
import logging as log

from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

import constants
import git_utils
import lock_util
import train_waybill
import utils
import waybill_regc
import threading
import import_dataset

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'identify_express_via_waybillno', version='1.0.0')

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

log.basicConfig(format=constants.log_format, level=constants.log_level)


@app.route('/', methods=['GET'])
@by_path_counter
def ok():
    return 'ok'

@app.route('/identify/detail/waybillno', methods=['GET'])
@by_path_counter
def identify_detail_waybillno():
    result_json = json.dumps({"code": "501", "message": "wait for a moment. calculating..."})
    try:
        waybill_no = request.args.get("waybillno")
        result_list = waybill_regc.regc_without_threshold(waybill_no)
        result_json = json.dumps(result_list)
    except Exception as ignored:
        log.error(ignored)
        return result_json
    return result_json

@app.route('/identify/waybillno', methods=['GET'])
@by_path_counter
def identify_waybillno():
    result_json = json.dumps({"code": "500", "message": "unknown err."})
    try:
        waybill_no = request.args.get("waybillno")
        result_list = waybill_regc.regc(waybill_no)
        result_json = json.dumps(result_list)
    except Exception as ignored:
        log.error(ignored)
        return result_json
    return result_json


@app.route('/train/waybillno', methods=['GET'])
@by_path_counter
def train_waybillno():
    result_json = json.dumps({"code": "500", "message": "unknown err."})
    try:
        waybill_no = request.args.get("waybillno")
        express_code = request.args.get("expressCode")
        token = request.args.get("token")
        if token == constants.train_waybill_token and utils.not_blank(waybill_no) and utils.not_blank(express_code):
            train_waybill.append_waybill(waybill_no, express_code)
            train_waybill.judge_out_of_limit()
            reload_thread = threading.Thread(target=identify_waybillno_reload)
            reload_thread.start()
            git_thread = threading.Thread(target=git_utils.commit_and_push)
            git_thread.start()
            return json.dumps({"code": "200", "message": "success"})
    except Exception as ignored:
        log.error(ignored)
        return result_json
    return result_json


@app.route('/identify/waybillno/reload', methods=['GET'])
@by_path_counter
def identify_waybillno_reload():
    current_lock = 'reload_dataset.lock'
    try:
        if lock_util.locked(current_lock):
            return 'locked'
        lock_util.create_lock(current_lock)
        import_dataset.main()
    except Exception as ignored:
        log.warning("重新加载数据集出现异常")
    finally:
        lock_util.remove_lock(current_lock)
    waybill_regc.reload = True
    return 'ok'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8150, debug=False)
