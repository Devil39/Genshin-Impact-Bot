banners = {}

def add_banner(banner_id, name, description, characters, items, start_date, end_date):
    banners[banner_id] = {
        'name': name,
        'description': description,
        'characters': characters,
        'items': items,
        'start_date': start_date,
        'end_date': end_date,
        'active': False
    }

def activate_banner(banner_id):
    if banner_id in banners:
        banners[banner_id]['active'] = True

def deactivate_banner(banner_id):
    if banner_id in banners:
        banners[banner_id]['active'] = False

def get_active_banners():
    return {bid: bnr for bid, bnr in banners.items() if bnr['active']}
