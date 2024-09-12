from telethon import events, Button
from storage.user_data import get_user_data
from data.characters import characters

def setup_character_commands(bot):
    @bot.on(events.NewMessage(pattern=r'/character (.+)'))
    async def character(event):
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
