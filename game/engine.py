import random
from game.balance import EXP_REWARDS, GOLD_REWARDS, COOLDOWNS
from game.units import UNITS
from models.database import SessionLocal, User, Battle, Quest
from datetime import datetime, timedelta


class GameEngine:
    """موتور بازی برای مدیریت تمام منطق بازی"""

    def __init__(self):
        self.db = SessionLocal()

    def get_user(self, telegram_id):
        """دریافت کاربر از دیتابیس"""
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()

    def create_user(self, telegram_id, username):
        """ایجاد کاربر جدید"""
        new_user = User(
            telegram_id=telegram_id,
            username=username,
            level=1,
            experience=0,
            gold=500,
            health=100,
            max_health=100,
            attack=10,
            defense=5
        )
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def solo_fight(self, user_id, difficulty='easy'):
        """جنگ تک نفره"""
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return {'success': False, 'message': 'کاربر پیدا نشد'}

        # شانس برد (بر اساس سطح)
        win_chance = 0.6 + (user.level * 0.01)
        is_win = random.random() < win_chance

        if is_win:
            exp_gain = EXP_REWARDS['solo_fight']
            gold_gain = GOLD_REWARDS['solo_fight']
            user.experience += exp_gain
            user.gold += gold_gain
            result = 'برد'
        else:
            exp_gain = EXP_REWARDS['pvp_lose']
            gold_gain = GOLD_REWARDS['pvp_lose']
            user.experience += exp_gain
            user.gold = max(0, user.gold - 50)  # جریمه باخت
            result = 'باخت'

        # چک سطح بندی
        self._check_level_up(user)
        self.db.commit()

        return {
            'success': True,
            'result': result,
            'exp_gain': exp_gain,
            'gold_gain': gold_gain,
            'current_level': user.level,
            'current_exp': user.experience,
            'current_gold': user.gold
        }

    def pvp_fight(self, attacker_id, defender_id):
        """جنگ بین دو بازیکن"""
        attacker = self.db.query(User).filter(User.user_id == attacker_id).first()
        defender = self.db.query(User).filter(User.user_id == defender_id).first()

        if not attacker or not defender:
            return {'success': False, 'message': 'یک یا هر دو بازیکن پیدا نشدند'}

        # محاسبه شانس برد
        attacker_power = attacker.attack + attacker.level * 2
        defender_power = defender.defense + defender.level * 2

        attacker_win_chance = attacker_power / (attacker_power + defender_power)
        is_attacker_win = random.random() < attacker_win_chance

        if is_attacker_win:
            winner = attacker
            loser = defender
            exp_reward = EXP_REWARDS['pvp_win']
            gold_reward = GOLD_REWARDS['pvp_win']
        else:
            winner = defender
            loser = attacker
            exp_reward = EXP_REWARDS['pvp_lose']
            gold_reward = GOLD_REWARDS['pvp_lose']

        # مکافات برنده
        winner.experience += exp_reward
        winner.gold += gold_reward
        loser.gold = max(0, loser.gold - int(gold_reward / 2))
        loser.health = max(0, loser.health - 20)

        self._check_level_up(winner)
        self._check_level_up(loser)

        # ثبت جنگ
        battle = Battle(
            player1_id=attacker_id,
            player2_id=defender_id,
            winner_id=winner.user_id,
            gold_reward=gold_reward,
            experience_reward=exp_reward,
            battle_type='pvp'
        )
        self.db.add(battle)
        self.db.commit()

        return {
            'success': True,
            'winner': winner.username,
            'loser': loser.username,
            'exp_gain': exp_reward,
            'gold_gain': gold_reward
        }

    def daily_quest(self, user_id):
        """کوئست روزانه"""
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return {'success': False, 'message': 'کاربر پیدا نشد'}

        # چک کول‌داون
        if user.last_daily_quest:
            time_diff = (datetime.utcnow() - user.last_daily_quest).total_seconds()
            if time_diff < COOLDOWNS['daily_quest']:
                remaining = COOLDOWNS['daily_quest'] - time_diff
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                return {
                    'success': False,
                    'message': f'کوئست روزانه در دسترس نیست. {hours}:{minutes} دیگر سعی کنید'
                }

        exp_gain = EXP_REWARDS['daily_quest']
        gold_gain = GOLD_REWARDS['daily_quest']

        user.experience += exp_gain
        user.gold += gold_gain
        user.last_daily_quest = datetime.utcnow()

        self._check_level_up(user)
        self.db.commit()

        return {
            'success': True,
            'exp_gain': exp_gain,
            'gold_gain': gold_gain,
            'current_level': user.level,
            'current_gold': user.gold
        }

    def _check_level_up(self, user):
        """چک سطح بندی"""
        from game.balance import LEVEL_REQUIREMENTS
        while user.level < 100:
            required_exp = LEVEL_REQUIREMENTS[user.level]
            if user.experience >= required_exp:
                user.level += 1
                user.experience -= required_exp
                user.max_health += 10
                user.health = user.max_health
                user.attack += 2
                user.defense += 1
            else:
                break

    def get_profile(self, user_id):
        """دریافت پروفایل کاربر"""
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        from game.balance import LEVEL_REQUIREMENTS
        next_level_exp = LEVEL_REQUIREMENTS.get(user.level, 0)

        return {
            'username': user.username,
            'level': user.level,
            'experience': user.experience,
            'next_level_exp': next_level_exp,
            'gold': user.gold,
            'health': user.health,
            'max_health': user.max_health,
            'attack': user.attack,
            'defense': user.defense,
            'territory': user.territory,
            'territory_gold': user.territory_gold,
            'created_at': user.created_at
        }

    def close(self):
        """بستن اتصال دیتابیس"""
        self.db.close()
