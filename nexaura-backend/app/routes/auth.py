from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from app.services.supabase_client import supabase
from gotrue.errors import AuthApiError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Pydantic Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Dependency to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # get_user validates the JWT and returns the user or raises an error
        response = supabase.auth.get_user(token)
        user = response.user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except AuthApiError as e:
        raise HTTPException(status_code=e.status, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=dict)
async def register(user: UserRegister):
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        if res.user:
            return {"message": "注册成功，请检查您的邮箱以完成验证", "user_id": res.user.id}
        elif res.session:
            return {"message": "注册并登录成功", "session": res.session}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="注册失败，请稍后重试"
            )
    except Exception as e:
        error_message = str(e)
        if "User already registered" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {error_message}"
        )

@router.post("/login", response_model=dict)
async def login(user: UserLogin):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return res.model_dump()
    except Exception as e:
        error_message = str(e)
        if "Invalid login credentials" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {error_message}"
        )

