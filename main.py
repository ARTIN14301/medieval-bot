import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from models.database import init_db
from handlers import commands_router, shop_router, combat_router, admin_router
from config import BOT_TOKEN

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ایجاد بات و دیسپچر
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# اضافه کردن routing
dp.include_router(commands_router)
dp.include_router(shop_router)
dp.include_router(combat_router)
dp.include_router(admin_router)


async def set_commands():
    """تنظیم دستورات بات"""
    commands = [
        BotCommand(command="start", description="شروع بازی"),
        BotCommand(command="register", description="ثبت‌نام کاربر جدید"),
        BotCommand(command="profile", description="نمایش پروفایل"),
        BotCommand(command="solo", description="جنگ تک‌نفره"),
        BotCommand(command="pvp", description="جنگ با بازیکن دیگر"),
        BotCommand(command="boss", description="جنگ با باس"),
        BotCommand(command="daily", description="کوئست روزانه"),
        BotCommand(command="shop", description="فروشگاه"),
        BotCommand(command="inventory", description="موجودی"),
        BotCommand(command="army", description="مدیریت ارتش"),
        BotCommand(command="territory", description="قلمرو"),
        BotCommand(command="dungeon", description="دانجن‌ها"),
        BotCommand(command="ranking", description="رنکینگ جهانی"),
        BotCommand(command="help", description="راهنما"),
        BotCommand(command="admin", description="پنل ادمین")
    ]
    await bot.set_my_commands(commands)


async def main():
    """تابع اصلی"""
    logger.info("🎮 بات Medieval RPG شروع شد...")
    
    # ایجاد دیتابیس
    init_db()
    logger.info("✅ دیتابیس آماده شد")
    
    # تنظیم دستورات
    await set_commands()
    logger.info("✅ دستورات تنظیم شدند")
    
    # شروع polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
