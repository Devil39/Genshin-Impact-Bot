from telethon import events
from config import bot

# Define help text that will be sent to the user
help_text = """
Welcome to the Genshin Impact Bot!
Here are the available commands:

/start - Start your journey
/character <name> - Show details about your character
/assign_slot <slot> - Assign a slot to a character
/setup_team - Setup your team
/my_characters - View your characters
/wish - Make a wish and unlock new characters or items
/challenge - Start a challenge
/help - Show this help message
"""

# Handle /help command
@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond(help_text)

