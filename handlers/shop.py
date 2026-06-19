from aiogram import Router, types
from aiogram.filters import Command
from game.engine import GameEngine
from game.units import UNITS, SHOP_ITEMS
from models.database import SessionLocal, User, Army
from config import EMOJI

router = Router()


@router.message(Command('shop'))
async def shop_command(message: types.Message):
    """فروشگاه"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        response = f"{EMOJI['gold']} فروشگاه\n\n"
        response += "انتخاب کنید:\n"
        response += "/shop_units - خریدن سربازان\n"
        response += "/shop_items - خریدن آیتم‌ها\n"
        response += f"\nطلای شما: {user.gold} {EMOJI['gold']}\n"
        await message.answer(response)

    engine.close()


@router.message(Command('shop_units'))
async def shop_units_command(message: types.Message):
    """خریدن سربازان"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        response = f"{EMOJI['sword']} خریدن سربازان\n\n"
        for unit_key, unit_info in UNITS.items():
            response += f"{unit_info['emoji']} {unit_info['name']}\n"
            response += f"  قیمت: {unit_info['cost']} {EMOJI['gold']}\n"
            response += f"  حمله: {unit_info['attack']} | دفاع: {unit_info['defense']} | سلامت: {unit_info['health']}\n\n"
        await message.answer(response)

    engine.close()


@router.message(Command('shop_items'))
async def shop_items_command(message: types.Message):
    """خریدن آیتم‌ها"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        response = f"{EMOJI['gold']} خریدن آیتم‌ها\n\n"
        for item_key, item_info in SHOP_ITEMS.items():
            response += f"{item_info['emoji']} {item_info['name']}\n"
            response += f"  قیمت: {item_info['cost']} {EMOJI['gold']}\n"
            response += f"  اثر: +{item_info['effect']}\n\n"
        await message.answer(response)

    engine.close()


@router.message(Command('inventory'))
async def inventory_command(message: types.Message):
    """نمایش موجودی"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        db = SessionLocal()
        inventory = db.query(User).filter(User.user_id == user.user_id).first()
        army = db.query(Army).filter(Army.user_id == user.user_id).all()

        response = f"{EMOJI['sword']} موجودی\n\n"
        
        if not army:
            response += "ارتشی ندارید.\n"
        else:
            response += "سربازان:\n"
            for unit in army:
                unit_info = UNITS.get(unit.unit_type, {})
                response += f"{unit_info.get('emoji', '⚔️')} {unit.unit_name}: {unit.quantity} نفر\n"
        
        await message.answer(response)
        db.close()

    engine.close()


@router.message(Command('army'))
async def army_command(message: types.Message):
    """مدیریت ارتش"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        response = f"{EMOJI['sword']} مدیریت ارتش\n\n"
        response += "انتخاب کنید:\n"
        response += "/army_default - استفاده از ارتش پیش‌فرض\n"
        response += "/army_custom - ساخت ارتش خودم\n"
        response += "/army_view - نمایش ارتش فعلی\n"
        await message.answer(response)

    engine.close()


@router.message(Command('territory'))
async def territory_command(message: types.Message):
    """مدیریت قلمرو"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        response = f"{EMOJI['territory']} قلمروی شما\n\n"
        response += f"قلمرو: {user.territory}\n"
        response += f"درآمد مالیات: {user.territory_gold} {EMOJI['gold']}\n\n"
        response += "انتخاب کنید:\n"
        response += "/territory_conquer - فتح قلمرو جدید\n"
        response += "/territory_tax - جمع‌آوری مالیات\n"
        await message.answer(response)

    engine.close()


@router.message(Command('dungeon'))
async def dungeon_command(message: types.Message):
    """داخل دانجن رفتن"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        response = f"{EMOJI['dungeon']} دانجن‌ها\n\n"
        response += "سطح سختی:\n"
        response += f"/dungeon_easy - آسان (سطح 1-10)\n"
        response += f"/dungeon_medium - متوسط (سطح 20-40)\n"
        response += f"/dungeon_hard - سخت (سطح 50-70)\n"
        response += f"/dungeon_nightmare - کابوس (سطح 80+)\n"
        await message.answer(response)

    engine.close()


@router.message(Command('help'))
async def help_command(message: types.Message):
    """راهنما"""
    response = f"{EMOJI['crown']} دستورات دستیاب:\n\n"
    response += f"/start - شروع بازی\n"
    response += f"/register - ثبت‌نام\n"
    response += f"/profile - پروفایل شما\n"
    response += f"/solo - جنگ تک‌نفره\n"
    response += f"/daily - کوئست روزانه\n"
    response += f"/shop - فروشگاه\n"
    response += f"/inventory - موجودی\n"
    response += f"/army - مدیریت ارتش\n"
    response += f"/territory - قلمرو\n"
    response += f"/dungeon - دانجن‌ها\n"
    response += f"/ranking - رنکینگ\n"
    response += f"/help - این پیام\n"
    await message.answer(response)
