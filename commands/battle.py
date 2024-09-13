import random
from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters
from data.monsters import monsters
from config import bot

# Encountering a Monster
@bot.on(events.NewMessage(pattern='/encounter_monster'))
async def encounter_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return
    
    # Randomly select a monster and save its state in user_data
    monster_key = random.choice(list(monsters.keys()))
    user_data["current_monster"] = {
        "key": monster_key,  # Store the monster's key
        "hp": monsters[monster_key]["hp"]  # Store the current HP of the monster
    }
    update_user_data(user_id, user_data)
    
    monster = monsters[monster_key]
    
    # Present the encounter to the user with character options and a 'Run' button
    await event.respond(
        f'You encountered a **{monster["name"]}**!\nHP: {monster["hp"]}\nSelect a character to use or run away:',
        buttons=[
            [Button.inline(characters[char]["name"], data=f"select_char_{char}") for char in user_data["characters"]],
            [Button.inline("Run", data="run_monster")]
        ]
    )

# Handling Character Selection for the Fight
@bot.on(events.CallbackQuery(pattern=b"select_char_.*"))
async def select_character(event):
    user_id = str(event.sender_id)
    selected_char = event.data.decode().split('_')[-1]
    user_data = get_user_data(user_id)
    
    if selected_char not in user_data["characters"]:
        await event.answer("Invalid character selected!", alert=True)
        return

    # Set the selected character for the fight
    user_data["selected_character"] = selected_char
    update_user_data(user_id, user_data)
    
    await event.respond(f'You selected {characters[selected_char]["name"]}. Now, choose an attack or action:')
    
    # Show available attack options after selecting the character
    await fight_monster(event)

# Presenting Fight Options (Attack or Run)
async def fight_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if "current_monster" not in user_data:
        await event.respond("You haven't encountered a monster.")
        return
    
    monster = monsters[user_data["current_monster"]["key"]]
    
    # Present attack options and run button
    await event.respond(
        f'You are fighting a **{monster["name"]}**!\nHP: {user_data["current_monster"]["hp"]}\nChoose an action:',
        buttons=[
            [
                Button.inline("Normal Attack", data="attack_normal"),
                Button.inline("Elemental Skill", data="attack_skill"),
                Button.inline("Elemental Burst", data="attack_burst")
            ],
            [Button.inline("Swap Character", data="swap_character"), Button.inline("Run", data="run_monster")]
        ]
    )

# Executing Attacks Based on the Player's Choice
@bot.on(events.CallbackQuery(pattern=b"attack_.*"))
async def execute_attack(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if "current_monster" not in user_data:
        await event.respond("You haven't encountered a monster.")
        return
    
    if "selected_character" not in user_data:
        await event.respond("You haven't selected a character.")
        return
    
    attack_type = event.data.decode().split("_")[-1]
    monster_key = user_data["current_monster"]["key"]
    monster = monsters[monster_key]
    
    character_key = user_data["selected_character"]
    character = characters[character_key]
    
    # Get the damage value from the character's abilities based on attack type
    damage = character["abilities"][attack_type]["damage"]
    user_data["current_monster"]["hp"] -= damage  # Subtract damage from monster's HP
    
    # If the monster is defeated
    if user_data["current_monster"]["hp"] <= 0:
        await event.respond(
            f'You defeated the **{monster["name"]}** with {character["name"]} using {character["abilities"][attack_type]["name"]}!'
        )
        del user_data["current_monster"]
        update_user_data(user_id, user_data)
    else:
        # If the monster is still alive, respond with remaining HP
        await event.respond(
            f'You used {character["abilities"][attack_type]["name"]} and dealt {damage} damage to **{monster["name"]}**.\n'
            f'Remaining HP: {user_data["current_monster"]["hp"]}'
        )
        update_user_data(user_id, user_data)

# Running Away from the Monster
@bot.on(events.CallbackQuery(pattern=b"run_monster"))
async def run_monster(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    
    if "current_monster" in user_data:
        del user_data["current_monster"]
        update_user_data(user_id, user_data)
    
    await event.respond('You successfully ran away from the monster.')

# Swapping Characters during the Fight
@bot.on(events.CallbackQuery(pattern=b"swap_character"))
async def swap_character(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)

    if not user_data:
        await event.respond('You need to start the bot first using /start.')
        return

    # Provide character options to swap
    await event.respond(
        'Select a new character:',
        buttons=[
            [Button.inline(characters[char]["name"], data=f"select_char_{char}") for char in user_data["characters"]]
        ]
    )
