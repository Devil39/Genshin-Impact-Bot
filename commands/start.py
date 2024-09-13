from telethon import events, Button
from storage.user_data import (
    initialize_user,
    get_user_data,
    update_user_data
)
from config import bot

# Sample character data with image URLs
character_images = {
    'traveler_anemo': 'images/characters/traveler_anemo.jpg',  # Replace with actual URL or local file path
    'traveler_geo': 'images/characters/traveler_geo.jpg'       # Replace with actual URL or local file path
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

    # If the user doesn't have a character, ask them to choose one
    if not user_data['character']:
        await event.respond(
            "Welcome to Genshin Bot! Choose your starting character:",
            buttons=[
                [Button.inline("Traveler (Anemo)", data="character_traveler_anemo")],
                [Button.inline("Traveler (Geo)", data="character_traveler_geo")]
            ]
        )
    else:
        await event.respond("You have already started your journey with Genshin Bot!")

@bot.on(events.CallbackQuery(data=b"character_traveler_anemo"))
async def choose_traveler_anemo(event):
    # Check if the callback is from a private chat
    if not is_private_chat(event):
        await event.answer("Please interact with me in private messages.", alert=True)
        return

    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        # Set traveler character for the user
        user_data['character'] = 'traveler_anemo'
        user_data['characters'] = ['traveler_anemo']
        user_data['region'] = 'mondstadt'
        user_data['unlocked_places'] = ['City of Mondstadt']
        update_user_data(user_id, user_data)

        # Send image of Traveler (Anemo)
        await bot.send_file(
            event.sender_id,
            character_images['traveler_anemo'],
            caption="You have chosen Traveler (Anemo) and started your journey!"
        )
    else:
        await event.respond("You have already chosen your starting character.")

@bot.on(events.CallbackQuery(data=b"character_traveler_geo"))
async def choose_traveler_geo(event):
    # Check if the callback is from a private chat
    if not is_private_chat(event):
        await event.answer("Please interact with me in private messages.", alert=True)
        return

    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        # Set traveler character for the user
        user_data['character'] = 'traveler_geo'
        user_data['characters'] = ['traveler_geo']
        user_data['region'] = 'mondstadt'
        user_data['unlocked_places'] = ['City of Mondstadt']
        update_user_data(user_id, user_data)

        # Send image of Traveler (Geo)
        await bot.send_file(
            event.sender_id,
            character_images['traveler_geo'],
            caption="You have chosen Traveler (Geo) and started your journey!"
        )
    else:
        await event.respond("You have already chosen your starting character.")
