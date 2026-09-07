from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    value: str = Field(..., min_length=1, max_length=200)


class TagOut(BaseModel):
    id: int
    name: str
    value: str

    class Config:
        from_attributes = True


class CaseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., pattern=r"^(男|女)$")
    birth_place: Optional[str] = None

    birth_year: int = Field(..., ge=1900, le=2100)
    birth_month: int = Field(..., ge=1, le=12)
    birth_day: int = Field(..., ge=1, le=31)
    birth_hour: Optional[int] = Field(None, ge=0, le=23)
    birth_minute: Optional[int] = Field(None, ge=0, le=59)

    is_lunar: bool = False
    lunar_year: Optional[int] = None
    lunar_month: Optional[int] = None
    lunar_day: Optional[int] = None

    verdict: Optional[str] = None
    notes: Optional[str] = None
    is_public: bool = False

    tags: list[TagCreate] = []


class CaseUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_year: Optional[int] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None
    birth_hour: Optional[int] = None
    birth_minute: Optional[int] = None
    is_lunar: Optional[bool] = None
    verdict: Optional[str] = None
    notes: Optional[str] = None
    is_public: Optional[bool] = None
    tags: Optional[list[TagCreate]] = None


class CaseOut(BaseModel):
    id: int
    user_id: int
    name: str
    gender: str
    birth_place: Optional[str] = None
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: Optional[int] = None
    birth_minute: Optional[int] = None
    is_lunar: bool
    bazi_result: Optional[dict] = None
    verdict: Optional[str] = None
    notes: Optional[str] = None
    is_public: bool
    tags: list[TagOut] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CaseListOut(BaseModel):
    id: int
    name: str
    gender: str
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: Optional[int] = None
    is_lunar: bool
    bazi_result: Optional[dict] = None
    verdict: Optional[str] = None
    tags: list[TagOut] = []
    created_at: datetime

    class Config:
        from_attributes = True


class CaseQuery(BaseModel):
    keyword: Optional[str] = None  # Search by name or verdict
    gender: Optional[str] = None
    tag_filters: list[TagCreate] = []  # Filter by tag name+value
    is_public: Optional[bool] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
