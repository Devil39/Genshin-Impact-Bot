from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters

# Ensure bot is properly initialized (place this in your main script or where the bot is set up)
# from telethon import TelegramClient
# bot = TelegramClient('session_name', api_id, api_hash)

async def challenge(event):
    user_id = str(event.sender_id)
    
    if event.is_reply:
        opponent = await event.get_reply_message()
        opponent_id = str(opponent.sender_id)
    else:
        try:
            opponent_tag = event.message.message.split()[1]  # Expecting @username format
            opponent_id = await get_user_id_from_tag(opponent_tag)  # Implement this function
        except (IndexError, ValueError):
            await event.respond("Please mention a valid opponent.")
            return
        except Exception as e:
            await event.respond(f"Error: {str(e)}")
            return

    if not opponent_id:
        await event.respond("Invalid opponent.")
        return

    await event.respond(
        f'You have challenged @{opponent_tag}!',
        buttons=[
            Button.inline("Accept", data=f"accept_{user_id}_{opponent_id}")
        ]
    )

async def accept(event):
    data = event.data.decode().split("_")
    user_id = data[1]
    opponent_id = data[2]

    user_data = get_user_data(user_id)
    opponent_data = get_user_data(opponent_id)

    if not user_data or not opponent_data:
        await event.respond('Both players need to be registered to start the challenge.')
        return

    await event.respond(f'@{opponent_id} has accepted the challenge!')
    await initiate_pvp_battle(user_id, opponent_id)

async def initiate_pvp_battle(user_id, opponent_id):
    user_data = get_user_data(user_id)
    opponent_data = get_user_data(opponent_id)

    user_character = user_data["character"]
    opponent_character = opponent_data["character"]

    if not user_character or not opponent_character:
        await bot.send_message(user_id, "Error: One or both players do not have a valid character.")
        await bot.send_message(opponent_id, "Error: One or both players do not have a valid character.")
        return

    await bot.send_message(
        user_id,
        f'You are fighting against @{opponent_id}!',
        buttons=[
            Button.inline("Normal Attack", data=f"pvp_attack_{user_id}_{opponent_id}"),
            Button.inline("Swap Character", data=f"pvp_swap_{user_id}_{opponent_id}")
        ]
    )

    await bot.send_message(
        opponent_id,
        f'You are fighting against @{user_id}!',
        buttons=[
            Button.inline("Normal Attack", data=f"pvp_attack_{user_id}_{opponent_id}"),
            Button.inline("Swap Character", data=f"pvp_swap_{user_id}_{opponent_id}")
        ]
    )

# Make sure to define get_user_id_from_tag function
async def get_user_id_from_tag(tag):
    # Implement this function to fetch user ID from username or tag
    pass
