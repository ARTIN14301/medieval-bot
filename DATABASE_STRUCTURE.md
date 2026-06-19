# ساختار دیتابیس و مدل‌های SQLAlchemy

## جداول اصلی

### users (کاربران)
- user_id: شناسه منحصر
- telegram_id: شناسه تلگرام
- username: نام کاربری
- level: سطح فعلی (1-100)
- experience: تجربه جمع‌شده
- gold: مقدار طلا
- health: سلامت فعلی
- max_health: حداکثر سلامت
- attack: قوه حمله
- defense: قوه دفاع
- territory: تعداد قلمرو
- territory_gold: درآمد روزانه قلمرو
- created_at: تاریخ ایجاد
- last_daily_quest: آخرین کوئست روزانه
- is_banned: وضعیت بن

### inventory (موجودی)
- item_id: شناسه منحصر
- user_id: کاربر مالک
- item_name: نام آیتم
- quantity: تعداد
- item_type: نوع (weapon, armor, potion)

### army (ارتش)
- army_id: شناسه منحصر
- user_id: کاربر مالک
- unit_name: نام سرباز
- unit_type: نوع سرباز
- quantity: تعداد
- attack: قوه حمله
- defense: قوه دفاع
- health: سلامت
- cost: هزینه

### battles (جنگ‌ها)
- battle_id: شناسه منحصر
- player1_id: بازیکن اول
- player2_id: بازیکن دوم
- winner_id: برنده
- gold_reward: طلای پاداش
- experience_reward: تجربه پاداش
- battle_type: نوع جنگ (pvp, solo, boss)
- created_at: تاریخ

### quests (کوئست‌ها)
- quest_id: شناسه منحصر
- user_id: کاربر
- quest_name: نام کوئست
- quest_type: نوع (daily, dungeon)
- gold_reward: طلای پاداش
- experience_reward: تجربه پاداش
- is_completed: وضعیت تکمیل
- created_at: تاریخ

### dungeons (دانجن‌ها)
- dungeon_id: شناسه منحصر
- name: نام
- difficulty: سطح سخت (1-5)
- required_level: سطح مورد نیاز
- gold_reward: پاداش طلا
- experience_reward: پاداش تجربه
- boss_health: سلامت بوس
- boss_attack: حمله بوس

### rankings (رتبه‌بندی)
- rank_id: شناسه منحصر
- user_id: کاربر
- rank_type: نوع (wealth, power, level, territory)
- rank_position: موقعیت رتبه‌بندی
- score: امتیاز
- updated_at: زمان به‌روزرسانی

## روابط

- User → Inventory (1:N)
- User → Army (1:N)
- User → Quest (1:N)
- Battle (player1_id, player2_id, winner_id → User)

## نکات مهم

1. تمام زمان‌ها به UTC ذخیره می‌شوند
2. طلا و تجربه مقادیر مثبت هستند
3. سطح‌ها از 1 تا 100 هستند
4. رتبه‌بندی روزانه به‌روزرسانی می‌شود
