from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from config import bot

regions = {
    'mondstadt': {
        'places': ['City of Mondstadt', 'Whispering Woods', 'Stormbearer Mountains', 'Windrise', 'Starfell Valley']
    },
    'liyue': {
        'places': ['Liyue Harbor', 'Jueyun Karst', 'Tianqiu Valley', 'Qingce Village', 'Dihua Marsh']
    },
    'inazuma': {
        'places': ['Ritou', 'Inazuma City', 'Tatarasuna', 'Narukami Island', 'Yashiori Island']
    }
}

@bot.on(events.NewMessage(pattern='/travel'))
async def travel(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    buttons = []
    for region in regions:
        if region == 'mondstadt' or user_data.get('unlocked_regions', {}).get(region):
            buttons.append([Button.inline(region.capitalize(), data=f"travel_{region}")])

    await event.respond("Select a region to travel to:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"travel_(.*)"))
async def select_region(event):
    user_id = str(event.sender_id)
    region = event.data.decode().split("_")[1]
    user_data = get_user_data(user_id)

    if region not in user_data.get('unlocked_regions', {}) and region != 'mondstadt':
        await event.respond("This region is locked. You need to unlock it first.")
        return

    user_data['region'] = region
    update_user_data(user_id, user_data)

    places = regions[region]['places']
    buttons = [Button.inline(place, data=f"explore_{place.replace(' ', '_')}") for place in places]

    await event.respond(f"You have traveled to {region.capitalize()}. Select a place to explore:", buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"explore_(.*)"))
async def explore_place(event):
    user_id = str(event.sender_id)
    place = event.data.decode().split("_")[1].replace('_', ' ')
    user_data = get_user_data(user_id)

    if 'unlocked_places' not in user_data:
        user_data['unlocked_places'] = []

    if place not in user_data['unlocked_places']:
        await event.respond(f"This place is locked. You need to unlock it first by offering items.")
        return

    update_user_data(user_id, user_data)
    await event.respond(f"You are now exploring {place}. Use /walk to explore the area.")
