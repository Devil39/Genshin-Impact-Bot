from telethon import events
from storage.user_data import get_user_data
from data.characters import characters
from config import bot
import difflib

# Helper function for fuzzy matching
def get_closest_character_name(user_characters, input_name):
    all_names = [characters[char]['name'].lower() for char in user_characters]
    closest_matches = difflib.get_close_matches(input_name.lower(), all_names, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

# Handle /character [name] command
@bot.on(events.NewMessage(pattern=r'/character(?:\s+(.+))?'))  # This will capture /character with or without a name
async def my_character(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    # Check if the user has started the bot
    if not user_data:
        await event.respond('You need to start the bot first by using /start.')
        return

    # Check if the user has any characters
    if not user_data.get('characters'):
        await event.respond('You do not have any characters in your collection.')
        return

    # Get the character name from the user input, or handle if it's missing
    character_name = event.pattern_match.group(1)
    if not character_name:
        await event.respond('Please provide a character name, like `/character Amber`.')
        return

    # Clean the input
    character_name = character_name.strip().lower()

    # Try to get the closest matching character name
    closest_name = get_closest_character_name(user_data['characters'], character_name)

    if not closest_name:
        await event.respond(f'Character "{character_name}" not found. Please check the name and try again.')
        return

    # Find the character's key in user data
    character_key = next(key for key in user_data['characters'] if characters[key]['name'].lower() == closest_name)
    char_info = characters[character_key]

    # Path to character image
    image_path = f"images/characters/{character_key}.jpg"

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
                f"XP: {char_info['xp']}/{char_info['level'] * 100}\n"
            ),
            parse_mode='markdown'
        )
