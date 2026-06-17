# config.py
import os
from pyrogram import filters

# --- বটের প্রধান এপিআই ক্রেডেনশিয়ালস ---
API_ID = 29738          # আপনার Telegram API ID (integer)
API_HASH = "297f520a09e80273628c3c24"  # আপনার Telegram API Hash (string)
BOT_TOKEN = "8873890756:AAE49O2dNrE94CN0m9FUce7Om1dmDin9cpE"  # BotFather থেকে পাওয়া টোকেন

# --- এডমিন কনফিগারেশন (মাল্টিপল এডমিন সাপোর্ট) ---
ADMINS = [8932594210, 7120801813]  # উদাহরণ: [8297458824, 12345678, 87654321]

# বটের প্রধান মালিক বা প্রথম এডমিন
ADMIN_ID = ADMINS[0] if ADMINS else None

# এডমিনদের জন্য পাইরোগ্রাম কাস্টম ফিল্টার
is_admin = filters.create(lambda _, __, message: message.from_user and message.from_user.id in ADMINS)

# --- চ্যানেল ও ডাটাবেজ আইডি ---
MAIN_CHANNEL_ID = -1004401594250  # প্রধান মুভি চ্যানেল আইডি (ফাইল ইন্ডেক্স চ্যানেল)
LOG_CHANNEL = -1004312011289      # আপনার রিকোয়েস্ট নোটিফিকেশন বা লগ চ্যানেল আইডি
UPDATE_CHANNEL_ID = -1004430001791 # 👈 আপনার মুভি আপডেট চ্যানেলের আইডি এখানে দিন (যেমন: -100123456789)
TMDB_API_KEY = "7dc544d9253bccc3cfecc1c7f69819" # 👈 themoviedb.org থেকে নেওয়া ফ্রি এপিআই কি এখানে দিন

# --- মাল্টিপল ডাটাবেজ কনফিগারেশন (Multi-DB Config) ---

# ১. ইউজার ডাটাবেজ (এখানে ৪র্থ ডাটাবেজের লিঙ্কটি দেওয়া হলো, এটিতে শুধুমাত্র ইউজাররা সেভ হবে, কোনো মুভি ফাইল সেভ হবে না)
USER_DATABASE_URI = "mongodb+srv://FlixBixs:FlixBixs@cluster0.awkvdsd.mongodb.net/?appName=Cluster0"

# ২. ফাইল বা মুভি ডাটাবেজগুলোর তালিকা (তালিকা থেকে ৪র্থ ডাটাবেজটি বাদ দেওয়া হলো, যাতে এখানে ভুল করেও কোনো ফাইল সেভ না হয়)
FILE_DATABASE_URIS = [
    "mongodb+srv://FlixBixs1:FlixBixs1@cluster0.6fj9062.mongodb.net/?appName=Cluster0", # ১ম ফাইল ডিবি (রিড-অনলি)
    "mongodb+srv://FlixBixs2:FlixBixs2@cluster0.bxn2crn.mongodb.net/?appName=Cluster0", # ২য় ফাইল ডিবি (নতুন ফাইল সেভ হবে)
    "mongodb+srv://FlixBixs3:FlixBixs3@cluster0.3bhietr.mongodb.net/?appName=Cluster0"  # ৩য় ফাইল ডিবি (নতুন ফাইল সেভ হবে)
]

# ৩. প্রতিটি ফাইল ডাটাবেজের সর্বোচ্চ স্টোরেজ লিমিট (আপনার নির্দেশ অনুযায়ী ৩০০ এমবি সেট করা হয়েছে)
DB_LIMIT_MB = 300

# --- আর্নিং ও মিনি অ্যাপ কনফিগারেশন ---
BOT_USERNAME = "FlixBoxsBot"  # বটের ইউজারনেম ( শুরুতে @ দেবেন না)
WEB_URL = "gorgeous-ashla-ctgnahid-3b872c36.koyeb.app"  # Koyeb অ্যাপের লিংক ( শুরুতে https:// দেবেন না)

# আপনার আয়ের ডিরেক্ট অ্যাড লিংকসমূহ (Adsterra এবং OMG10)
DIRECT_AD_LINKS = [
    "https://www.effectivecpmnetwork.com/wsck7gj1?key=2f49c16a80560c9b810503b65da32363",
    "https://www.effectivecpmnetwork.com/iqs1w6v06c?key=19b65cbb2964d6f0a3c934b5ee855f18",
    "https://www.effectivecpmnetwork.com/tpxm5krbv?key=a9a3e08835e93a54ffdaad1597bfe6cb",
    "https://www.effectivecpmnetwork.com/vrstnq7p2s?key=257dbfc9920ae1f06a0a7b33cbeb410d",
    "https://www.effectivecpmnetwork.com/qw8kn1x7h?key=5fdb7c5ecd8aff08f9ffb43334a9d3e6",
    "https://www.effectivecpmnetwork.com/xqmb731x1?key=0267816362fc4320de630e064b317db1",
    "https://omg10.com/4/10357652",
    "https://omg10.com/4/10488925",
    "https://omg10.com/4/10586806"
]

# --- বাটনগুলোর জন্য নিজস্ব প্রমোショナル ও সোশ্যাল লিংকসমূহ ---
CHANNEL_LINK_1 = "https://t.me/FlixBoxs"       # 🍿 All Movies বাটন লিংক
CHANNEL_LINK_2 = "https://t.me/FlixBoxsOfficial"              # 📢 Backup Channel বাটন লিংক

GROUP_LINK = "https://t.me/FlixBoxsChat"           # 💬 Movie Group বাটন লিংক
HOW_TO_USE_LINK = "https://t.me/FlixBoxsDownloadMovies"             # ❓ How to Use বাটন লিংক
DEVELOPER_LINK = "https://t.me/FlixBoxsAdminBot"     # 👨‍💻 Owner & Developer বাটন লিংক

# --- নতুন ভিজ্যুয়াল ডিজাইন কনফিগারেশন ---
START_BANNER = "https://i.postimg.cc/kXP71xdv/IMG-20260617-194252-411.jpg"
