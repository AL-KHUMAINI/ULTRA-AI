import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from services.chat_service import chat_service
from services.auth_service import auth_service
from services.subscription_service import subscription_service
from localization.i18n import i18n
from core.config import APP_NAME

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='login', **kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        title = Label(
            text=f"Welcome to {APP_NAME}",
            font_size='26sp',
            size_hint_y=0.25,
            bold=True
        )
        layout.add_widget(title)

        self.email_input = TextInput(
            hint_text="Enter your Gmail address",
            multiline=False,
            size_hint_y=0.15
        )
        layout.add_widget(self.email_input)

        self.google_btn = Button(
            text="Sign in with Google",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 0.9, 1),
            font_size='18sp',
            bold=True
        )
        self.google_btn.bind(on_release=self.perform_google_login)
        layout.add_widget(self.google_btn)

        self.status_label = Label(
            text="",
            size_hint_y=0.15,
            font_size='14sp',
            color=(1, 0, 0, 1)
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def perform_google_login(self, instance):
        email = self.email_input.text.strip()
        if not email or "@" not in email:
            self.status_label.text = "Please enter a valid Gmail address."
            return

        if auth_service.login_with_google(email):
            self.manager.get_screen('main').update_user_header(email)
            self.manager.current = 'main'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='main', **kwargs)
        self.user_email = "user@gmail.com"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.header = Label(
            text=f"{APP_NAME} - Free Plan",
            size_hint_y=0.08,
            font_size='16sp',
            bold=True
        )
        layout.add_widget(self.header)

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
        layout.add_widget(self.scroll)

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
        layout.add_widget(input_box)

        self.add_widget(layout)

    def update_user_header(self, email):
        self.user_email = email
        status = subscription_service.get_user_status(email)
        self.header.text = f"User: {email} | Plan: [{status['tier']}] | Remaining: {status['remaining']}"

    def _update_text_height(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width, None)

    def send_message(self, instance):
        msg = self.text_input.text.strip()
        if not msg:
            return

        self.chat_display.text += f"\n[b]You:[/b] {msg}\n"
        self.text_input.text = ""

        response = chat_service.process_user_message(self.user_email, msg, i18n.current_lang)
        self.chat_display.text += f"[b]ULTRA AI:[/b] {response}\n"
        self.update_user_header(self.user_email)

class UltraAIApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(MainScreen())
        return sm

if __name__ == '__main__':
    UltraAIApp().run()
