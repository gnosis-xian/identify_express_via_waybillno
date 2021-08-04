cd /home/yjt/identify_express_via_waybillno/ && git pull && \
sudo docker rm -f identify_express_via_waybillno && \
sudo docker run --name identify_express_via_waybillno \
-v /home/yjt/identify_express_via_waybillno/:/identify_express_via_waybillno/  \
-v /root/.ssh/:/root/.ssh/ \
-p 8150:8150 \
-d --privileged=true \
--restart=always \
registry.cn-hangzhou.aliyuncs.com/docker-gnosis/identify_express_via_waybillno:v1.0 \
sh /identify_express_via_waybillno/startup.sh && \
sudo docker logs -f identify_express_via_waybillno