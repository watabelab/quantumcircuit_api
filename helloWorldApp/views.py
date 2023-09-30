from django.shortcuts import render
from django.http import JsonResponse

# 以下を追加
def execute_python_code(request):
    # ここでPythonコードを実行
    result = {"message": "Hello from Python!"}
    return JsonResponse(result)
def index (request):
    return render(request,'hello_world/index.html')