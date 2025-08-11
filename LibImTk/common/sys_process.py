
import datetime
import os
import sys


class SysProcess():
    @property
    def run_path():
        args = sys.argv
        return os.path.dirname(args[0]).replace('\\', '/').lower()
    
    @property
    def date():
        now = datetime.datetime.now()
        now_ymd = "{0:%Y%m%d_%H_%M_%S}".format(now)
        return now_ymd

    # @staticmethod
    # def get_run_path():
    #     args = sys.argv
    #     return os.path.dirname(args[0]).replace('\\', '/').lower()

    # @staticmethod
    # def create_directory(dir_path):
    #     os.makedirs(dir_path, exist_ok=True)

    # @staticmethod
    # def get_date():
    #     now = datetime.datetime.now()
    #     now_ymd = "{0:%Y%m%d_%H_%M_%S}".format(now)
    #     return now_ymd
