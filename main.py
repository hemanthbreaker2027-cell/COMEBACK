import asyncio
import os
from bot import bot
from app import app
import uvicorn

async def start_bot():
    print("Starting Telegram Bot...")
    await bot.start()
    print("Bot started!")

async def start_web():
    print("Starting Web Server...")
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Run both bot and web server concurrently
    await asyncio.gather(
        start_bot(),
        start_web()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
