import random
from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters
from data.monsters import monsters

async def encounter_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return
    
    monster = random.choice(list(monsters.keys()))
    user_data["current_monster"] = monster
    update_user_data(user_id, user_data)
    
    await event.respond(f'You encountered a **{monsters[monster]["name"]}**!\nHP: {monsters[monster]["hp"]}\nSelect a character to use or run away:', buttons=[
        [Button.inline(characters[char]["name"], data=f"select_char_{char}") for char in user_data["characters"]],
        [Button.inline("Run", data="run_monster")]
    ])
    
async def fight_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return
    
    if "current_monster" not in user_data:
        await event.respond("You haven't encountered a monster.")
        return
    
    monster_key = user_data["current_monster"]
    monster = monsters[monster_key]
    await event.respond(f'You are fighting a **{monster["name"]}**!\nHP: {monster["hp"]}\nChoose an action:', buttons=[
        [Button.inline("Normal Attack", data="attack_normal"), Button.inline("Elemental Skill", data="attack_skill"), Button.inline("Elemental Burst", data="attack_burst")],
        [Button.inline("Swap Character", data="swap_character"), Button.inline("Run", data="run_monster")]
    ])

async def execute_attack(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return
    
    attack_type = event.data.decode().split("_")[-1]
    monster_key = user_data["current_monster"]
    monster = monsters[monster_key]
    character_key = user_data["character"]
    character = characters[character_key]
    
    damage = character["abilities"][attack_type]["damage"]
    monster["hp"] -= damage
    
    if monster["hp"] <= 0:
        await event.respond(f'You defeated the **{monster["name"]}** with {character["name"]} using {character["abilities"][attack_type]["name"]}!')
        del user_data["current_monster"]
    else:
        await event.respond(f'You used {character["abilities"][attack_type]["name"]} and dealt {damage} damage to **{monster["name"]}**.\nRemaining HP: {monster["hp"]}')
    
    update_user_data(user_id, user_data)

async def run_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return
    
    if "current_monster" in user_data:
        del user_data["current_monster"]
        update_user_data(user_id, user_data)
    
    await event.respond('You successfully ran away from the monster.')
