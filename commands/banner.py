from telethon import events as tevents
from data.banners import add_banner, activate_banner, deactivate_banner, get_active_banners
from datetime import datetime

# Command to add a new banner (Admin only)
async def add_banner_command(event):
    user_id = str(event.sender_id)
    # Check if user is an admin (replace with actual admin check)
    if user_id != 'admin_user_id':  # Replace 'admin_user_id' with actual admin user ID
        await event.respond('You do not have permission to add banners.')
        return

    try:
        command_parts = event.message.message.split('|')
        banner_id = command_parts[1].strip()
        name = command_parts[2].strip()
        description = command_parts[3].strip()
        characters = command_parts[4].strip().split(',')
        items = command_parts[5].strip().split(',')
        start_date = datetime.strptime(command_parts[6].strip(), '%Y-%m-%d')
        end_date = datetime.strptime(command_parts[7].strip(), '%Y-%m-%d')

        add_banner(banner_id, name, description, characters, items, start_date, end_date)
        await event.respond(f'Banner "{name}" added successfully.')
    except Exception as e:
        await event.respond(f'Error adding banner: {str(e)}')

# Command to activate a banner (Admin only)
async def activate_banner_command(event):
    user_id = str(event.sender_id)
    # Check if user is an admin (replace with actual admin check)
    if user_id != 'admin_user_id':  # Replace 'admin_user_id' with actual admin user ID
        await event.respond('You do not have permission to activate banners.')
        return

    try:
        banner_id = event.message.message.split()[1].strip()
        activate_banner(banner_id)
        await event.respond(f'Banner "{banner_id}" activated successfully.')
    except Exception as e:
        await event.respond(f'Error activating banner: {str(e)}')

# Command to deactivate a banner (Admin only)
async def deactivate_banner_command(event):
    user_id = str(event.sender_id)
    # Check if user is an admin (replace with actual admin check)
    if user_id != 'admin_user_id':  # Replace 'admin_user_id' with actual admin user ID
        await event.respond('You do not have permission to deactivate banners.')
        return

    try:
        banner_id = event.message.message.split()[1].strip()
        deactivate_banner(banner_id)
        await event.respond(f'Banner "{banner_id}" deactivated successfully.')
    except Exception as e:
        await event.respond(f'Error deactivating banner: {str(e)}')

# Command to list active banners
async def list_banners(event):
    active_banners = get_active_banners()
    if not active_banners:
        await event.respond("No active banners at the moment.")
        return

    response = "Active banners:\n"
    for bid, bnr in active_banners.items():
        response += f"{bnr['name']}: {bnr['description']}\n"

    await event.respond(response)
