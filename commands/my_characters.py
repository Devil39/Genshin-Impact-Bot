from telethon import events, Button
from storage.user_data import get_user_data
from data.characters import characters
from config import bot

@bot.on(events.NewMessage(pattern='/my_characters'))
async def my_characters(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    if not user_data['characters']:
        await event.respond('You do not have any characters.')
        return

    buttons = []
    for char_key in user_data['characters']:
        char_info = characters[char_key]
        buttons.append([Button.inline(f"{char_info['name']}", data=f"show_character_{char_key}")])

    await event.respond("Your characters:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"show_character_(.*)"))
async def show_character(event):
    user_id = str(event.sender_id)
    character_key = event.data.decode().split("_")[2]
    user_data = get_user_data(user_id)

    if character_key not in user_data['characters']:
        await event.respond("Character not found.")
        return

    char_info = characters[character_key]
    character_data = user_data['characters'][character_key]

    image_path = f"images/characters/{character_key}.jpg"
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
                f"Level: {character_data['level']}\n"
                f"XP: {character_data['xp']}/{character_data['level'] * 100}\n"
            ),
            parse_mode='markdown'
        )
