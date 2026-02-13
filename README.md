# WhatsApp NG

NVDA add-on that provides accessibility enhancements for the web-based WhatsApp Desktop.

## Features

- **Alt+1**: Go to WhatsApp conversation list
- **Alt+2**: Go to WhatsApp message list
- **Alt+D**: Focus message input field
- **Enter**: Play voice message (works in individual chats and groups)
- **Shift+Enter**: Open message context menu
- **Control+C**: Copy current message to clipboard
- **Control+R**: Read complete message (clicks "read more" button if needed)

### Toggle Scripts (no default shortcut - configure in Input Gestures)

- Toggle phone number filtering in conversation list
- Toggle phone number filtering in message list
- Toggle automatic Focus Mode (allows Browse Mode when needed)

## Requirements

- NVDA 2021.1 or later
- WhatsApp Desktop (web-based version)

## Installation

1. Download the `whatsAppNG.nvda-addon` file
2. In NVDA, go to **Tools → Add-on Manager**
3. Click **Install** and select the file
4. Restart NVDA

## Configuration

Phone number filters can be toggled:
- In conversation list: Configure a shortcut in Input Gestures
- In message list: Configure a shortcut in Input Gestures

Configure shortcuts in:
**NVDA menu → Preferences → Input Gestures → WhatsApp NG**

## Credits

Developed by Nuno Costa to provide accessibility enhancements for the modern WhatsApp Desktop experience.

## Support

For issues or suggestions, please visit:
https://github.com/nunotfc/WhatsAppNG/issues

## Translation Compilation

To update or compile translations:
```bash
scons pot
```

This requires GNU Gettext tools to be installed.
