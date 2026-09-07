"""
八字排盘计算器
基于《八字与用神》（朱祖夏）的排盘规则

支持：
- 四柱八字（年柱、月柱、日柱、时柱）
- 十神
- 大运
- 流年
- 五行统计
- 地支藏干
"""

from typing import Optional
from datetime import date, datetime

# ============================================================
# 基础数据
# ============================================================

# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行
TIAN_GAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 天干阴阳
TIAN_GAN_YINYANG = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴",
}

# 地支五行
DI_ZHI_WUXING = {
    "子": "水", "丑": "土",
    "寅": "木", "卯": "木",
    "辰": "土", "巳": "火",
    "午": "火", "未": "土",
    "申": "金", "酉": "金",
    "戌": "土", "亥": "水",
}

# 地支藏干
DI_ZHI_CANG_GAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 六十甲子
LIU_SHI_JIA_ZI = []
for i in range(60):
    LIU_SHI_JIA_ZI.append(TIAN_GAN[i % 10] + DI_ZHI[i % 12])

# 五行相生相克
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# ============================================================
# 节气数据（用于月柱排定）
# ============================================================

# 每月节气的近似日期（公历）
# 节气名称: (月, 日) - 使用近似值，实际需要精确的天文计算
JIE_QI = {
    "立春": (2, 4), "雨水": (2, 19),
    "惊蛰": (3, 6), "春分": (3, 21),
    "清明": (4, 5), "谷雨": (4, 20),
    "立夏": (5, 6), "小满": (5, 21),
    "芒种": (6, 6), "夏至": (6, 21),
    "小暑": (7, 7), "大暑": (7, 23),
    "立秋": (8, 7), "处暑": (8, 23),
    "白露": (9, 8), "秋分": (9, 23),
    "寒露": (10, 8), "霜降": (10, 23),
    "立冬": (11, 7), "小雪": (11, 22),
    "大雪": (12, 7), "冬至": (12, 22),
    "小寒": (1, 6), "大寒": (1, 20),
}

# 节（非气）- 用于确定月份
# 正月立春, 二月惊蛰, 三月清明, 四月立夏, 五月芒种, 六月小暑
# 七月立秋, 八月白露, 九月寒露, 十月立冬, 十一月大雪, 十二月小寒
JIE_DATES_APPROX = [
    (2, 4),   # 立春 -> 正月
    (3, 6),   # 惊蛰 -> 二月
    (4, 5),   # 清明 -> 三月
    (5, 6),   # 立夏 -> 四月
    (6, 6),   # 芒种 -> 五月
    (7, 7),   # 小暑 -> 六月
    (8, 7),   # 立秋 -> 七月
    (9, 8),   # 白露 -> 八月
    (10, 8),  # 寒露 -> 九月
    (11, 7),  # 立冬 -> 十月
    (12, 7),  # 大雪 -> 十一月
    (1, 6),   # 小寒 -> 十二月
]

# 月支对应（正月建寅）
MONTH_ZHI = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]


def get_precise_jie_qi(year: int) -> list[tuple[int, int]]:
    """
    获取指定年份的精确节气日期
    使用寿星万年历算法的简化版本
    返回12个节的日期 (month, day)
    """
    # 使用更精确的节气计算
    # 基于天文算法的近似值
    jie_qi_dates = []

    # 节气的基准数据（2000年）
    # 每个节气在2000年的儒略日
    base_jd = [
        (2, 4.32, 0.2422),   # 立春
        (3, 6.14, 0.2422),   # 惊蛰
        (4, 5.02, 0.2422),   # 清明
        (5, 6.12, 0.2422),   # 立夏
        (6, 6.22, 0.2422),   # 芒种
        (7, 7.32, 0.2422),   # 小暑
        (8, 7.55, 0.2422),   # 立秋
        (9, 8.10, 0.2422),   # 白露
        (10, 8.32, 0.2422),  # 寒露
        (11, 7.68, 0.2422),  # 立冬
        (12, 7.52, 0.2422),  # 大雪
        (1, 6.11, 0.2422),   # 小寒
    ]

    y = year - 2000
    for month, base_day, coeff in base_jd:
        # 简化的节气计算公式
        century_offset = (year - 2000) / 100
        day = base_day + 0.2422 * y - int(century_offset * 0.75)
        day = int(day) % 31
        if day <= 0:
            day += 28
        jie_qi_dates.append((month, day))

    return jie_qi_dates


