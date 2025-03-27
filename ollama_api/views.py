from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def chat_with_ollama(request):
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        model = data.get('model', 'llama2')  # 預設使用 llama2 模型
        
        # 發送請求到本地 Ollama API
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return JsonResponse({
                'status': 'success',
                'response': result.get('response', '')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Ollama API 返回錯誤: {response.status_code}'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
