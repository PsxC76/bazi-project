from pydantic import BaseModel, Field
from typing import Optional


class BaziInput(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: Optional[int] = Field(None, ge=0, le=23)
    minute: Optional[int] = Field(None, ge=0, le=59)
    gender: str = Field(..., pattern=r"^(男|女)$")
    is_lunar: bool = False


class Pillar(BaseModel):
    stem: str  # 天干
    branch: str  # 地支
    stem_element: str  # 天干五行
    branch_element: str  # 地支五行
    ten_god: Optional[str] = None  # 十神 (relative to day master)


class BaziResult(BaseModel):
    year_pillar: Pillar
    month_pillar: Pillar
    day_pillar: Pillar
    hour_pillar: Optional[Pillar] = None

    day_master: str  # 日主天干
    day_master_element: str  # 日主五行

    # Ten gods for each position
    year_ten_god: str
    month_ten_god: str
    day_ten_god: str  # 日主本身
    hour_ten_god: Optional[str] = None

    # Major luck periods
    major_luck: list[dict] = []  # [{stem, branch, start_age, end_age, ten_god}]

    # Five elements statistics
    five_elements: dict = {}  # {wood: count, fire: count, earth: count, metal: count, water: count}

    # Hidden stems in branches
    hidden_stems: dict = {}  # {branch: [stems]}
