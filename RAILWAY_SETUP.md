# ⚔️ Medieval RPG Bot - راهنمای استقرار روی Railway

## 🚀 راه‌اندازی سریع

### گام 1: آماده‌سازی
1. یک پروژه جدید در Railway ایجاد کنید
2. دیتابیس PostgreSQL اضافه کنید
3. متغیرهای محیط را تنظیم کنید

### گام 2: متغیرهای محیط (Environment Variables)

در پنل Railway، متغیرهای زیر را اضافه کنید:

```
BOT_TOKEN=8535219651:AAHGNL7Mauslv60Bsk73L6AWfi06z_Iwe44
DATABASE_URL=postgresql://user:password@host:port/database
ADMIN_ID=YOUR_ADMIN_ID
```

### گام 3: استقرار

1. مخزن را به Railway متصل کنید
2. Railway به‌طور خودکار کد را استقرار می‌دهد
3. بات شروع به کار می‌کند!

## 📊 ساختار دیتابیس

دیتابیس شامل جداول زیر است:
- `users` - اطلاعات کاربران
- `inventory` - موجودی آیتم‌ها
- `army` - ارتش سربازان
- `battles` - سابقه جنگ‌ها
- `quests` - کوئست‌ها
- `dungeons` - دانجن‌ها
- `rankings` - رنکینگ‌ها

## 🎮 دستورات اصلی

### حساب کاربری
- `/start` - شروع بازی
- `/register` - ثبت‌نام
- `/profile` - نمایش پروفایل

### جنگ و معارکه
- `/solo` - جنگ تک‌نفره
- `/pvp [user_id]` - جنگ با بازیکن دیگر
- `/boss` - جنگ با باس
- `/daily` - کوئست روزانه

### فروشگاه و موجودی
- `/shop` - فروشگاه
- `/shop_units` - خریدن سربازان
- `/shop_items` - خریدن آیتم‌ها
- `/inventory` - نمایش موجودی

### ارتش و قلمرو
- `/army` - مدیریت ارتش
- `/territory` - مدیریت قلمرو

### سیستم
- `/dungeon` - دانجن‌ها
- `/ranking` - رنکینگ جهانی
- `/help` - راهنما

### پنل ادمین
- `/admin` - دسترسی ادمین
- `/admin_stats` - آمار بازی
- `/admin_ban [user_id]` - بن کردن کاربر
- `/admin_give [user_id] [amount]` - دادن طلا
- `/admin_setlevel [user_id] [level]` - تنظیم سطح

## 💰 سیستم اقتصادی

### پاداش‌ها
- جنگ تک‌نفره: 100 طلا + 50 تجربه
- کوئست روزانه: 200 طلا + 100 تجربه
- جنگ PVP (برد): 300 طلا + 150 تجربه
- جنگ باس (برد): 2000 طلا + 1000 تجربه

### سطح‌ها
حداکثر سطح: **100**

## 🔧 توسعه محلی

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# تنظیم متغیرهای محیط
cp .env.example .env
# سپس .env را ویرایش کنید

# اجرای بات
python main.py
```

## 📝 یادداشت‌های مهم

- توکن بات را در `.env` نگه‌دارید و **هرگز** در GitHub آن را commit نکنید
- DATABASE_URL باید یک رشته PostgreSQL معتبر باشد
- ADMIN_ID باید ID تلگرام مدیر ربات باشد

## 🤝 کمک

اگر مشکلی دارید، issues یا pull requests ارسال کنید!

## 📄 لایسنس

MIT License
