from flask import Flask,request
from json import loads
import requests
import re
from sendmsg import getData

bot_server = Flask(__name__)

@bot_server.route('/api/message',methods=['POST'])
#路径是你在酷Q配置文件里自定义的
def server():
    data_in = request.get_data().decode('utf-8')
    data_in = loads(data_in)
    #print(data_in)
    api_url='http://127.0.0.1:5700/send_{}_msg'.format(data_in['message_type'])
    data_out=getData(data_in)
    requests.post(api_url,data=data_out)
    print(data_out)
    return ''

if __name__ == '__main__':
    bot_server.run(port=5701)
    #端口也是你在酷Q配置文件里自定义的