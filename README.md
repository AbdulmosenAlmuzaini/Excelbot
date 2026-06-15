# بوت خبير إكسل المحترف (Excel Expert Telegram Bot)

هذا المشروع عبارة عن بوت تليجرام مدعوم بنموذج الذكاء الاصطناعي `Qwen/Qwen2.5-Coder-32B-Instruct` عبر Hugging Face Router API، ليعمل كخبير محترف في Microsoft Excel لمساعدة المستخدمين في كتابة المعادلات، تنسيق الجداول، تحليل البيانات، وكتابة أكواد VBA و Power Query.

---

## 🛠️ متطلبات التشغيل (Requirements)

1. **Python 3.8 أو أحدث** (مثبت لديك بالفعل الإصدار 3.14)
2. **رمز بوت التليجرام (Telegram Bot Token):** يمكنك الحصول عليه مجاناً بمراسلة [@BotFather](https://t.me/BotFather) وإرسال أمر `/newbot`.
3. **مفتاح الوصول من Hugging Face (Hugging Face Access Token):** (تم توفيره وإعداده بالفعل في المشروع).

---

## 🚀 طريقة الإعداد والتشغيل (Setup & Run)

### 1. إعداد ملف البيئة `.env`
قم بفتح ملف الإعدادات [.env](file:///d:/excel-boot/.env) وضع رمز البوت الخاص بك مكان القيمة الاحتياطية:
```env
TELEGRAM_BOT_TOKEN=ضع_هنا_رمز_البوت_الخاص_بك
HF_TOKEN=ضع_هنا_رمز_Hugging_Face_الخاص_بك
HF_MODEL=Qwen/Qwen2.5-Coder-32B-Instruct
```

### 2. تثبيت المكتبات المطلوبة (إذا لم تكن مثبتة)
افتح سطر الأوامر في مجلد المشروع وقم بتفعيل البيئة الافتراضية وتثبيت الحزم:
```powershell
# تفعيل البيئة الافتراضية
.\venv\Scripts\activate

# تثبيت الحزم (تم بالفعل أثناء البناء)
pip install -r requirements.txt
```

### 3. اختبار التوصيل مع Hugging Face
يمكنك تشغيل ملف الفحص للتأكد من أن مفتاح Hugging Face يعمل بشكل سليم:
```powershell
python check_tokens.py
```

### 4. تشغيل البوت
لتشغيل البوت وجعله جاهزاً لاستقبال الرسائل على تليجرام:
```powershell
python bot.py
```

---

## 💡 أمثلة للاستخدام
بمجرد تشغيل البوت ودخول المستخدمين إليه، يمكنهم إرسال أسئلة مثل:
- *كيف أبحث عن قيمة في جدول آخر بناءً على شرطين؟*
- *أريد كود VBA لدمج عدة خلايا وتغيير لونها للأزرق.*
- *ما هي المعادلة المناسبة لاستخراج الاسم الأول من نص كامل؟*

---

## 📂 هيكل المجلدات (Project Structure)
- [bot.py](file:///d:/excel-boot/bot.py): الملف البرمجي الرئيسي للبوت.
- [check_tokens.py](file:///d:/excel-boot/check_tokens.py): ملف فحص صلاحية رمز Hugging Face والاتصال بالنموذج.
- [.env](file:///d:/excel-boot/.env): ملف تخزين الرموز والمفاتيح السرية.
- [requirements.txt](file:///d:/excel-boot/requirements.txt): ملف المكتبات المطلوبة للتشغيل.
