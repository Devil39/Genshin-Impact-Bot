from telethon import events, Button
from storage.user_data import (
    initialize_user,
    get_user_data,
    update_user_data
)
from config import bot

# Sample character data with image URLs and info
character_data = {
    'lumine': {
        'name': 'Lumine',
        'element': 'Anemo/Geo',
        'story': 'Lumine, the female traveler, is on a journey to find her brother.',
        'image': 'images/characters/lumine.jpg'  # Replace with actual image path
    },
    'aether': {
        'name': 'Aether',
        'element': 'Anemo/Geo',
        'story': 'Aether, the male traveler, is on a journey to find his sister.',
        'image': 'images/characters/aether.jpg'  # Replace with actual image path
    }
}

# Function to check if the chat is private
def is_private_chat(event):
    return event.is_private

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Check if the message is from a private chat
    if not is_private_chat(event):
        bot_info = await bot.get_me()  # Get bot details
        await event.respond(
            "Please use the bot in private messages.",
            buttons=[Button.url("Start here", f"https://t.me/{bot_info.username}?start=start")]
        )
        return

    user_id = str(event.sender_id)
    initialize_user(user_id)  # Initialize user if not present
    user_data = get_user_data(user_id)

    # If the user doesn't have a character, show Lumine first
    if not user_data['character']:
        await bot.send_file(
            event.sender_id,
            character_data['lumine']['image'],
            caption=f"Character: {character_data['lumine']['name']}\nElement: {character_data['lumine']['element']}\nStory: {character_data['lumine']['story']}",
            buttons=[Button.inline("Next", data="next_character"), Button.inline("Select", data="select_lumine")]
        )
    else:
        await event.respond("You have already started your journey with Genshin Bot!")

@bot.on(events.CallbackQuery(data=b"next_character"))
async def show_aether(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        # Show Aether after Lumine
        await bot.send_file(
            event.sender_id,
            character_data['aether']['image'],
            caption=f"Character: {character_data['aether']['name']}\nElement: {character_data['aether']['element']}\nStory: {character_data['aether']['story']}",
            buttons=[Button.inline("Select", data="select_aether")]
        )

@bot.on(events.CallbackQuery(data=b"select_lumine"))
async def choose_lumine(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        # Set Lumine as the selected character
        user_data['character'] = 'lumine'
        user_data['characters'] = ['lumine']
        user_data['region'] = 'mondstadt'
        user_data['unlocked_places'] = ['City of Mondstadt']
        update_user_data(user_id, user_data)

        # Show Lumine's image and info
        await bot.send_file(
            event.sender_id,
            character_data['lumine']['image'],
            caption=f"You have chosen {character_data['lumine']['name']}!\n\nElement: {character_data['lumine']['element']}\nStory: {character_data['lumine']['story']}"
        )
    else:
        await event.respond("You have already chosen your starting character.")

@bot.on(events.CallbackQuery(data=b"select_aether"))
async def choose_aether(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        # Set Aether as the selected character
        user_data['character'] = 'aether'
        user_data['characters'] = ['aether']
        user_data['region'] = 'mondstadt'
        user_data['unlocked_places'] = ['City of Mondstadt']
        update_user_data(user_id, user_data)

        # Show Aether's image and info
        await bot.send_file(
            event.sender_id,
            character_data['aether']['image'],
            caption=f"You have chosen {character_data['aether']['name']}!\n\nElement: {character_data['aether']['element']}\nStory: {character_data['aether']['story']}"
        )
    else:
        await event.respond("You have already chosen your starting character.")
