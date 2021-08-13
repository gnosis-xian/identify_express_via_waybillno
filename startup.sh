pip install -r /identify_express_via_waybillno/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install gunicorn prometheus-flask-exporter -i https://pypi.tuna.tsinghua.edu.cn/simple
export PYTHONPATH=$PYTHONPATH:/identify_express_via_waybillno
cd /identify_express_via_waybillno && python import_dataset.py
cd /identify_express_via_waybillno && rm -rf *.lock
#cd /identify_express_via_waybillno && gunicorn --workers=4 --threads=1 -b 0.0.0.0:8150 controller:app
cd /identify_express_via_waybillno && python controller.py