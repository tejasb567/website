#from flask import jsonify,request
#from flask import Flask
import pythonwhois


#app = Flask(__name__)

#@app.route('/whoiss',methods=['POST'])

def whois_cal(targetUrl):
	#req_data=request.get_json()
	#targetUrl=req_data['url']
	w=pythonwhois.net.get_whois_raw(targetUrl)
	return w
	#test=whoiss()                                                          
	#whoiss.index(targetUrl)                                                

#if __name__ == '__main__':
#        app.run()


