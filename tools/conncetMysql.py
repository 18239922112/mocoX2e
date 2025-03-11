# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/5 14:40
@Auth ： 七月
@File ：conncetMysql.py
@IDE ：PyCharm
"""
import pymysql
import base64
from tools.readConf  import readConfig
from tools.makeLog import Logger

log = Logger()

def connect_mysql(sqlp,params=None):
    """

    :param sqlp: 传递sql
    :param params: sql中变量，防止sql注入
    :return:
    """
    mysql_conf = readConfig(confname='mysql')
    #单独取出来对密码进行加密
    password = mysql_conf['password']
    passwdresult = is_base64_encoded(password)

    # 连接数据库
    connection = pymysql.connect(
        host=mysql_conf['host'],  # 数据库主机地址
        port=int(mysql_conf['port']),
        user=mysql_conf['user'],  # 数据库用户名
        password=passwdresult,  # 数据库密码
        database=mysql_conf['database']  # 数据库名称
    )

    try:
        with connection.cursor() as cursor:
            # 执行查询操作
            sql = sqlp

            cursor.execute(sql,params)
            connection.commit()
            result = cursor.fetchall()
    except Exception as e:
        log.error(e)
        return '{"code":500,"msg":%s}'%e

    finally:
        connection.close()

    return result

def is_base64_encoded(passad):
    try:
        decoded = base64.b64decode(passad)
        decoded_str = decoded.decode('utf-8')  # 尝试将解码后的字节串转换为字符串


        # 如果解码成功，并且解码后的内容是合法的字符串，则返回 True
        return decoded_str
    except Exception:
        passwordenc = base64.b64encode(passad.encode('utf-8'))
        passwdstr = passwordenc.decode('utf-8')
        # 将加密后的密码写入文件
        readConfig(confname='mysql',editkey='password', editcontent=passwdstr)

        return passad



def mysqlResult(query_result):
    '''
    主要用来特殊处理外部接口请求的时候看看接口是否存在且启用
    :param query_result: 获取查询的结果
    :return:
    '''

    apitext =query_result[0][0]
    isenable = query_result[0][1]

    return apitext,isenable



def mysqlAllResult(query_result):
    '''
    用来特殊处理查询全部数据
    :param query_result: 获取查询的结果
    :return:
    '''

    dictdata = {}
    listdata = []
    for list in query_result:
        listdata.append({'apimame':list[1],'apipath':list[2],'isenable':list[4]})
    dictdata["success"] = listdata
    return dictdata



