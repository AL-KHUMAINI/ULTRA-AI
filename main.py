import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from services.chat_service import chat_service
from services.auth_service import auth_service
from services.subscription_service import subscription_service
from localization.i18n import i18n
from core.config import APP_NAME

class GeminiBackgroundBox(BoxLayout):
    def __init__(self, bg_color=[0.07, 0.07, 0.08, 1], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='login', **kwargs)
        layout = GeminiBackgroundBox(orientation='vertical', padding=30, spacing=20)

        title = Label(
            text=f"✨ ULTRA AI",
            font_size='32sp',
            size_hint_y=0.2,
            bold=True,
            color=[0.65, 0.78, 0.98, 1]
        )
        layout.add_widget(title)

        subtitle = Label(
            text="Experience the next generation of Gemini AI",
            font_size='14sp',
            size_hint_y=0.1,
            color=[0.7, 0.7, 0.75, 1]
        )
        layout.add_widget(subtitle)

        self.email_input = TextInput(
            hint_text="Enter your Gmail address",
            multiline=False,
            size_hint_y=0.12,
            background_color=[0.14, 0.15, 0.17, 1],
            foreground_color=[1, 1, 1, 1],
            padding=[15, 12, 15, 12]
        )
        layout.add_widget(self.email_input)

        self.google_btn = Button(
            text="Sign in with Google",
            size_hint=(1, 0.14),
            background_color=[0.26, 0.53, 0.96, 1],
            font_size='18sp',
            bold=True
        )
        self.google_btn.bind(on_release=self.perform_google_login)
        layout.add_widget(self.google_btn)

        self.status_label = Label(
            text="",
            size_hint_y=0.15,
            font_size='14sp',
            color=[1, 0.3, 0.3, 1]
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

        main_layout = GeminiBackgroundBox(orientation='vertical', spacing=10, padding=12)

        # Gemini Style Top Bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        self.header_label = Label(
            text="ULTRA AI | FREE PLAN",
            font_size='15sp',
            bold=True,
            halign='left',
            color=[0.8, 0.85, 0.95, 1]
        )
        top_bar.add_widget(self.header_label)

        redeem_btn = Button(
            text="Redeem Code",
            size_hint_x=0.35,
            background_color=[0.2, 0.6, 0.86, 1],
            bold=True,
            font_size='12sp'
        )
        redeem_btn.bind(on_release=self.open_redeem_popup)
        top_bar.add_widget(redeem_btn)
        main_layout.add_widget(top_bar)

        # Scrollable Chat Container
        self.scroll = ScrollView(size_hint=(1, 0.78))
        self.chat_display = Label(
            text="[color=888888]Welcome to ULTRA AI! How can I help you today?[/color]\n",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        self.chat_display.bind(texture_size=self._update_text_height)
        self.scroll.add_widget(self.chat_display)
        main_layout.add_widget(self.scroll)

        # Gemini Style Input Bar
        input_box = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=8)
        self.text_input = TextInput(
            hint_text="Ask Ultra AI anything...",
            multiline=False,
            background_color=[0.14, 0.15, 0.17, 1],
            foreground_color=[1, 1, 1, 1],
            padding=[15, 12, 15, 12]
        )
        self.send_btn = Button(
            text="Send",
            size_hint_x=0.25,
            background_color=[0.26, 0.53, 0.96, 1],
            bold=True
        )
        self.send_btn.bind(on_release=self.send_message)

        input_box.add_widget(self.text_input)
        input_box.add_widget(self.send_btn)
        main_layout.add_widget(input_box)

        self.add_widget(main_layout)

    def update_user_header(self, email):
        self.user_email = email
        status = subscription_service.get_user_status(email)
        tier = status['tier']
        remaining = status['remaining']
        self.header_label.text = f"👤 {email}\nPlan: [{tier}] | Left: {remaining}"

    def _update_text_height(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width, None)

    def send_message(self, instance):
        msg = self.text_input.text.strip()
        if not msg:
            return

        self.chat_display.text += f"\n[color=a8c7fa][b]You:[/b][/color] {msg}\n"
        self.text_input.text = ""

        response = chat_service.process_user_message(self.user_email, msg, i18n.current_lang)
        self.chat_display.text += f"[color=ffffff][b]Gemini ULTRA:[/b][/color] {response}\n"
        self.update_user_header(self.user_email)

    def open_redeem_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        code_input = TextInput(
            hint_text="Enter activation code (e.g. PRO-2026, ULTRA-VIP)",
            multiline=False,
            size_hint_y=0.4
        )
        status_lbl = Label(text="", size_hint_y=0.2, color=[1, 0.3, 0.3, 1])
        btn_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.4)

        popup = Popup(title="Redeem Activation Code", content=content, size_hint=(0.85, 0.4))

        def process_code(btn):
            code = code_input.text.strip()
            if not code:
                status_lbl.text = "Please enter a code"
                return
            success, result = subscription_service.redeem_code(self.user_email, code)
            if success:
                status_lbl.color = [0.3, 1, 0.3, 1]
                status_lbl.text = f"Success! Plan upgraded to {result}"
                self.update_user_header(self.user_email)
            else:
                status_lbl.text = f"Failed: {result}"

        submit_btn = Button(text="Activate", background_color=[0.2, 0.8, 0.3, 1])
        submit_btn.bind(on_release=process_code)
        close_btn = Button(text="Close")
        close_btn.bind(on_release=popup.dismiss)

        btn_box.add_widget(submit_btn)
        btn_box.add_widget(close_btn)

        content.add_widget(code_input)
        content.add_widget(status_lbl)
        content.add_widget(btn_box)

        popup.open()

class UltraAIApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(MainScreen())
        return sm

if __name__ == '__main__':
    UltraAIApp().run()
