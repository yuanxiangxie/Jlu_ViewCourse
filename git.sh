#!/bin/bash
git add "$1"
git commit -m "cmomit $1"
git remote add origin https://github.com/yuanxiangxie/test.git
git push origin master

