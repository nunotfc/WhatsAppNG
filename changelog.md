# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.8.1] - 2026-05-06

### Changed
- NVDA 2026 compatibility

### Fixed
- **Control+R**: Not working for messages with "read more" button (now finds the button by structure instead of language-dependent text)
- **Control+R**: Not working when usage hints filter is disabled
- **Control+R**: Not reading messages that contain links or formatted text

## [1.8.0] - 2026-05-01

### Added
- **Donation dialog**: Shown during add-on installation to support development

### Changed
- **Navigation refactored**: Alt+1, Alt+2, Alt+D now use a stable reference point, making them more resilient to WhatsApp UI changes

### Fixed
- **Enter and Shift+Enter**: Not working when usage hints filter is disabled
- **Enter key**: Not working in file dialogs and conversation list
- **Toggle phone filtering**: In conversation list not updating correctly after toggle
- **Finnish translation**: Improved translation and documentation

## [1.7.1] - 2026-04-10

### Fixed
- **Enter key playback order**: Fixed issue where audio messages no longer played with Enter key
  - Button check now only happens outside message list
  - Audio messages play correctly when navigating message list

## [1.7.0] - 2026-04-10

### Added
- **Finnish translation**: Full Finnish language support

### Fixed
- **Enter key on buttons**: Enter now correctly passes through when focus is on a button
  - Previously, pressing Enter on any button in WhatsApp would trigger audio playback
  - Now buttons behave correctly (e.g., save file button works as expected)

## [1.6.0] - 2026-03-23

### Added
- **Usage hints filtering**: Automatically hides "For more options..." and similar tooltips from message announcements
  - Supports multiple languages
  - Can be toggled with NVDA+Shift+H

### Fixed
- **Duplicate announce in conversation list**: NVDA no longer announces each chat row twice when navigating with arrow keys (#11)
- **Alt+1 navigation**: Improved reliability when locating conversation list
- **Message copying**: Enhanced accuracy when copying messages with Control+C

## [1.5.0] - 2026-03-05

### Added
- **Control+Shift+Enter**: React to messages (opens reaction menu)
- **Alt+Enter**: Read complete message in browse mode window
- **Native shortcuts documentation**: All WhatsApp Desktop keyboard shortcuts added to documentation

### Changed
- **Performance significantly optimized**: Navigation is now more fluid and responsive
  - Faster response time for all keyboard shortcuts
  - Code internally optimized - reduced by over 100 lines for better efficiency
- **Alt+2** more reliable and precise in navigation
- **Control+C** now only works in message list

### Fixed
- **Control+R**: Now reads complete text correctly when expanding long messages

## [1.4.0] - 2026-02-23

### Added
- **Arabic translation**: Full Arabic language support
- **German translation**: Full German language support
- **Spanish translation**: Full Spanish language support
- **Italian translation**: Full Italian language support
- **Russian translation**: Full Russian language support
- **Ukrainian translation update**: Updated Ukrainian translation with latest strings

### Fixed
- **Control+R "Text not found" error**: Fixed error that occurred after clicking "read more" button
- **Control+R now works only on text messages**: Shows "Not a text message" for voice/images, then passes through

### Changed
- **Repository links updated**: All issue links now point to the new repository (nunotfc/WhatsAppNG)
- **Documentation**: All localized READMEs now include complete changelog through version 1.3.0

## [1.3.0] - 2026-02-07

### Added
- **Turkish translation**: Full Turkish language support thanks to Umut KORKMAZ
- **Toggle automatic Focus Mode**: Option to disable automatic Focus Mode when you need Browse Mode
  - Configure your preferred gesture in Input Gestures dialog
  - Useful when you need to use Browse Mode features in WhatsApp

### Changed
- **Improved performance**: Navigation commands (Alt+1, Alt+2, Alt+D) are now faster on repeated use
- **Escape key now passes through**: Works correctly with WhatsApp's native behavior

### Fixed
- **Enter now plays videos**: Pressing Enter on a video message now starts playback (previously only worked for audio)

## [1.1.1] - 2025-01-31

### Added
- **Browse mode auto-disable**: Automatically disables browse mode on focus for better WhatsApp experience
- **Control+R**: Read complete message - clicks "read more" button and speaks full text automatically
- **Control+C**: Copy current message to clipboard
  - Searches for complete message text (>800 chars) first
  - Falls back to filtered text if complete message not found
  - All user-facing messages translatable

### Changed
- **Improved error messages**: All scripts now provide clear feedback
  - Alt+1: Reports "Conversation list not found" on failure
  - Alt+2: Reports "Message list not found" on failure
  - Alt+D: Reports "Message composer not found" on failure
  - Enter: Reports "No audio message found" when no slider detected
  - Shift+Enter: Reports "No menu found" when context menu unavailable
  - Control+R: Reports "Not in message list" or "No message found" on errors
  - Control+C: Reports "Cannot copy" when copy operation fails
- **Silent success**: Navigation commands (Alt+1, Alt+2, Alt+D) no longer speak on success (NVDA already announces focus)
- **All strings translatable**: Every user-facing message now uses `_()` function
- **Enter (play voice message)**: Improved logic using slider detection instead of counting buttons
- Cleaner event handling with focus-based browse mode management

### Fixed
- Alt+2 now correctly tries all navigation paths if first attempt fails
- Alt+1 and Alt+2 now correctly report errors when all navigation paths fail
- Optimized object filtering to reduce input lag during navigation

## [1.0.0] - 2025-01-29

### Added
- Initial release of WhatsApp NG add-on
- Alt+1: Navigate to conversation list
- Alt+2: Navigate to message list
- Alt+D: Focus message composer
- Enter: Play voice message (supports individual chats and groups)
- Shift+Enter: Open message context menu
- Toggle scripts for phone number filtering in conversations and messages
- Automatic focus mode activation in WhatsApp Desktop
- Phone number filtering for "Talvez" messages and international formats

### Technical
- Supports NVDA 2021.1 through 2025.3.1
- Based on web-based WhatsApp Desktop architecture
- Uses event_NVDAObject_init for real-time phone filtering
- Translation support for multiple languages
- SCons build system integration
