# Discord Bot for Aavikko

Welcome to the **Discord Bot for Sponsors**! This bot is designed to manage sponsor roles, interact with users, and log important events in a Discord server. It features custom commands, role management, private messaging, and response handling for specific keywords.

## Features

- **Sponsor Role Management**: Automatically manages sponsor roles, including sending private messages and logging actions when roles are added or removed.
- **Custom Commands**: Includes several commands like `/my_ckey` for users to register their game key and `/add_disposable` to manage sponsor benefits.
- **Automatic Role Assignment**: Assigns or removes a specific role (configured as `BOOSTY_ROLE_ID`) when sponsor roles are added or removed.
- **Keyword Response**: The bot responds to specific keywords (e.g., "когда") in designated channels.
- **Event Logging**: Logs all user actions and commands to a `.txt` file for easy tracking and auditing.
- **Insult Detection**: Monitors messages for inappropriate content and notifies the specified role when necessary.
- **Token Management**: Provides commands for admins to manage tokens and slots for users.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- A Discord account
- [Discord Developer Portal](https://discord.com/developers/applications) access to create your bot

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/LerkOFF/LERK_bot.git
    cd LERK_bot
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the `.env` File**:
    - Create a `.env` file in the root directory of the project.
    - Add your configuration variables:
      ```env
      DISCORD_TOKEN=your-discord-bot-token
      GUILD_IDS=***,***
      TRACKED_ROLES=***,***
      ROLE_ID_TO_MENTION=***
      CKEY_CHANNEL_ID=***
      INFO_CHANNEL_ID=***
      SPONSORS_FILE_PATH="discord_sponsors.txt"
      LOG_FILE_PATH="logs.txt"
      DISPOSABLE_FILE_PATH="disposable.txt"
      RESPOND_CHANNEL_IDS=***,***
      CAN_GIVES_ROLES=user1,user2,user3
      ROLE_GIVER_CHANNEL=***
      BOOSTY_ROLE_ID=***
      ```

5. **Run the Bot**:
    ```bash
    python main.py
    ```

## Usage

### Commands

- **/my_ckey**: Allows users to register their game key (CKEY). Example: `/my_ckey ckey_here`.
- **/change_my_name_color**: Allows users to change their name color by providing a HEX code. Example: `/change_my_name_color #FF5733`.
- **/give_role**: Admins can assign a role to a user by specifying their nickname and the role ID. Example: `/give_role Joulerk 1234567890`.
- **/remove_role**: Admins can remove a role from a user by specifying their nickname and the role ID. Example: `/remove_role Joulerk 1234567890`.
- **/add_disposable**: Admins can add or update disposable slots and tokens for a user. Example: `/add_disposable Joulerk 3 100`.
- **/make_roles_file**: Creates a file listing all role IDs and their names for easy reference. Example: `/make_roles_file`.

### Keyword Response

- The bot will automatically respond with "Завтра" if the word "когда" is detected in specified channels, which are configured via `RESPOND_CHANNEL_IDS`.

### Event Handling

- When a sponsor role is added or removed, the bot logs the event and sends a private message to the user.
- The bot also automatically assigns or removes the `BOOSTY_ROLE_ID` when sponsor roles are managed.
- Insult detection is in place to monitor for inappropriate content, notifying the specified role (`ROLE_ID_TO_MENTION`).

### Token and Slot Management

- Admins can manage disposable tokens and slots for sponsors using the `/add_disposable` command. This is useful for providing extra perks to sponsors.
- If a user changes their CKEY, the disposable token information will automatically update to reflect their new CKEY.

### Logging

- The bot logs all user actions, including role changes, token updates, and color changes, to `log_file.txt`. The logs include timestamps and clear descriptions of the actions taken.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for review.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, please contact [lerk@joulerk.ru](mailto:lerk@joulerk.ru).

ls for sponsors. Let me know if you'd like further adjustments or additions!
