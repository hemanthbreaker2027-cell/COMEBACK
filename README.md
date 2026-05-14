# ANIZONEFLIX (Alpha v1.0) - Full Stack Anime Bot & Website

ANIZONEFLIX is a high-end anime repository system featuring a Telegram Bot for content management and a beautiful, responsive FastAPI website for streaming and downloading.

## 🚀 Alpha Version v1.0 Features

- **High-End UI:** Glassmorphism design, dark theme, and smooth animations.
- **Dynamic Branding:** LOGO_URL and Name globally controlled via environment variables.
- **Automated Workflow:** Bot fetches metadata from Jikan API and publishes to the website instantly.
- **Category Management:** Manage website categories directly via the bot.
- **Admin Controls:** Search, Add, Delete, and Categorize anime from Telegram.
- **Mobile Optimized:** Fully responsive design with functional mobile navigation.
- **Production Ready:** Supports Docker, Render, and Railway.

---

## 🛠 Setup Guide

### 1. Get Credentials
- **API_ID & API_HASH:** Get from [my.telegram.org](https://my.telegram.org).
- **BOT_TOKEN:** Create via [@BotFather](https://t.me/BotFather).
- **MONGO_URI:** Get from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
- **ADMIN_IDS:** Your Telegram User ID (get from [@userinfobot](https://t.me/userinfobot)).
- **LOGO_URL:** A direct link to your logo image.

### 2. Deployment on Render
1. Connect your GitHub repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Select your repository.
4. Render will automatically detect `render.yaml`.
5. Add all Environment Variables mentioned above.

---

## 🤖 Bot Usage & Guide

### Commands
- `/start` - Start the bot.
- `/help` - Show command list.
- `/search <name>` - Search for anime on Jikan API and start the upload flow.
- `/categories` - Manage website categories (Add/Remove).
- `/del <mal_id>` - Delete an anime from the database.
- `/cancel` - Stop the current operation.

### How to Add a Post (Anime)
1. Send `/search Naruto` (or any anime name).
2. The bot will show a numbered list. **Reply with the number** of the correct anime.
3. The bot will fetch and show the poster and synopsis.
4. **Step 1:** Enter the **Season Number** (e.g., `1`).
5. **Step 2:** Enter the **480p Download Link** or send `/skip`.
6. **Step 3:** Enter the **720p Download Link** or send `/skip`.
7. **Step 4:** Enter the **1080p Download Link** or send `/skip`.
8. **Step 5:** Enter the **Batch Download Link** or send `/skip`.
9. **Step 6:** Enter the **YouTube Trailer Link** or send `/skip`.
10. The bot will automatically generate the slug, save to MongoDB, and provide the live website URL.

### How to Manage Categories
1. Send `/categories`.
2. Click **➕ Add Category**.
3. Send the name of the category (e.g., `Action`).
4. To remove, click **➖ Remove Category** and select the name from the list.

---

## 🌐 Website Navigation

- **Home:** Main landing page with Trending and Recent sections.
- **Categories:** Hover over "Categories" in the navbar to see available genres. On mobile, open the menu (bars icon) to see them.
- **Search:** Use the search bar in the header to find anime stored in your database.
- **Details Page:** Each anime has its own page with synopsis, metadata, download buttons, and an embedded trailer.

---

## 📁 Directory Structure

```
anizoneflix-repo/
├── bot.py              # Pyrogram Bot logic (Search & Category flow)
├── app.py              # FastAPI Web logic & Routes
├── main.py             # Unified Entry point (Bot + Web)
├── api/                # Jikan API Wrapper
├── database/           # MongoDB Motor logic
├── templates/          # HTML Templates (Jinja2)
├── static/             # Assets (CSS/JS/Img)
├── utils/              # Helper functions
├── config/             # Configuration handler
├── requirements.txt    # Python dependencies
├── Dockerfile          # Containerization
└── render.yaml         # Render deployment config
```

## Credits
- **Jikan API** for metadata.
- **Pyrogram** for bot framework.
- **FastAPI** for web backend.
