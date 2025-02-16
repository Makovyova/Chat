from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from telegram import Bot
from bot.bot_config import TOKEN


# Initialize bot instance
bot = Bot(token=TOKEN)

# Set webhook URL (replace <your_domain> with actual domain when deploying)
# bot.set_webhook(url='https://<your_domain>/bot/webhook/')


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        update = json.loads(request.body)
        # ����� ���� �������� ������ ��������� ����������
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)
