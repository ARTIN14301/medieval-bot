import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///medieval_bot.db')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# پیکربندی Aiogram
AIOGRAM_CONFIG = {
    'timeout': 10,
    'api_url': 'https://api.telegram.org'
}

# تنظیمات بازی
GAME_CONFIG = {
    'max_level': 100,
    'max_gold': 1000000,
    'starting_gold': 500,
    'max_territory': 100
}

# پیام‌های ایموجی
EMOJI = {
    'sword': '⚔️',
    'shield': '🛡️',
    'gold': '💰',
    'exp': '✨',
    'level': '📊',
    'heart': '❤️',
    'fire': '🔥',
    'crown': '👑',
    'territory': '🏰',
    'quest': '📜',
    'dungeon': '🗿',
    'boss': '👹'
}
