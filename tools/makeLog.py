# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/15 10:59
@Auth ： 七月
@File ：makeLog.py
@IDE ：PyCharm
"""

import logging
import os

class Logger():
    _instance = None

    def __new__(cls, level=logging.DEBUG):
        if cls._instance is None:
            try:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance.logger = logging.getLogger()
                cls._instance.logger.setLevel(level)

                log_dir = os.path.join(os.getcwd(),'log')
                #log_dir = os.path.abspath('../log')
                os.makedirs(log_dir, exist_ok=True)

                formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
                file_path = os.path.join(log_dir, 'moco.log')
                file_handler = logging.FileHandler(file_path, encoding='utf-8', mode='a+')
                file_handler.setFormatter(formatter)
                cls._instance.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Logger初始化失败: {e}")
                cls._instance = None  # 重置实例，避免返回未完成的实例
        return cls._instance

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)














