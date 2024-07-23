# Game Master Telegram Bot

(In progress)
This is a simple Telegram bot that can be used to play RPG with my friends.
It can be added to a group chat and will command the group chat to play RPG.

# Roadmap:

- [x] Direct chat with gemini with in memory history;
- [x] Chat persistence and clear history command;
- [x] Only reply to group messages when user reply to a narrador's message or when use /narrator command;
- [x] Multi-language (`pt-br`, `en`) commands `/start` and `/narrator` to talk with bot;
- [x] Use simple system prompt on `/start`;
- [x] Transform markdown text to telegram format (telegram uses a special sintax);
- [ ] Better introduction message on `/start` command;
- [ ] Allow user to choose between more complex system prompts (different worlds and setting);
- [ ] Transparency about Gemini quotas and the possibility for the user to use the `flash` model. Ex: Better error messages; Automatic switch to flash and warnings; Quota logging;
- [ ] Return history options as buttons to user;
- [ ] Allow user to buy credits to solve gemini quotas limits.
