from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, projects, content

app = FastAPI(
    title="NEXAURA API",
    description="基於國產算力平台的智能文檔創作助手 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中應該設置具體的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router, prefix="/api/auth", tags=["認證"])
app.include_router(projects.router, prefix="/api/projects", tags=["項目管理"])
app.include_router(content.router, prefix="/api/content", tags=["內容生成"])

@app.get("/")
async def root():
    return {"message": "歡迎使用 NEXAURA API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

