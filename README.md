# Genshin Bot

![Genshin Bot Overview](https://telegra.ph//file/03075e1fa3ab13c7f4a49.jpg)

Genshin Bot is a Telegram bot designed to enhance your Genshin Impact experience by providing various functionalities such as character management, battles, and more.

## Features

- **Start Command**: Initialize your bot and user profile.
- **Character Management**: Add, level up, and manage characters.
- **Battle System**: Engage in battles with monsters.
- **Resource Management**: Add and manage in-game resources.
- **Help Command**: Get help on how to use the bot.

## Installation

### Prerequisites

- Python 3.6+
- `pip` (Python package installer)
- Telegram Bot Token (from BotFather)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Genshin-Bot.git
    cd Genshin-Bot
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure your bot:

    Open `config.py` and add your Telegram bot token:

    ```python
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

## Usage

Once the bot is running, you can interact with it via Telegram. Use the following commands:

- `/start` - Initialize your user profile.
- `/add_resource` - Add in-game resources.
- `/battle` - Engage in battles.
- `/character` - Manage your characters.
- `/level_up` - Level up your characters.
- `/help` - Get help on using the bot.

## File Structure

- `main.py`: The main entry point of the bot.
- `config.py`: Configuration file for the bot settings.
- `Comands/`: Directory containing command scripts.
  - `Start.py`: Code for the start command.
  - `add_resource.py`: Code for adding resources.
  - `battle.py`: Code for battle functionality.
  - `character.py`: Code for character management.
  - `character_spin.py`: Code for character spin functionality.
  - `help.py`: Code for the help command.
  - `level_up.py`: Code for leveling up characters.
  - `spin.py`: Code for spin functionality.
  - `weapon.py`: Code for managing weapons.
- `data/`: Directory containing data modules.
  - `characters.py`: Character data.
  - `elements.py`: Elemental data.
  - `level_up_rewards.py`: Level up rewards data.
  - `monsters.py`: Monster data.
  - `resources.py`: Resource data.
  - `weapons.py`: Weapon data.
- `storage/`: Directory for storing persistent data.
  - `user_data.py`: User data storage.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
