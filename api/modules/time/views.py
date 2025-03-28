from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import pytz

@csrf_exempt
@require_http_methods(["GET"])
def get_current_time(request):
    try:
        # 獲取台北時區
        tz = pytz.timezone('Asia/Taipei')
        # 獲取當前時間
        current_time = datetime.now(tz)
        # 格式化時間
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        return JsonResponse({
            'status': 'success',
            'time': formatted_time,
            'timezone': 'Asia/Taipei'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500) 