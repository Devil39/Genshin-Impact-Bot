user_data = {}

# Initialize new user data with default values
def initialize_user(user_id):
    user_data[user_id] = {
        'character': None,
        'level': 1,
        'xp': 0,
        'resources': {},
        'currencies': {
            'primogem': 100,  # Starting with 100 Primogems
            'mora': 5000,
            'acquaint_fate': 0,
            'intertwined_fate': 0,
            'genesis_crystal': 0
        },
        'characters': {},
        'region': 'mondstadt'
    }

# Retrieve the user data by their user ID
def get_user_data(user_id):
    return user_data.get(user_id, None)

# Update the user data after any changes
def update_user_data(user_id, data):
    user_data[user_id] = data

# Add XP to a specific character and handle leveling up
def add_xp_to_character(user_id, character_name, xp):
    user = get_user_data(user_id)
    if not user or character_name not in user['characters']:
        return False

    character = user['characters'][character_name]
    character['xp'] += xp
    while character['xp'] >= character['level'] * 100:
        character['xp'] -= character['level'] * 100
        character['level'] += 1
    update_user_data(user_id, user)
    return True

# Function to level up the character
def level_up(user_id, character_name):
    user = get_user_data(user_id)
    if not user or character_name not in user['characters']:
        return False

    character = user['characters'][character_name]
    character['level'] += 1
    character['xp'] = 0  # Reset XP after leveling up
    update_user_data(user_id, user)
    print(f"{character_name} has leveled up to level {character['level']}!")
    return True

# Add a new character to the user's account
def add_character_to_user(user_id, character_name):
    user = get_user_data(user_id)
    if not user:
        return False

    if character_name not in user['characters']:
        user['characters'][character_name] = {
            'level': 1,
            'xp': 0
        }
        update_user_data(user_id, user)
    return True

# Add resources to the user's account
def add_resource_to_user(user_id, resource_name, amount):
    user = get_user_data(user_id)
    if not user:
        return False

    if resource_name not in user['resources']:
        user['resources'][resource_name] = 0

    user['resources'][resource_name] += amount
    update_user_data(user_id, user)
    return True

# Spend a specified amount of currency
def spend_currency(user_id, currency_name, amount):
    user = get_user_data(user_id)
    if not user:
        return False

    if user['currencies'].get(currency_name, 0) >= amount:
        user['currencies'][currency_name] -= amount
        update_user_data(user_id, user)
        return True
    return False

# Add currency to the user's account
def add_currency_to_user(user_id, currency_name, amount):
    user = get_user_data(user_id)
    if not user:
        return False

    if currency_name not in user['currencies']:
        user['currencies'][currency_name] = 0

    user['currencies'][currency_name] += amount
    update_user_data(user_id, user)
    return True
