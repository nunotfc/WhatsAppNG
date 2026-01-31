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
}

MAYBE_RE = re.compile(r"\bTalvez\b\s*", re.IGNORECASE)

# WhatsAppPlus regex: minimum 12 chars, lookahead to avoid matching time
PHONE_RE = re.compile(r"\+\d[()\d\s-]{8,15}(?=[^\d]|$|\s)")

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

		self._toggling = False  # Flag to skip filter during focus changes

		# Register handler to auto-reactivate browse mode if deactivated
		treeInterceptorHandler.post_browseModeStateChange.register(self._onBrowseModeStateChange)

	def _onBrowseModeStateChange(self, **kwargs):
		"""
		Auto-disable browse mode to keep Focus Mode active.
		If browse mode gets activated (e.g. by Escape), immediately disable it.
		Only affects WhatsApp, not other applications.
		"""
		try:
			focus = api.getFocusObject()
			if focus and focus.treeInterceptor:
				# Only process WhatsApp objects (check by appModule)
				app = getattr(focus, "appModule", None)
				if app and hasattr(app, "appName") and app.appName == "whatsapp.root":
					# Force passThrough = True (Focus Mode)
					focus.treeInterceptor.passThrough = True
		except:
			pass

	def _shouldFilterChatList(self):
		"""Always read from config.conf and convert to boolean"""
		try:
			section = config.conf[CONFIG_SECTION]
			val = section.get("filterChatList", False)
			# Explicitly convert (may come as string from NVDA)
			if isinstance(val, str):
				val = val.lower() == 'true'
			return val
		except Exception:
			return False

	def _shouldFilterMessageList(self):
		"""Always read from config.conf and convert to boolean"""
		try:
			section = config.conf[CONFIG_SECTION]
			val = section.get("filterMessageList", True)
			# Explicitly convert (may come as string from NVDA)
			if isinstance(val, str):
				val = val.lower() == 'true'
			return val
		except Exception:
			return True

	@scriptHandler.script(
		description=_("Copy current message to clipboard"),
		gesture="kb:control+c"
	)
	def script_copyMessage(self, gesture):
		"""Copy current message to clipboard."""
		obj = api.getFocusObject()
		role_val = _role(obj)

		# Check if focused on a message (LISTITEM or SECTION with name)
		if (role_val == controlTypes.Role.LISTITEM or role_val == 86) and obj.name:
			parent = getattr(obj, "parent", None)
			if parent:
				siblings = getattr(parent, "children", []) or []

				# FIRST: Check if complete text already exists (> 800 chars)
				longest_text = ""
				for sibling in siblings:
					def find_longest(obj):
						nonlocal longest_text
						try:
							role = _role(obj)
							if role is None:
								return
							if role == controlTypes.Role.STATICTEXT:
								name = getattr(obj, "name", "") or ""
								if name and len(name.strip()) > len(longest_text):
									longest_text = name.strip()
							value = getattr(obj, "value", "") or ""
							if value and len(str(value).strip()) > len(longest_text):
								longest_text = str(value).strip()
							children = getattr(obj, "children", []) or []
							for child in children:
								find_longest(child)
						except Exception:
							pass

					find_longest(sibling)

				# If complete text found, copy it
				if len(longest_text) > 800:
					api.copyToClip(longest_text)
					ui.message(_("Copied"))
					return

				# SECOND: Not found, try to find first TEXT object
				for sibling in siblings:
					def find_first_text(obj):
						try:
							role = _role(obj)
							if role == controlTypes.Role.STATICTEXT:
								name = getattr(obj, "name", "") or ""
								if name and len(name.strip()) > 20:
									# Filter out NVDA labels
									nvda_labels = ['secção', 'section', 'list item', 'item', 'de', 'message', 'mensagem']
									if not any(label.lower() in name.lower() for label in nvda_labels):
										return name.strip()
							children = getattr(obj, "children", []) or []
							for child in children:
								result = find_first_text(child)
								if result:
									return result
						except Exception:
							pass
						return None

					clean_text = find_first_text(obj)

					if clean_text:
						api.copyToClip(clean_text)
						ui.message(_("Copied"))
						return

			# Fallback: use obj.name with filters
			text = obj.name.strip()
			text = re.sub(r'\s*secção$', '', text, flags=re.IGNORECASE)
			text = re.sub(r'\s*list\s*item$', '', text, flags=re.IGNORECASE)
			text = re.sub(r'\s*\d+\s*de\s*\d+$', '', text)
			text = re.sub(r'\s*$', '', text)

			if text.strip():
				api.copyToClip(text)
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

			# Search for slider in siblings
			siblings = getattr(parent, "children", []) or []
			for sibling in siblings:
				# First pass: find the slider object
				slider_obj = None

				def find_slider(obj):
					"""Find slider object (no depth limit)."""
					try:
						role = _role(obj)
						if role is None:
							return
						# Check for SLIDER or PROGRESSBAR
						if role == controlTypes.Role.SLIDER or role == controlTypes.Role.PROGRESSBAR:
							nonlocal slider_obj
							slider_obj = obj
							return

						# Continue searching in children
						children = getattr(obj, "children", []) or []
						for child in children:
							find_slider(child)
					except Exception:
						pass

				find_slider(sibling)

				# If found slider, collect all buttons until slider
				if slider_obj:
					all_buttons = []

					def collect_buttons_until_slider(obj):
						"""Collect all buttons in order."""
						try:
							# Stop if we reached the slider
							if obj is slider_obj:
								return True

							role = _role(obj)
							if role == controlTypes.Role.BUTTON:
								all_buttons.append(obj)

							# Continue searching in children
							children = getattr(obj, "children", []) or []
							for child in children:
								if collect_buttons_until_slider(child):
									return True
						except Exception:
							pass
						return False

					collect_buttons_until_slider(sibling)

					# Click the last button before the slider
					if all_buttons:
						all_buttons[-1].doAction()
						return

			# No slider or button found
			ui.message(_("No audio message found"))

		except Exception:
			ui.message(_("No audio message found"))

	@scriptHandler.script(
		# Translators: Read complete message (click "read more" and speak text)
		description=_("Read complete message (clicks 'read more' button)"),
		gesture="kb:control+r"
	)
	def script_readCompleteMessage(self, gesture):
		"""Control+R: Reads complete message (clicks 'read more' if needed)."""
		try:
			# Only works in message list
			if not self._isMessageListFocus():
				ui.message(_("Not in message list"))
				return

			focus = api.getFocusObject()
			parent = getattr(focus, "parent", None)
			if not parent:
				ui.message(_("No message found"))
				return

			siblings = getattr(parent, "children", []) or []

			# FIRST: Check if complete text already exists (> 800 chars)
			longest_text = ""
			for sibling in siblings:
				def find_longest(obj):
					nonlocal longest_text
					try:
						role = _role(obj)
						if role is None:
							return
						if role == controlTypes.Role.STATICTEXT:
							name = getattr(obj, "name", "") or ""
							if name and len(name.strip()) > len(longest_text):
								longest_text = name.strip()
						value = getattr(obj, "value", "") or ""
						if value and len(str(value).strip()) > len(longest_text):
							longest_text = str(value).strip()
						children = getattr(obj, "children", []) or []
						for child in children:
							find_longest(child)
					except Exception:
						pass

				find_longest(sibling)

			# If complete text already exists, read it and done
			if len(longest_text) > 800:
				ui.message(longest_text)
				return

			# SECOND: Complete text not found, search for "read more" button
			for sibling in siblings:
				# First pass: find the COLLAPSED button
				collapsed_obj = None

				def find_collapsed(obj):
					"""Find button with COLLAPSED state."""
					try:
						role = _role(obj)
						if role is None:
							return
						# Check for BUTTON with COLLAPSED state (512)
						if role == controlTypes.Role.BUTTON:
							states = getattr(obj, "states", set())
							if 512 in states:
								nonlocal collapsed_obj
								collapsed_obj = obj
								return

						# Continue searching in children
						children = getattr(obj, "children", []) or []
						for child in children:
							find_collapsed(child)
					except Exception:
						pass

				find_collapsed(sibling)

				# If found COLLAPSED button, collect all buttons until it
				if collapsed_obj:
					all_buttons = []

					def collect_buttons_until_collapsed(obj):
						"""Collect all buttons until COLLAPSED position."""
						try:
							# Stop if we reached the COLLAPSED button
							if obj is collapsed_obj:
								return True

							role = _role(obj)
							if role == controlTypes.Role.BUTTON:
								all_buttons.append(obj)

							# Continue searching in children
							children = getattr(obj, "children", []) or []
							for child in children:
								if collect_buttons_until_collapsed(child):
									return True
						except Exception:
							pass
						return False

					collect_buttons_until_collapsed(sibling)

					# Find the FIRST FOCUSABLE button (16777216)
					for btn in all_buttons:
						states = getattr(btn, "states", set())
						if 16777216 in states:  # FOCUSABLE
							# This is the "read more" button! Click it
							btn.doAction()
							# Wait for text to load, then speak
							def speak_after_click():
								new_longest = ""
								for sib in siblings:
									def find_new_longest(o):
										nonlocal new_longest
										try:
											r = _role(o)
											if r is None:
												return
											if r == controlTypes.Role.STATICTEXT:
												n = getattr(o, "name", "") or ""
												if n and len(n.strip()) > len(new_longest):
													new_longest = n.strip()
											v = getattr(o, "value", "") or ""
											if v and len(str(v).strip()) > len(new_longest):
												new_longest = str(v).strip()
											ch = getattr(o, "children", []) or []
											for c in ch:
												find_new_longest(c)
										except Exception:
											pass
									find_new_longest(sib)

								if new_longest and len(new_longest) > 800:
									ui.message(new_longest)
								else:
									ui.message(_("Text not found"))

							wx.CallLater(500, speak_after_click)
							return  # Done!

		except Exception:
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
				ui.message(_("Not in message list"))
				return

			focus = api.getFocusObject()
			parent = getattr(focus, "parent", None)
			if not parent:
				ui.message(_("No menu found"))
				return

			# Search for buttons in siblings
			siblings = getattr(parent, "children", [])

			for sibling in siblings:
				def find_buttons(obj):
					buttons = []
					if _role(obj) == controlTypes.Role.BUTTON:
						buttons.append(obj)
					for child in getattr(obj, "children", []):
						buttons.extend(find_buttons(child))
					return buttons

				buttons = find_buttons(sibling)
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

			root = ti.rootNVDAObject
			paths_to_try = [
				[0, 0, 0, 0, 3, 5, 0, 3, 0, 0, 0, 2, 0],
			]

			success = False
			for path_indices in paths_to_try:
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
						obj.setFocus()
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
			if app and hasattr(app, "appName") and app.appName == "whatsapp.root":
				self._filterObjectName(obj)
		except Exception:
			pass

	def _filterObjectName(self, obj):
		"""Apply filters to object name (lightweight version for init)"""
		if not obj.name or self._toggling:
			return

		obj_role = _role(obj)

		# Check if has TABLE as ancestor up to 3 levels
		has_table_ancestor = self._hasAncestorWithRole(obj, ["TABLE"], limit=3)

		# SECTION WITHOUT TABLE ancestor = message list
		if obj_role == 86 and not has_table_ancestor:
			# Always filter "Talvez"
			obj.name = MAYBE_RE.sub("", obj.name)
			# Filter phones if toggle enabled
			if self._shouldFilterMessageList():
				obj.name = PHONE_RE.sub("", obj.name)

		# Any object WITH TABLE ancestor = conversation list
		elif has_table_ancestor:
			if self._shouldFilterChatList():
				obj.name = PHONE_RE.sub("", obj.name)

		# Remove extra spaces
		obj.name = re.sub(r"\s{2,}", " ", obj.name).strip()

	def _hasAncestorWithRole(self, obj, roleNames, limit=18):
		if Role is None:
			return False

		wanted = []
		for n in roleNames:
			if hasattr(Role, n):
				wanted.append(getattr(Role, n))

		for a in _get_ancestors(obj, limit=limit):
			if _role(a) in wanted:
				return True
		return False

	def _isConversationListFocus(self):
		try:
			focus = api.getFocusObject()
		except Exception:
			return False
		return self._hasAncestorWithRole(focus, ["TABLE"], limit=40)

	def _isMessageListFocus(self):
		try:
			focus = api.getFocusObject()
		except Exception:
			return False

		# The focus itself must be SECTION (not EDITABLETEXT inside SECTION)
		if _role(focus) != 86:
			return False

		# And does NOT have TABLE as ancestor
		return not self._hasAncestorWithRole(focus, ["TABLE"], limit=40)

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
			focus = api.getFocusObject()
			ti = getattr(focus, "treeInterceptor", None)

			if not ti or not hasattr(ti, "rootNVDAObject"):
				ui.message(_("Conversation list not found"))
				return

			# Temporarily enable browse mode
			orig_pass_through = ti.passThrough
			ti.passThrough = False

			root = ti.rootNVDAObject
			paths_to_try = [
				[0, 0, 0, 0, 3, 4, 1, 2, 0, 0, 0],
			]

			for path_indices in paths_to_try:
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
						def find_first_cell(o, depth=0):
							if depth > 3:
								return None
							try:
								if _role(o) == 29:
									return o
								for c in getattr(o, "children", []):
									f = find_first_cell(c, depth + 1)
									if f:
										return f
							except:
								pass
							return None

						cell = find_first_cell(obj)
						if cell:
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
		success = False
		try:
			focus = api.getFocusObject()
			ti = getattr(focus, "treeInterceptor", None)

			if not ti or not hasattr(ti, "rootNVDAObject"):
				ui.message(_("Message list not found"))
				return

			# Temporarily enable browse mode
			orig_pass_through = ti.passThrough
			ti.passThrough = False

			root = ti.rootNVDAObject
			paths_to_try = [
				[0, 0, 0, 0, 3, 5, 0, 2, 2, 0],
				[0, 0, 0, 0, 3, 5, 0, 2, 1, 0],
				[0, 0, 0, 0, 3, 5, 0, 2, 2, 0, 9],
				[0, 0, 0, 0, 3, 5, 0, 2, 1, 0, 9],
				[0, 0, 0, 0, 3, 5, 0, 2, 1, 1],
				[0, 0, 0, 0, 3, 5, 0, 2, 2, 1],
			]

			for path_indices in paths_to_try:
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

					# Try to focus
					obj.setFocus()
					success = True
					break

				except Exception:
					continue

			if not success:
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

			if new_val:
				ui.message(_("Message list: phone numbers hidden"))
			else:
				ui.message(_("Message list: phone numbers visible"))
		except Exception:
			pass

def _role(obj):
	try:
		return obj.role
	except Exception:
		return None

def _get_ancestors(obj, limit=40):
	cur = obj
	out = []
	for _ in range(limit):
		try:
			cur = cur.parent
		except Exception:
			break
		if not cur:
			break
		out.append(cur)
	return out
