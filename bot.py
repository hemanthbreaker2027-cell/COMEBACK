import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config.config import Config
from api.jikan import jikan
from database.db import db
from utils.utils import slugify

bot = Client(
    "anizoneflix_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Temporary storage for search flow
search_results = {}
user_state = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo=Config.LOGO_URL,
        caption=f"Welcome to **ANIZONEFLIX** Bot!\n\nI can help you add anime to your website.\nUse /search to begin."
    )

@bot.on_message(filters.command("search") & filters.user(Config.ADMIN_IDS))
async def search_cmd(client, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide an anime name. Example: `/search Naruto`")

    msg = await message.reply("Searching...")
    results = await jikan.search_anime(query)

    if not results:
        return await msg.edit("No results found.")

    search_results[message.from_user.id] = results[:8]

    text = "Select the anime by replying with the number:\n\n"
    for i, anime in enumerate(search_results[message.from_user.id], 1):
        text += f"{i}. {anime['title']} ({anime.get('year', 'N/A')})\n"

    await msg.edit(text)
    user_state[message.from_user.id] = {"action": "select_anime"}

@bot.on_message(filters.reply & filters.user(Config.ADMIN_IDS))
async def handle_reply(client, message):
    uid = message.from_user.id
    state = user_state.get(uid)

    if not state:
        return

    if state["action"] == "select_anime":
        try:
            idx = int(message.text) - 1
            if not (0 <= idx < len(search_results[uid])):
                return await message.reply("Invalid selection.")

            selected = search_results[uid][idx]
            mal_id = selected["mal_id"]

            msg = await message.reply("Fetching details...")
            details = await jikan.get_anime_details(mal_id)

            caption = (
                f"**{details['title']}**\n\n"
                f"**Score:** {details.get('score', 'N/A')}\n"
                f"**Episodes:** {details.get('episodes', 'N/A')}\n"
                f"**Status:** {details.get('status', 'N/A')}\n"
                f"**Genres:** {', '.join([g['name'] for g in details.get('genres', [])])}\n\n"
                f"**Synopsis:** {details.get('synopsis', 'N/A')[:500]}..."
            )

            user_state[uid] = {
                "action": "ask_season",
                "anime_data": details
            }

            await message.reply_photo(
                photo=details['images']['jpg']['large_image_url'],
                caption=caption
            )
            await message.reply("Please enter the **Season Number**:")

        except ValueError:
            await message.reply("Please enter a valid number.")

    elif state["action"] == "ask_season":
        user_state[uid]["season"] = message.text
        user_state[uid]["action"] = "ask_480p"
        await message.reply("Enter **480p Download Link** (or /skip):")

    elif state["action"] == "ask_480p":
        user_state[uid]["links_480p"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_720p"
        await message.reply("Enter **720p Download Link** (or /skip):")

    elif state["action"] == "ask_720p":
        user_state[uid]["links_720p"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_1080p"
        await message.reply("Enter **1080p Download Link** (or /skip):")

    elif state["action"] == "ask_1080p":
        user_state[uid]["links_1080p"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_batch"
        await message.reply("Enter **Batch Download Link** (or /skip):")

    elif state["action"] == "ask_batch":
        user_state[uid]["links_batch"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_trailer"
        await message.reply("Enter **Trailer YouTube Link** (or /skip):")

    elif state["action"] == "ask_trailer":
        user_state[uid]["trailer_link"] = message.text if message.text != "/skip" else None

        # Publish
        data = state["anime_data"]
        season = state["season"]
        slug = slugify(f"{data['title']} Season {season}")

        anime_entry = {
            "mal_id": data["mal_id"],
            "title": data["title"],
            "slug": slug,
            "season": season,
            "synopsis": data.get("synopsis"),
            "score": data.get("score"),
            "image": data['images']['jpg']['large_image_url'],
            "genres": [g['name'] for g in data.get('genres', [])],
            "studios": [s['name'] for s in data.get('studios', [])],
            "episodes": data.get("episodes"),
            "rating": data.get("rating"),
            "status": data.get("status"),
            "aired": data.get("aired", {}).get("string"),
            "trailer": state["trailer_link"],
            "links": {
                "480p": state["links_480p"],
                "720p": state["links_720p"],
                "1080p": state["links_1080p"],
                "batch": state["links_batch"]
            }
        }

        await db.add_anime(anime_entry)

        url = f"{Config.BASE_URL}/anime/{slug}"
        await message.reply(
            f"Successfully published **{data['title']} S{season}**!\n\n"
            f"URL: {url}",
            disable_web_page_preview=False
        )
        del user_state[uid]

@bot.on_message(filters.command("cancel") & filters.user(Config.ADMIN_IDS))
async def cancel(client, message):
    if message.from_user.id in user_state:
        del user_state[message.from_user.id]
        await message.reply("Operation cancelled.")
    else:
        await message.reply("Nothing to cancel.")

@bot.on_message(filters.command("del") & filters.user(Config.ADMIN_IDS))
async def delete_anime_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply("Provide MAL ID to delete.")
    mal_id = int(message.command[1])
    await db.delete_anime(mal_id)
    await message.reply("Deleted.")

@bot.on_message(filters.command("add_admin") & filters.user(Config.ADMIN_IDS))
async def add_admin(client, message):
    # This would normally update env or db. For now, just a placeholder as per requirements
    await message.reply("Add the ID to ADMIN_IDS in .env and restart.")

@bot.on_message(filters.command("update_channel") & filters.user(Config.ADMIN_IDS))
async def update_channel(client, message):
    await message.reply("Channel update feature not implemented in this demo.")

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = (
        "**ANIZONEFLIX Bot Commands**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/search <name> - Search and add anime (Admins only)\n"
        "/cancel - Cancel current operation\n"
        "/del <mal_id> - Delete anime (Admins only)\n"
        "/add_admin - Info on adding admins\n"
        "/update_channel - Placeholder for channel updates"
    )
    await message.reply(text)

if __name__ == "__main__":
    bot.run()
