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
        caption=f"Hi {message.from_user.first_name}!\n\nI am the **ANIZONEFLIX** Management Bot. Use /help to see what I can do."
    )

async def is_authorized(user_id):
    return user_id in Config.ADMIN_IDS or await db.is_admin(user_id)

@bot.on_message(filters.command(["search", "add_post"]))
async def search_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
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

@bot.on_message((filters.reply | filters.text))
async def handle_reply(client, message):
    if not message.text: return
    if not await is_authorized(message.from_user.id): return
    if message.text.startswith("/") and message.text != "/skip": return
    uid = message.from_user.id
    state = user_state.get(uid)

    if not state:
        return

    if state["action"] == "add_category_name":
        await db.add_category(message.text)
        await message.reply(f"Category **{message.text}** added successfully!")
        del user_state[uid]
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
        await message.reply("Enter **480p Download Link**:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_480p")]]))

    elif state["action"] == "ask_480p":
        user_state[uid]["links_480p"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_720p"
        await message.reply("Enter **720p Download Link**:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_720p")]]))

    elif state["action"] == "ask_720p":
        user_state[uid]["links_720p"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_1080p"
        await message.reply("Enter **1080p Download Link**:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_1080p")]]))

    elif state["action"] == "ask_1080p":
        user_state[uid]["links_1080p"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_batch"
        await message.reply("Enter **Batch Download Link**:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_batch")]]))

    elif state["action"] == "ask_batch":
        user_state[uid]["links_batch"] = message.text if message.text != "/skip" else None
        user_state[uid]["action"] = "ask_trailer"
        await message.reply("Enter **Trailer YouTube Link**:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_trailer")]]))

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

@bot.on_message(filters.command("cancel"))
async def cancel(client, message):
    if not await is_authorized(message.from_user.id): return
    if message.from_user.id in user_state:
        del user_state[message.from_user.id]
        await message.reply("Operation cancelled.")
    else:
        await message.reply("Nothing to cancel.")

@bot.on_message(filters.command("del"))
async def delete_anime_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
    if len(message.command) < 2:
        return await message.reply("Provide MAL ID or Website URL to delete.")

    input_data = message.command[1]
    if "/anime/" in input_data:
        slug = input_data.split("/anime/")[1].split("?")[0]
        await db.delete_anime_by_slug(slug)
        await message.reply(f"Deleted anime with slug: {slug}")
    else:
        try:
            mal_id = int(input_data)
            await db.delete_anime(mal_id)
            await message.reply(f"Deleted anime with MAL ID: {mal_id}")
        except ValueError:
            await message.reply("Invalid input. Provide MAL ID or full anime URL.")

@bot.on_message(filters.command("add_admin"))
async def add_admin_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
    if len(message.command) < 2:
        return await message.reply("Provide User ID to add as admin.")
    try:
        user_id = int(message.command[1])
        await db.add_admin(user_id)
        await message.reply(f"User {user_id} added as admin in database.")
    except ValueError:
        await message.reply("Invalid User ID.")

@bot.on_message(filters.command("update_channel"))
async def update_channel(client, message):
    if not await is_authorized(message.from_user.id): return
    await message.reply("Channel update feature not implemented in this demo.")

@bot.on_message(filters.command("categories"))
async def categories_cmd(client, message):
    if not await is_authorized(message.from_user.id): return
    categories = await db.get_all_categories()
    text = "**Current Categories:**\n\n"
    for cat in categories:
        text += f"• {cat['name']}\n"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add Category", callback_data="add_cat"),
            InlineKeyboardButton("➖ Remove Category", callback_data="del_cat")
        ]
    ])
    await message.reply(text, reply_markup=keyboard)

@bot.on_callback_query(filters.regex("^add_cat$"))
async def add_cat_cb(client, callback_query):
    if not await is_authorized(callback_query.from_user.id): return
    await callback_query.message.edit("Please send the **name** of the new category:")
    user_state[callback_query.from_user.id] = {"action": "add_category_name"}

@bot.on_callback_query(filters.regex("^del_cat$"))
async def del_cat_cb(client, callback_query):
    if not await is_authorized(callback_query.from_user.id): return
    categories = await db.get_all_categories()
    if not categories:
        return await callback_query.answer("No categories to delete.", show_alert=True)

    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(cat['name'], callback_data=f"remove_cat_{cat['name']}")])

    await callback_query.message.edit("Select category to remove:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex("^remove_cat_"))
async def remove_cat_confirm(client, callback_query):
    if not await is_authorized(callback_query.from_user.id): return
    cat_name = callback_query.data.split("remove_cat_")[1]
    await db.delete_category(cat_name)
    await callback_query.answer(f"Removed {cat_name}", show_alert=True)
    await categories_cmd(client, callback_query.message)

@bot.on_callback_query(filters.regex("^skip_"))
async def skip_callback(client, callback_query):
    if not await is_authorized(callback_query.from_user.id): return
    uid = callback_query.from_user.id
    state = user_state.get(uid)
    if not state: return

    action = callback_query.data.split("skip_")[1]

    # Mock a /skip message
    class MockMessage:
        def __init__(self, uid, text):
            self.from_user = type('obj', (object,), {'id': uid})
            self.text = text
        async def reply(self, text, reply_markup=None):
            return await bot.send_message(uid, text, reply_markup=reply_markup)

    await handle_reply(client, MockMessage(uid, "/skip"))
    await callback_query.answer()

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = (
        "**ANIZONEFLIX (Alpha v1.0) Bot Commands**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/search <name> - Search and add anime (Admins only)\n"
        "/add_post <name> - Alias for /search\n"
        "/categories - Manage categories (Admins only)\n"
        "/cancel - Cancel current operation\n"
        "/del <mal_id/url> - Delete anime from website (Admins only)\n"
        "/add_admin <id> - Add new admin to database (Admins only)\n"
        "/update_channel - Placeholder for channel updates"
    )
    await message.reply(text)

if __name__ == "__main__":
    bot.run()
