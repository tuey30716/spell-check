#!/bin/bash
app="spellcheck.test"
docker build -t ${app} .
# docker run -d -p 56733:80 \
#   --name=${app} \
#   -v $PWD:/app ${app}\
#   --runtime=nvidia
docker run -itd -p 56733:80 \
  --name ${app} ${app}  