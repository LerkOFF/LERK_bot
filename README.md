# Discord Bot for Sponsors

Welcome to the **Discord Bot for Sponsors**! This bot is designed to manage sponsor roles, interact with users, and log important events in a Discord server. It features custom commands, private messaging, and response handling for specific keywords.

## Features

- **Sponsor Role Management**: Automatically manages sponsor roles, including sending private messages and logging actions when roles are added or removed.
- **Custom Commands**: Includes a `/my_ckey` command for users to register their game key.
- **Keyword Response**: The bot responds to specific keywords in designated channels.
- **Event Logging**: Logs user actions to a `.txt` file for easy tracking and auditing.
- **Insult Detection**: Monitors messages for inappropriate content and notifies the appropriate role.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Discord account
- [Discord Developer Portal](https://discord.com/developers/applications) access

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
      RESPOND_CHANNEL_IDS=***,***
      ```

5. **Run the Bot**:
    ```bash
    python main.py
    ```

## Usage

### Commands

- **/my_ckey**: Allows users to register their game key.

### Responses

- **Keyword Response**: The bot will respond with "Завтра" if the word "когда" is detected in specified channels.

### Event Handling

- The bot logs when a sponsor role is added or removed and sends a private message to the user.
- Insult detection is in place to monitor inappropriate content and notify specific roles.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for review.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, please contact [lerk@joulerk.ru](mailto:lerk@joulerk.ru).

