```shell script
sudo docker commit -a "gnosis-xian" -m "identify_express_via_waybillno" identify_express_via_waybillno registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.0

sudo docker login --username=gaojing1996@vip.qq.com registry.cn-hangzhou.aliyuncs.com
sudo docker push registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.0

sudo docker rm -f identify_express_via_waybillno

sudo docker run --name identify_express_via_waybillno \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8150:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.0 \
sh /identify_express_via_waybillno/startup.sh
```