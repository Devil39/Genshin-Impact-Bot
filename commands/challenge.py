from telethon import events, Button
from storage.user_data import get_user_data, update_user_data
from data.characters import characters

async def challenge(event):
    user_id = str(event.sender_id)
    if event.is_reply:
        opponent = await event.get_reply_message()
        opponent_id = str(opponent.sender_id)
    else:
        opponent_id = event.message.message.split()[1][1:]
    
    await event.respond(f'You have challenged @{opponent_id} to a duel!', buttons=[
        [Button.inline("Accept", data=f"accept_{user_id}_{opponent_id}")]
    ])

async def accept(event):
    user_id, opponent_id = event.data.decode().split("_")[1:]
    user_data = get_user_data(user_id)
    opponent_data = get_user_data(opponent_id)
    
    if not user_data or not opponent_data:
        await event.respond('Both players need to start the bot first using /start.')
        return
    
    await event.respond(f'@{opponent_id} has accepted the duel from @{user_id}! Let the battle begin!')
    await initiate_pvp_battle(user_id, opponent_id)

async def initiate_pvp_battle(user_id, opponent_id):
    user_data = get_user_data(user_id)
    opponent_data = get_user_data(opponent_id)
    
    user_character = user_data["character"]
    opponent_character = opponent_data["character"]
    
    await bot.send_message(user_id, f'You are fighting against @{opponent_id}!\nYour character: {characters[user_character]["name"]}\nOpponent\'s character: {characters[opponent_character]["name"]}', buttons=[
        [Button.inline("Normal Attack", data=f"pvp_attack_{opponent_id}_normal"), Button.inline("Elemental Skill", data=f"pvp_attack_{opponent_id}_skill"), Button.inline("Elemental Burst", data=f"pvp_attack_{opponent_id}_burst")],
        [Button.inline("Swap Character", data=f"pvp_swap_{opponent_id}"), Button.inline("Run", data=f"pvp_run_{opponent_id}")]
    ])
    
    await bot.send_message(opponent_id, f'You are fighting against @{user_id}!\nYour character: {characters[opponent_character]["name"]}\nOpponent\'s character: {characters[user_character]["name"]}', buttons=[
        [Button.inline("Normal Attack", data=f"pvp_attack_{user_id}_normal"), Button.inline("Elemental Skill", data=f"pvp_attack_{user_id}_skill"), Button.inline("Elemental Burst", data=f"pvp_attack_{user_id}_burst")],
        [Button.inline("Swap Character", data=f"pvp_swap_{user_id}"), Button.inline("Run", data=f"pvp_run_{user_id}")]
    ])
