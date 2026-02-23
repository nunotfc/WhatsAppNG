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

## Changelog

### Version 1.4.0 (2026-02-23)

**Added:**
- Full language support: Arabic, German, Spanish, Italian, and Russian
- Ukrainian translation updated with latest strings

**Fixed:**
- "Text not found" error in Control+R after clicking "read more" button
- Control+R now works only on text messages (shows "Not a text message" for voice/images)

**Changed:**
- Repository links updated to new repository (nunotfc/WhatsAppNG)
- Documentation: All localized READMEs now include complete changelog through version 1.3.0

### Version 1.3.0 (2026-02-07)

**Added:**
- Turkish translation support
- Toggle automatic Focus Mode option (configure gesture in Input Gestures)

**Changed:**
- Improved performance: Navigation commands are now faster on repeated use
- Escape key now passes through to WhatsApp correctly

**Fixed:**
- Enter now plays video messages (previously only worked for audio)

### Version 1.1.1 (2025-01-31)

**Added:**
- Control+R: Read complete message (clicks "read more" button automatically)
- Control+C: Copy current message to clipboard
- Browse mode auto-disable (keeps focus mode active for better WhatsApp experience)

**Changed:**
- Improved error messages: All scripts now provide clear feedback on failure
- Navigation commands (Alt+1, Alt+2, Alt+D) now silent on success
- Enter: Slider-based detection instead of button counting (more reliable)

**Fixed:**
- Alt+1 and Alt+2 correctly report errors when all paths fail
- Optimized object filtering to reduce input lag

### Version 1.1.0 (2025-01-30)

**Added:**
- Control+R: Read complete message
- Smart voice message playback using slider detection

**Changed:**
- Enter: Improved logic using slider detection instead of counting buttons

**Fixed:**
- Alt+2 now correctly tries all navigation paths if first attempt fails

### Version 1.0.0 (2025-01-29)

**Initial release:**
- Navigation shortcuts for conversation list, message list, and message composer
- Voice message playback with support for individual chats and groups
- Context menu access for message actions
- Phone number filtering toggle for conversations and messages
- Automatic focus mode activation in WhatsApp Desktop

## Credits

Developed by Nuno Costa to provide accessibility enhancements for the modern WhatsApp Desktop experience.

## Support

For issues or suggestions, please visit:
https://github.com/nunotfc/whatsAppNG/issues

## Translation Compilation

To update or compile translations:
```bash
scons pot
```

This requires GNU Gettext tools to be installed.
