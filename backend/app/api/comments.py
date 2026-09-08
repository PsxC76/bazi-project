from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.case import Case
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentOut
from app.schemas.user import UserOut

router = APIRouter(tags=["评论"])


@router.post("/cases/{case_id}/comments", response_model=CommentOut, summary="创建评论")
async def create_comment(
    case_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建评论（需登录，只能评论公开案例）"""
    # 检查案例是否存在且公开
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")

    if not case.is_public and case.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只能评论公开案例")

    comment = Comment(
        case_id=case_id,
        user_id=current_user.id,
        content=data.content,
    )
    db.add(comment)
    await db.flush()
    await db.refresh(comment)

    return CommentOut(
        id=comment.id,
        case_id=comment.case_id,
        user_id=comment.user_id,
        content=comment.content,
        user=UserOut.model_validate(current_user),
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


@router.get("/cases/{case_id}/comments", response_model=dict, summary="获取案例评论列表")
async def list_case_comments(
    case_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取案例评论列表"""
    # 检查案例是否存在
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")

    # 统计总数
    count_result = await db.execute(
        select(func.count()).where(Comment.case_id == case_id)
    )
    total = count_result.scalar()

    # 查询评论
    result = await db.execute(
        select(Comment)
        .where(Comment.case_id == case_id)
        .order_by(Comment.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    comments = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            CommentOut(
                id=c.id,
                case_id=c.case_id,
                user_id=c.user_id,
                content=c.content,
                user=UserOut.model_validate(c.user) if c.user else None,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in comments
        ],
    }


@router.delete("/comments/{comment_id}", summary="删除评论")
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除评论（本人或管理员）"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    if comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权删除此评论")

    await db.delete(comment)
    await db.flush()
    return {"message": "评论已删除"}


@router.get("/comments/list", response_model=dict, summary="评论列表（管理员）")
async def list_all_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """评论列表（管理员）"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")

    # 统计总数
    count_result = await db.execute(select(func.count()).select_from(Comment))
    total = count_result.scalar()

    # 查询评论
    result = await db.execute(
        select(Comment)
        .order_by(Comment.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    comments = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            CommentOut(
                id=c.id,
                case_id=c.case_id,
                user_id=c.user_id,
                content=c.content,
                user=UserOut.model_validate(c.user) if c.user else None,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in comments
        ],
    }
