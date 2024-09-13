from telethon import TelegramClient, events, Button
from config import api_id, api_hash, bot_token
from config  import bot
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Import commands
from commands.start import start, choose_traveler_anemo, choose_traveler_geo
from commands.help import help
from commands.character import character, my_character, assign_slot, setup_team, select_team_character
from commands.weapon import  weapon, select_weapon_type, weapon_detail, select_weapon, assign_weapon
from commands.battle import encounter_monster, fight_monster, execute_attack
from commands.wish import wish, show_wish_options, perform_single_wish, perform_ten_wish, show_banner_details
from commands.add import add
from commands.level_up import show_characters, show_level_up_requirements, level_up_character
from commands.travel import travel, select_region, explore_place
from commands.walk import walk, fight_monster, run_monster, collect_resource, use_element
from commands.shop import shop, buy_item
from commands.event import add_event_command, start_event_command, end_event_command, list_events
#from commands.challenge import challenge, accept_challenge, challenge_attack, challenge_run
from commands.banner import add_banner_command, activate_banner_command, deactivate_banner_command, list_banners

#bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Register command handlers
bot.add_event_handler(start, events.NewMessage(pattern='/start'))
bot.add_event_handler(help, events.NewMessage(pattern='/help'))
bot.add_event_handler(character, events.NewMessage(pattern='/character'))
bot.add_event_handler(my_character, events.NewMessage(pattern='/my_characters'))
bot.add_event_handler(assign_slot, events.NewMessage(pattern='/assign_slot (.+)'))
bot.add_event_handler(setup_team, events.NewMessage(pattern='/setup_team'))
bot.add_event_handler(select_team_character, events.CallbackQuery(pattern=b"select_team_character_.*"))
bot.add_event_handler(weapon, events.NewMessage(pattern='/weapon'))
bot.add_event_handler(select_weapon_type, events.CallbackQuery(pattern=b"weapon_type_.*"))
bot.add_event_handler(weapon_detail, events.CallbackQuery(pattern=b"weapon_detail_.*"))
bot.add_event_handler(select_weapon, events.CallbackQuery(pattern=b"select_weapon_.*"))
bot.add_event_handler(assign_weapon, events.CallbackQuery(pattern=b"assign_weapon_.*_.*"))
bot.add_event_handler(encounter_monster, events.NewMessage(pattern='/battle'))
bot.add_event_handler(wish, events.NewMessage(pattern='/wish'))
bot.add_event_handler(show_wish_options, events.CallbackQuery(pattern=b'wish_.*'))
bot.add_event_handler(perform_single_wish, events.CallbackQuery(pattern=b'wish_.*_1'))
bot.add_event_handler(perform_ten_wish, events.CallbackQuery(pattern=b'wish_.*_10'))
bot.add_event_handler(show_banner_details, events.CallbackQuery(pattern=b'wish_.*_details'))
bot.add_event_handler(add, events.NewMessage(pattern=r'/add (resource|currency) (\w+) (\d+)'))
bot.add_event_handler(show_characters, events.NewMessage(pattern='/level_up'))
bot.add_event_handler(show_level_up_requirements, events.CallbackQuery(pattern=b"show_level_up_.*"))
bot.add_event_handler(level_up_character, events.CallbackQuery(pattern=b"level_up_.*_.*_.*"))
bot.add_event_handler(travel, events.NewMessage(pattern='/travel'))
bot.add_event_handler(select_region, events.CallbackQuery(pattern=b"travel_.*"))
bot.add_event_handler(explore_place, events.CallbackQuery(pattern=b"explore_.*"))
bot.add_event_handler(walk, events.NewMessage(pattern='/walk'))
bot.add_event_handler(fight_monster, events.CallbackQuery(pattern=b'fight_monster'))
bot.add_event_handler(run_monster, events.CallbackQuery(pattern=b'run_monster'))
bot.add_event_handler(collect_resource, events.CallbackQuery(pattern=b"collect_resource_.*"))
bot.add_event_handler(use_element, events.CallbackQuery(pattern=b"use_element_.*"))
bot.add_event_handler(shop, events.NewMessage(pattern='/shop'))
bot.add_event_handler(buy_item, events.CallbackQuery(pattern=b"buy_item_.*"))
bot.add_event_handler(add_event_command, events.NewMessage(pattern='/add_event'))
bot.add_event_handler(start_event_command, events.NewMessage(pattern='/start_event'))
bot.add_event_handler(end_event_command, events.NewMessage(pattern='/end_event'))
bot.add_event_handler(list_events, events.NewMessage(pattern='/events'))
#bot.add_event_handler(challenge, events.NewMessage(pattern='/challenge'))
#bot.add_event_handler(challenge_user, events.NewMessage(pattern='/challenge @'))
#bot.add_event_handler(accept_challenge, events.CallbackQuery(pattern=b"accept_challenge_.*"))
#bot.add_event_handler(challenge_attack, events.CallbackQuery(pattern=b"challenge_attack_.*_.*"))
#bot.add_event_handler(challenge_run, events.CallbackQuery(pattern=b"challenge_run_.*_.*"))
bot.add_event_handler(add_banner_command, events.NewMessage(pattern='/add_banner'))
bot.add_event_handler(activate_banner_command, events.NewMessage(pattern='/activate_banner'))
bot.add_event_handler(deactivate_banner_command, events.NewMessage(pattern='/deactivate_banner'))
bot.add_event_handler(list_banners, events.NewMessage(pattern='/banners'))

def main():
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()

