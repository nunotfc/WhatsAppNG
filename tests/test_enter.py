"""Testes do Enter sem precisar de iniciar o NVDA."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


class Role:
	BUTTON = 1
	SLIDER = 2
	PROGRESSBAR = 3
	STATICTEXT = 4
	LISTITEM = 5
	TABLECELL = 29
	TABLE = 28


def carregar_modulo():
	modulos = {
		"appModuleHandler": types.SimpleNamespace(AppModule=object),
		"api": types.SimpleNamespace(getFocusObject=Mock(), getForegroundObject=Mock()),
		"ui": types.SimpleNamespace(message=Mock()),
		"scriptHandler": types.SimpleNamespace(script=lambda **kwargs: lambda func: func),
		"controlTypes": types.SimpleNamespace(Role=Role),
		"config": types.SimpleNamespace(),
		"addonHandler": types.SimpleNamespace(initTranslation=lambda: None),
		"wx": types.SimpleNamespace(),
		"treeInterceptorHandler": types.SimpleNamespace(),
		"speech": types.SimpleNamespace(),
	}
	caminho = Path(__file__).resolve().parents[1] / "addon/appModules/whatsapp_root.py"
	spec = importlib.util.spec_from_file_location("whatsapp_root_test", caminho)
	modulo = importlib.util.module_from_spec(spec)
	modulo.__dict__["_"] = lambda mensagem: mensagem
	with patch.dict(sys.modules, modulos):
		spec.loader.exec_module(modulo)
	return modulo


class TestEnter(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.modulo = carregar_modulo()

	def setUp(self):
		self.app = self.modulo.AppModule.__new__(self.modulo.AppModule)
		self.gesto = Mock()
		self.modulo.api.getForegroundObject.return_value = types.SimpleNamespace(name="WhatsApp")
		self.modulo.ui.message.reset_mock()

	def focar(self, obj):
		self.modulo.api.getFocusObject.return_value = obj

	def test_conversa_arquivada_recebe_enter(self):
		item = types.SimpleNamespace(role=Role.LISTITEM, parent=types.SimpleNamespace(children=[]))
		self.focar(item)

		self.app.script_playAudio(self.gesto)

		self.gesto.send.assert_called_once()
		self.modulo.ui.message.assert_not_called()

	def test_audio_clica_no_botao_antes_do_slider(self):
		botao = types.SimpleNamespace(role=Role.BUTTON, name="Play", children=[], doAction=Mock())
		slider = types.SimpleNamespace(role=Role.SLIDER, children=[])
		conteudo = types.SimpleNamespace(role=86, children=[botao, slider])
		pai = types.SimpleNamespace(children=[conteudo])
		self.focar(types.SimpleNamespace(role=86, parent=pai))

		self.app.script_playAudio(self.gesto)

		botao.doAction.assert_called_once()
		self.gesto.send.assert_not_called()

	def test_video_clica_no_primeiro_botao(self):
		botao = types.SimpleNamespace(role=Role.BUTTON, name="0:45", children=[], doAction=Mock())
		pai = types.SimpleNamespace(children=[botao])
		self.focar(types.SimpleNamespace(role=86, parent=pai))

		self.app.script_playAudio(self.gesto)

		botao.doAction.assert_called_once()
		self.gesto.send.assert_not_called()

	def test_botao_fora_das_mensagens_recebe_enter(self):
		self.focar(types.SimpleNamespace(role=Role.BUTTON, parent=None))

		self.app.script_playAudio(self.gesto)

		self.gesto.send.assert_called_once()


if __name__ == "__main__":
	unittest.main()
