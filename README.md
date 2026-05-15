# 🎬 ANIZONEFLIX - Full Stack Anime Platform

ANIZONEFLIX is a high-performance, professional anime website and Telegram bot system. It allows admins to search for anime metadata via the Jikan API and publish content instantly to a beautiful glassmorphism-themed website.

---

## 🚀 Key Features

- **High-End UI:** Modern dark theme with glassmorphism, trending carousels, and smooth animations.
- **Automated Bot Flow:** Search -> Select -> Details -> Season -> Links -> Publish.
- **Dynamic Branding:** LOGO_URL and Name globally controlled via Environment Variables.
- **SEO Optimized:** Fast loading with clean meta tags for better search visibility.
- **Mobile Responsive:** Fully functional sidebar and navigation on all mobile devices.
- **Production Ready:** Pre-configured for Render, Docker, and Railway.

---

## 🛠 Deployment Guide (Render)

### 1. Obtain Your Credentials

You need the following variables to run the system:

1.  **API_ID & API_HASH:** Get them from [my.telegram.org](https://my.telegram.org).
2.  **BOT_TOKEN:** Create a new bot via [@BotFather](https://t.me/BotFather) on Telegram.
3.  **MONGO_URI:** Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), create a free cluster, and get your connection string.
4.  **ADMIN_IDS:** Your numeric Telegram ID. Get it from [@userinfobot](https://t.me/userinfobot).
5.  **LOGO_URL:** A direct link to your branding logo (e.g., `https://example.com/logo.png`).
6.  **BASE_URL:** Your website URL (e.g., `https://anizoneflix.onrender.com`).

### 2. Deploy to Render

1.  **Fork/Upload:** Ensure this repository is in your GitHub account.
2.  **Create Web Service:** On [Render](https://render.com), click **New +** and select **Web Service**.
3.  **Connect Repo:** Select your `anizoneflix-repo`.
4.  **Runtime:** Select **Docker**.
5.  **Environment Variables:** Add the following:
    - `API_ID`
    - `API_HASH`
    - `BOT_TOKEN`
    - `MONGO_URI`
    - `ADMIN_IDS` (Comma separated if multiple, e.g., `12345,67890`)
    - `LOGO_URL`
    - `BASE_URL`
    - `JIKAN_API` (Set to `https://api.jikan.moe/v4`)
    - `SECRET_KEY` (Any random string)
    - `ADMIN_API_KEY` (Any random string)
6.  **Deploy:** Render will build the Docker image and start both the bot and website automatically.

---

## 🤖 Telegram Bot Usage

Only authorized **Admins** can use the bot.

### Core Commands
- `/start` - Check if bot is alive.
- `/search <name>` - Search for anime and start the adding flow.
- `/categories` - Add or remove website genres.
- `/del <id/url>` - Remove an entry (Paste MAL ID or the Website Link).
- `/help` - View all admin commands.

### The "Adding" Flow
1. Send `/search One Piece`.
2. Pick the correct result by replying with its **number**.
3. The bot fetches full details (Poster, Score, Synopsis).
4. Enter **Season Number**.
5. The bot asks for **480p, 720p, 1080p, and Batch** links. Send the link or click **Skip**.
6. Enter the **YouTube Trailer** link or Skip.
7. **Done!** The anime is now live on your website.

---

## 📁 Repository Structure

```text
anizoneflix-repo/
├── bot/                # Telegram Bot package
│   └── __init__.py     # Core Bot logic & Handlers
├── web/                # Web logic package
├── api/                # Jikan API wrapper
├── database/           # MongoDB Motor integration
├── static/             # Assets (CSS/JS/Images)
├── templates/          # HTML Templates (Jinja2)
├── config/             # Environment configuration
├── main.py             # Entry Point (Runs Bot + Web)
├── bot.py              # Bot proxy entry
├── app.py              # FastAPI app definition
├── Dockerfile          # Container build config
└── render.yaml         # Render blueprint
```

---

## 🔧 Troubleshooting

- **Bot not responding?** Check your `API_ID` and `API_HASH`. Ensure `BOT_TOKEN` is correct.
- **Database error?** Ensure your MongoDB IP Whitelist is set to `0.0.0.0/0` in Atlas.
- **Render Build Failed?** Check the logs for `ImportError`. Ensure the repository structure matches the guide above.

---

**Developed for ANIZONEFLIX.** Built for Anime Fans.
