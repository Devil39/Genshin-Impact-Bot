from telethon import events
from storage.user_data import get_user_data, update_user_data
from data.resources import resources
from data.currencies import currencies
from config import bot

@bot.on(events.NewMessage(pattern=r'/add (resource|currency) (\w+) (\d+)'))
async def add(event):
    user_id = str(event.sender_id)
    user_data = get_user_data(user_id)
    command_type = event.pattern_match.group(1)
    item = event.pattern_match.group(2)
    amount = int(event.pattern_match.group(3))

    if command_type == "resource":
        await add_resource(user_id, user_data, item, amount, event)
    elif command_type == "currency":
        await add_currency(user_id, user_data, item, amount, event)

async def add_resource(user_id, user_data, resource, amount, event):
    if resource not in resources:
        await event.respond(f"Resource '{resource}' not found.")
        return

    if 'resources' not in user_data:
        user_data['resources'] = {}

    if resource in user_data['resources']:
        user_data['resources'][resource] += amount
    else:
        user_data['resources'][resource] = amount

    update_user_data(user_id, user_data)
    await event.respond(f"Added {amount} {resource}(s).")

async def add_currency(user_id, user_data, currency, amount, event):
    if currency not in currencies:
        await event.respond(f"Currency '{currency}' not found.")
        return

    if 'currencies' not in user_data:
        user_data['currencies'] = {}

    if currency in user_data['currencies']:
        user_data['currencies'][currency] += amount
    else:
        user_data['currencies'][currency] = amount

    update_user_data(user_id, user_data)
    await event.respond(f"Added {amount} {currency}(s).")
