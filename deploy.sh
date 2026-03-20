#!/bin/bash
sudo docker stop sixsense-final-test 2>/dev/null
sudo docker rm sixsense-final-test 2>/dev/null

# 볼륨 마운트(-v)를 빼고 순수하게 컨테이너 내부 저장소만 사용해 봅니다.
sudo docker build -t doc-converter:latest .
sudo docker run -d -p 8000:8000 --name sixsense-final-test doc-converter:latest

sudo docker logs -f sixsense-final-test
