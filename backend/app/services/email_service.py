"""
邮件发送服务
支持 SMTP（QQ邮箱、163邮箱等）
"""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.user import EmailVerification
from app.core.config import settings


def generate_code(length: int = 6) -> str:
    """生成数字验证码"""
    return ''.join(random.choices(string.digits, k=length))


async def create_verification_code(db: AsyncSession, email: str, purpose: str = "bind") -> str:
    """创建验证码并存入数据库"""
    code = generate_code(6)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # 使旧的未使用验证码失效
    result = await db.execute(
        select(EmailVerification).where(
            and_(
                EmailVerification.email == email,
                EmailVerification.purpose == purpose,
                EmailVerification.is_used == False,
            )
        )
    )
    for old_code in result.scalars().all():
        old_code.is_used = True

    # 创建新验证码
    verification = EmailVerification(
        email=email,
        code=code,
        purpose=purpose,
        expires_at=expires_at,
    )
    db.add(verification)
    await db.flush()

    return code


async def verify_code(db: AsyncSession, email: str, code: str, purpose: str = "bind") -> bool:
    """验证验证码"""
    result = await db.execute(
        select(EmailVerification).where(
            and_(
                EmailVerification.email == email,
                EmailVerification.code == code,
                EmailVerification.purpose == purpose,
                EmailVerification.is_used == False,
                EmailVerification.expires_at > datetime.now(timezone.utc),
            )
        )
    )
    verification = result.scalar_one_or_none()
    if verification:
        verification.is_used = True
        await db.flush()
        return True
    return False


async def send_verification_email(email: str, code: str) -> bool:
    """
    发送验证码邮件
    需要在 .env 中配置 SMTP 设置：
    - SMTP_HOST: SMTP服务器地址（如 smtp.qq.com）
    - SMTP_PORT: SMTP端口（如 465）
    - SMTP_USER: 发信邮箱
    - SMTP_PASSWORD: SMTP授权码（不是邮箱登录密码）
    """
    smtp_host = getattr(settings, "SMTP_HOST", "")
    smtp_port = getattr(settings, "SMTP_PORT", 465)
    smtp_user = getattr(settings, "SMTP_USER", "")
    smtp_password = getattr(settings, "SMTP_PASSWORD", "")

    if not all([smtp_host, smtp_user, smtp_password]):
        print(f"[邮件未配置] 验证码 {code} 发送目标: {email}")
        # 未配置SMTP时，将验证码打印到控制台（开发模式）
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "八字命理案例库 - 邮箱验证码"
        msg["From"] = smtp_user
        msg["To"] = email

        html_content = f"""
        <div style="font-family: 'Microsoft YaHei', sans-serif; max-width: 500px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #16a34a, #22c55e); padding: 20px; border-radius: 12px 12px 0 0; text-align: center;">
                <h2 style="color: white; margin: 0;">八字命理案例库</h2>
            </div>
            <div style="background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 12px 12px;">
                <p style="color: #374151; font-size: 16px;">您好，</p>
                <p style="color: #374151;">您正在进行邮箱绑定操作，验证码为：</p>
                <div style="background: white; border: 2px solid #16a34a; border-radius: 8px; padding: 15px; text-align: center; margin: 20px 0;">
                    <span style="font-size: 32px; font-weight: bold; color: #16a34a; letter-spacing: 8px;">{code}</span>
                </div>
                <p style="color: #6b7280; font-size: 14px;">验证码 10 分钟内有效，请勿泄露给他人。</p>
                <p style="color: #6b7280; font-size: 14px;">如非本人操作，请忽略此邮件。</p>
            </div>
        </div>
        """

        msg.attach(MIMEText(html_content, "html", "utf-8"))

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [email], msg.as_string())

        return True
    except Exception as e:
        print(f"[邮件发送失败] {e}")
        return False
