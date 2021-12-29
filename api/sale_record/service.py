from django.http import JsonResponse
from django.views import View
import json
from datetime import datetime
from django.utils import timezone
from api.tools import *
from api.models import  BmProductRecords, BmPair

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def timedecode(input_time):
    return input_time.strftime('%Y-%m-%d %H:%M:%S')

class SaleInfoRecord(View):
    def __init__(self, *args, **kwargs):
        print("run api : sale info record")

    def post(self, request):
        try:
            data = json.loads(request.body)
            """
            {
                "device_id":"ABCDE",
                "code":"123456",
                "price":100,
                "count":1
            }
            """
            print(data)
            status, err = checkDataParam(data, check_list=["device_id", "code"])
            if not status: return JsonResponse(codeStatus(0, msg=err))
            client_ip = get_client_ip(request)
            device_id = data["device_id"] if "device_id" in data else ""
            pair_code = data["code"]
            price = data["price"]
            count = data["count"]
            total_amount = price * count

            trigger = datetime.now(tz=timezone.utc)
            try:
                bm_pair = BmPair.objects.get(id=pair_code)
            except:
                res = codeStatus(0, msg="pair_not_found")
                return JsonResponse(res)
            share_percent = bm_pair.share_percent
            if not share_percent:
                share_percent = 0
            share_amount = total_amount * share_percent

           
            BmProductRecords.objects.create(
                pair_id = pair_code,
                recorded_at = trigger,  
                total_amount = total_amount,
                share_percentage = share_percent,
                share_amount = share_amount,
                
                device_id = device_id,
                locate_ip = client_ip,
                is_pc = 1 if request.user_agent.is_pc else 0,
                is_mobile = 1 if request.user_agent.is_mobile else 0,
                device_family = request.user_agent.device.family,
                os_family = request.user_agent.os.family,
                browser_family = request.user_agent.browser.family,

                is_collect = 0
            )
            res = codeStatus(1, msg="success")
        except Exception as e:
            print(f"sale info record exception, details as below :\n{str(e)}")
            res = codeStatus(-1, msg=str(e))
        print(res)
        return JsonResponse(res)