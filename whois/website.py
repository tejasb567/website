from flask import Flask,request,jsonify

#import sys
#sys.path.insert(0,'/whoise/')
#import whoisData

from whoise.whoisData import *

app=Flask(__name__)
 
@app.route('/whoiss',methods=['POST'])
def whoiss():
	req_data=request.get_json()
	targetUrl=req_data['url']
	result=whois_cal(targetUrl)
	return jsonify(result)
 	
if __name__ == '__main__':
	app.run()
 	
