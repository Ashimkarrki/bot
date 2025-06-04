import os
from google import genai
import json
import asyncio 
import redis
from dotenv import load_dotenv
load_dotenv()
# host=os.getenv("DEV_HOST")
host=os.getenv("PROD_HOST")


r = redis.Redis(host=host, port=6379, db=0)

load_dotenv()
API_KEY=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
     
async def call_llm_after_x_min(title,date,content,x): 
    await asyncio.sleep(x*60)  

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=f'तपाईं एक नेपाली समाचार विश्लेषक हुनुहुन्छ । तपाईंलाई एक नेपाली भाषामा लेखिएको समाचार दिइनेछ । तपाईंको काम सो समाचारलाई पढेर एउटा उपयुक्त शीर्षक बनाउने र त्यस समाचारका मुख्य बुँदाहरू संक्षेपमा, बुलेट पोइन्टमा नेपाली भाषामै लेख्ने हो । जवाफ Markdown ढाँचामा दिनुहोस् — शीर्षकलाई ** प्रयोग गरेर बोल्ड बनाउनुहोस्, र मुख्य बुँदाहरूलाई - चिह्न प्रयोग गरेर लेख्नुहोस्। जवाफ सिधै शीर्षकबाट सुरु गर्नूस्, कुनै लेबल (जस्तै “शीर्षक:”, “मुख्य बुँदाहरू:”) नलेख्नूस्। उत्तर संक्षिप्त र सटिक हुनुपर्छ। अनावश्यक व्याख्या नगर्नूस्। इनपुट समाचार: शीर्षक: {title} मिति: {date} सामग्री: {content}',
 )

    return response.text
     

redisList=r.lrange("news",0,-1)


news=[  json.loads(x.decode()) for x in redisList]
newsSummary=[]
for newsItem in news:
    res=asyncio.run(call_llm_after_x_min(newsItem["title"],newsItem["date"],newsItem["content"],0.3)) 
    # newsSummary.append({"summary":res})
    newsSummary.append(res)


   
r.delete("summary")
for s in newsSummary:
    r.lpush("summary",s)

print("Summary Generated")

