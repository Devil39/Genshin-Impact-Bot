import random
from telethon import events, Button
from storage.user_data import get_user_data, update_user_data, add_resource_to_user, add_xp_to_character
from data.monsters import monsters
from data.resources import resources
from data.regions import regions
from data.characters import characters
from PIL import Image

@bot.on(events.NewMessage(pattern='/walk'))
async def walk(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data['character']:
        await event.respond('You need to choose a character first using /start.')
        return

    current_region = user_data.get('region', 'mondstadt')
    region_data = regions.get(current_region, {})
    encounter_type = random.choice(['monster', 'resource', 'nothing'])

    if encounter_type == 'monster':
        monster = random.choice(region_data['monsters'])
        user_data['current_monster'] = monster
        update_user_data(user_id, user_data)
        image_path = f'images/monsters/{monsters[monster]["image"]}'

        with open(image_path, 'rb') as image_file:
            await bot.send_file(
                event.chat_id,
                image_file,
                caption=f"You encountered a {monsters[monster]['name']}! HP: {monsters[monster]['hp']}\nDo you want to fight?",
                buttons=[
                    [Button.inline("Fight", b"fight_monster")],
                    [Button.inline("Run", b"run_monster")]
                ]
            )

    elif encounter_type == 'resource':
        resource = random.choice(list(resources.keys()))
        resource_info = resources[resource]
        image_path = f'images/rewards/{resource_info["image"]}'
        
        if resource_info['element'] != 'None':
            await event.respond(
                f"You found a {resource_info['name']}! To collect it, you need to use a {resource_info['element']} element attack.",
                buttons=[
                    [Button.inline(f"Use {resource_info['element']} Attack", f"use_element_{resource}_{resource_info['element']}")]
                ]
            )
        else:
            with open(image_path, 'rb') as image_file:
                await bot.send_file(
                    event.chat_id,
                    image_file,
                    caption=f"You found a {resource_info['name']}! Do you want to collect it?",
                    buttons=[
                        [Button.inline("Collect", f"collect_resource_{resource}")]
                    ]
                )

    else:
        await event.respond('You walked around but found nothing.')

@bot.on(events.CallbackQuery(pattern=b"fight_monster"))
async def fight_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    monster = user_data['current_monster']

    if not monster:
        await event.respond('No monster to fight.')
        return

    monster_hp = monsters[monster]['hp']
    user_data['current_monster_hp'] = monster_hp
    update_user_data(user_id, user_data)

    xp_gain = monster_hp // 10  # Example XP gain formula
    add_xp_to_character(user_id, user_data['character'], xp_gain)

    await event.respond(f"You are fighting {monsters[monster]['name']}! HP: {monster_hp}. You earned {xp_gain} XP.")

@bot.on(events.CallbackQuery(pattern=b"run_monster"))
async def run_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    user_data['current_monster'] = None
    update_user_data(user_id, user_data)
    await event.respond('You successfully ran away from the monster.')

@bot.on(events.CallbackQuery(pattern=b"collect_resource_(.*)"))
async def collect_resource(event):
    user_id = str(event.sender_id)
    resource = event.data.decode().split("_")[2]
    resource_info = resources[resource]

    user_data = get_user_data(user_id)
    character_element = characters[user_data['character']]['element']

    if resource_info['element'] != 'None' and resource_info['element'] != character_element:
        await event.respond(f"You need a {resource_info['element']} element character to collect this resource.")
        return

    if 'rewards' in resource_info:
        for reward, amount in resource_info['rewards'].items():
            add_resource_to_user(user_id, reward, amount)
        await event.respond(f"You collected a {resource_info['name']} and received rewards.")
    else:
        add_resource_to_user(user_id, resource, 1)
        await event.respond(f"You collected a {resource_info['name']}.")

@bot.on(events.CallbackQuery(pattern=b"use_element_(.*)"))
async def use_element(event):
    user_id = str(event.sender_id)
    data = event.data.decode().split("_")
    resource = data[2]
    required_element = data[3]
    resource_info = resources[resource]

    user_data = get_user_data(user_id)
    character_element = characters[user_data['character']]['element']

    if character_element != required_element:
        await event.respond(f"You need a {required_element} element character to perform this action.")
        return

    add_resource_to_user(user_id, resource, 1)
    await event.respond(f"You used {required_element} element to collect {resource_info['name']}.")
