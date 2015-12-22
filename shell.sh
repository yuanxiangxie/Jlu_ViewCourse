#!/usr/bin/expect
spawn ./git.sh
expect "Username for 'https://github.com': " 
send "yuanxiangxie@outlook.com\n"
expect "Password for 'https://yuanxiangxie@outlook.com@github.com':"
send "xyx19950301\n"



