# سرباز‌های موجود در بازی

UNITS = {
    'knight': {
        'name': 'شوالیه',
        'attack': 15,
        'defense': 20,
        'health': 50,
        'cost': 100,
        'emoji': '⚔️'
    },
    'archer': {
        'name': 'تیرانداز',
        'attack': 20,
        'defense': 8,
        'health': 30,
        'cost': 80,
        'emoji': '🏹'
    },
    'mage': {
        'name': 'جادوگر',
        'attack': 25,
        'defense': 5,
        'health': 25,
        'cost': 120,
        'emoji': '🔮'
    },
    'barbarian': {
        'name': 'بربر',
        'attack': 30,
        'defense': 10,
        'health': 60,
        'cost': 150,
        'emoji': '🪓'
    },
    'paladin': {
        'name': 'پالادین',
        'attack': 18,
        'defense': 25,
        'health': 70,
        'cost': 200,
        'emoji': '⛪'
    },
    'assassin': {
        'name': 'ترور',
        'attack': 35,
        'defense': 3,
        'health': 20,
        'cost': 180,
        'emoji': '🗡️'
    }
}

DEFAULT_ARMY = [
    {'type': 'knight', 'quantity': 3},
    {'type': 'archer', 'quantity': 2},
    {'type': 'mage', 'quantity': 1}
]

SHOP_ITEMS = {
    'health_potion': {
        'name': 'عصاره سلامتی',
        'type': 'potion',
        'effect': 50,
        'cost': 50,
        'emoji': '🧪'
    },
    'power_potion': {
        'name': 'عصاره قدرت',
        'type': 'potion',
        'effect': 10,
        'cost': 100,
        'emoji': '⚡'
    },
    'armor': {
        'name': 'زره',
        'type': 'armor',
        'effect': 15,
        'cost': 200,
        'emoji': '🛡️'
    }
}
