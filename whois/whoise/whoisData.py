#from flask import jsonify,request
#from flask import Flask
import whois


#app = Flask(__name__)

#@app.route('/whoi',methods=['POST'])

def whois_cal(targetUrl):
	#req_data=request.get_json()
	#targetUrl=req_data['url']
	w=whois.whois(targetUrl)
	return w
	#test=whoiss()
	#whoiss.index(targetUrl)
	
	
	
#if __name__ == '__main__':
	#app.run()
