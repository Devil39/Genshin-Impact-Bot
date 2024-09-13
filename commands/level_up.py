from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters
from data.resources import resources
from config import bot

@bot.on(events.NewMessage(pattern='/level_up'))
async def show_characters(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['characters']:
        await event.respond('You have no characters to level up.')
        return

    buttons = []
    for char_key in user_data['characters']:
        char_info = characters[char_key]
        buttons.append([Button.inline(f"{char_info['name']}", data=f"show_level_up_{char_key}")])

    await event.respond("Select a character to level up:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"show_level_up_(.*)"))
async def show_level_up_requirements(event):
    user_id = str(event.sender_id)
    character_key = event.data.decode().split("_")[2]
    user_data = get_user_data(user_id)

    if character_key not in user_data['characters']:
        await event.respond("Character not found.")
        return

    character_data = user_data['characters'][character_key]
    required_xp = character_data['level'] * 100  # Example formula for required XP to level up
    heros_wit_needed = required_xp // 20  # Example conversion rate: 20 XP per Hero's Wit
    mora_needed = required_xp // 10  # Example conversion rate: 10 XP per Mora

    char_info = characters[character_key]
    await event.respond(
        f"{char_info['name']} - Level {character_data['level']}\n"
        f"XP: {character_data['xp']}/{character_data['level'] * 100}\n"
        f"To level up, you need:\n"
        f"{heros_wit_needed} Hero's Wit\n"
        f"{mora_needed} Mora",
        buttons=[
            [Button.inline("Level Up", f"level_up_{character_key}_{heros_wit_needed}_{mora_needed}")]
        ]
    )

@bot.on(events.CallbackQuery(pattern=b"level_up_(.*)_(.*)_(.*)"))
async def level_up_character(event):
    user_id = str(event.sender_id)
    data = event.data.decode().split("_")
    character_key = data[2]
    heros_wit_needed = int(data[3])
    mora_needed = int(data[4])

    user_data = get_user_data(user_id)

    if user_data['resources'].get('heros_wit', 0) < heros_wit_needed or user_data['currencies'].get('mora', 0) < mora_needed:
        await event.respond(f"You need {heros_wit_needed} Hero's Wit and {mora_needed} Mora to level up {characters[character_key]['name']}.")
        return

    user_data['resources']['heros_wit'] -= heros_wit_needed
    user_data['currencies']['mora'] -= mora_needed
    character_data = user_data['characters'][character_key]
    character_data['xp'] += heros_wit_needed * 20  # Example conversion rate

    while character_data['xp'] >= character_data['level'] * 100:
        character_data['xp'] -= character_data['level'] * 100
        character_data['level'] += 1

    update_user_data(user_id, user_data)
    await event.respond(f"{characters[character_key]['name']} has been leveled up to Level {character_data['level']}.\nCurrent XP: {character_data['xp']}/{character_data['level'] * 100}.")
