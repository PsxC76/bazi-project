from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.case import Case, Tag, case_tags
from app.schemas.case import CaseCreate, CaseUpdate, CaseOut, CaseListOut, TagOut, TagCreate, CaseQuery
from app.services.bazi_calculator import calculate_bazi

router = APIRouter(prefix="/cases", tags=["案例"])


@router.post("", response_model=CaseOut, summary="创建案例")
async def create_case(
    data: CaseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Calculate Bazi
    bazi_result = calculate_bazi(
        year=data.birth_year,
        month=data.birth_month,
        day=data.birth_day,
        hour=data.birth_hour,
        minute=data.birth_minute,
        gender=data.gender,
    )

    # Create case
    case = Case(
        user_id=current_user.id,
        name=data.name,
        gender=data.gender,
        birth_place=data.birth_place,
        birth_year=data.birth_year,
        birth_month=data.birth_month,
        birth_day=data.birth_day,
        birth_hour=data.birth_hour,
        birth_minute=data.birth_minute,
        is_lunar=data.is_lunar,
        lunar_year=data.lunar_year,
        lunar_month=data.lunar_month,
        lunar_day=data.lunar_day,
        bazi_result=bazi_result,
        verdict=data.verdict,
        notes=data.notes,
        is_public=data.is_public,
    )
    db.add(case)
    await db.flush()

    # Handle tags
    for tag_data in data.tags:
        # Find or create tag
        result = await db.execute(
            select(Tag).where(Tag.name == tag_data.name, Tag.value == tag_data.value)
        )
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_data.name, value=tag_data.value, user_id=current_user.id)
            db.add(tag)
            await db.flush()
        case.tags.append(tag)

    await db.flush()
    await db.refresh(case)

    # Convert to output
    return _case_to_out(case)


@router.get("", response_model=dict, summary="获取案例列表")
async def list_cases(
    keyword: Optional[str] = None,
    gender: Optional[str] = None,
    is_public: Optional[bool] = None,
    tag_name: Optional[str] = None,
    tag_value: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Base query: user's own cases + public cases
    query = select(Case).options(selectinload(Case.tags))

    if is_public is True:
        # Only public cases
        query = query.where(Case.is_public == True)
    elif is_public is False:
        # Only own private cases
        query = query.where(Case.user_id == current_user.id, Case.is_public == False)
    else:
        # Own cases + public cases
        query = query.where(or_(Case.user_id == current_user.id, Case.is_public == True))

    # Filters
    if keyword:
        query = query.where(or_(Case.name.contains(keyword), Case.verdict.contains(keyword)))

    if gender:
        query = query.where(Case.gender == gender)

    # Tag filter
    if tag_name and tag_value:
        query = query.join(case_tags).join(Tag).where(
            Tag.name == tag_name, Tag.value.contains(tag_value)
        )

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Paginate
    query = query.order_by(Case.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    cases = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_case_to_list_out(c) for c in cases],
    }


@router.get("/{case_id}", response_model=CaseOut, summary="获取案例详情")
async def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Case).options(selectinload(Case.tags)).where(Case.id == case_id)
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")

    # Check access
    if case.user_id != current_user.id and not case.is_public and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权访问此案例")

    return _case_to_out(case)


@router.put("/{case_id}", response_model=CaseOut, summary="更新案例")
async def update_case(
    case_id: int,
    data: CaseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Case).options(selectinload(Case.tags)).where(Case.id == case_id)
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    if case.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权修改此案例")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    tags_data = update_data.pop("tags", None)

    for field, value in update_data.items():
        setattr(case, field, value)

    # Recalculate bazi if date changed
    date_changed = any(
        update_data.get(f) is not None
        for f in ["birth_year", "birth_month", "birth_day", "birth_hour", "birth_minute", "gender"]
    )
    if date_changed:
        case.bazi_result = calculate_bazi(
            year=case.birth_year,
            month=case.birth_month,
            day=case.birth_day,
            hour=case.birth_hour,
            minute=case.birth_minute,
            gender=case.gender,
        )

    # Update tags
    if tags_data is not None:
        case.tags.clear()
        for tag_data in tags_data:
            tag_result = await db.execute(
                select(Tag).where(Tag.name == tag_data["name"], Tag.value == tag_data["value"])
            )
            tag = tag_result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_data["name"], value=tag_data["value"], user_id=current_user.id)
                db.add(tag)
                await db.flush()
            case.tags.append(tag)

    await db.flush()
    await db.refresh(case)
    return _case_to_out(case)


@router.delete("/{case_id}", summary="删除案例")
async def delete_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    if case.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权删除此案例")

    await db.delete(case)
    await db.flush()
    return {"message": "案例已删除"}


@router.post("/{case_id}/recalculate", response_model=CaseOut, summary="重新计算八字")
async def recalculate_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Case).options(selectinload(Case.tags)).where(Case.id == case_id)
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    if case.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权操作此案例")

    case.bazi_result = calculate_bazi(
        year=case.birth_year,
        month=case.birth_month,
        day=case.birth_day,
        hour=case.birth_hour,
        minute=case.birth_minute,
        gender=case.gender,
    )
    await db.flush()
    await db.refresh(case)
    return _case_to_out(case)


# ============================================================
# Tag endpoints
# ============================================================

@router.get("/tags/list", response_model=list[TagOut], summary="获取标签列表")
async def list_tags(
    name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Tag).distinct()
    if name:
        query = query.where(Tag.name.contains(name))
    query = query.order_by(Tag.name, Tag.value).limit(100)
    result = await db.execute(query)
    return [TagOut.model_validate(t) for t in result.scalars().all()]


@router.get("/tags/names", response_model=list[str], summary="获取所有标签名称")
async def list_tag_names(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Tag.name).distinct().order_by(Tag.name))
    return [row[0] for row in result.all()]


# ============================================================
# Helper functions
# ============================================================

def _case_to_out(case: Case) -> dict:
    return CaseOut(
        id=case.id,
        user_id=case.user_id,
        name=case.name,
        gender=case.gender,
        birth_place=case.birth_place,
        birth_year=case.birth_year,
        birth_month=case.birth_month,
        birth_day=case.birth_day,
        birth_hour=case.birth_hour,
        birth_minute=case.birth_minute,
        is_lunar=case.is_lunar,
        bazi_result=case.bazi_result,
        verdict=case.verdict,
        notes=case.notes,
        is_public=case.is_public,
        tags=[TagOut.model_validate(t) for t in case.tags],
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


def _case_to_list_out(case: Case) -> dict:
    return CaseListOut(
        id=case.id,
        name=case.name,
        gender=case.gender,
        birth_year=case.birth_year,
        birth_month=case.birth_month,
        birth_day=case.birth_day,
        birth_hour=case.birth_hour,
        is_lunar=case.is_lunar,
        bazi_result=case.bazi_result,
        verdict=case.verdict,
        tags=[TagOut.model_validate(t) for t in case.tags],
        created_at=case.created_at,
    )
