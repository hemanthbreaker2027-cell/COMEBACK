import asyncio
import os
from bot import bot
from app import app
import uvicorn

async def start_bot():
    print("Starting Telegram Bot...")
    try:
        await bot.start()
        print("Bot started!")
    except Exception as e:
        print(f"Error starting bot: {e}")

async def start_web():
    print("Starting Web Server...")
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Run both bot and web server concurrently
    bot_task = asyncio.create_task(start_bot())
    web_task = asyncio.create_task(start_web())

    try:
        await asyncio.gather(bot_task, web_task)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Shutting down...")
        bot_task.cancel()
        web_task.cancel()
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
