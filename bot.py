import os
import sys
import telebot
import requests
from dotenv import load_dotenv

# Reconfigure stdout for Windows console emoji support
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-Coder-32B-Instruct")

# Hugging Face Router endpoint
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

# System prompt for Excel and Google Sheets Expert (in Arabic as requested)
SYSTEM_PROMPT = (
    "أنت خبير إكسل وقوقل شيت محترف. مهمتك مساعدة المستخدمين في كتابة المعادلات المعقدة، تحليل البيانات، وتنسيق الجداول. "
    "عندما يسأل المستخدم عن مهام متكررة أو معقدة، لا تعطِ حلولاً يدوية مملة. ابحث دائماً عن الحلول التي تعتمد على الأتمتة (Automation) "
    "مثل: الدوال المتقدمة (FILTER, QUERY, LAMBDA)، Power Query، Google Apps Script، أو كود VBA. "
    "واشرح الحل بأسلوب: (المشكلة -> الحل الذكي -> الخطوات العملية). "
    "عند إجابتك، قدم المعادلة بوضوح، واشرح الخطوات، وقدم مثالاً إذا لزم الأمر. "
    "افترض دائماً أن المستخدم قد يستخدم إكسل باللغة العربية أو الإنجليزية، واذكر دائماً أن الفاصلة "
    "قد تكون (,) أو (;) حسب إعدادات جهاز المستخدم."
)

if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
    print("❌ ERROR: TELEGRAM_BOT_TOKEN is not configured in the .env file!")
    sys.exit(1)

# Initialize the Telegram Bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك! 👋\n\n"
        "أنا مساعدك الذكي وخبير Microsoft Excel المحترف. 📊\n"
        "مهمتي هي مساعدتك في:\n"
        "🔹 كتابة وشرح المعادلات المعقدة (Formulas)\n"
        "🔹 تحليل البيانات وتنسيق الجداول\n"
        "🔹 كتابة أكواد VBA وماكرو (Macros)\n"
        "🔹 استعلامات Power Query\n\n"
        "اكتب سؤالك أو مشكلتك وسأقوم بمساعدتك فوراً!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "💡 *أمثلة على الأسئلة التي يمكنك طرحها:*\n\n"
        "1️⃣ *المعادلات:* \"كيف أبحث عن قيمة في جدول آخر بناءً على شرطين؟\"\n"
        "2️⃣ *أكواد VBA:* \"أحتاج كود VBA يقوم بنسخ البيانات من ورقة عمل إلى أخرى تلقائياً.\"\n"
        "3️⃣ *تحليل البيانات:* \"كيف يمكنني حساب النسبة المئوية للنمو الشهري للمبيعات؟\"\n"
        "4️⃣ *تنسيق الجداول:* \"كيف أطبق تنسيقاً شرطياً لتظليل الصفوف المكررة؟\"\n\n"
        "اكتب سؤالك مباشرة وسأجيبك بالتفصيل مع الأمثلة!"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    chat_id = message.chat.id

    if not HF_TOKEN:
        bot.reply_to(message, "❌ خطأ: لم يتم تهيئة مفتاح Hugging Face (HF_TOKEN) في ملف الإعدادات.")
        return

    # Send an immediate status message to reassure the user
    status_msg = bot.reply_to(message, "⚡ جاري التفكير ومعالجة طلبك، يرجى الانتظار...")

    # Show typing status
    bot.send_chat_action(chat_id, 'typing')

    # Prepare payload for Hugging Face Router
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 2048,
        "temperature": 0.3 # Low temperature for accurate formulas/code
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            bot_response = data["choices"][0]["message"]["content"]
            
            try:
                # Edit the status message with the final formatted response
                bot.edit_message_text(
                    text=bot_response,
                    chat_id=chat_id,
                    message_id=status_msg.message_id,
                    parse_mode="Markdown"
                )
            except Exception:
                # If Markdown parsing fails, fallback to plain text edit
                bot.edit_message_text(
                    text=bot_response,
                    chat_id=chat_id,
                    message_id=status_msg.message_id
                )
        else:
            print(f"HF API Error: Status {response.status_code}, Body: {response.text}")
            bot.edit_message_text(
                text="⚠️ عذراً، حدث خطأ أثناء الاتصال بنموذج الذكاء الاصطناعي. يرجى المحاولة مرة أخرى لاحقاً.",
                chat_id=chat_id,
                message_id=status_msg.message_id
            )
    except Exception as e:
        print(f"Error handling message: {e}")
        bot.edit_message_text(
            text="❌ حدث خطأ غير متوقع أثناء معالجة طلبك.",
            chat_id=chat_id,
            message_id=status_msg.message_id
        )

if __name__ == "__main__":
    print("🤖 Excel Expert Telegram Bot is starting...")
    print(f"🤖 Connected to Hugging Face Model: {HF_MODEL}")
    print("Press Ctrl+C to stop the bot.")
    bot.infinity_polling()
