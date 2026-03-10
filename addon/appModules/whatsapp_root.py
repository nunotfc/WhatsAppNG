# -*- coding: UTF-8 -*-
import appModuleHandler
import api
import ui
import scriptHandler
import controlTypes
import config
import re
import addonHandler
import wx
import treeInterceptorHandler
import speech

try:
	from controlTypes import Role
except Exception:
	Role = None

# Initialize translation
addonHandler.initTranslation()

CONFIG_SECTION = "whatsappPhoneFilter"

# Configuration specification (required for NVDA to correctly read boolean values)
SPEC = {
	'filterChatList': 'boolean(default=False)',
	'filterMessageList': 'boolean(default=True)',
	'autoFocusMode': 'boolean(default=True)',
}

MAYBE_RE = re.compile(r"\bTalvez\b\s*", re.IGNORECASE)

# WhatsAppPlus regex: minimum 12 chars, lookahead to avoid matching time
PHONE_RE = re.compile(r"\+\d[()\d\s-]{8,15}(?=[^\d]|$|\s)")

# Video duration pattern: detect "3:41", "0:45", etc.
DURATION_RE = re.compile(r"\b\d+:\d{2}\b")  # Time pattern like "3:41"

class AppModule(appModuleHandler.AppModule):
	"""
	App Module for WhatsApp Desktop.
	Alt+1: Conversation list
	Alt+2: Message list
	"""

	scriptCategory = _("WhatsApp NG")

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)

		# Register config spec (required for NVDA to correctly read boolean values)
		if CONFIG_SECTION not in config.conf:
			config.conf[CONFIG_SECTION] = {}
		config.conf.spec[CONFIG_SECTION] = SPEC

		# Performance cache: store config values in memory
		self._config_cache = {
			'filterChatList': False,
			'filterMessageList': True,
			'autoFocusMode': True,
		}
		self._loadConfigCache()

		self._toggling = False  # Flag to skip filter during focus changes
		self._electron_container = None  # Cache for Electron container element
		self._conv_list_prefix = None  # Cache for conversation list prefix (container[4][1])
		self._conv_list_container = None  # Cache for conversation list container (role 28)
		self._conv_list_cell = None  # Cache for conversation list first cell (role 29)
		self._composer_path = None  # Cache for last working composer path

		# Register handler to auto-reactivate browse mode if deactivated
		treeInterceptorHandler.post_browseModeStateChange.register(self._onBrowseModeStateChange)

	def _loadConfigCache(self):
		"""Load all config values into cache once."""
		try:
			section = config.conf.get(CONFIG_SECTION, {})
			for key in self._config_cache:
				val = section.get(key)
				if val is None:
					continue
				# Explicitly convert (may come as string from NVDA)
				if isinstance(val, str):
					val = val.lower() == 'true'
				self._config_cache[key] = bool(val)
		except Exception:
			pass

	def _onBrowseModeStateChange(self, **kwargs):
		"""
		Auto-disable browse mode to keep Focus Mode active.
		If browse mode gets activated (e.g. by Escape), immediately disable it.
		Only affects WhatsApp, not other applications.
		Respects autoFocusMode configuration setting.
		"""
		try:
			# Check if auto Focus Mode is enabled (use cache)
			if not self._config_cache['autoFocusMode']:
				return

			focus = api.getFocusObject()
			if focus and focus.treeInterceptor:
				# Only process WhatsApp objects (check by appModule)
				app = getattr(focus, "appModule", None)
				if app and hasattr(app, "appName") and app.appName == "whatsapp.root":
					# CRITICAL: Only act if this instance matches the focus processID
					# NVDA creates multiple instances for different processes
					focus_process_id = getattr(focus, "processID", None)
					if focus_process_id != self.processID:
						return
					# Force passThrough = True (Focus Mode)
					focus.treeInterceptor.passThrough = True
		except:
			pass

	def _findElectronContainer(self, start_obj, depth=0, max_depth=8):
		"""
		Find the Electron container by traversing down the object tree.
		The container is typically at: root.children[0].children[0].children[0].children[0].children[3]

		This method searches more robustly instead of using hardcoded paths.

		"""
		if depth > max_depth:
			return None

		try:
			children = getattr(start_obj, "children", None)
			if not children:
				return None

			# Try the known index path first
			if len(children) > 3:
				# Common path: down to children[3]
				if depth < 4:
					candidate = children[0] if len(children) > 0 else None
					if candidate:
						result = self._findElectronContainer(candidate, depth + 1, max_depth)
						if result:
							return result

			# If depth 4 and we have enough children, this might be the container
			if depth == 4 and len(children) > 3:
				return start_obj

		except Exception:
			pass

		return None

	def _cacheElectronContainerFromRoot(self, root_obj):
		"""
		Try to cache the Electron container using the known root prefix path.
		Root prefix: [0, 0, 0, 0, 3]
		"""
		try:
			obj = root_obj
			for i in [0, 0, 0, 0, 3]:
				children = getattr(obj, "children", []) or []
				if i < len(children):
					obj = children[i]
				else:
					return None
			self._electron_container = obj
			return obj
		except Exception:
			return None

	def _getConversationListPrefix(self, container):
		"""
		Cache and return the conversation list prefix under the container.
		Prefix path: container[4][1]
		"""
		if self._conv_list_prefix:
			try:
				_ = self._conv_list_prefix.children
				return self._conv_list_prefix
			except Exception:
				self._conv_list_prefix = None

		try:
			children = getattr(container, "children", []) or []
			if len(children) <= 4:
				return None

			lvl1 = children[4]
			lvl1_children = getattr(lvl1, "children", []) or []
			if len(lvl1_children) <= 1:
				return None

			self._conv_list_prefix = lvl1_children[1]
			return self._conv_list_prefix
		except Exception:
			return None

	def _getConversationListContainer(self):
		"""
		Return cached conversation list container (role 28) if valid.
		"""
		if self._conv_list_container:
			try:
				_ = self._conv_list_container.children
				if _role(self._conv_list_container) == 28:
					return self._conv_list_container
				self._conv_list_container = None
			except Exception:
				self._conv_list_container = None
		return None

	def _setConversationListContainer(self, obj):
		"""Cache conversation list container (role 28)."""
		try:
			if obj and _role(obj) == 28:
				self._conv_list_container = obj
				return True
		except Exception:
			pass
		return False

	def _getConversationListCell(self):
		"""Return cached conversation list cell (role 29) if valid."""
		if self._conv_list_cell:
			try:
				_ = self._conv_list_cell.children
				if _role(self._conv_list_cell) == 29:
					return self._conv_list_cell
				self._conv_list_cell = None
			except Exception:
				self._conv_list_cell = None
		return None

	def _setConversationListCell(self, obj):
		"""Cache conversation list cell (role 29)."""
		try:
			if obj and _role(obj) == 29:
				self._conv_list_cell = obj
				return True
		except Exception:
			pass
		return False

	def _getElectronContainer(self):
		"""
		Get the cached Electron container.
		If not cached yet, try to find it in the current tree.
		"""
		if self._electron_container:
			try:
				# Verify container is still valid
				_ = self._electron_container.children
				return self._electron_container
			except Exception:
				# Container became invalid, reset cache
				self._electron_container = None

		# Try to find it again
		try:
			fg_obj = api.getForegroundObject()
			if fg_obj:
				container = self._findElectronContainer(fg_obj)
				if container:
					self._electron_container = container
					return container
				# Fallback: try root prefix cache
				container = self._cacheElectronContainerFromRoot(fg_obj)
				if container:
					return container
		except Exception:
			pass

		return None

	def _shouldFilterChatList(self):
		"""Read from cache (much faster than config.conf)"""
		return self._config_cache.get('filterChatList', False)

	def _shouldFilterMessageList(self):
		"""Read from cache (much faster than config.conf)"""
		return self._config_cache.get('filterMessageList', True)

	def _shouldAutoFocusMode(self):
		"""Read from cache (much faster than config.conf)"""
		return self._config_cache.get('autoFocusMode', True)

	def _findButtons(self, obj):
		"""Find all buttons recursively."""
		buttons = []
		if _role(obj) == controlTypes.Role.BUTTON:
			buttons.append(obj)
		for child in getattr(obj, "children", []):
			buttons.extend(self._findButtons(child))
		return buttons

	def _findSlider(self, obj):
		"""Find slider or progressbar object recursively."""
		try:
			role = _role(obj)
			if role is None:
				return None
			if role == controlTypes.Role.SLIDER or role == controlTypes.Role.PROGRESSBAR:
				return obj
			for child in getattr(obj, "children", []):
				result = self._findSlider(child)
				if result:
					return result
		except Exception:
			pass
		return None

	def _collectButtonsUntil(self, obj, stop_obj):
		"""Collect all buttons until reaching stop_obj (stop searching when found)."""
		buttons = []
		if obj is stop_obj:
			return buttons, True  # Found! Return empty list and True flag
		if _role(obj) == controlTypes.Role.BUTTON:
			buttons.append(obj)
		for child in getattr(obj, "children", []):
			child_buttons, found = self._collectButtonsUntil(child, stop_obj)
			buttons.extend(child_buttons)
			if found:
				return buttons, True  # Stop searching other branches
		return buttons, False

	def _collectTexts(self, obj, min_length=20):
		"""Collect STATICTEXT content recursively."""
		texts = []
		try:
			role = _role(obj)
			if role is None:
				return texts
			if role == controlTypes.Role.STATICTEXT:
				name = getattr(obj, "name", "") or ""
				if name:
					clean = name.strip()
					if clean and not clean.startswith("00:") and len(clean) > min_length:
						texts.append(clean)
			value = getattr(obj, "value", "") or ""
			if value:
				clean_v = str(value).strip()
				if len(clean_v) > min_length:
					texts.append(clean_v)
			for child in getattr(obj, "children", []):
				texts.extend(self._collectTexts(child, min_length))
		except Exception:
			pass
		return texts

	def _findCollapsed(self, obj):
		"""Find button with COLLAPSED state (512) recursively."""
		try:
			role = _role(obj)
			if role is None:
				return None
			if role == controlTypes.Role.BUTTON:
				states = getattr(obj, "states", set())
				if 512 in states:
					return obj
			for child in getattr(obj, "children", []):
				result = self._findCollapsed(child)
				if result:
					return result
		except Exception:
			pass
		return None

	def _findFirstButton(self, obj):
		"""Find first button recursively."""
		if _role(obj) == controlTypes.Role.BUTTON:
			return obj
		for child in getattr(obj, "children", []):
			result = self._findFirstButton(child)
			if result:
				return result
		return None

	def _findFirstCell(self, obj, depth=0, max_depth=3):
		"""Find first table cell recursively."""
		if depth > max_depth:
			return None
		try:
			if _role(obj) == controlTypes.Role.TABLECELL:
				return obj
			for child in getattr(obj, "children", []):
				result = self._findFirstCell(child, depth + 1, max_depth)
				if result:
					return result
		except Exception:
			pass
		return None

	@scriptHandler.script(
		description=_("Copy current message to clipboard"),
		gesture="kb:control+c"
	)
	def script_copyMessage(self, gesture):
		"""Copy current message to clipboard."""
		# Only works in message list
		if not self._isMessageListFocus():
			gesture.send()
			return

		focus = api.getFocusObject()
		focus_name = getattr(focus, "name", "") or ""

		if not focus_name:
			gesture.send()
			return

		# Try to get expanded text first (if there's "read more")
		text, error = self._getMessageText(require_expanded=False)

		if text:
			api.copyToClip(text)
			ui.message(_("Copied"))
			return

		# Fallback: collect text from siblings (same as Alt+Enter)
		parent = getattr(focus, "parent", None)
		if parent:
			siblings = getattr(parent, "children", []) or []
			all_text_parts = []
			for sibling in siblings:
				all_text_parts.extend(self._collectTexts(sibling, 20))

			existing_text = " ".join(all_text_parts)

			if existing_text.strip():
				api.copyToClip(existing_text)
				ui.message(_("Copied"))
				return

		# Not a message or couldn't copy
		ui.message(_("Cannot copy"))
		gesture.send()

	@scriptHandler.script(
		description=_("Play voice message"),
		gesture="kb:enter"
	)
	def script_playAudio(self, gesture):
		"""Enter: Clicks play button (button before slider) without moving focus."""
		try:
			# Only works in message list
			if not self._isMessageListFocus():
				gesture.send()
				return

			focus = api.getFocusObject()
			parent = getattr(focus, "parent", None)
			if not parent:
				ui.message(_("No audio message found"))
				return

			# Check if this is a video by looking for duration pattern in message
			if self._isVideoMessage(parent):
				# Video: click first button directly
				self._clickFirstButton(focus)
				return

			# Audio: search for slider and click button before it
			siblings = getattr(parent, "children", []) or []
			for sibling in siblings:
				slider_obj = self._findSlider(sibling)
				if slider_obj:
					all_buttons, _found = self._collectButtonsUntil(sibling, slider_obj)
					if all_buttons:
						all_buttons[-1].doAction()
						return

			# No slider or button found
			ui.message(_("No audio message found"))

		except Exception:
			ui.message(_("No audio message found"))

	def _getMessageText(self, require_expanded=True):
		"""
		Get formatted message text from current focused message.
		Returns (text, error_message) tuple.
		If error_message is None, text was retrieved successfully.
		"""
		# Validation
		if not self._isMessageListFocus():
			return None, _("Not in message list")

		focus = api.getFocusObject()
		focus_name = getattr(focus, "name", "") or ""

		if "…" not in focus_name:
			return None, _("Not a text message")

		parent = getattr(focus, "parent", None)
		if not parent:
			return None, _("No message found")

		siblings = getattr(parent, "children", []) or []

		# Collect text parts
		all_text_parts = []
		for sibling in siblings:
			all_text_parts.extend(self._collectTexts(sibling, 20))

		existing_text = " ".join(all_text_parts)

		# If text already complete, return it
		if len(existing_text) > 800:
			return existing_text, None

		# Need to expand "read more"
		if not require_expanded:
			return existing_text, None

		# Find and click "read more" button
		for sibling in siblings:
			collapsed_obj = self._findCollapsed(sibling)
			if collapsed_obj:
				all_buttons, _found = self._collectButtonsUntil(sibling, collapsed_obj)

				focusable_buttons = []
				for btn in all_buttons:
					states = getattr(btn, "states", set())
					if 16777216 in states:
						focusable_buttons.append(btn)

				if len(focusable_buttons) >= 2:
					read_more_btn = focusable_buttons[1]
				elif len(focusable_buttons) == 1:
					read_more_btn = focusable_buttons[0]
				else:
					continue

				# Click and wait for expansion
				read_more_btn.doAction()
				wx.CallLater(100, lambda: None)  # Wait for expansion

				# Re-fetch text after expansion
				all_text_parts = []
				try:
					updated_siblings = getattr(parent, "children", []) or []
					for sib in updated_siblings:
						all_text_parts.extend(self._collectTexts(sib, 20))
				except Exception:
					pass

				full_text = "\r\n".join(all_text_parts)

				if full_text and len(full_text) > 300:
					return full_text, None
				else:
					return None, _("Text not found")

		return None, _("Text not found")

	@scriptHandler.script(
		# Translators: Read complete message (click "read more" and speak text)
		description=_("Read complete message (clicks 'read more' button)"),
		gesture="kb:control+r"
	)
	def script_readCompleteMessage(self, gesture):
		"""Control+R: Reads complete message (clicks 'read more' if needed)."""
		# Validation
		if not self._isMessageListFocus():
			gesture.send()
			return

		focus = api.getFocusObject()
		focus_name = getattr(focus, "name", "") or ""

		if "…" not in focus_name:
			ui.message(_("Not a text message"))
			gesture.send()
			return

		parent = getattr(focus, "parent", None)
		if not parent:
			ui.message(_("No message found"))
			return

		siblings = getattr(parent, "children", []) or []

		# Collect existing text
		all_text_parts = []
		for sibling in siblings:
			all_text_parts.extend(self._collectTexts(sibling, 20))

		existing_text = " ".join(all_text_parts)

		# If text already complete, read it
		if len(existing_text) > 800:
			ui.message(existing_text)
			return

		# Need to expand "read more" - find and click button
		for sibling in siblings:
			collapsed_obj = self._findCollapsed(sibling)
			if collapsed_obj:
				all_buttons, _found = self._collectButtonsUntil(sibling, collapsed_obj)

				focusable_buttons = []
				for btn in all_buttons:
					states = getattr(btn, "states", set())
					if 16777216 in states:
						focusable_buttons.append(btn)

				if len(focusable_buttons) >= 2:
					read_more_btn = focusable_buttons[1]
				elif len(focusable_buttons) == 1:
					read_more_btn = focusable_buttons[0]
				else:
					continue

				# Click and then speak after expansion
				read_more_btn.doAction()
				message_parent = parent

				def speak_after_click():
					speech.cancelSpeech()  # Cancel any speech before reading expanded text
					nonlocal all_text_parts
					all_text_parts = []
					try:
						updated_siblings = getattr(message_parent, "children", []) or []
						for sib in updated_siblings:
							all_text_parts.extend(self._collectTexts(sib, 20))
					except Exception:
						pass

					full_text = "\r\n".join(all_text_parts)

					if full_text and len(full_text) > 300:
						ui.message(full_text)
					else:
						ui.message(_("Text not found"))

				wx.CallLater(150, speak_after_click)
				return

		ui.message(_("Text not found"))

	@scriptHandler.script(
		description=_("Read complete message in browse mode"),
		gesture="kb:alt+enter"
	)
	def script_readCompleteMessageBrowse(self, gesture):
		"""Alt+Enter: Read complete message in browse mode."""
		# Validation
		if not self._isMessageListFocus():
			gesture.send()
			return

		focus = api.getFocusObject()
		focus_name = getattr(focus, "name", "") or ""

		if not focus_name:
			gesture.send()
			return

		# Try to get expanded text first (if there's "read more")
		text, error = self._getMessageText(require_expanded=True)

		if not error and text:
			# Successfully got expanded text
			ui.browseableMessage(text)
		else:
			# Fallback: show current message text (even if short or no "read more")
			parent = getattr(focus, "parent", None)
			if parent:
				siblings = getattr(parent, "children", []) or []
				all_text_parts = []
				for sibling in siblings:
					all_text_parts.extend(self._collectTexts(sibling, 20))

				existing_text = " ".join(all_text_parts)

				if existing_text.strip():
					ui.browseableMessage(existing_text)
				else:
					# Last resort: use obj.name with filters (same as Ctrl+C)
					text = focus_name.strip()
					text = re.sub(r'\s*secção$', '', text, flags=re.IGNORECASE)
					text = re.sub(r'\s*list\s*item$', '', text, flags=re.IGNORECASE)
					text = re.sub(r'\s*\d+\s*de\s*\d+$', '', text)
					text = re.sub(r'\s*$', '', text)

					if text.strip():
						ui.browseableMessage(text)
					else:
						gesture.send()
			else:
				gesture.send()

	@scriptHandler.script(
		description=_("Open context menu"),
		gesture="kb:shift+enter"
	)
	def script_contextMenu(self, gesture):
		"""Shift+Enter: Opens message context menu without moving focus."""
		try:
			# Only works in message list
			if not self._isMessageListFocus():
				gesture.send()
				return

			focus = api.getFocusObject()
			parent = getattr(focus, "parent", None)
			if not parent:
				ui.message(_("No menu found"))
				return

			# Search for buttons in siblings
			siblings = getattr(parent, "children", [])

			for sibling in siblings:
				buttons = self._findButtons(sibling)
				if not buttons:
					continue

				# Search for button with COLLAPSED or use last one
				for btn in buttons:
					states = getattr(btn, "states", set())
					if 512 in states:  # COLLAPSED
						btn.doAction()
						return

				# Fallback: last button (menu)
				buttons[-1].doAction()
				return

			ui.message(_("No menu found"))

		except Exception:
			ui.message(_("No menu found"))

	@scriptHandler.script(
		description=_("React to message"),
		gesture="kb:control+shift+enter"
	)
	def script_reactMessage(self, gesture):
		"""Control+Shift+Enter: React to message (opens reaction menu)."""
		try:
			# Only works in message list
			if not self._isMessageListFocus():
				gesture.send()
				return

			focus = api.getFocusObject()
			parent = getattr(focus, "parent", None)
			if not parent:
				gesture.send()
				return

			siblings = getattr(parent, "children", [])

			for sibling in siblings:
				all_buttons = self._findButtons(sibling)
				# Find COLLAPSED index, then get next button
				for i, btn in enumerate(all_buttons):
					states = getattr(btn, "states", set())
					if 512 in states:  # COLLAPSED
						# Next button is the react button
						if i + 1 < len(all_buttons):
							all_buttons[i + 1].doAction()
							return

			gesture.send()

		except Exception:
			gesture.send()

	@scriptHandler.script(
		description=_("Focus message composer"),
		gesture="kb:alt+d"
	)
	def script_focusComposer(self, gesture):
		"""Alt+D: Focuses message input field."""
		self._toggling = True
		orig_pass_through = None
		try:
			focus = api.getFocusObject()
			ti = getattr(focus, "treeInterceptor", None)

			if not ti or not hasattr(ti, "rootNVDAObject"):
				ui.message(_("Message composer not found"))
				return

			# Temporarily enable browse mode
			orig_pass_through = ti.passThrough
			ti.passThrough = False

			container = self._getElectronContainer()

			# Try to use cache first
			if self._composer_path and container:
				try:
					obj = container
					for i in self._composer_path:
						children = getattr(obj, "children", []) or []
						if i < len(children):
							obj = children[i]
						else:
							raise Exception("Cache path invalid")
					obj.setFocus()
					success = True
					return
				except Exception:
					self._composer_path = None

			paths_to_try = []
			if container:
				paths_to_try.append((container, [5, 0, 3, 0, 0, 0, 2, 0]))
			paths_to_try.append((ti.rootNVDAObject, [0, 0, 0, 0, 3, 5, 0, 3, 0, 0, 0, 2, 0]))

			success = False
			for root, path_indices in paths_to_try:
				try:
					obj = root
					valid_path = True

					for i in path_indices:
						children = getattr(obj, "children", []) or []
						if i < len(children):
							obj = children[i]
						else:
							valid_path = False
							break

					if valid_path:
						if root is ti.rootNVDAObject and not self._electron_container:
							self._cacheElectronContainerFromRoot(root)

						obj.setFocus()

						if root is container:
							self._composer_path = path_indices

						success = True
						break

				except Exception:
					continue

			if not success:
				ui.message(_("Message composer not found"))
		except Exception:
			ui.message(_("Message composer not found"))
		finally:
			self._toggling = False
			# Restore Focus Mode
			if orig_pass_through is not None:
				try:
					focus = api.getFocusObject()
					if focus and focus.treeInterceptor:
						focus.treeInterceptor.passThrough = True
				except:
					pass

	def event_gainFocus(self, obj, nextHandler):
		"""Handle focus gain events in WhatsApp."""
		# Check if auto Focus Mode is enabled (use cache - faster)
		if not self._config_cache['autoFocusMode']:
			nextHandler()
			return

		# Only process WhatsApp objects (check by appModule)
		try:
			app = getattr(obj, "appModule", None)
			if app and hasattr(app, "appName") and app.appName == "whatsapp.root":
				# Force Focus Mode when entering WhatsApp
				if obj.treeInterceptor:
					obj.treeInterceptor.passThrough = True
		except Exception:
			pass
		nextHandler()

	def event_NVDAObject_init(self, obj):
		"""Filters phone numbers in object name before speaking (WhatsApp only)."""
		# Skip filtering if toggling (during Alt+1/Alt+2/Alt+D navigation)
		if self._toggling:
			return

		# Only process WhatsApp objects (check by appModule)
		try:
			app = getattr(obj, "appModule", None)
			if not (app and hasattr(app, "appName") and app.appName == "whatsapp.root"):
				return
		except Exception:
			return

		# CRITICAL: Only process objects from this instance's process
		# NVDA creates multiple instances for multi-process apps like Electron
		# This instance should only handle events from its own processID
		try:
			obj_process_id = getattr(obj, "processID", None)
			if obj_process_id is not None and obj_process_id != self.processID:
				return
		except Exception:
			pass

		# Quick exit: no name or empty name
		if not obj.name:
			return

		name = obj.name
		name_len = len(name)

		# Early exit: name too short to have valid phone number
		if name_len < 12 and not name.startswith('Talvez '):
			return

		# Quick pattern check: if no '+' and no 'Talvez' prefix, nothing to filter
		has_plus = '+' in name
		starts_with_maybe = name.startswith('Talvez ')

		if not has_plus and not starts_with_maybe:
			return

		# Read from cache (much faster than config.conf)
		filter_chat = self._config_cache['filterChatList']
		filter_msg = self._config_cache['filterMessageList']

		# If both filters disabled and no Talvez, nothing to do
		if not filter_chat and not filter_msg and not starts_with_maybe:
			return

		try:
			obj_role = _role(obj)

			# Quick exit: only process SECTION and TABLECELL
			if obj_role != 86 and obj_role != 29:
				return

			filtered = False

			# SECTION (role 86): check ancestor to decide which filter to use
			if obj_role == 86:
				has_table_ancestor = self._hasTableInAncestors(obj)

				if has_table_ancestor:
					# Conversation list: use filter_chat
					if filter_chat:
						obj.name = PHONE_RE.sub("", name)
						filtered = True
				else:
					# Message list: use filter_msg
					if filter_msg:
						obj.name = PHONE_RE.sub("", name)
						filtered = True

				# Filter "Talvez" if it's the first word
				if starts_with_maybe:
					if filtered:
						obj.name = obj.name[7:] if obj.name.startswith('Talvez ') else obj.name
					else:
						obj.name = name[7:]
					filtered = True

			# TABLECELL (role 29) = conversation list items
			elif obj_role == 29:
				if filter_chat:
					obj.name = PHONE_RE.sub("", name)
					filtered = True

			# Only clean spaces if we actually changed something
			if filtered:
				obj.name = re.sub(r"\s{2,}", " ", obj.name).strip()
		except Exception:
			pass

	def _hasTableInAncestors(self, obj):
		"""Fast check: only 3 levels up with early exit."""
		if Role is None:
			return False
		table_role = getattr(Role, "TABLE", None)
		if table_role is None:
			return False

		# Check up to 3 levels (reduced from 4 for better performance)
		current = obj
		for _ in range(3):
			try:
				current = current.parent
				if current is None:
					return False
				# Fast role check without function call
				role = getattr(current, "role", None)
				if role == table_role:
					return True
			except Exception:
				break
		return False

	def _isConversationListFocus(self):
		try:
			focus = api.getFocusObject()
		except Exception:
			return False
		return self._hasTableInAncestors(focus)

	def _isMessageListFocus(self):
		try:
			focus = api.getFocusObject()
		except Exception:
			return False

		# The focus itself must be SECTION (not EDITABLETEXT inside SECTION)
		if _role(focus) != 86:
			return False

		# And does NOT have TABLE as ancestor
		return not self._hasTableInAncestors(focus)

	def _isVideoMessage(self, parent):
		"""Check if message is a video by checking first button name for duration pattern."""
		try:
			# Get all children of parent and search for buttons
			children = getattr(parent, "children", []) or []
			all_buttons = []
			for child in children:
				all_buttons.extend(self._findButtons(child))

			if not all_buttons:
				return False

			# Check first button name for duration pattern
			first_button = all_buttons[0]
			name = getattr(first_button, "name", "") or ""
			return bool(DURATION_RE.search(name))

		except Exception:
			return False

	def _clickFirstButton(self, focus):
		"""Click first button in message (for video playback)."""
		try:
			parent = getattr(focus, "parent", None)
			if not parent:
				return

			# Search in all children
			for child in getattr(parent, "children", []):
				button = self._findFirstButton(child)
				if button:
					button.doAction()
					return
		except Exception:
			pass

	@scriptHandler.script(
		description=_("Go to WhatsApp conversation list"),
		gesture="kb:alt+1"
	)
	def script_goToConversationList(self, gesture):
		"""Alt+1: Go to WhatsApp conversation list."""
		self._toggling = True
		# Store original passThrough state
		orig_pass_through = None
		success = False
		try:
			cached_cell = self._getConversationListCell()
			if cached_cell:
				cached_cell.setFocus()
				success = True
				return
			ti = None

			container = self._getElectronContainer()
			paths_to_try = []
			if container:
				cached_list = self._getConversationListContainer()
				if cached_list:
					paths_to_try.append((cached_list, []))
				else:
					prefix = self._getConversationListPrefix(container)
					if prefix:
						paths_to_try.append((prefix, [2, 0, 0, 0]))
					else:
						paths_to_try.append((container, [4, 1, 2, 0, 0, 0]))
			else:
				focus = api.getFocusObject()
				ti = getattr(focus, "treeInterceptor", None)

				if not ti or not hasattr(ti, "rootNVDAObject"):
					ui.message(_("Conversation list not found"))
					return

				# Temporarily enable browse mode
				orig_pass_through = ti.passThrough
				ti.passThrough = False
				paths_to_try.append((ti.rootNVDAObject, [0, 0, 0, 0, 3, 4, 1, 2, 0, 0, 0]))

			for root, path_indices in paths_to_try:
				try:
					obj = root
					valid_path = True

					for i in path_indices:
						children = getattr(obj, "children", []) or []
						if i < len(children):
							obj = children[i]
						else:
							valid_path = False
							break

					if valid_path and _role(obj) == 28:
						if ti and root is ti.rootNVDAObject and not self._electron_container:
							self._cacheElectronContainerFromRoot(root)
						if root is container and not self._conv_list_prefix:
							self._getConversationListPrefix(container)
						self._setConversationListContainer(obj)

						cell = self._findFirstCell(obj)
						if cell:
							self._setConversationListCell(cell)
							cell.setFocus()
							success = True
							break
						else:
							obj.setFocus()
							success = True
							break

				except Exception:
					continue

			if not success:
				ui.message(_("Conversation list not found"))

		except Exception:
			ui.message(_("Conversation list not found"))
		finally:
			self._toggling = False
			# Restore Focus Mode
			if orig_pass_through is not None:
				try:
					focus = api.getFocusObject()
					if focus and focus.treeInterceptor:
						focus.treeInterceptor.passThrough = True
				except:
					pass

	@scriptHandler.script(
		description=_("Go to WhatsApp message list"),
		gesture="kb:alt+2"
	)
	def script_goToMessageList(self, gesture):
		"""Alt+2: Go to WhatsApp message list."""
		self._toggling = True
		orig_pass_through = None
		try:
			focus = api.getFocusObject()
			ti = getattr(focus, "treeInterceptor", None)

			if not ti or not hasattr(ti, "rootNVDAObject"):
				ui.message(_("Message list not found"))
				return

			# Temporarily enable browse mode
			orig_pass_through = ti.passThrough
			ti.passThrough = False

			container = self._getElectronContainer()
			paths_to_try = []
			if container:
				paths_to_try.extend([
					(container, [5, 0, 2, 2, 0]),  # 0
					(container, [5, 0, 2, 1, 0]),  # 1
					(container, [5, 0, 2, 1, 1]),  # 4
					(container, [5, 0, 2, 2, 1]),  # 5 - PRINCIPAL
					(container, [5, 0, 3, 2, 0]),  # 6
					(container, [5, 0, 3, 2, 1]),  # 11 - problemática
				])
			paths_to_try.extend([
				(ti.rootNVDAObject, [0, 0, 0, 0, 3, 5, 0, 2, 2, 0]),  # fallback
				(ti.rootNVDAObject, [0, 0, 0, 0, 3, 5, 0, 2, 1, 1]),  # fallback
				(ti.rootNVDAObject, [0, 0, 0, 0, 3, 5, 0, 2, 2, 1]),  # fallback
				(ti.rootNVDAObject, [0, 0, 0, 0, 3, 5, 0, 3, 2, 1]),  # fallback problemática
			])

			# Try all paths and pick the one with most children (real message list)
			best_obj = None
			max_children = -1

			for root, path_indices in paths_to_try:
				try:
					obj = root
					valid_path = True

					for i in path_indices:
						children = getattr(obj, "children", []) or []
						if i < len(children):
							obj = children[i]
						else:
							valid_path = False
							break

					if not valid_path:
						continue

					# Count children - message list should have many
					obj_children = getattr(obj, "children", []) or []
					child_count = len(obj_children)

					if child_count > max_children:
						max_children = child_count
						best_obj = obj
						if root is ti.rootNVDAObject and not self._electron_container:
							self._cacheElectronContainerFromRoot(root)

				except Exception:
					continue

			# Focus the best candidate
			if best_obj:
				best_obj.setFocus()
			else:
				ui.message(_("Message list not found"))

		except Exception:
			ui.message(_("Message list not found"))
		finally:
			self._toggling = False
			# Restore Focus Mode
			if orig_pass_through is not None:
				try:
					focus = api.getFocusObject()
					if focus and focus.treeInterceptor:
						focus.treeInterceptor.passThrough = True
				except:
					pass

	@scriptHandler.script(
		description=_("Toggle phone number filtering in conversation list")
	)
	def script_togglePhoneReadingInChatList(self, gesture):
		"""Toggle phone number reading in conversation list."""
		try:
			if not self._isConversationListFocus():
				ui.message(_("Use this command in the conversation list"))
				return

			current = self._shouldFilterChatList()
			new_val = not current
			config.conf[CONFIG_SECTION]["filterChatList"] = new_val
			config.conf.save()

			if new_val:
				ui.message(_("Conversation list: phone numbers hidden"))
			else:
				ui.message(_("Conversation list: phone numbers visible"))
		except Exception:
			pass

	@scriptHandler.script(
		description=_("Toggle phone number filtering in message list")
	)
	def script_togglePhoneReadingInMessageList(self, gesture):
		"""Toggle phone number reading in message list."""
		try:
			if not self._isMessageListFocus():
				ui.message(_("Use this command in the message list"))
				return

			current = self._shouldFilterMessageList()
			new_val = not current
			config.conf[CONFIG_SECTION]["filterMessageList"] = new_val
			config.conf.save()
			self._config_cache['filterMessageList'] = new_val  # Update cache

			if new_val:
				ui.message(_("Message list: phone numbers hidden"))
			else:
				ui.message(_("Message list: phone numbers visible"))
		except Exception:
			pass

	@scriptHandler.script(
		gesture="kb:escape"
	)
	def script_escape(self, gesture):
		"""Escape: Pass through to application."""
		gesture.send()

	@scriptHandler.script(
		description=_("Toggle automatic Focus Mode")
	)
	def script_toggleAutoFocusMode(self, gesture):
		"""Toggle automatic Focus Mode activation."""
		current = self._shouldAutoFocusMode()
		new_val = not current
		config.conf[CONFIG_SECTION]["autoFocusMode"] = new_val
		config.conf.save()
		self._config_cache['autoFocusMode'] = new_val  # Update cache

		if new_val:
			ui.message(_("Auto Focus Mode: enabled"))
		else:
			ui.message(_("Auto Focus Mode: disabled"))

def _role(obj):
	try:
		return obj.role
	except Exception:
		return None
