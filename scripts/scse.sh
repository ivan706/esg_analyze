#!/bin/bash

# 循环从 1 到 10
for pageNum in {1..20}
do
  # 执行 curl 命令，并将 pageNum 变量插入到 --data-raw 中
  curl 'http://www.szse.cn/api/disc/announcement/annList?random=0.6717472588290101' \
    -H 'Accept: application/json, text/javascript, */*; q=0.01' \
    -H 'Content-Type: application/json' \
    -H 'Origin: http://www.szse.cn' \
    -H 'Referer: http://www.szse.cn/disclosure/listed/notice/index.html' \
    --data-raw "{\"seDate\":[\"2024-01-01\",\"2024-10-01\"],\"searchKey\":[\"社会\",\"报告\"],\"channelCode\":[\"listedNotice_disc\"],\"pageSize\":50,\"pageNum\":$pageNum}" \
    --insecure >> x.json
  
  # 等待 3 秒
  sleep 3
done