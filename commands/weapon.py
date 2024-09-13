from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.weapons import weapons
from config import bot

# Handle /weapon command
@bot.on(events.NewMessage(pattern='/weapon'))
async def weapon(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['weapon']:
        await event.respond('You have not selected a weapon yet. Use /choose_weapon to start.')
        return

    weapon_name = weapons[user_data['weapon']]['name']
    await event.respond(f'Your current weapon is {weapon_name}.')

# Handle selecting a weapon type
@bot.on(events.NewMessage(pattern='/select_weapon_type'))
async def select_weapon_type(event):
    buttons = [
        [Button.inline('Sword', data='select_weapon_type_sword')],
        [Button.inline('Bow', data='select_weapon_type_bow')],
        [Button.inline('Polearm', data='select_weapon_type_polearm')],
    ]
    await event.respond('Select a weapon type:', buttons=buttons)

# Handle weapon details
@bot.on(events.NewMessage(pattern='/weapon_detail'))
async def weapon_detail(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['weapon']:
        await event.respond('You have not selected a weapon yet.')
        return

    weapon = weapons[user_data['weapon']]
    await event.respond(f"Weapon: {weapon['name']}\nType: {weapon['type']}\nLevel: {weapon['level']}")

# Handle weapon selection (CallbackQuery)
@bot.on(events.CallbackQuery(pattern=b"select_weapon_.*"))
async def select_weapon(event):
    user_id = str(event.sender_id)
    selected_weapon = event.data.decode().split('_')[-1]
    user_data = get_user_data(user_id)

    if selected_weapon not in weapons:
        await event.respond('Invalid weapon selection.')
        return

    user_data['weapon'] = selected_weapon
    update_user_data(user_id, user_data)

    await event.respond(f'{weapons[selected_weapon]["name"]} has been selected as your weapon.')

# Handle assigning a weapon
@bot.on(events.NewMessage(pattern='/assign_weapon'))
async def assign_weapon(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['weapon']:
        await event.respond('You have not selected a weapon yet.')
        return

    weapon = weapons[user_data['weapon']]
    await event.respond(f'Weapon {weapon["name"]} has been assigned.')
