from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.weapons import weapons
from data.characters import characters

@bot.on(events.NewMessage(pattern='/weapon'))
async def weapon(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    await event.respond("Select a weapon type:", buttons=[
        [Button.inline("Sword", data="weapon_type_sword"), Button.inline("Bow", data="weapon_type_bow")],
        [Button.inline("Claymore", data="weapon_type_claymore"), Button.inline("Polearm", data="weapon_type_polearm")],
        [Button.inline("Catalyst", data="weapon_type_catalyst")]
    ])

@bot.on(events.CallbackQuery(pattern=b"weapon_type_(.*)"))
async def select_weapon_type(event):
    weapon_type = event.data.decode().split("_")[2]
    available_weapons = [w for w in weapons if w['type'].lower() == weapon_type]

    buttons = [[Button.inline(w['name'], data=f"weapon_detail_{w['name']}")] for w in available_weapons]
    await event.respond(f"Select a {weapon_type.capitalize()} to view details:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"weapon_detail_(.*)"))
async def weapon_detail(event):
    weapon_name = event.data.decode().split("_")[2]
    weapon = next((w for w in weapons if w['name'] == weapon_name), None)

    if not weapon:
        await event.respond(f"No weapon found with the name {weapon_name}.")
        return

    image_path = f'images/weapons/{weapon["image"]}'
    response = (
        f"**{weapon['name']}**\n"
        f"Type: {weapon['type']}\n"
        f"Description: {weapon['description']}\n"
        f"Damage: {weapon['damage']}\n"
        f"Rarity: {'⭐' * weapon['rarity']}"
    )

    with open(image_path, 'rb') as image_file:
        await bot.send_file(
            event.chat_id,
            image_file,
            caption=response,
            buttons=[
                [Button.inline("Select Weapon", f"select_weapon_{weapon_name}")]
            ],
            parse_mode='markdown'
        )

@bot.on(events.CallbackQuery(pattern=b"select_weapon_(.*)"))
async def select_weapon(event):
    weapon_name = event.data.decode().split("_")[2]
    weapon = next((w for w in weapons if w['name'] == weapon_name), None)
    
    if not weapon:
        await event.respond(f"No weapon found with the name {weapon_name}.")
        return

    compatible_characters = [char for char in characters if characters[char]['weapon'] == weapon['type']]
    buttons = [[Button.inline(characters[char]['name'], data=f"assign_weapon_{weapon_name}_{char}")] for char in compatible_characters]

    await event.respond(f"Select a character to equip {weapon_name}:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"assign_weapon_(.*)_(.*)"))
async def assign_weapon(event):
    data = event.data.decode().split("_")
    weapon_name = data[2]
    char_key = data[3]

    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if char_key not in user_data['characters']:
        await event.respond("Character not found.")
        return

    user_data['characters'][char_key]['weapon'] = weapon_name
    update_user_data(user_id, user_data)

    await event.respond(f"{weapon_name} has been equipped to {characters[char_key]['name']}.")
