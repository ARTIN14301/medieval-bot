from aiogram import Router, types, F
from aiogram.filters import Command
from game.engine import GameEngine
from config import EMOJI
import random

router = Router()


@router.message(Command('pvp'))
async def pvp_command(message: types.Message):
    """جنگ با بازیکن دیگر"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
        engine.close()
        return

    # دریافت شناسه حریف
    args = message.text.split()
    if len(args) < 2:
        await message.answer("نحوه استفاده: /pvp [user_id]")
        engine.close()
        return

    try:
        defender_id = int(args[1])
    except ValueError:
        await message.answer("شناسه باید عدد باشد")
        engine.close()
        return

    result = engine.pvp_fight(user.user_id, defender_id)
    if result['success']:
        response = f"{EMOJI['fire']} جنگ PVP\n\n"
        response += f"برنده: {result['winner']}\n"
        response += f"بازنده: {result['loser']}\n"
        response += f"{EMOJI['exp']} تجربه: +{result['exp_gain']}\n"
        response += f"{EMOJI['gold']} طلا: +{result['gold_gain']}\n"
    else:
        response = result['message']

    await message.answer(response)
    engine.close()


@router.message(Command('boss'))
async def boss_fight_command(message: types.Message):
    """جنگ با باس"""
    engine = GameEngine()
    user = engine.get_user(message.from_user.id)

    if not user:
        await message.answer("ابتدا /register را بزنید")
        engine.close()
        return

    # شبیه‌سازی جنگ با باس
    boss_health = 100 + (user.level * 5)
    player_damage = user.attack
    boss_damage = 5 + (user.level * 0.5)

    # احتمال برد
    win_chance = (user.attack * 2) / (user.attack * 2 + boss_damage)
    is_win = random.random() < win_chance

    if is_win:
        exp_reward = 1000
        gold_reward = 2000
        response = f"{EMOJI['boss']} شکست داده شد!\n\n"
        response += f"{EMOJI['exp']} تجربه: +{exp_reward}\n"
        response += f"{EMOJI['gold']} طلا: +{gold_reward}\n"
        
        user.experience += exp_reward
        user.gold += gold_reward
    else:
        exp_reward = 100
        gold_reward = 0
        response = f"{EMOJI['boss']} باس برد!\n\n"
        response += f"{EMOJI['exp']} تجربه: +{exp_reward}\n"
        response += "این بار شانسی نداشتی 😅\n"
        
        user.experience += exp_reward
        user.health = max(0, user.health - 30)

    engine.db.commit()
    await message.answer(response)
    engine.close()
