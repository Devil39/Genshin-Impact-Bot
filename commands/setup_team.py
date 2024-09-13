from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters
from config import bot

# Handle /setup_team command
@bot.on(events.NewMessage(pattern='/setup_team'))
async def setup_team(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    # Check if the user has started the bot
    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    # Check if the user has any characters
    if not user_data.get('characters'):
        await event.respond('You do not have any characters to set up a team.')
        return

    # Create buttons for each character the user has
    buttons = []
    for char_key in user_data['characters']:
        char_info = characters[char_key]
        buttons.append([Button.inline(f"{char_info['name']}", data=f"add_to_team_{char_key}")])

    await event.respond("Select characters to add to your team:", buttons=buttons)

@bot.on(events.NewMessage(pattern='/assign_slot (.+)'))
async def assign_slot(event):
    await event.respond(f'Slot {slot_name} has been assigned.')

# Handle /setup_team command
@bot.on(events.NewMessage(pattern='/setup_team'))
async def setup_team(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['characters']:
        await event.respond('You don’t have enough characters to set up a team.')
        return

    # Create buttons for each character the user has
    buttons = [
        [Button.inline(f'{characters[char]["name"]}', data=f'select_team_character_{char}') for char in user_data['characters']]
    ]

    await event.respond('Select characters to set up your team:', buttons=buttons)


# Handle adding a character to the team (CallbackQuery)
@bot.on(events.CallbackQuery(pattern=b"add_to_team_.*"))
async def add_to_team(event):
    user_id = str(event.sender_id)
    character_key = event.data.decode().split("_")[3]
    user_data = get_user_data(user_id)

    # Initialize the team if it doesn't exist
    if 'team' not in user_data:
        user_data['team'] = []

    # Check if the character is already in the team
    if character_key in user_data['team']:
        await event.respond(f"{characters[character_key]['name']} is already in your team.")
        return

    # Check if the team is full (max 4 characters)
    if len(user_data['team']) >= 4:
        await event.respond("Your team is already full. You can only have 4 characters.")
        return

    # Add the character to the user's team
    user_data['team'].append(character_key)
    update_user_data(user_id, user_data)

    await event.respond(f"{characters[character_key]['name']} has been added to your team.")

    # If the team is complete, notify the user
    if len(user_data['team']) == 4:
        await event.respond("Your team is now complete.")
    else:
        current_team = ", ".join([characters[char]['name'] for char in user_data['team']])
        await event.respond(f"Current team: {current_team}")

@bot.on(events.CallbackQuery(pattern=b"select_team_character_.*"))
async def select_team_character(event):
    user_id = str(event.sender_id)
    selected_char_id = event.data.decode().split('_')[-1]
    user_data = get_user_data(user_id)

    # Check if the selected character is valid
    if selected_char_id not in user_data['characters']:
        await event.respond('Invalid character selection.')
        return

    # Add character to the user's team
    user_data['team'].append(selected_char_id)
    update_user_data(user_id, user_data)

    await event.respond(f'{characters[selected_char_id]["name"]} has been added to your team.')
