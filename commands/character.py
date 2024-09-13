from telethon import events, Button
from storage.user_data import get_user_data
from data.characters import characters
from config import bot

# Handle /character command
@bot.on(events.NewMessage(pattern='/character'))
async def character(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        await event.respond('You have not selected a character yet. Use /choose_character to start.')
        return

    char_name = characters[user_data['character']]['name']
    await event.respond(f'Your current character is {char_name}.')

# Handle /assign_slot command
@bot.on(events.NewMessage(pattern='/assign_slot (.+)'))
async def assign_slot(event):
    user_id = str(event.sender_id)
    slot_name = event.pattern_match.group(1)
    user_data = get_user_data(user_id)

    # Check if the slot is valid
    if slot_name not in user_data['slots']:
        await event.respond('Invalid slot name.')
        return

    # Assign the slot to the user
    user_data['assigned_slot'] = slot_name
    update_user_data(user_id, user_data)

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

# Handle selecting a character for the team (CallbackQuery)
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

# Helper functions for getting character info
def get_character_info(char_id):
    """Returns detailed information about a character by their ID."""
    return characters.get(char_id, {})


@bot.on(events.NewMessage(pattern=r'/character (.+)'))
async def my_character(event):
        user_id = str(event.sender_id)
        character_name = event.pattern_match.group(1).strip().lower()  # Correct handling of user input
        user_data = get_user_data(user_id)

        # Check if the user has started the bot
        if not user_data:
            await event.respond('You need to start the bot first by using /start.')
            return

        # Check if the user has the specified character
        if character_name not in user_data['characters']:
            await event.respond(f'Character "{character_name}" not found in your character list.')
            return

        # Fetch character info
        character = user_data['characters'][character_name]
        char_info = characters[character]

        # Path to character image
        image_path = f"images/characters/{character}.jpg"

        # Send character info along with image
        with open(image_path, 'rb') as image_file:
            await event.client.send_file(
                event.sender_id,
                file=image_file,
                caption=(
                    f"**{char_info['name']}**\n"
                    f"Element: {char_info['element']}\n"
                    f"Weapon: {char_info['weapon']}\n"
                    f"Abilities:\n"
                    f"- Normal Attack: {char_info['abilities']['normal']}\n"
                    f"- Elemental Skill: {char_info['abilities']['skill']}\n"
                    f"- Elemental Burst: {char_info['abilities']['burst']}\n"
                    f"Level: {char_info['level']}\n"
                    f"XP: {char_info['xp']}/{char_info['level'] * 100}\n"  # Assuming XP threshold is level * 100
                ),
                parse_mode='markdown'
            )
