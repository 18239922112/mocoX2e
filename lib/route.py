# -*- coding: utf-8 -*-
"""
@Time ： 2024/2/2 14:39
@Auth ： 七月
@File ：route.py
@IDE ：PyCharm
"""
import json
import os

from flask import Flask, request, jsonify, render_template, send_file
from tools.conncetMysql import connect_mysql, mysqlResult, mysqlAllResult
from tools.makeLog import Logger
from tools.tool import exisDir, delFile, dataParWriteExcel

app = Flask(__name__, static_url_path='/../static', static_folder='../static',template_folder='../templates')

log = Logger()




@app.before_request
def get_call_ip():
    '''
    获取调用者的ip
    :return:
    '''
    # 尝试获取 X-Forwarded-For 头部中的 IP 地址
    if 'X-Forwarded-For' in request.headers:
        # 使用nginx部署的时候需要通过这种方式获取真实的客户端ip，不然的话返回的就是代理服务器的地址就不正确了
        client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()  # 取第一个 IP 并去除空格
    else:
        client_ip = request.remote_addr
    log.info('请求来自于' + client_ip)


@app.route('/moco')
def index():
    return render_template('index.html')

@app.route('/x2e')
def x2e():
    return render_template('x2e.html')



@app.route('/moco/addMoco',methods=['POST'])
def addMoco():
    data = request.json
    #print(data)
    apiname = data["apiname"]
    apipath = data["apipath"]
    apitext = data["apitext"]
    isChecked = data["isChecked"]
    sql = "select  apitext from apitest where apipath=%s;"
    query_result = connect_mysql(sql, params=apipath)

    if query_result:
        log.info('%s:该接口路径已使用，请核对后再添加'%apipath)
        return jsonify({"code":300,"msg":"该接口路径已使用，请核对后再添加"})
    else:
        sql = "insert into apitest (apiname,apipath,apitext,isEnable) VALUES(%s,%s,%s,%s);"
        params = (apiname,apipath,apitext,isChecked)
        connect_mysql(sql,params)
        log.info('添加接口成功,路径为：%s'%apipath)
        return jsonify({"code":200,"msg":"添加接口成功"})

@app.route('/moco/delMoco',methods=['POST'])
def delMoco():
    data = request.json
    apipath = data["apipath"]

    sql = "delete from apitest where apipath=%s;"

    try:
        connect_mysql(sql, params=apipath)
        return jsonify({"code": 200, "msg": "删除成功"})
    except Exception as e:
        log.error(e)
        return jsonify({"code":"500","msg":"sql执行报错了错误原因:%s"%e})




@app.route('/moco/editMoco',methods=['POST'])
def editMoco():
    data = request.json
    # print(data)
    apiname = data["apiname"]
    apipath = data["apipath"]
    apitext = data["apitext"]
    isEnable = data["isChecked"]
    sql = "update apitest set  apiname=%s,apitext=%s,isEnable=%s where apipath=%s;"
    params = (apiname,apitext,isEnable,apipath)
    try:
        connect_mysql(sql, params=params)
        return jsonify({"code": 200, "msg": "修改成功"})
    except Exception as e:
        log.error(e)
        return jsonify({"code":"500","msg":f"sql执行报错了错误原因:{e}"})








@app.route('/moco/queryAll',methods=['GET'])
def queryAll():
    #sql = "select  * from apitest order by id desc;"
    sql = "select  * from apitest order by id desc limit 0,10;"
    query_result = connect_mysql(sql)
    query_all = mysqlAllResult(query_result)
    return jsonify(query_all)


@app.route('/moco/queryLike',methods=['POST'])
def queryLike():
    data = request.json

    apipath = data["apipath"]

    sql = "select  * from apitest  where apipath like %s order by id desc limit 0,10;"

    query_result = connect_mysql(sql,params=('%' + apipath + '%'))

    query_all = mysqlAllResult(query_result)
    return jsonify(query_all)



@app.route('/moco/queryApi',methods=['POST'])
def queryApi():
    data = request.json

    apipath = data["apipath"]

    sql = "select  apitext,isEnable from apitest where apipath=%s;"
    query_result = connect_mysql(sql, params=apipath)
    apitext,isable = mysqlResult(query_result)

    return jsonify({"apitext":apitext,"isable":isable})



@app.route('/moco/queryLimit',methods=['POST'])
def queryLimit():
    data = request.json
    page = data["page"]

    sql = "select  * from apitest order by id desc limit %s,10;"

    query_result = connect_mysql(sql,params=page)
    query_all = mysqlAllResult(query_result)
    return jsonify(query_all)





@app.route('/moco/queryCount', methods=['GET'])
def queryCount():


    sql = "select  count(*) from apitest;"

    count = connect_mysql(sql)
    return jsonify({"count":count})

@app.route('/x2e/upload', methods=['POST'])
def uploadFileHhandler():
    #获取前端上传的文件
    file = request.files['file']
    #上传前先检查目录是否存在，不存在则创建
    xmind_dir = exisDir(file.filename)
    #上传前先删除目录下同名文件
    delFile(file.filename)
    #保存文件至目录
    xmind_path = os.path.join(xmind_dir,file.filename)
    file.save(xmind_path)
    log.info('上传文件成功：'+file.filename)

    #开始解析文件
    excel_file_name = xmind_path.split(xmind_dir)[1].split(".")[0][1:] + "测试用例.xlsx"

    excel_dir = exisDir(excel_file_name)

    excel_path = os.path.join(excel_dir,excel_file_name)

    dataParWriteExcel(xmind_path,excel_path)
    log.info('解析xmind成功，生成excel成功')
    app.config['excel_path'] = excel_path
    return excel_path


@app.route('/x2e/download')
def downLoadFile():

    if os.path.exists(app.config['excel_path']):
        log.info('下载文件成功:'+app.config['excel_path'])
        return send_file(app.config['excel_path'],as_attachment=True)
    else:
        return app.config['excel_path']+'文件不存在'


@app.route('/<path:apipath>',methods=['GET','POST'])
def mocoServer(apipath):
    '''
    通配符路由通常至于最后一个，不妨碍其他路由优先执行
    :param apipath:
    :return:
    '''
    sql = "select  apitext,isEnable from apitest where apipath=%s;"
    query_result = connect_mysql(sql,params='/'+apipath)


    if query_result:
        apitext,isEnable = mysqlResult(query_result)
        if isEnable == 0:
            try:
                return json.loads(apitext)
            except Exception as e:
                log.error(e)
                return jsonify({"code":"500","msg":f"请检查你的接口数据格式是否正确"})
        else:
            log.info('%s此接口已停用'%apipath)
            return jsonify({"code":"500","msg":"此接口已停用"})
    else:
        log.info('%s此接口不存在请核对后再请求' % apipath)
        return jsonify({"code":"500","msg":"此接口不存在请核对后再请求"})