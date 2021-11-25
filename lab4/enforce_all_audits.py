import os
import re
import json

def enforce_all_audits():
	file = open('to_enforce_audits.json',)
	audit = json.load(file)

	#os.popen('sudo su')
	#os.popen('cd ~')
	for custom_item in audit:
		cmd = custom_item['cmd_to_enforce'][1:-1]
		#print(cmd)
		output = os.popen(cmd).read()
	#os.popen('exit')

def rollback_audits():
	file = open('to_enforce_audits.json',)
	audit = json.load(file)

	#os.popen('sudo su')
	#os.popen('cd ~')
	for custom_item in audit:
		cmd = custom_item['cmd_to_back_up'][1:-1]
		#print(cmd)
		output = os.popen(cmd).read()
	#os.popen('exit')