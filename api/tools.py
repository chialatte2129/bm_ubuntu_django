from django.db import connections
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from api import models
import json

# 關閉無效連線
def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

# 時間轉換        
def timedecode(input_time):
    return input_time.strftime('%Y-%m-%d %H:%M:%S')

def timeencode(input_time, utc):
    if isinstance(input_time, str):
        input_time = datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
    input_time += timedelta(hours=utc)
    return input_time

def timedecode_with_zone(input_time, utc):
    if input_time:
        input_time += timedelta(hours=utc)
        return input_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ""

# 確認 Data參數
def checkDataParam(data, check_list=[]):
    status, err = True, ""
    for item in check_list:
        if status and item not in data:
            err = f"Require {item}"
            status = False
    return status, err


# 回覆範例
def codeStatus(code, msg=""):
    res = {'code':code, 'msg':msg, 'response_at':timedecode(timezone.now())}
    if code < 0:
        close_old_connections()
    return res

class ErrorWithCode(Exception):
    def __init__(self, code, msg=""):
        self.code = code
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

def dict_to_json(dictionary):
    return json.dumps(dictionary, ensure_ascii=False, indent=4, sort_keys=False)


