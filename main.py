
from lib.route import  app
from tools.readConf import readConfig
from tools.tool import get_local_ip
from tools.makeLog import Logger

ip = get_local_ip()
log = Logger()





if __name__ == '__main__':

    mocodata = readConfig(confname='moco')
    log.info("程序入口为:" + "http://" + ip + ":9090/moco")
    app.run(host='0.0.0.0',port=mocodata['port'],debug=False)



