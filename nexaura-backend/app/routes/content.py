from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import random
from app.routes.auth import get_current_user
from app.services import xunfei_api
import json
import re

router = APIRouter()

# Pydantic 模型
class ContentRequest(BaseModel):
    topic: str
    platform: str = "xiaohongshu"
    style: str = "explore"
    project_id: Optional[int] = None

class GeneratedContent(BaseModel):
    title: str
    content: str
    tags: List[str]
    image_descriptions: Optional[List[str]] = None

# 改造这个函数，让它调用真实的讯飞API
async def call_xunfei_api(topic: str, platform: str, style: str) -> GeneratedContent:
    """
    调用真实的讯飞星火API生成内容
    """
    if platform != "xiaohongshu":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"暂不支持平台：{platform}"
        )

    # 改造Prompt，使用分隔符而不是要求返回JSON
    prompt = f"""
请你扮演一位资深的小红书运营专家。
你的任务是根据以下要求，为我创作一篇爆款小redbook文案。

【主题】: {topic}
【风格】: {style}

【要求】:
1. 严格按照下面的格式和分隔符输出，不要添加任何额外的解释性文字。
2. 各个部分之间使用 '---xxx---' 作为分隔符。

---xxx---
[TITLE]
这里是生成的标题

---xxx---
[CONTENT]
这里是生成的正文内容
段落之间请用空行隔开

---xxx---
[TAGS]
这里是生成的标签, 每个标签用英文逗号分隔

---xxx---
[IMAGES]
这里是生成的3条配图建议, 每个建议占一行
"""

    try:
        # 调用我们封装好的函数
        response_text = await xunfei_api.generate_text_with_spark(prompt)
        
        if not response_text:
            print("讯飞API未返回任何内容，使用默认响应")
            default_response = {
                "title": f"关于{topic}的分享",
                "content": "由于AI生成内容出现问题，这是一个默认内容。\n\n请稍后再试。",
                "tags": ["小红书", "分享", topic],
                "image_descriptions": ["相关图片"]
            }
            return GeneratedContent(**default_response)
        
        print(f"讯飞API原始返回: {response_text}")
        
        # 解析由'---xxx---'分隔的文本
        parts = response_text.split('---xxx---')
        
        response_data = {}
        
        for part in parts:
            part = part.strip()
            if part.startswith('[TITLE'):
                try:
                    response_data['title'] = part.split('\n', 1)[1].strip()
                except IndexError:
                    pass # Ignore empty parts
            elif part.startswith('[CONTENT'):
                try:
                    response_data['content'] = part.split('\n', 1)[1].strip()
                except IndexError:
                    pass
            elif part.startswith('[TAGS'):
                try:
                    tags_str = part.split('\n', 1)[1].strip()
                    response_data['tags'] = [tag.strip() for tag in tags_str.split(',')]
                except IndexError:
                    pass
            elif part.startswith('[IMAGES'):
                try:
                    images_str = part.split('\n', 1)[1].strip()
                    response_data['image_descriptions'] = [desc.strip() for desc in images_str.split('\n')]
                except IndexError:
                    pass
        
        # 确保所有必需字段都存在，提供默认值
        if 'title' not in response_data:
            response_data['title'] = f"关于{topic}的分享"
        if 'content' not in response_data:
            response_data['content'] = "AI未能按预期格式生成内容，请稍后再试。"
        if 'tags' not in response_data:
            response_data['tags'] = [topic]
        if 'image_descriptions' not in response_data:
            response_data['image_descriptions'] = ["AI未能生成图片建议"]
            
        return GeneratedContent(**response_data)

    except Exception as e:
        print(f"调用AI服务或解析内容时发生错误: {e}")
        raise HTTPException(status_code=500, detail=f"AI服务调用或解析失败: {str(e)}")

@router.post("/generate", response_model=GeneratedContent)
async def generate_content(
    request: ContentRequest, 
    current_user: dict = Depends(get_current_user)
):
    """
    生成內容接口
    """
    if not request.topic.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="主題不能為空"
        )
    
    try:
        # 調用內容生成服務
        generated_content = await call_xunfei_api(
            topic=request.topic,
            platform=request.platform,
            style=request.style
        )
        
        if generated_content is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="內容生成服務返回了空的結果"
            )
            
        return generated_content
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"內容生成失敗：{str(e)}"
        )

@router.get("/platforms")
async def get_supported_platforms():
    """
    獲取支持的平台列表
    """
    return {
        "platforms": [
            {
                "id": "xiaohongshu",
                "name": "小紅書",
                "description": "適合生活分享、探店種草等內容",
                "supported": True
            },
            {
                "id": "wechat",
                "name": "微信公眾號",
                "description": "適合長文章、專業內容",
                "supported": False
            },
            {
                "id": "weibo",
                "name": "微博",
                "description": "適合短文、熱點話題",
                "supported": False
            }
        ]
    }

@router.get("/styles")
async def get_supported_styles():
    """
    獲取支持的風格列表
    """
    return {
        "styles": [
            {
                "id": "explore",
                "name": "探店種草風",
                "description": "適合分享探店、購物、體驗類內容",
                "supported": True
            },
            {
                "id": "lifestyle",
                "name": "生活分享風",
                "description": "適合日常生活、心得分享",
                "supported": False
            },
            {
                "id": "professional",
                "name": "專業科普風",
                "description": "適合知識分享、專業內容",
                "supported": False
            }
        ]
    }

