import requests
import redis
from dotenv import load_dotenv
import os
load_dotenv()
# host=os.getenv("DEV_HOST")
host=os.getenv("PROD_HOST")


r = redis.Redis(host=host, port=6379, db=0)

redisList=r.lrange("summary",0,-1)
summary=[ x.decode() for x in redisList]
redisList=r.smembers("users")
users=[ x.decode() for x in redisList]
TOKEN = os.getenv("BOT_TOKEN")

for user in users:
    for news in summary:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': user,
            'text': news,
            'parse_mode':"Markdown"
        }
        response = requests.post(url, data=payload)

print(f'{len(summary)} news broadcasted to {len(users)} users. ')