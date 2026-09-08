from fastapi import APIRouter
from app.schemas.bazi import BaziInput, BaziResult
from app.services.bazi_calculator import calculate_bazi

router = APIRouter(prefix="/bazi", tags=["八字排盘"])


@router.post("/calculate", summary="八字排盘计算")
async def calculate(data: BaziInput):
    """
    根据出生日期时间进行八字排盘

    - **year**: 公历年份
    - **month**: 公历月份
    - **day**: 公历日期
    - **hour**: 小时 (0-23)，可选
    - **minute**: 分钟，可选
    - **gender**: 性别 "男" 或 "女"
    - **is_lunar**: 是否为农历日期
    """
    result = calculate_bazi(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        minute=data.minute,
        gender=data.gender,
    )
    return result
