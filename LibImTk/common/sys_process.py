
import datetime
import os
import sys


class SysProcess():
    @staticmethod
    def run_path():
        args = sys.argv
        return os.path.dirname(args[0]).replace('\\', '/').lower()
    
    @staticmethod
    def date():
        now = datetime.datetime.now()
        now_ymd = "{0:%Y%m%d_%H_%M_%S}".format(now)
        return now_ymd

