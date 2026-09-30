#!/usr/bin/env python3
"""
Daily AI ecosystem updater.
Uses Google News RSS with site restrictions to discover fresh articles, then stores
a compact update feed in data.json. The company/model catalog remains curated so
the tracker does not silently invent model names.
"""
import json, re, urllib.parse, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data.json"

SEARCHES={
"OpenAI":"site:openai.com/news AI OpenAI model OR API OR agent",
"Anthropic":"site:anthropic.com/news Claude model OR agent",
"Google DeepMind":"site:deepmind.google AI Gemini model",
"Meta":"site:ai.meta.com/blog Muse OR Llama OR AI model",
"xAI":"site:x.ai Grok AI model",
"Mistral AI":"site:mistral.ai/news OR site:docs.mistral.ai model",
"DeepSeek":"site:deepseek.com/en/news DeepSeek model",
"Alibaba / Qwen":"site:qwen.ai Qwen model",
"Microsoft":"site:microsoft.com AI Phi model Copilot",
"NVIDIA":"site:nvidia.com AI model Nemotron",
"Amazon / AWS":"site:aws.amazon.com/about-aws/whats-new AI Nova model",
"Cohere":"site:cohere.com/newsroom AI model",
"Databricks":"site:databricks.com/blog AI model Mosaic",
"IBM":"site:ibm.com/new AI Granite model",
"Baidu":"site:baidu.com ERNIE AI model",
"Zhipu AI":"site:zhipuai.cn GLM AI model",
"Moonshot AI":"site:moonshot.cn Kimi AI model",
"Indian AI ecosystem":"site:sarvam.ai OR site:krutrim.ai AI model"
}

def rss(q):
    url="https://news.google.com/rss/search?q="+urllib.parse.quote(q)+"&hl=en-US&gl=US&ceid=US:en"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 AI-Ecosystem-Tracker/1.0"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return r.read()

def parse_company(company,q):
    root=ET.fromstring(rss(q))
    out=[]
    for item in root.findall("./channel/item")[:12]:
        title=(item.findtext("title") or "").strip()
        link=(item.findtext("link") or "").strip()
        pub=(item.findtext("pubDate") or "").strip()
        desc=re.sub("<[^>]+>"," ",item.findtext("description") or "").strip()
        try: dt=datetime.strptime(pub,"%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc).isoformat()
        except: dt=datetime.now(timezone.utc).isoformat()
        out.append({"date":dt,"company":company,"title":title,"summary":desc[:280],"url":link,"kind":"News"})
    return out

data=json.loads(DATA.read_text(encoding="utf-8"))
existing={(u["company"],u["title"]) for u in data.get("updates",[])}
new=[]
for company,q in SEARCHES.items():
    try:
        for u in parse_company(company,q):
            if (u["company"],u["title"]) not in existing:
                new.append(u); existing.add((u["company"],u["title"]))
    except Exception as e:
        print("WARN",company,e)

data["updates"]=(new+data.get("updates",[]))[:500]
data["generated_at"]=datetime.now(timezone.utc).isoformat()
DATA.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
print("Added",len(new),"updates")
