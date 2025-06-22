import base64
import datetime
import hashlib
import hmac
import json
import os
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urlencode
import websocket
import asyncio
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import calendar

# --- 配置讯飞API的认证信息 ---
APP_ID = os.environ.get("XUNFEI_APP_ID", "5dbda2f6")
API_KEY = os.environ.get("XUNFEI_API_KEY", "5daa663a42b7ee003b8de6fc42578cad")
API_SECRET = os.environ.get("XUNFEI_API_SECRET", "MzQ2YzY2NzViMmEzMDExNzlkYjMxZDU2")

# 打印API凭证，确认正确
print("使用的API凭证:")
print(f"APP_ID: {APP_ID}")
print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")

# 星火大模型 v3.5 的 WebSocket 地址
SPARK_URL = "wss://spark-api.xf-yun.com/v3.5/chat"
# 文本向量化服务的 WebSocket 地址
EMBEDDING_URL = "wss://spark-api.xf-yun.com/v3.5/embedding"

# 是否使用模拟响应（用于测试）
USE_MOCK = False  # 关闭模拟响应，使用真实API

# 全局变量，用于存储WebSocket的返回结果
answer = ""

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(time.mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        return url

# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)

# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    # print("### closed ###")
    pass

# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))

def run(ws, *args):
    data = json.dumps(ws.question)
    ws.send(data)

# 收到websocket消息的处理
def on_message(ws, message):
    global answer
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f"请求错误: {code}, {data}")
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # print(content,end ="")
        answer += content
        if status == 2:
            ws.close()

def gen_params(appid, question, domain="4.0Ultra"):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data

def verify_api_credentials():
    """验证API凭证是否有效"""
    print("验证API凭证:")
    print(f"APP_ID: {APP_ID}, 长度: {len(APP_ID)}")
    print(f"API_KEY: {API_KEY}, 长度: {len(API_KEY)}")
    print(f"API_SECRET: {API_SECRET}, 长度: {len(API_SECRET)}")
    
    if not APP_ID or not API_KEY or not API_SECRET:
        print("警告: API凭证不完整")
        return False
    
    # 讯飞API凭证长度验证
    if len(APP_ID) != 8:
        print(f"警告: APP_ID长度异常，应为8位，实际为{len(APP_ID)}位")
    
    if len(API_KEY) != 32:
        print(f"警告: API_KEY长度异常，应为32位，实际为{len(API_KEY)}位")
    
    if len(API_SECRET) != 32:
        print(f"警告: API_SECRET长度异常，应为32位，实际为{len(API_SECRET)}位")
    
    print("API凭证验证完成")
    return True

# 在模块加载时验证API凭证
verify_api_credentials()

async def generate_text_with_spark(prompt: str) -> Optional[str]:
    # 从环境变量或默认值获取API凭证
    APPID = os.environ.get("XUNFEI_APP_ID", "5dbda2f6")
    APISecret = os.environ.get("XUNFEI_API_SECRET", "MzQ2YzY2NzViMmEzMDExNzlkYjMxZDU2")
    APIKey = os.environ.get("XUNFEI_API_KEY", "5daa663a42b7ee003b8de6fc42578cad")
    
    # 构建请求
    question = [{"role": "user", "content": prompt}]
    
    # 重置全局变量
    global answer
    answer = ""
    
    # 创建WebSocket连接
    wsParam = Ws_Param(APPID, APIKey, APISecret, "wss://spark-api.xf-yun.com/v4.0/chat")
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.question = gen_params(APPID, question)
    
    # 运行WebSocket
    # 使用 asyncio.to_thread 包装阻塞调用
    try:
        await asyncio.to_thread(ws.run_forever, sslopt={"cert_reqs": ssl.CERT_NONE})
        
        # 检查 answer 是否有内容
        if answer:
            return answer
        else:
            print("讯飞API调用完成，但未返回任何内容。")
            return None
            
    except Exception as e:
        print(f"WebSocket 运行出错: {e}")
        return None

async def get_text_embedding(text: str) -> List[float]:
    """获取文本的向量表示"""
    if not text or not text.strip():
        print("文本为空，返回空向量")
        return []
    
    try:
        print(f"开始获取文本向量，文本长度: {len(text)}")
        url = create_url(EMBEDDING_URL)
        print(f"生成的URL: {url}")
        
        ws = websocket.create_connection(url)
        print("WebSocket连接已创建")
        
        data = {
            "header": {
                "app_id": APP_ID,
                "uid": "user1"
            },
            "parameter": {
                "chat": {
                    "domain": "general",
                    "temperature": 0.5,
                    "max_tokens": 4096
                }
            },
            "payload": {
                "message": {
                    "text": [{"role": "user", "content": text}]
                }
            }
        }
        
        print(f"发送数据: {json.dumps(data)}")
        ws.send(json.dumps(data))
        print("数据已发送，等待响应...")
        
        response = ws.recv()
        print(f"收到响应: {response}")
        ws.close()
        print("WebSocket连接已关闭")
        
        result = json.loads(response)
        if "payload" in result and "embedding" in result["payload"]:
            print("成功解析向量")
            return result["payload"]["embedding"]["vector"]
        
        print(f"响应中未找到向量: {result}")
        return []
        
    except Exception as e:
        print(f"获取文本向量时出错: {e}")
        return []

