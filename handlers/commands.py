from aiogram import Router, types
from aiogram.filters import Command
from game.engine import GameEngine
from game.ranking import RankingSystem
from config import EMOJI

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message):
    """دستور شروع"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if user:
        response = f"سلام {user.username}! 👑\n\nشما قبلاً ثبت‌نام کرده‌اید!\n"
        response += f"سطح: {user.level} {EMOJI['level']}\n"
        response += f"طلا: {user.gold} {EMOJI['gold']}\n\n"
        response += "دستورات دستیاب:\n"
        response += "/profile - پروفایل شما\n"
        response += "/solo - جنگ تک نفره\n"
        response += "/daily - کوئست روزانه\n"
        response += "/shop - فروشگاه\n"
        response += "/ranking - رنکینگ\n"
    else:
        response = f"خوش‌آمدید {EMOJI['crown']}\n\n"
        response += f"برای شروع بازی، از دستور /register استفاده کنید"

    engine.close()
    await message.answer(response)


@router.message(Command('register'))
async def register_command(message: types.Message):
    """ثبت‌نام کاربر جدید"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if user:
        await message.answer("شما قبلاً ثبت‌نام کرده‌اید!")
    else:
        username = message.from_user.username or f"Player_{message.from_user.id}"
        engine.create_user(message.from_user.id, username)
        response = f"ثبت‌نام موفقیت‌آمیز! {EMOJI['crown']}\n\n"
        response += f"نام کاربری: {username}\n"
        response += f"سطح: 1\n"
        response += f"طلا: 500 {EMOJI['gold']}\n\n"
        response += "دستور /start را بزنید تا شروع کنید!"
        await message.answer(response)

    engine.close()


@router.message(Command('profile'))
async def profile_command(message: types.Message):
    """نمایش پروفایل"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        profile = engine.get_profile(user.user_id)
        response = f"👤 {profile['username']}\n\n"
        response += f"📊 سطح: {profile['level']}\n"
        response += f"✨ تجربه: {profile['experience']}/{profile['next_level_exp']}\n"
        response += f"💰 طلا: {profile['gold']}\n"
        response += f"❤️ سلامت: {profile['health']}/{profile['max_health']}\n"
        response += f"⚔️ حمله: {profile['attack']}\n"
        response += f"🛡️ دفاع: {profile['defense']}\n"
        response += f"🏰 قلمرو: {profile['territory']}\n"
        await message.answer(response)

    engine.close()


@router.message(Command('solo'))
async def solo_fight_command(message: types.Message):
    """جنگ تک نفره"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        result = engine.solo_fight(user.user_id, 'easy')
        if result['success']:
            response = f"⚔️ جنگ تک نفره\n\n"
            response += f"نتیجه: {result['result']} {EMOJI['fire']}\n"
            response += f"✨ تجربه: +{result['exp_gain']}\n"
            response += f"💰 طلا: +{result['gold_gain']}\n"
            response += f"\n📊 سطح: {result['current_level']}\n"
            response += f"💰 کل طلا: {result['current_gold']}\n"
        else:
            response = result['message']
        await message.answer(response)

    engine.close()


@router.message(Command('daily'))
async def daily_quest_command(message: types.Message):
    """کوئست روزانه"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
    else:
        result = engine.daily_quest(user.user_id)
        if result['success']:
            response = f"📜 کوئست روزانه\n\n"
            response += f"✨ تجربه: +{result['exp_gain']}\n"
            response += f"💰 طلا: +{result['gold_gain']}\n"
            response += f"\n📊 سطح: {result['current_level']}\n"
            response += f"💰 کل طلا: {result['current_gold']}\n"
        else:
            response = result['message']
        await message.answer(response)

    engine.close()


@router.message(Command('ranking'))
async def ranking_command(message: types.Message):
    """رنکینگ"""
    ranking_system = RankingSystem()
    ranking_system.update_rankings()

    response = "🏆 رنکینگ جهانی\n\n"

    # رنکینگ ثروت
    response += "💰 رنکینگ ثروت:\n"
    wealth_ranking = ranking_system.get_top_ranking('wealth', 5)
    for rank in wealth_ranking:
        response += f"{rank['position']}. {rank['username']} - {rank['score']} {EMOJI['gold']}\n"

    response += "\n"

    # رنکینگ قدرت
    response += "⚔️ رنکینگ قدرت:\n"
    power_ranking = ranking_system.get_top_ranking('power', 5)
    for rank in power_ranking:
        response += f"{rank['position']}. {rank['username']} - {rank['score']}\n"

    response += "\n"

    # رنکینگ سطح
    response += "📊 رنکینگ سطح:\n"
    level_ranking = ranking_system.get_top_ranking('level', 5)
    for rank in level_ranking:
        response += f"{rank['position']}. {rank['username']} - سطح {rank['score']}\n"

    await message.answer(response)
    ranking_system.close()
