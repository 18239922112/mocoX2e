#!/bin/sh
for pid in `ps -ef|grep main.py|grep -v grep|awk '{print $2}'`
do
  kill -9 $pid
done
echo "moco server 已停止"