import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.models.user import User
from app.schemas.user import (
    UserRegister, UserLogin, UserOut, UserUpdate,
    PasswordChange, Token, EmailBindRequest, EmailVerifyRequest,
)
from app.services.email_service import create_verification_code, verify_code, send_verification_email
from app.core.config import settings

router = APIRouter(prefix="/users", tags=["用户"])


@router.post("/register", response_model=Token, summary="用户注册")
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该账号已被注册")

    user = User(
        username=data.username,
        hashed_password=get_password_hash(data.password),
        nickname=data.username,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    token = create_access_token(data={"sub": user.id})
    return Token(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=Token, summary="用户登录")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="账号已被禁用")

    token = create_access_token(data={"sub": user.id})
    return Token(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut, summary="获取当前用户信息")
async def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.put("/me", response_model=UserOut, summary="更新用户信息")
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.nickname is not None:
        current_user.nickname = data.nickname
    if data.bio is not None:
        current_user.bio = data.bio
    await db.flush()
    await db.refresh(current_user)
    return UserOut.model_validate(current_user)


@router.post("/me/password", summary="修改密码")
async def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    current_user.hashed_password = get_password_hash(data.new_password)
    await db.flush()
    return {"message": "密码修改成功"}


@router.post("/me/avatar", response_model=UserOut, summary="上传头像")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    contents = await file.read()
    if len(contents) > settings.MAX_AVATAR_SIZE:
        raise HTTPException(status_code=400, detail="图片大小不能超过2MB")

    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    avatar_dir = os.path.join(settings.UPLOAD_DIR, "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    filepath = os.path.join(avatar_dir, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    current_user.avatar = f"/uploads/avatars/{filename}"
    await db.flush()
    await db.refresh(current_user)
    return UserOut.model_validate(current_user)


# ============================================================
# 邮箱绑定
# ============================================================

@router.post("/me/email/send-code", summary="发送邮箱验证码")
async def send_email_code(
    data: EmailBindRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 检查邮箱是否已被其他用户绑定
    result = await db.execute(select(User).where(User.email == data.email))
    existing = result.scalar_one_or_none()
    if existing and existing.id != current_user.id:
        raise HTTPException(status_code=400, detail="该邮箱已被其他账号绑定")

    # 创建验证码
    code = await create_verification_code(db, data.email, purpose="bind")

    # 发送邮件
    sent = await send_verification_email(data.email, code)
    if not sent:
        raise HTTPException(status_code=500, detail="邮件发送失败，请稍后重试")

    return {"message": "验证码已发送到您的邮箱，10分钟内有效"}


@router.post("/me/email/verify", summary="验证邮箱并绑定")
async def verify_email(
    data: EmailVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 验证验证码
    valid = await verify_code(db, data.email, data.code, purpose="bind")
    if not valid:
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 绑定邮箱
    current_user.email = data.email
    current_user.email_verified = True
    await db.flush()
    await db.refresh(current_user)

    return {"message": "邮箱绑定成功", "email": data.email}


# Admin endpoints
@router.get("/list", response_model=list[UserOut], summary="获取用户列表（管理员）")
async def list_users(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")

    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    )
    return [UserOut.model_validate(u) for u in result.scalars().all()]
