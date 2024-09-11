import random
from telethon import events, Button
from data.banners import get_active_banners
from data.characters import characters
from storage.user_data import get_user_data, add_character_to_user, spend_currency

# Define rarity tiers for characters and items
character_rarity = {
    'common': ['traveler_anemo', 'traveler_geo', 'amber', 'kaeya', 'lisa'],
    'rare': ['diluc', 'jean', 'venti'],
    'epic': ['zhongli', 'ganyu', 'klee']
}

item_rarity = {
    'common': ['sword', 'bow', 'claymore'],
    'rare': ['dragonspine_spear', 'sacrificial_sword'],
    'epic': ['skyward_blade', 'amos_bow']
}

@bot.on(events.NewMessage(pattern='/wish'))
async def wish(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data['character']:
        await event.respond('You need to choose a character first using /start.')
        return

    active_banners = get_active_banners()
    if not active_banners:
        await event.respond("No active banners at the moment.")
        return

    buttons = []
    for bid, bnr in active_banners.items():
        buttons.append([Button.inline(f"{bnr['name']}", data=f"wish_{bid}")])

    await event.respond(
        'Choose your banner to wish on:\n',
        buttons=buttons
    )
    raise events.StopPropagation

@bot.on(events.CallbackQuery(pattern=b"wish_.*"))
async def show_wish_options(event):
    banner_id = event.data.decode().split("_")[1]
    active_banners = get_active_banners()
    
    if banner_id not in active_banners:
        await event.respond("This banner is no longer active.")
        return
    
    banner_info = active_banners[banner_id]

    await event.respond(
        f'You selected the "{banner_info["name"]}" banner. {banner_info["description"]}\n'
        'Choose your wish option:\n',
        buttons=[
            [Button.inline("1 Wish (10 Primogems)", data=f"wish_{banner_id}_1")],
            [Button.inline("10 Wishes (100 Primogems)", data=f"wish_{banner_id}_10")],
            [Button.inline("Banner Details", data=f"wish_{banner_id}_details")]
        ]
    )
    raise events.StopPropagation

@bot.on(events.CallbackQuery(pattern=b"wish_.*_1"))
async def perform_single_wish(event):
    banner_id = event.data.decode().split("_")[1]
    await perform_wish(event, banner_id, 1)

@bot.on(events.CallbackQuery(pattern=b"wish_.*_10"))
async def perform_ten_wish(event):
    banner_id = event.data.decode().split("_")[1]
    await perform_wish(event, banner_id, 10)

@bot.on(events.CallbackQuery(pattern=b"wish_.*_details"))
async def show_banner_details(event):
    banner_id = event.data.decode().split("_")[1]
    active_banners = get_active_banners()

    if banner_id not in active_banners:
        await event.respond("This banner is no longer active.")
        return

    banner_info = active_banners[banner_id]
    details = f'**{banner_info["name"]}**\n{banner_info["description"]}\n\n**Characters:**\n'
    for character in banner_info['characters']:
        details += f'- {characters[character]["name"]}\n'
    details += '\n**Items:**\n'
    for item in banner_info['items']:
        details += f'- {item}\n'
    
    await event.respond(details, parse_mode='markdown')
    raise events.StopPropagation

async def perform_wish(event, banner_id, spins):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    active_banners = get_active_banners()
    if banner_id not in active_banners:
        await event.respond("This banner is no longer active.")
        return
    
    banner_info = active_banners[banner_id]
    cost = 10 * spins  # 10 Primogems per wish

    if not spend_currency(user_id, 'primogem', cost):
        await event.respond(f'You do not have enough Primogems to perform {spins} wish(es).')
        return

    for _ in range(spins):
        reward_type = random.choices(
            population=['character', 'item'],
            weights=[70, 30],  # Example probabilities
            k=1
        )[0]

        if reward_type == 'character':
            rarity = random.choices(
                population=list(character_rarity.keys()),
                weights=[80, 15, 5],  # Example probabilities for common, rare, and epic
                k=1
            )[0]
            chosen_character = random.choice(character_rarity[rarity])
            add_character_to_user(user_id, chosen_character)

            character_info = characters[chosen_character]
            image_path = f"images/characters/{chosen_character}.jpg"
            with open(image_path, 'rb') as image_file:
                await event.client.send_file(
                    event.sender_id,
                    file=image_file,
                    caption=f'You wished on the {banner_info["name"]} banner and got {character_info["name"]}!',
                    parse_mode='markdown'
                )
        else:
            rarity = random.choices(
                population=list(item_rarity.keys()),
                weights=[80, 15, 5],  # Example probabilities for common, rare, and epic
                k=1
            )[0]
            chosen_item = random.choice(item_rarity[rarity])
            # Add item logic here

    await event.respond(f'You have completed {spins} wish(es) on the {banner_info["name"]} banner.')
    raise events.StopPropagation
