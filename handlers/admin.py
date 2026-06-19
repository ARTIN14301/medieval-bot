from aiogram import Router, types
from aiogram.filters import Command
from models.database import SessionLocal, User
from config import EMOJI

router = Router()


@router.message(Command('admin'))
async def admin_command(message: types.Message):
    """پنل ادمین"""
    # بررسی ادمین بودن
    if message.from_user.id != 0:  # تغییر دهید
        await message.answer("شما ادمین نیستید")
        return

    response = f"{EMOJI['crown']} پنل ادمین\n\n"
    response += "/admin_stats - آمار بازی\n"
    response += "/admin_ban [user_id] - بن کردن کاربر\n"
    response += "/admin_give [user_id] [amount] - دادن طلا\n"
    response += "/admin_setlevel [user_id] [level] - تنظیم سطح\n"
    await message.answer(response)


@router.message(Command('admin_stats'))
async def admin_stats_command(message: types.Message):
    """آمار بازی"""
    if message.from_user.id != 0:  # تغییر دهید
        await message.answer("شما ادمین نیستید")
        return

    db = SessionLocal()
    total_users = db.query(User).count()
    total_gold = sum([u.gold for u in db.query(User).all()])
    avg_level = sum([u.level for u in db.query(User).all()]) / max(1, total_users)

    response = f"{EMOJI['crown']} آمار بازی\n\n"
    response += f"کل کاربران: {total_users}\n"
    response += f"کل طلای سیستم: {total_gold} {EMOJI['gold']}\n"
    response += f"میانگین سطح: {avg_level:.1f}\n"
    
    await message.answer(response)
    db.close()


@router.message(Command('admin_ban'))
async def admin_ban_command(message: types.Message):
    """بن کردن کاربر"""
    if message.from_user.id != 0:  # تغییر دهید
        await message.answer("شما ادمین نیستید")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("نحوه استفاده: /admin_ban [user_id]")
        return

    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("شناسه باید عدد باشد")
        return

    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.is_banned = True
        db.commit()
        await message.answer(f"کاربر {user.username} بن شد")
    else:
        await message.answer("کاربر پیدا نشد")
    db.close()


@router.message(Command('admin_give'))
async def admin_give_command(message: types.Message):
    """دادن طلا"""
    if message.from_user.id != 0:  # تغییر دهید
        await message.answer("شما ادمین نیستید")
        return

    args = message.text.split()
    if len(args) < 3:
        await message.answer("نحوه استفاده: /admin_give [user_id] [amount]")
        return

    try:
        user_id = int(args[1])
        amount = int(args[2])
    except ValueError:
        await message.answer("شناسه و مقدار باید عدد باشند")
        return

    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.gold += amount
        db.commit()
        await message.answer(f"{amount} {EMOJI['gold']} به {user.username} داده شد")
    else:
        await message.answer("کاربر پیدا نشد")
    db.close()
