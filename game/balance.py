# توازن اقتصادی بازی

# پاداش تجربه
EXP_REWARDS = {
    'solo_fight': 50,
    'daily_quest': 100,
    'dungeon_easy': 200,
    'dungeon_medium': 400,
    'dungeon_hard': 800,
    'boss_fight': 1000,
    'pvp_win': 150,
    'pvp_lose': 50
}

# پاداش طلا
GOLD_REWARDS = {
    'solo_fight': 100,
    'daily_quest': 200,
    'dungeon_easy': 300,
    'dungeon_medium': 600,
    'dungeon_hard': 1200,
    'boss_fight': 2000,
    'pvp_win': 300,
    'pvp_lose': 50,
    'territory_tax': 0.1  # ۱۰ درصد مالیات روزانه
}

# سطح‌ها و XP مورد نیاز
LEVEL_REQUIREMENTS = {
    i: 100 * (2 ** (i-1)) for i in range(1, 101)
}

# ضریب سختی
DIFFICULTY_MULTIPLIER = {
    'easy': 1.0,
    'medium': 1.5,
    'hard': 2.5,
    'nightmare': 4.0
}

# حداکثر و حداقل طلا
MIN_GOLD = 0
MAX_GOLD = 1000000
STARTING_GOLD = 500

# کولداون (ثانیه)
COOLDOWNS = {
    'solo_fight': 300,  # 5 دقیقه
    'pvp_fight': 600,   # 10 دقیقه
    'daily_quest': 86400,  # 24 ساعت
    'dungeon': 1800     # 30 دقیقه
}