async def get_chat_response(messages: List[Dict[str, str]]) -> str:
    """获取对话回复
    
    :param messages: 消息列表，格式为 [{"role": "user", "content": "你好"}, {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}]
    :return: 对话回复
    """
    if not messages:
        print("消息列表为空，返回空响应")
        return ""
    
    try:
        print(f"开始获取对话回复，消息数量: {len(messages)}")
        url = create_url(SPARK_URL)
        print(f"生成的URL: {url}")
        
        try:
            ws = websocket.create_connection(url, timeout=30)
            print("WebSocket连接已创建")
        except Exception as conn_err:
            print(f"WebSocket连接失败: {conn_err}")
            if hasattr(conn_err, 'status_code'):
                print(f"状态码: {conn_err.status_code}")
            if hasattr(conn_err, 'headers'):
                print(f"响应头: {conn_err.headers}")
            if hasattr(conn_err, 'resp_data'):
                print(f"响应数据: {conn_err.resp_data}")
            raise
        
        # 构建符合星火大模型v3.5规范的请求
        data = {
            "header": {
                "app_id": APP_ID,
                "uid": "12345678"
            },
            "parameter": {
                "chat": {
                    "domain": "general",
                    "temperature": 0.5,
                    "max_tokens": 4096
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }
        
        print(f"发送数据: {json.dumps(data)}")
        ws.send(json.dumps(data))
        print("数据已发送，等待响应...")
        
        # 星火大模型可能会分多次返回结果，需要循环接收
        response_text = ""
        while True:
            response = ws.recv()
            print(f"收到响应: {response}")
            
            result = json.loads(response)
            
            # 检查是否有错误
            if "header" in result and "code" in result["header"] and result["header"]["code"] != 0:
                print(f"API返回错误码: {result['header']['code']}, 消息: {result['header'].get('message', '无')}")
                break
            
            # 提取回复内容
            if "payload" in result and "text" in result["payload"]:
                for item in result["payload"]["text"]:
                    if "content" in item:
                        response_text += item["content"]
            
            # 检查是否是最后一条消息
            if "header" in result and "status" in result["header"] and result["header"]["status"] == 2:
                print("这是最后一条消息，结束接收")
                break
        
        ws.close()
        print("WebSocket连接已关闭")
        
        if response_text:
            print(f"成功获取回复，长度: {len(response_text)}")
            return response_text
        
        print("未能获取有效回复")
        return ""
        
    except Exception as e:
        print(f"获取对话回复时出错: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return ""

async def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """批量获取文本向量
    
    :param texts: 文本列表
    :return: 向量列表
    """
    if not texts:
        return []
        
    results = []
    for text in texts:
        embedding = await get_text_embedding(text)
        results.append(embedding)
        
    return results

# 添加模拟响应函数
def get_mock_response(prompt: str) -> str:
    """生成模拟的API响应，用于测试"""
    if "小红书" in prompt or "xiaohongshu" in prompt.lower():
        return """
{
  "title": "☕探店推荐 | 无锡最受欢迎的5家小众咖啡厅，人少环境好！",
  "content": "今天给大家分享无锡最值得打卡的5家咖啡厅！这些店不仅颜值高，咖啡也超级好喝，重点是人不多，很适合安静地坐一下午～\n\n🏠【啡想】\n位于无锡市中心的一家隐藏小店，店面不大但很温馨。他们家的手冲咖啡特别香醇，老板是咖啡师大赛冠军，每一杯都很用心。周末去要早点，位置不多。\n\n🌿【木几咖啡】\n这家店的环境是我最爱的，满满的绿植和原木风，坐在里面感觉特别放松。他们家的脏脏包配冰美式简直绝配！笔记本带去办公也很舒适，插座超多。\n\n🎨【画室咖啡】\n一家结合了艺术展览的咖啡店，经常会有一些小型画展。店内的拉花艺术感很强，咖啡豆都是自己烘焙的，香气特别。甜点也很推荐，特别是提拉米苏！\n\n📚【阅见书房】\n半咖啡厅半书店的概念，书架上全是可以阅读的书籍。他们家的桂花拿铁是招牌，淡淡的桂花香配上醇厚的咖啡，别有一番风味。环境安静，很适合看书发呆。\n\n🌙【夜澜咖啡】\n这家是晚上才营业的咖啡馆，从下午五点到凌晨。夜景超级美，可以看到无锡的城市灯光。他们家的酒精咖啡很特别，微醺的感觉很放松，周末还会有驻唱。",
  "tags": ["无锡探店", "咖啡馆推荐", "小众咖啡", "无锡美食", "治愈系咖啡馆", "周末好去处", "拍照圣地"],
  "image_descriptions": ["咖啡厅外观照片，展示店面的文艺招牌和入口处的绿植装饰", "正在制作的咖啡照片，特写镜头捕捉咖啡师正在进行精细的拉花过程", "咖啡厅内部环境照片，展示舒适的座位区、原木桌椅和温馨的灯光氛围"]
}
"""
    else:
        return """
{
  "title": "关于" + topic + "的内容",
  "content": "这是一个模拟生成的内容，用于测试系统功能。\n\n当您看到这段文字时，表示系统正在使用模拟数据而非真实API。\n\n请配置正确的讯飞API凭证以获取真实内容。",
  "tags": ["测试", "模拟数据", "开发中"],
  "image_descriptions": ["测试图片1", "测试图片2", "测试图片3"]
}
"""

async def generate_image_with_spark(prompt: str) -> Optional[str]:
    """
    (占位) 调用讯飞图片生成API，根据给定的Prompt生成图片。

    :param prompt: 描述图片内容的文本
    :return: 生成的图片的URL，如果生成失败则返回None
    """
    try:
        if not prompt.strip():
            return None
            
        # TODO: 实现调用讯飞图片生成API的逻辑
        print(f"接收到图片生成请求: {prompt}")
        time.sleep(1)  # 模拟API调用延迟
        return "https://dummyimage.com/600x400/000/fff&text=Generated+Image"
    except Exception as e:
        print(f"图片生成失败：{str(e)}")
        return None 