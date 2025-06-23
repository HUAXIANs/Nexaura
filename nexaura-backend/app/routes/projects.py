from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.routes.auth import get_current_user

router = APIRouter()

# Pydantic 模型
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Project(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: int

# 模擬項目數據庫
fake_projects_db = {}
project_counter = 0

@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    global project_counter
    project_counter += 1
    
    now = datetime.utcnow()
    new_project = {
        "id": project_counter,
        "title": project.title,
        "description": project.description,
        "status": "新建",
        "created_at": now,
        "updated_at": now,
        "user_id": current_user["id"]
    }
    
    fake_projects_db[project_counter] = new_project
    return Project(**new_project)

@router.get("/", response_model=List[Project])
async def get_projects(current_user: dict = Depends(get_current_user)):
    user_projects = [
        project for project in fake_projects_db.values() 
        if project["user_id"] == current_user["id"]
    ]
    return [Project(**project) for project in user_projects]

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: int, current_user: dict = Depends(get_current_user)):
    project = fake_projects_db.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="項目不存在"
        )
    
    if project["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限訪問此項目"
        )
    
    return Project(**project)

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: int, 
    project_update: ProjectUpdate, 
    current_user: dict = Depends(get_current_user)
):
    project = fake_projects_db.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="項目不存在"
        )
    
    if project["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改此項目"
        )
    
    # 更新項目信息
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        project[field] = value
    
    project["updated_at"] = datetime.utcnow()
    fake_projects_db[project_id] = project
    
    return Project(**project)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, current_user: dict = Depends(get_current_user)):
    project = fake_projects_db.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="項目不存在"
        )
    
    if project["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限刪除此項目"
        )
    
    del fake_projects_db[project_id]
    return

