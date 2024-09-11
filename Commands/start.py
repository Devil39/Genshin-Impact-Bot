from telethon import events, Button
from storage.user_data import initialize_user, get_user_data, update_user_data
from data.characters import characters

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = str(event.sender_id)
    initialize_user(user_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        await event.respond(
            "Welcome to Genshin Bot! Choose your starting character:",
            buttons=[
                [Button.inline("Traveler (Anemo)", data="character_traveler_anemo")],
                [Button.inline("Traveler (Geo)", data="character_traveler_geo")]
            ]
        )
    else:
        await event.respond("You have already started your journey!")

@bot.on(events.CallbackQuery(data=b"character_traveler_anemo"))
async def choose_traveler_anemo(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        user_data['character'] = 'traveler_anemo'
        user_data['characters'] = ['traveler_anemo']
        user_data['region'] = 'mondstadt'
        user_data['unlocked_places'] = ['City of Mondstadt']
        update_user_data(user_id, user_data)
        await event.respond("You have chosen Traveler (Anemo) as your starting character! Let the adventure begin!")
    else:
        await event.respond("You have already chosen your starting character.")

@bot.on(events.CallbackQuery(data=b"character_traveler_geo"))
async def choose_traveler_geo(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data['character']:
        user_data['character'] = 'traveler_geo'
        user_data['characters'] = ['traveler_geo']
        user_data['region'] = 'mondstadt'
        user_data['unlocked_places'] = ['City of Mondstadt']
        update_user_data(user_id, user_data)
        await event.respond("You have chosen Traveler (Geo) as your starting character! Let the adventure begin!")
    else:
        await event.respond("You have already chosen your starting character.")
