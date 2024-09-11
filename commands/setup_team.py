from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters

@bot.on(events.NewMessage(pattern='/setup_team'))
async def setup_team(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    if not user_data['characters']:
        await event.respond('You do not have any characters to set up a team.')
        return

    buttons = []
    for char_key in user_data['characters']:
        char_info = characters[char_key]
        buttons.append([Button.inline(f"{char_info['name']}", data=f"add_to_team_{char_key}")])

    await event.respond("Select characters to add to your team (up to 4):", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"add_to_team_(.*)"))
async def add_to_team(event):
    user_id = str(event.sender_id)
    character_key = event.data.decode().split("_")[3]
    user_data = get_user_data(user_id)

    if 'team' not in user_data:
        user_data['team'] = []

    if character_key in user_data['team']:
        await event.respond(f"{characters[character_key]['name']} is already in your team.")
        return

    if len(user_data['team']) >= 4:
        await event.respond("Your team is already full. You can only have up to 4 characters in your team.")
        return

    user_data['team'].append(character_key)
    update_user_data(user_id, user_data)
    await event.respond(f"{characters[character_key]['name']} has been added to your team.")

    if len(user_data['team']) == 4:
        await event.respond("Your team is now complete.")
    else:
        await event.respond(f"Current team: {[characters[char]['name'] for char in user_data['team']]}")