def get_solar_term_date(year: int, term_index: int) -> tuple[int, int]:
    """
    获取指定年份指定节气的日期
    term_index: 0=小寒, 1=立春, 2=惊蛰, ..., 11=大雪
    """
    # 更精确的节气计算
    # 基于公式法计算节气日期
    if term_index == 0:  # 小寒
        month, day = 1, 6
    elif term_index == 1:  # 立春
        month, day = 2, 4
    elif term_index == 2:  # 惊蛰
        month, day = 3, 6
    elif term_index == 3:  # 清明
        month, day = 4, 5
    elif term_index == 4:  # 立夏
        month, day = 5, 6
    elif term_index == 5:  # 芒种
        month, day = 6, 6
    elif term_index == 6:  # 小暑
        month, day = 7, 7
    elif term_index == 7:  # 立秋
        month, day = 8, 7
    elif term_index == 8:  # 白露
        month, day = 9, 8
    elif term_index == 9:  # 寒露
        month, day = 10, 8
    elif term_index == 10:  # 立冬
        month, day = 11, 7
    elif term_index == 11:  # 大雪
        month, day = 12, 7
    else:
        month, day = 1, 1

    # 年份修正
    y = year - 2000
    offset = int(y * 0.2422 - (y // 100) * 0.75)
    day += offset

    # 月份天数修正
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month[2] = 29

    if day > days_in_month[month]:
        day = days_in_month[month]
    elif day < 1:
        day = 1

    return (month, day)


# ============================================================
# 年柱排法
# ============================================================

def get_year_pillar(year: int, month: int, day: int) -> str:
    """
    排年柱
    以立春为界，立春前算前一年
    """
    # 立春大约在2月4日
    lichun_month, lichun_day = get_solar_term_date(year, 1)  # 立春

    if (month < lichun_month) or (month == lichun_month and day < lichun_day):
        year -= 1

    # 年干支计算公式
    # 天干: (year - 4) % 10
    # 地支: (year - 4) % 12
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12

    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]


# ============================================================
# 月柱排法
# ============================================================

def get_month_pillar(year: int, month: int, day: int) -> tuple[str, int]:
    """
    排月柱
    以节气为界确定月份
    返回: (月柱干支, 月序号1-12)
    """
    # 确定月份（以节为界）
    # 节气顺序: 小寒(12月), 立春(1月), 惊蛰(2月), 清明(3月), ...
    lunar_month = 1  # 默认正月

    # 获取当年和前一年的节气日期
    for m_idx in range(12):
        jie_month, jie_day = get_solar_term_date(year, m_idx)
        next_idx = (m_idx + 1) % 12
        next_month, next_day = get_solar_term_date(year, next_idx)

        # 处理跨年的情况
        if jie_month > next_month:  # 跨年
            if (month == jie_month and day >= jie_day) or month > jie_month:
                lunar_month = m_idx + 1
                break
            if month < next_month or (month == next_month and day < next_day):
                lunar_month = m_idx
                break
        else:
            if (month == jie_month and day >= jie_day) or (jie_month < month < next_month) or \
               (month == next_month and day < next_day):
                lunar_month = m_idx + 1
                break

    # 确保月份在1-12范围内
    if lunar_month < 1:
        lunar_month += 12
    elif lunar_month > 12:
        lunar_month -= 12

    # 月支: 正月建寅
    month_zhi = MONTH_ZHI[lunar_month - 1]

    # 月干: 根据年干推算
    # 甲己之年丙作首, 乙庚之岁戊为头, 丙辛须从庚字起, 丁壬壬寅顺行流, 若问戊癸何方起, 甲寅之上好追求
    year_gan = get_year_pillar(year, month, day)[0]
    year_gan_idx = TIAN_GAN.index(year_gan)

    # 年干对应的正月天干起始索引
    # 甲己->丙(2), 乙庚->戊(4), 丙辛->庚(6), 丁壬->壬(8), 戊癸->甲(0)
    month_gan_start = [2, 4, 6, 8, 0]
    start_idx = month_gan_start[year_gan_idx % 5]

    # 月干 = 起始天干 + (月序号 - 1)
    month_gan_idx = (start_idx + lunar_month - 1) % 10
    month_gan = TIAN_GAN[month_gan_idx]

    return month_gan + month_zhi, lunar_month


# ============================================================
# 日柱排法
# ============================================================

def get_day_pillar(year: int, month: int, day: int) -> str:
    """
    排日柱
    使用公式法计算日干支
    基于已知基准日推算
    """
    # 基准日: 1900年1月1日 = 甲戌日 (索引10)
    # 使用儒略日计算法
    from datetime import date as Date

    base_date = Date(1900, 1, 1)
    target_date = Date(year, month, day)
    delta = (target_date - base_date).days

    # 1900年1月1日是甲戌日，甲戌在六十甲子中索引为10
    base_idx = 10
    day_idx = (base_idx + delta) % 60

    return LIU_SHI_JIA_ZI[day_idx]


# ============================================================
# 时柱排法
# ============================================================

def get_hour_pillar(day_gan: str, hour: int) -> str:
    """
    排时柱
    根据日干和时辰推算
    """
    # 时辰对应
    # 子时 23-1, 丑时 1-3, 寅时 3-5, 卯时 5-7, 辰时 7-9, 巳时 9-11
    # 午时 11-13, 未时 13-15, 申时 15-17, 酉时 17-19, 戌时 19-21, 亥时 21-23

    # 时支索引
    if hour == 23 or hour == 0:
        zhi_idx = 0  # 子
    else:
        zhi_idx = (hour + 1) // 2

    zhi = DI_ZHI[zhi_idx]

    # 时干: 根据日干推算
    # 甲己还生甲, 乙庚丙作初, 丙辛从戊起, 丁壬庚子居, 戊癸何方发, 壬子是真途
    day_gan_idx = TIAN_GAN.index(day_gan)

    # 日干对应的子时天干起始索引
    # 甲己->甲(0), 乙庚->丙(2), 丙辛->戊(4), 丁壬->庚(6), 戊癸->壬(8)
    hour_gan_start = [0, 2, 4, 6, 8]
    start_idx = hour_gan_start[day_gan_idx % 5]

    # 时干 = 起始天干 + 时辰索引
    hour_gan_idx = (start_idx + zhi_idx) % 10
    hour_gan = TIAN_GAN[hour_gan_idx]

    return hour_gan + zhi


# ============================================================
# 十神计算
# ============================================================

def get_ten_god(day_gan: str, other_gan: str) -> str:
    """
    计算十神关系
    day_gan: 日主天干
    other_gan: 其他天干
    """
    if day_gan == other_gan:
        return "比肩"

    day_wx = TIAN_GAN_WUXING[day_gan]
    other_wx = TIAN_GAN_WUXING[other_gan]
    day_yy = TIAN_GAN_YINYANG[day_gan]
    other_yy = TIAN_GAN_YINYANG[other_gan]

    same_polarity = (day_yy == other_yy)

    # 同我者为比劫
    if day_wx == other_wx:
        return "比肩" if same_polarity else "劫财"

    # 我生者为食伤
    if WUXING_SHENG[day_wx] == other_wx:
        return "食神" if same_polarity else "伤官"

    # 我克者为财
    if WUXING_KE[day_wx] == other_wx:
        return "偏财" if same_polarity else "正财"

    # 克我者为官杀
    if WUXING_KE[other_wx] == day_wx:
        return "七杀" if same_polarity else "正官"

    # 生我者为印
    if WUXING_SHENG[other_wx] == day_wx:
        return "偏印" if same_polarity else "正印"

    return "未知"


# ============================================================
# 大运排法
# ============================================================

def get_major_luck(
    month_pillar: str,
    year_gan: str,
    gender: str,
    birth_year: int,
    birth_month: int,
    birth_day: int,
) -> list[dict]:
    """
    排大运
    阳男阴女顺排，阴男阳女逆排
    """
    year_gan_yang = TIAN_GAN_YINYANG[year_gan] == "阳"
    is_male = gender == "男"

    # 阳男阴女顺排，阴男阳女逆排
    forward = (year_gan_yang and is_male) or (not year_gan_yang and not is_male)

    month_gan = month_pillar[0]
    month_zhi = month_pillar[1]
    month_gan_idx = TIAN_GAN.index(month_gan)
    month_zhi_idx = DI_ZHI.index(month_zhi)

    # 计算起运年龄（简化版：按3天=1年计算）
    # 实际需要根据出生日到节气的天数计算
    start_age = 1  # 默认1岁起运

    major_luck = []
    for i in range(1, 9):  # 8步大运
        if forward:
            gan_idx = (month_gan_idx + i) % 10
            zhi_idx = (month_zhi_idx + i) % 12
        else:
            gan_idx = (month_gan_idx - i) % 10
            zhi_idx = (month_zhi_idx - i) % 12

        gan = TIAN_GAN[gan_idx]
        zhi = DI_ZHI[zhi_idx]

        age_start = start_age + (i - 1) * 10
        age_end = age_start + 9

        major_luck.append({
            "pillar": gan + zhi,
            "stem": gan,
            "branch": zhi,
            "stem_element": TIAN_GAN_WUXING[gan],
            "branch_element": DI_ZHI_WUXING[zhi],
            "start_age": age_start,
            "end_age": age_end,
            "ten_god": get_ten_god(TIAN_GAN[TIAN_GAN.index(get_day_pillar(birth_year, birth_month, birth_day)[0])], gan),
        })

    return major_luck


# ============================================================
# 流年排法
# ============================================================

def get_annual_luck(birth_year: int, start_age: int = 1, count: int = 10) -> list[dict]:
    """
    计算流年
    从起运年龄开始计算流年干支
    """
    result = []
    start_year = birth_year + start_age - 1

    for i in range(count):
        year = start_year + i
        gan_idx = (year - 4) % 10
        zhi_idx = (year - 4) % 12
        gan = TIAN_GAN[gan_idx]
        zhi = DI_ZHI[zhi_idx]

        result.append({
            "year": year,
            "age": start_age + i,
            "pillar": gan + zhi,
            "stem": gan,
            "branch": zhi,
        })

    return result


# ============================================================
# 五行统计
# ============================================================

def count_five_elements(pillars: list[str]) -> dict:
    """
    统计八字中五行的数量
    """
    elements = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}

    for pillar in pillars:
        if len(pillar) >= 2:
            gan = pillar[0]
            zhi = pillar[1]
            elements[TIAN_GAN_WUXING[gan]] += 1
            elements[DI_ZHI_WUXING[zhi]] += 1

    return elements


