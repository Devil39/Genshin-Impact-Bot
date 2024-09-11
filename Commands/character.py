from telethon import events, Button
from storage.user_data import get_user_data
from data.characters import characters

@bot.on(events.NewMessage(pattern=r'/character (.+)'))
async def character(event):
    user_id = str(event.sender_id)
    character_name = event.pattern_match.group(1).strip().lower()
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    if character_name not in user_data['characters']:
        await event.respond(f'Character "{character_name}" not found in your collection.')
        return

    character = user_data['characters'][character_name]
    char_info = characters[character]

    image_path = f"images/characters/{character}.jpg"
    with open(image_path, 'rb') as image_file:
        await event.client.send_file(
            event.sender_id,
            file=image_file,
            caption=(
                f"**{char_info['name']}**\n"
                f"Element: {char_info['element']}\n"
                f"Weapon: {char_info['weapon']}\n"
                f"Abilities:\n"
                f"- Normal Attack: {char_info['abilities']['normal_attack']['name']}\n"
                f"- Elemental Skill: {char_info['abilities']['elemental_skill']['name']}\n"
                f"- Elemental Burst: {char_info['abilities']['elemental_burst']['name']}\n"
                f"Level: {char_info['level']}\n"
                f"XP: {char_info['xp']}/{char_info['level'] * 100}\n"
            ),
            parse_mode='markdown'
        )
