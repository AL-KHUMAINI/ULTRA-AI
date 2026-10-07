import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from services.chat_service import chat_service
from localization.i18n import i18n
from core.config import APP_NAME

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.header = Label(
            text=f"{APP_NAME} - {i18n.get_text('app_title')}",
            size_hint_y=0.08,
            font_size='20sp'
        )
        self.add_widget(self.header)

        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.chat_display = Label(
            text="",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        self.chat_display.bind(texture_size=self._update_text_height)
        self.scroll.add_widget(self.chat_display)
        self.add_widget(self.scroll)

        input_box = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=5)
        self.text_input = TextInput(
            hint_text=i18n.get_text('input_placeholder'),
            multiline=False
        )
        self.send_btn = Button(
            text=i18n.get_text('send_button'),
            size_hint_x=0.25
        )
        self.send_btn.bind(on_release=self.send_message)

        input_box.add_widget(self.text_input)
        input_box.add_widget(self.send_btn)
        self.add_widget(input_box)

    def _update_text_height(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width, None)

    def send_message(self, instance):
        msg = self.text_input.text.strip()
        if not msg:
            return

        self.chat_display.text += f"\n[b]You:[/b] {msg}\n"
        self.text_input.text = ""

        response = chat_service.process_user_message(msg, i18n.current_lang)
        self.chat_display.text += f"[b]ULTRA AI:[/b] {response}\n"

class UltraAIApp(App):
    def build(self):
        self.title = APP_NAME
        return MainScreen()

if __name__ == '__main__':
    UltraAIApp().run()
