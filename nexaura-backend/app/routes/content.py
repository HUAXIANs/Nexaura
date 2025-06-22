from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import random
from app.routes.auth import get_current_user

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

# 模擬內容生成服務
class ContentGenerator:
    @staticmethod
    async def generate_xiaohongshu_content(topic: str, style: str) -> GeneratedContent:
        # 模擬 API 調用延遲
        await asyncio.sleep(2)
        
        # 模擬不同風格的內容生成
        if style == "explore":
            return ContentGenerator._generate_explore_style(topic)
        else:
            return ContentGenerator._generate_default_style(topic)
    
    @staticmethod
    def _generate_explore_style(topic: str) -> GeneratedContent:
        # 模擬探店種草風格的內容生成
        titles = [
            f"📍{topic}｜隱藏在城市裡的寶藏店！",
            f"🔥{topic}｜這家店真的太絕了！",
            f"✨{topic}｜終於找到了心中的完美店鋪",
            f"💯{topic}｜強烈推薦這家神仙店鋪！"
        ]
        
        content_templates = [
            f"""今天要和大家分享關於{topic}的超棒體驗！🥰

📍 地點：市中心附近
🕐 營業時間：10:00-22:00

✨ 亮點：
• 環境超棒，很適合拍照📸
• 服務態度很好，店員很熱情
• 性價比很高，值得推薦💰

真的是一次很棒的體驗！姐妹們快去打卡吧～

#推薦理由：
1. 環境優雅，氛圍感滿分
2. 產品質量很好，值得信賴
3. 價格合理，學生黨也能承受

總的來說，這次的{topic}體驗讓我很滿意，已經加入我的收藏清單了！下次還會再來的～""",
            
            f"""關於{topic}，我終於找到了心中的完美選擇！💕

🌟 第一印象：
一進門就被環境吸引了，裝修風格很有特色，每個角落都很用心。

🌟 體驗感受：
• 氛圍很棒，讓人感覺很放鬆
• 細節處理得很好，可以看出用心程度
• 整體感受超出預期

💡 小貼士：
建議大家提前預約，避免排隊等待。最好選擇非高峰時段，體驗會更好～

真的很推薦大家去試試！相信你們也會喜歡的～"""
        ]
        
        tags_pool = [
            f"{topic}", "打卡聖地", "強烈推薦", "性價比高", "環境很棒",
            "服務貼心", "值得收藏", "下次還來", "朋友聚會", "週末好去處"
        ]
        
        image_descriptions = [
            f"{topic}的外觀環境，展現整體氛圍",
            f"內部環境細節，突出特色裝修風格",
            f"產品或服務的特寫，展現品質感"
        ]
        
        return GeneratedContent(
            title=random.choice(titles),
            content=random.choice(content_templates),
            tags=random.sample(tags_pool, min(5, len(tags_pool))),
            image_descriptions=image_descriptions
        )
    
    @staticmethod
    def _generate_default_style(topic: str) -> GeneratedContent:
        return GeneratedContent(
            title=f"關於{topic}的分享",
            content=f"今天想和大家分享關於{topic}的一些心得和體驗...",
            tags=[topic, "分享", "推薦"],
            image_descriptions=[f"{topic}相關圖片"]
        )

# 模擬訊飛 API 調用
async def call_xunfei_api(topic: str, platform: str, style: str) -> GeneratedContent:
    """
    模擬調用訊飛 API 生成內容
    在實際項目中，這裡會調用真實的訊飛星火 API
    """
    # TODO: 實現真實的訊飛 API 調用
    # 這裡使用模擬數據
    
    if platform == "xiaohongshu":
        return await ContentGenerator.generate_xiaohongshu_content(topic, style)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"暫不支持平台：{platform}"
        )

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

