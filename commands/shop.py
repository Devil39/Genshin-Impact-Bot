from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.resources import resources
from config import bot

@bot.on(events.NewMessage(pattern='/shop'))
async def shop(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    shop_items = {
        'heros_wit': {'name': "Hero's Wit", 'price': 100},
        'mystic_enhancement_ore': {'name': 'Mystic Enhancement Ore', 'price': 50},
        'crystal_core': {'name': 'Crystal Core', 'price': 150}
    }

    buttons = []
    for item_key, item_info in shop_items.items():
        buttons.append([Button.inline(f"{item_info['name']} - {item_info['price']} Mora", data=f"buy_{item_key}")])

    await event.respond("Welcome to the shop! Select an item to buy:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"buy_(.*)"))
async def buy_item(event):
    user_id = str(event.sender_id)
    item_key = event.data.decode().split("_")[1]
    user_data = get_user_data(user_id)

    shop_items = {
        'heros_wit': {'name': "Hero's Wit", 'price': 100},
        'mystic_enhancement_ore': {'name': 'Mystic Enhancement Ore', 'price': 50},
        'crystal_core': {'name': 'Crystal Core', 'price': 150}
    }

    if item_key not in shop_items:
        await event.respond("Item not found.")
        return

    item_info = shop_items[item_key]
    if user_data['currencies'].get('mora', 0) < item_info['price']:
        await event.respond(f"You do not have enough Mora to buy {item_info['name']}.")
        return

    user_data['currencies']['mora'] -= item_info['price']
    if 'resources' not in user_data:
        user_data['resources'] = {}

    if item_key in user_data['resources']:
        user_data['resources'][item_key] += 1
    else:
        user_data['resources'][item_key] = 1

    update_user_data(user_id, user_data)
    await event.respond(f"You have bought {item_info['name']} for {item_info['price']} Mora.")