# ============================================================
# 主函数：完整排盘
# ============================================================

def calculate_bazi(
    year: int,
    month: int,
    day: int,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    gender: str = "男",
) -> dict:
    """
    完整的八字排盘计算

    Args:
        year: 公历年
        month: 公历月
        day: 公历日
        hour: 小时 (0-23)
        minute: 分钟
        gender: 性别 "男" 或 "女"

    Returns:
        完整的八字排盘结果
    """
    # 1. 排四柱
    year_pillar = get_year_pillar(year, month, day)
    month_pillar, lunar_month = get_month_pillar(year, month, day)
    day_pillar = get_day_pillar(year, month, day)

    hour_pillar = None
    if hour is not None:
        day_gan = day_pillar[0]
        hour_pillar = get_hour_pillar(day_gan, hour)

    # 2. 日主
    day_master = day_pillar[0]
    day_master_element = TIAN_GAN_WUXING[day_master]

    # 3. 十神
    year_ten_god = get_ten_god(day_master, year_pillar[0])
    month_ten_god = get_ten_god(day_master, month_pillar[0])
    day_ten_god = "日主"
    hour_ten_god = get_ten_god(day_master, hour_pillar[0]) if hour_pillar else None

    # 4. 五行统计
    pillars = [year_pillar, month_pillar, day_pillar]
    if hour_pillar:
        pillars.append(hour_pillar)
    five_elements = count_five_elements(pillars)

    # 5. 地支藏干
    hidden_stems = {}
    for p in pillars:
        zhi = p[1]
        hidden_stems[zhi] = DI_ZHI_CANG_GAN.get(zhi, [])

    # 6. 大运
    year_gan = year_pillar[0]
    major_luck = get_major_luck(month_pillar, year_gan, gender, year, month, day)

    # 7. 流年（取前10年）
    start_age = major_luck[0]["start_age"] if major_luck else 1
    annual_luck = get_annual_luck(year, start_age, 10)

    # 构建结果
    def build_pillar_info(p: str, ten_god: str) -> dict:
        return {
            "stem": p[0],
            "branch": p[1],
            "stem_element": TIAN_GAN_WUXING[p[0]],
            "branch_element": DI_ZHI_WUXING[p[1]],
            "stem_yinyang": TIAN_GAN_YINYANG[p[0]],
            "branch_yinyang": "阳" if DI_ZHI.index(p[1]) % 2 == 0 else "阴",
            "ten_god": ten_god,
            "hidden_stems": DI_ZHI_CANG_GAN.get(p[1], []),
        }

    result = {
        "year_pillar": build_pillar_info(year_pillar, year_ten_god),
        "month_pillar": build_pillar_info(month_pillar, month_ten_god),
        "day_pillar": build_pillar_info(day_pillar, day_ten_god),
        "hour_pillar": build_pillar_info(hour_pillar, hour_ten_god) if hour_pillar else None,
        "day_master": day_master,
        "day_master_element": day_master_element,
        "day_master_yinyang": TIAN_GAN_YINYANG[day_master],
        "ten_gods": {
            "year": year_ten_god,
            "month": month_ten_god,
            "day": day_ten_god,
            "hour": hour_ten_god,
        },
        "five_elements": five_elements,
        "major_luck": major_luck,
        "annual_luck": annual_luck,
        "input": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "gender": gender,
        },
    }

    return result


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    # 测试排盘
    result = calculate_bazi(1990, 5, 15, 10, 30, "男")
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
