user_data = {}

def initialize_user(user_id):
    user_data[user_id] = {
        'character': None,
        'level': 1,
        'xp': 0,
        'resources': {},
        'currencies': {
            'primogem': 0,
            'mora': 0,
            'acquaint_fate': 0,
            'intertwined_fate': 0,
            'genesis_crystal': 0
        },
        'characters': [],
        'region': 'mondstadt'
    }

def get_user_data(user_id):
    return user_data.get(user_id, None)

def update_user_data(user_id, data):
    user_data[user_id] = data

def add_currency_to_user(user_id, currency, amount):
    user = get_user_data(user_id)
    if not user:
        return False

    if currency in user['currencies']:
        user['currencies'][currency] += amount
    else:
        user['currencies'][currency] = amount
    update_user_data(user_id, user)
    return True

def spend_currency(user_id, currency, amount):
    user = get_user_data(user_id)
    if not user:
        return False

    if currency in user['currencies'] and user['currencies'][currency] >= amount:
        user['currencies'][currency] -= amount
        update_user_data(user_id, user)
        return True
    return False

def add_resource_to_user(user_id, resource, amount):
    user = get_user_data(user_id)
    if not user:
        return False

    if resource in user['resources']:
        user['resources'][resource] += amount
    else:
        user['resources'][resource] = amount
    update_user_data(user_id, user)
    return True

def add_character_to_user(user_id, character):
    user = get_user_data(user_id)
    if not user:
        return False

    if 'characters' not in user:
        user['characters'] = []

    if character not in user['characters']:
        user['characters'].append(character)
    
    update_user_data(user_id, user)
    return True

def add_xp_to_user(user_id, xp):
    user = get_user_data(user_id)
    if not user:
        return False

    user['xp'] += xp
    while user['xp'] >= user['level'] * 100:  # Example XP requirement
        user['xp'] -= user['level'] * 100
        user['level'] += 1
        check_level_rewards(user_id)
    update_user_data(user_id, user)
    return True

def check_level_rewards(user_id):
    user = get_user_data(user_id)
    if user['level'] == 5 and 'amber' not in user['characters']:
        user['characters'].append('amber')
        update_user_data(user_id, user)
        return True
    return False
