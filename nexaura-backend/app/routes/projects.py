from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.services.supabase_client import supabase  # 导入 Supabase 客户端
from app.routes.auth import get_current_user # 导入新的依赖函数
from gotrue.errors import AuthApiError

router = APIRouter()

# Pydantic 模型
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectUpdate(ProjectCreate): # 更新模型可以继承创建模型
    status: Optional[str] = None

# 注意：为了与数据库和前端的 Supabase 返回值保持一致，
# Project 模型现在包含一个 auth_uid (UUID) 而不是 user_id (int)
class Project(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = "新建" # 提供默认值
    created_at: datetime
    updated_at: Optional[datetime] = None # 更新时间可能为空
    user_id: str # Supabase 的 user.id 是 UUID 字符串

@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, current_user = Depends(get_current_user)):
    try:
        response = supabase.from_("projects").insert({
            "title": project.title,
            "description": project.description,
            "user_id": current_user.id
        }).execute()
        
        if response.data:
            return response.data[0]
        else:
            # Supabase 的 Python 客户端在插入失败时可能会通过 postgrest.exceptions.APIError 抛出异常
            # 这里的通用异常处理可以捕获它们
            raise HTTPException(status_code=400, detail="创建项目失败")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.get("/", response_model=List[Project])
async def get_projects(current_user = Depends(get_current_user)):
    try:
        response = supabase.from_("projects").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取项目列表失败: {str(e)}")

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: int, current_user = Depends(get_current_user)):
    try:
        response = supabase.from_("projects").select("*").eq("id", project_id).single().execute()
        
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
        
        if response.data.get('user_id') != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问此项目")
            
        return response.data
    except AuthApiError as e:
        raise HTTPException(status_code=e.status, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取项目失败: {str(e)}")

@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: int, project_update: ProjectUpdate, current_user = Depends(get_current_user)):
    try:
        # 首先验证所有权
        project_res = supabase.from_("projects").select("user_id").eq("id", project_id).single().execute()
        if not project_res.data or project_res.data.get('user_id') != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权修改此项目")

        # 准备更新数据
        update_data = project_update.model_dump(exclude_unset=True)
        update_data['updated_at'] = datetime.utcnow().isoformat()

        response = supabase.from_("projects").update(update_data).eq("id", project_id).select().single().execute()

        if response.data:
            return response.data
        else:
            raise HTTPException(status_code=400, detail="更新项目失败")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"更新项目时发生错误: {str(e)}")

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, current_user = Depends(get_current_user)):
    try:
        # 首先，验证项目所有权
        project_res = supabase.from_("projects").select("user_id").eq("id", project_id).single().execute()
        if not project_res.data or project_res.data.get('user_id') != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权删除此项目")

        # 删除项目
        supabase.from_("projects").delete().eq("id", project_id).execute()
        return
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="删除项目时发生错误")

