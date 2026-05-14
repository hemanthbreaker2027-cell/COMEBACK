# ANIZONEFLIX - Full Stack Anime Bot & Website

ANIZONEFLIX is a high-end anime repository system featuring a Telegram Bot for content management and a beautiful, responsive FastAPI website for streaming and downloading.

## Features

- **High-End UI:** Glassmorphism design, dark theme, and smooth animations.
- **Dynamic Branding:** LOGO_URL and Name globally controlled via environment variables.
- **Automated Workflow:** Bot fetches metadata from Jikan API and publishes to the website instantly.
- **Admin Controls:** Search, Add, and Delete anime directly from Telegram.
- **Mobile Optimized:** Fully responsive design for mobile users.
- **Production Ready:** Supports Docker, Render, and Railway.

## Directory Structure

```
anizoneflix-repo/
├── bot/                # Bot related utilities
├── web/                # Web related utilities
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, and Images
├── api/                # Jikan API wrapper
├── database/           # MongoDB Motor logic
├── utils/              # Common utilities (slugify, etc.)
├── config/             # Configuration handler
├── requirements.txt    # Dependencies
├── Dockerfile          # Container config
├── docker-compose.yml  # Local stack
├── render.yaml         # Render deployment
├── Procfile            # Platform entry
├── main.py             # Main entry (Bot + Web)
├── bot.py              # Pyrogram Bot logic
├── app.py              # FastAPI Web logic
└── README.md
```

## Setup Guide

### 1. Get Credentials
- **API_ID & API_HASH:** Get from [my.telegram.org](https://my.telegram.org).
- **BOT_TOKEN:** Create via [@BotFather](https://t.me/BotFather).
- **MONGO_URI:** Get from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
- **ADMIN_IDS:** Your Telegram User ID (get from [@userinfobot](https://t.me/userinfobot)).
- **LOGO_URL:** A direct link to your logo image.

### 2. Local Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/anizoneflix.git
cd anizoneflix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat <<EOT >> .env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongo_uri
ADMIN_IDS=12345678,87654321
LOGO_URL=https://your-logo-url.jpg
BASE_URL=http://localhost:8000
EOT

# Run the application
python main.py
```

### 3. Deployment on Render
1. Connect your GitHub repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Select your repository.
4. Render will automatically detect `render.yaml` or you can manually set:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
5. Add all Environment Variables mentioned in Step 2.

## Bot Search Flow
1. Send `/search <anime name>` to the bot.
2. Reply with the number of the correct anime.
3. The bot fetches metadata automatically.
4. Follow the prompts to add Season, 480p, 720p, 1080p, and Batch links.
5. The anime is instantly published to your ANIZONEFLIX website.

## Credits
- **Jikan API** for anime metadata.
- **Pyrogram** for Telegram Bot framework.
- **FastAPI** for high-performance web backend.
