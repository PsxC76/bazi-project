from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


# Many-to-many relationship between cases and tags
case_tags = Table(
    "case_tags",
    Base.metadata,
    Column("case_id", Integer, ForeignKey("cases.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)  # e.g., "职业", "学历", "婚姻"
    value = Column(String(200), nullable=False)  # e.g., "教师", "本科", "已婚"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # null = system tag
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    cases = relationship("Case", secondary=case_tags, back_populates="tags", lazy="selectin")


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Basic info
    name = Column(String(100), nullable=False, index=True)  # 姓名
    gender = Column(String(10), nullable=False)  # 男/女
    birth_place = Column(String(200), nullable=True)  # 出生地点

    # Birth date (solar calendar)
    birth_year = Column(Integer, nullable=False)
    birth_month = Column(Integer, nullable=False)
    birth_day = Column(Integer, nullable=False)
    birth_hour = Column(Integer, nullable=True)  # 0-23, null if unknown
    birth_minute = Column(Integer, nullable=True)

    # Lunar date (optional)
    lunar_year = Column(Integer, nullable=True)
    lunar_month = Column(Integer, nullable=True)
    lunar_day = Column(Integer, nullable=True)
    is_lunar = Column(Boolean, default=False)  # Whether the input was lunar

    # Bazi result (stored as JSON)
    bazi_result = Column(JSON, nullable=True)  # Stores the full bazi calculation result

    # Verdict / notes
    verdict = Column(Text, nullable=True)  # 断语
    notes = Column(Text, nullable=True)  # 备注

    # Visibility
    is_public = Column(Boolean, default=False)  # Public cases visible to all

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", back_populates="cases", lazy="selectin")
    tags = relationship("Tag", secondary=case_tags, back_populates="cases", lazy="selectin")
