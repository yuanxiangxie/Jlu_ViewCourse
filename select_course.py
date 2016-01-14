#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import hashlib
class login:
	def __init__(self, url):
		self.url = url
		self.name = "uesrname" # your teaching number when you login the uims.jlu.edu.cn webpage
		self.passwd = "passwd" # your passwd when you login the uims.jlu.edu.cn webpage
		self.pwd = self.MD5("UIMS"+self.name+self.passwd)
		self.s = requests.session()
	
	def MD5(self, key_word):
		key = hashlib.md5()
		key.update(key_word)
		return key.hexdigest()

	def login_page(self):
		self.r = self.s.get(self.url)
		param = { 'j_username':self.name, 'j_password':self.pwd}
		self.p = self.s.post('http://uims.jlu.edu.cn/ntms/j_spring_security_check', param)
		self.personal = self.s.post('http://uims.jlu.edu.cn/ntms/action/getCurrentUserInfo.do')
		self.personalID = json.loads(self.personal.text)['userId']
#		print "%s"%(self.personalID)

	def get_score(self):
		param = json.dumps({'tag': "student_sch_dept", 'branch': "byId", 'params': {'studId': self.personalID}})
		content = {'Content-Type':"application/json"}
		self.score_page = self.s.post('http://uims.jlu.edu.cn/ntms/service/res.do', param, headers = content)
		self.score = json.loads(self.score_page.text)
		self.welcome_Info(self.score)
	
	def welcome_Info(self, info):
		if isinstance(info, dict):
			for i in range(len(info)):
				temp_key = info.keys()[i]
				temp_value = info[temp_key]
				if (temp_key == "name" and temp_key is not None):
					print '------------------------------------------------------------------'
					print '| \t Welcome %s, the following is your coursesname!\t |'%(temp_value)
					print '------------------------------------------------------------------'
				else:
					pass
				self.welcome_Info(temp_value)
		elif isinstance(info, list):
			for j in range(len(info)):
				self.welcome_Info(info[j])
		else:
			pass
				

	def return_Info(self):
		param = json.dumps({'tag': "teachClassStud@schedule", 'branch': "default", 'params': {'termId': '129', 'studId': self.personalID}})
		content = {'Content-Type':'application/json;charset=UTF-8'}
		self.info = self.s.post('http://uims.jlu.edu.cn/ntms/service/res.do', param, headers = content)
		self.infomation = json.loads(self.info.text)
		self.listall_Dict(self.infomation)
		print '------------------------------------------------------------------'
	
	def listall_Dict(self, Dict):
		if isinstance(Dict, dict):
			for i in range(len(Dict)):
				temp_key = Dict.keys()[i]
				temp_values = Dict[temp_key]
				courseName = Dict.get('courName')
				if courseName is not None:
					print '------------------------------------------------------------------'
					print " \t %20s \t"%(courseName)
				else:
					pass
				self.listall_Dict(temp_values)
		elif isinstance(Dict, list):
			for j in range(len(Dict)):
				self.listall_Dict(Dict[j])
		else:
			pass

def start():
	login_uims = login('http://www.uims.jlu.edu.cn')
	login_uims.login_page()
	login_uims.get_score()
	login_uims.return_Info()
if __name__ == "__main__":
	start()

