import requests
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters, Client
from MukeshAPI import api
from urllib.parse import quote as urlquote

# Override or fix the scraper.get method
def safe_get_sticker_text(query, page):
    try:
        # Adjust the problematic part of the URL construction
        fixed_query = query.replace(" ", "")  # Remove spaces from query
        # Ensure proper URL formatting using urlquote to encode the query
        url = f"{combot_stickers_url}&page={page}&{urlquote(fixed_query)}"
        
        # Use the api.scraper.get method with the corrected URL
        response = api.scraper.get(url)
        
        # Return the response text
        return response.text
    except Exception as e:
        print(f"Error while fetching sticker text: {e}")
        return None  # Or handle as appropriate

# Use the safe function in your bot
@Client.on_message(filters.command(["chatgpt", "ai", "hey", "ucy", "gpt"], prefixes=[".", "L", "l", "", "S", "/"]))
async def chat_gpt(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        # Check if name is defined, if not, set a default value
        name = message.from_user.first_name if message.from_user else "User"
        
        if len(message.command) < 2:
            await message.reply_text(f"**ʜᴇʟʟᴏ {name}, ʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏᴅᴀʏ?**")
        else:
            query = message.text.split(' ', 1)[1]
            
            # Call the overridden safe_get_sticker_text function here
            response = safe_get_sticker_text(query, page=1)  # Example: you may pass a dynamic page number
            
            if response:
                await message.reply_text(f"{response}", parse_mode=ParseMode.MARKDOWN)
            else:
                await message.reply_text(f"Error fetching sticker information.")
    except Exception as e:
        await message.reply_text(f"**Error: {e}**")
