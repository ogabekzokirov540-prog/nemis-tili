# 🇩🇪 GermanMaster AI

**Nemis tilini o'rganish uchun shaxsiy AI-platforma**

---

## 📋 Loyiha haqida

GermanMaster AI — bu nemis tilini mustaqil o'rganish uchun mo'ljallangan to'liq funksional web-platforma. U multimedia kutubxonasi, interaktiv flashcardlar, aqlli eslatmalar tizimi va progress tracker'ni o'z ichiga oladi.

## 🚀 Xususiyatlar

### Asosiy modullar:
- **📊 Dashboard** — Umumiy statistika, kunlik streak, tezkor harakatlar
- **📚 Darslar (Study Room)** — Split-screen: video/PDF/audio + interaktiv lug'at paneli
- **📝 Lug'at** — Nemischa-o'zbekcha lug'at, rasm va audio bilan
- **🃏 Flashcards (SRS)** — Anki usulida SM-2 algoritmi bilan takrorlash
- **📓 Eslatmalar** — Markdown qo'llab-quvvatlovchi smart notes
- **📁 Media Kutubxona** — PDF viewer, video/audio player
- **📈 Progress Tracker** — Grafiklar, streak, statistika
- **🤖 AI Asboblar** — Tarjima, kontekst qidirish

### Texnik xususiyatlar:
- ✅ Dark Mode (qorong'u rejim)
- ✅ Responsive dizayn (mobil qurilmalarga moslashgan)
- ✅ PDF.js bilan PDF ko'rish
- ✅ SM-2 Spaced Repetition algoritmi
- ✅ Keyboard shortcuts (Ctrl+K, Space, 1-4)
- ✅ Chart.js bilan progress grafiklari
- ✅ Django Admin panel (kontent boshqaruvi)
- ✅ AJAX-based interaktiv UI
- ✅ Browser TTS (Text-to-Speech) nemischa talaffuz

## 🛠 Texnologiyalar

| Texnologiya | Maqsad |
|---|---|
| **Django 4.2+** | Backend framework |
| **SQLite** | Ma'lumotlar bazasi (development) |
| **Tailwind CSS** | Frontend dizayn |
| **Chart.js** | Progress grafiklari |
| **PDF.js** | PDF viewer |
| **JavaScript** | Interaktiv UI |

## ⚙️ O'rnatish (Linux)

```bash
# 1. Repositoriyani klonlash
git clone https://github.com/YOUR_USERNAME/nemis-tili.git
cd nemis-tili

# 2. Virtual environment yaratish
python3 -m venv venv
source venv/bin/activate

# 3. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 4. Ma'lumotlar bazasini yaratish
python manage.py makemigrations lessons vocabulary media flashcards notes progress ai_features
python manage.py migrate

# 5. Admin foydalanuvchi yaratish
python manage.py createsuperuser

# 6. Serverni ishga tushirish
python manage.py runserver

# 7. Brauzerda ochish
# http://127.0.0.1:8000/ — Bosh sahifa
# http://127.0.0.1:8000/admin/ — Admin panel
```

## 📁 Loyiha tuzilishi

```
nemis-tili/
├── germanmaster/          # Django loyiha konfiguratsiyasi
│   ├── settings.py        # Sozlamalar
│   ├── urls.py            # URL marshrutlash
│   ├── lessons/           # Darslar app
│   ├── vocabulary/        # Lug'at app
│   ├── flashcards/        # Flashcards + SRS app
│   ├── media/             # Multimedia kutubxona app
│   ├── notes/             # Eslatmalar app
│   ├── progress/          # Progress tracker app
│   ├── dashboard/         # Dashboard app
│   └── ai_features/       # AI xususiyatlar app
├── templates/             # HTML templatelar
├── static/                # CSS, JS, rasmlar
├── media/                 # Yuklangan fayllar (gitignore)
├── manage.py              # Django CLI
└── requirements.txt       # Python kutubxonalar
```

## 🎯 Foydalanish

### Admin paneldan kontent qo'shish:
1. `/admin/` sahifasiga kiring
2. Kategoriyalar yarating (Grammatika, Lug'at, Tinglash...)
3. Darslar qo'shing (PDF, video, audio biriktirib)
4. So'zlarni qo'shing (rasm, audio talaffuz bilan)
5. Flashcard to'plamlar yarating

### O'rganish jarayoni:
1. Dashboard'dan boshlang
2. Darsni oching (Study Room)
3. So'zlarni o'rganing
4. Flashcard bilan mustahkamlang
5. Progress'ni kuzating

## 🔑 AI funksiyalar sozlash (ixtiyoriy)

```bash
# .env faylida yoki environment variable sifatida:
export DEEPL_API_KEY="your-deepl-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## 📱 Keyboard Shortcuts

| Tugma | Funksiya |
|---|---|
| `Ctrl+K` | Global qidirish |
| `Space` / `Enter` | Flashcard'ni aylantirish |
| `1` | Bilmadim (SRS reset) |
| `2` | Qiyin |
| `3` | Yaxshi |
| `4` | Oson |

---

**Muallif:** GermanMaster AI Team  
**Litsenziya:** MIT
