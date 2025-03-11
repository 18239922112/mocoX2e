# -*- coding: utf-8 -*-
"""
@Time ： 2025/3/7 10:58
@Auth ： 七月
@File ：tool.py
@IDE ：PyCharm

"""
import os
import socket
from xmindparser import xmind_to_dict
import pandas as pd
from tools.makeLog import Logger

log = Logger()
def get_local_ip():
    '''
    获取本机ip
    :return:
    '''
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address
def exisDir(file_name):
    xmind_dir = os.path.join(os.getcwd(), 'upload')
    excel_dir = os.path.join(os.getcwd(), 'download')


    if file_name.split('.')[1] == 'xmind':
        if not os.path.exists(xmind_dir):
            os.mkdir(xmind_dir,0o777)
            log.info('目录不存在正在创建:'+xmind_dir)
            return xmind_dir
        log.info(xmind_dir+'目录已存在，不再创建')
        return xmind_dir
    else:
        if not os.path.exists(excel_dir):
            os.mkdir(excel_dir,0o777)
            log.info('目录不存在正在创建:' + excel_dir)
            return excel_dir
        log.info(excel_dir + '目录已存在，不再创建')
        return excel_dir

def delFile(file_name):
    '''
    判断上传前是否有重复文件，如果有就先删除再上传
    :param file_name:
    :return:
    '''
    dir = exisDir(file_name)
    path = os.path.join(dir,file_name)
    if os.path.exists(path):
        os.remove(path)
        log.info('已存在相同的文件准备删除旧的文件:'+path)
        return True
    else:
        return False


def dataParWriteExcel(xmind_path, excel_path):
    '''
    数据解析并写入excel
    :param xmind_path:
    :param excel_path:
    :return:
    '''
    # 解析后的xmind格式化数据
    xmind_data = xmind_to_dict(xmind_path)

    # 用例列表
    case_list = xmind_data[0]['topic']['topics'][0]['topics']

    # 初始化DataFrame
    data = {
        "用例名称": [],
        "需求号": [],
        "测试范围": [],
        "模块名称": [],
        "优先级": [],
        "为核心用例": [],
        "已自动化": [],
        "为回归用例": [],
        "前提条件": [],
        "操作步骤": [],
        "期望结果": [],
        "执行结果": []
    }

    try:
        for i in case_list:
            # 需求号
            ipd_number = xmind_data[0]['topic']['topics'][0]['title'].split('#')[1]
            # 模块名称
            module_name = xmind_data[0]['topic']['topics'][0]['title'].split('#')[0]
            # 用例名称
            case_name = i['title']
            # 前提条件
            preconditions = i.get('note') if i.get('note') else ''

            # 优先级
            level = '紧急' if i['makers'][0] == 'priority-1' else i['makers'][0]
            count = 0
            # 操作步骤
            op_step = ""
            # 期望结果
            exp_result = ""
            for j in i['topics']:
                if j.get('title') and j.get('topics'):
                    count += 1
                    step_title = j['title']
                    result_title = j['topics'][0].get('title', '')

                    # 操作步骤
                    op_step += f"{count}. {step_title}\n"
                    # 期望结果
                    exp_result += f"{count}. {result_title}\n"

            # 组装DataFrame
            data["用例名称"].append(case_name)
            data["需求号"].append(ipd_number)
            data["测试范围"].append("功能测试")
            data["模块名称"].append(module_name)
            data["优先级"].append(level)
            data["为核心用例"].append("是")
            data["已自动化"].append("未自动化")
            data["为回归用例"].append("否")
            data["前提条件"].append(preconditions)
            data["操作步骤"].append(op_step)
            data["期望结果"].append(exp_result)
            data["执行结果"].append("成功")

            df = pd.DataFrame(data)
        log.info('生成DataFrame成功')
    except:
        log.error('生成DataFrame失败')

    # 写入Excel文件
    df.to_excel(excel_path, index=False)
    log.info('解析xmind成功，生成excel成功')


if __name__ == '__main__':
    exisDir("MSPSOARCN-570 【浙江移动中台】F8终端安全封堵解封下线需求开发.xls")