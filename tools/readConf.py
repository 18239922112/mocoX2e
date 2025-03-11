# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/9 10:33
@Auth ： 七月
@File ：readConf.py
@IDE ：PyCharm
"""
import configparser


def readConfig(confname=None,editkey=None,editcontent=None):
    '''

    :param confname: 配置文件中[]
    :param editkey: 需要编辑的key就是配置文件中[]下的k，比如[mysql] 下的password
    :param editcontent: 要写入的内容
    :return:
    '''
    # 创建ConfigParser对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('conf/moco.conf', encoding='utf-8')
    if editkey:
        # 修改配置项

        config.set(confname, editkey, editcontent)

        # 写入修改后的配置文件
        with open('../conf/moco.conf', 'w') as configfile:
            config.write(configfile)
            return



    else:
        data = (dict(config[confname]))

        return data
