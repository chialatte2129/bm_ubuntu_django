from django.http import JsonResponse
from django.views import View
import json
from datetime import datetime
from django.utils import timezone
from api.tools import *
from api.models import  BmRedirectRecords, BmPair

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def timedecode(input_time):
    return input_time.strftime('%Y-%m-%d %H:%M:%S')

class GetUrlPath(View):
    def __init__(self, *args, **kwargs):
        print("run api : get day item option")

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            status, err = checkDataParam(data, check_list=["client_id", "code", "device"])
            if not status: return JsonResponse(codeStatus(0, msg=err))
            client_ip = get_client_ip(request)
            client_id = data["client_id"]
            pair_code = data["code"]
            device = data["device"]
            trigger = datetime.now(tz=timezone.utc)
            try:
                bm_pair = BmPair.objects.get(id=pair_code)
            except:
                res = codeStatus(0, msg="pair_not_found")
                return JsonResponse(res)

            target_url = f"{bm_pair.product.url}?id={pair_code}"
            BmRedirectRecords.objects.create(
                pair_id = pair_code,
                device = device,
                device_id = client_id,
                locate_ip = client_ip,
                recorded_at = trigger,
                is_pc = 1 if request.user_agent.is_pc else 0,
                is_mobile = 1 if request.user_agent.is_mobile else 0,
                device_family = request.user_agent.device.family,
                os_family = request.user_agent.os.family,
                browser_family = request.user_agent.browser.family,
            )
            res = codeStatus(1, msg="success")
            res['data'] = {
                "target":target_url
            }
        except Exception as e:
            print(f"get day item option exception, details as below :\n{str(e)}")
            res = codeStatus(-1, msg=str(e))
        print(res)
        return JsonResponse(res)