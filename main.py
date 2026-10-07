import os
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from services.chat_service import chat_service
from services.auth_service import auth_service
from services.subscription_service import subscription_service
from services.voice_service import voice_service
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

class GeminiOverlayHandle(Button):
    """ Modern Bottom Handle / Line matching Android Gemini gesture bar """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "━━━"
        self.font_size = '22sp'
        self.bold = True
        self.background_color = [0, 0, 0, 0]
        self.color = [0.8, 0.8, 0.85, 0.8]
        self.size_hint_y = None
        self.height = 25

class HoldToVerifyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "🔒 اضغط بشكل متواصل للتحقق من أنك لست روبوت"
        self.background_color = [0.2, 0.3, 0.4, 1]
        self.bold = True
        self.is_verified = False
        self.hold_time = 0
        self._clock_event = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.is_verified:
            self.hold_time = 0
            self._clock_event = Clock.schedule_interval(self._update_progress, 0.1)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
            if not self.is_verified:
                self.text = "🔒 اضغط بشكل متواصل للتحقق من أنك لست روبوت"
                self.background_color = [0.2, 0.3, 0.4, 1]
        return super().on_touch_up(touch)

    def _update_progress(self, dt):
        self.hold_time += 0.1
        progress = int((self.hold_time / 2.0) * 100)
        if progress < 100:
            self.text = f"⏳ جارٍ التحقق... {progress}%"
            self.background_color = [0.8, 0.5, 0.1, 1]
        else:
            self.is_verified = True
            self.text = "✅ تم التحقق بنجاح!"
            self.background_color = [0.2, 0.7, 0.3, 1]
            if self._clock_event:
                self._clock_event.cancel()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='login', **kwargs)
        layout = GeminiBackgroundBox(orientation='vertical', padding=25, spacing=15)

        title = Label(
            text="✨ ULTRA AI ASSISTANT",
            font_size='30sp',
            size_hint_y=0.18,
            bold=True,
            color=[0.65, 0.78, 0.98, 1]
        )
        layout.add_widget(title)

        self.email_input = TextInput(
            hint_text="ادخل بريد أندرويد/Gmail الخاص بك",
            multiline=False,
            size_hint_y=0.12,
            background_color=[0.14, 0.15, 0.17, 1],
            foreground_color=[1, 1, 1, 1],
            padding=[15, 12, 15, 12]
        )
        layout.add_widget(self.email_input)

        self.verify_btn = HoldToVerifyButton(size_hint_y=0.14)
        layout.add_widget(self.verify_btn)

        self.google_btn = Button(
            text="تسجيل الدخول مع جوجل",
            size_hint=(1, 0.14),
            background_color=[0.26, 0.53, 0.96, 1],
            font_size='18sp',
            bold=True
        )
        self.google_btn.bind(on_release=self.perform_google_login)
        layout.add_widget(self.google_btn)

        self.status_label = Label(
            text="",
            size_hint_y=0.12,
            font_size='14sp',
            color=[1, 0.3, 0.3, 1]
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def perform_google_login(self, instance):
        if not self.verify_btn.is_verified:
            self.status_label.text = "يرجى الضغط المستمر للتحقق أولاً!"
            return

        email = self.email_input.text.strip()
        if not email or "@" not in email:
            self.status_label.text = "يرجى إدخال بريد Gmail صحيح."
            return

        if auth_service.login_with_google(email):
            self.manager.get_screen('main').update_user_header(email)
            self.manager.current = 'main'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='main', **kwargs)
        self.user_email = "user@gmail.com"

        main_layout = GeminiBackgroundBox(orientation='vertical', spacing=6, padding=10)

        # Top Bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        self.header_label = Label(
            text="Gemini Ultra Assistant",
            font_size='12sp',
            bold=True,
            color=[0.8, 0.85, 0.95, 1]
        )
        top_bar.add_widget(self.header_label)

        redeem_btn = Button(
            text="تفعيل كود",
            size_hint_x=0.28,
            background_color=[0.2, 0.6, 0.86, 1],
            bold=True,
            font_size='12sp'
        )
        redeem_btn.bind(on_release=self.open_redeem_popup)
        top_bar.add_widget(redeem_btn)
        main_layout.add_widget(top_bar)

        # 7-day alert banner
        self.notification_banner = Label(
            text="",
            size_hint_y=None,
            height=0,
            color=[1, 0.8, 0.2, 1],
            bold=True,
            font_size='12sp'
        )
        main_layout.add_widget(self.notification_banner)

        # Chat display area
        self.scroll = ScrollView(size_hint=(1, 0.72))
        self.chat_display = Label(
            text="[color=888888]🎙️ مرحباً بك! أنا مساعد Gemini الذكي. اضغط على الشريط السفلي لتفعيل المترجم، البحث، والتحديد السريع.[/color]\n",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        self.chat_display.bind(texture_size=self._update_text_height)
        self.scroll.add_widget(self.chat_display)
        main_layout.add_widget(self.scroll)

        # Gemini Floating Rounded Bar
        gemini_bar = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=6, padding=[5, 2, 5, 2])

        self.mic_btn = Button(
            text="🎙️",
            size_hint_x=0.16,
            background_color=[0.2, 0.5, 0.9, 1],
            font_size='18sp',
            bold=True
        )
        self.mic_btn.bind(on_release=self.toggle_voice_input)

        self.text_input = TextInput(
            hint_text="اسأل Gemini...",
            multiline=False,
            background_color=[0.14, 0.15, 0.17, 1],
            foreground_color=[1, 1, 1, 1],
            padding=[12, 10, 12, 10]
        )

        self.tools_btn = Button(
            text="✨",
            size_hint_x=0.14,
            background_color=[0.3, 0.3, 0.35, 1],
            font_size='18sp'
        )
        self.tools_btn.bind(on_release=self.open_gemini_tools_overlay)

        self.send_btn = Button(
            text="إرسال",
            size_hint_x=0.22,
            background_color=[0.26, 0.53, 0.96, 1],
            bold=True
        )
        self.send_btn.bind(on_release=self.send_message)

        gemini_bar.add_widget(self.mic_btn)
        gemini_bar.add_widget(self.text_input)
        gemini_bar.add_widget(self.tools_btn)
        gemini_bar.add_widget(self.send_btn)
        main_layout.add_widget(gemini_bar)

        # Bottom Gemini Drag/Gesture Handle Line (Clickable line)
        self.overlay_handle = GeminiOverlayHandle()
        self.overlay_handle.bind(on_release=self.open_gemini_tools_overlay)
        main_layout.add_widget(self.overlay_handle)

        self.add_widget(main_layout)

    def toggle_voice_input(self, instance):
        if not voice_service.is_listening:
            self.mic_btn.background_color = [0.2, 0.8, 0.3, 1]
            self.chat_display.text += "\n[color=00ff00]🎙️ جاري الاستماع صَوْتياً... تتحدث الآن[/color]\n"
            voice_service.start_listening(None)
        else:
            self.mic_btn.background_color = [0.2, 0.5, 0.9, 1]
            voice_service.stop_listening()

    def update_user_header(self, email):
        self.user_email = email
        status = subscription_service.get_user_status(email)
        
        mode_str = "غير مقيد ⚡" if status['unrestricted'] else "قياسي 🛡️"
        self.header_label.text = f"👤 {email}\nالخطة: [{status['tier']}] | النمط: {mode_str}\nالرسائل: {status['used']}/{status['max_messages']} | الوقت: {status['remaining_time_str']}"

        if status["show_7day_warning"]:
            self.notification_banner.text = f"⚠️ تنبيه: متبقي {status['remaining_days']} أيام فقط على انتهاء اشتراكك!"
            self.notification_banner.height = 30
        else:
            self.notification_banner.text = ""
            self.notification_banner.height = 0

    def _update_text_height(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width, None)

    def send_message(self, instance):
        msg = self.text_input.text.strip()
        if not msg:
            return

        self.chat_display.text += f"\n[color=a8c7fa][b]أنت:[/b][/color] {msg}\n"
        self.text_input.text = ""

        response = chat_service.process_user_message(self.user_email, msg, i18n.current_lang)
        self.chat_display.text += f"[color=ffffff][b]Gemini ULTRA:[/b][/color] {response}\n"
        
        voice_service.speak(response)
        self.update_user_header(self.user_email)

    def open_gemini_tools_overlay(self, instance):
        """ Gemini Bottom Overlay Tools Modal (Translator, Search, Select & Analyze) """
        content = BoxLayout(orientation='vertical', padding=15, spacing=12)

        title = Label(
            text="✨ أدوات Gemini المباشرة",
            font_size='18sp',
            bold=True,
            size_hint_y=0.15,
            color=[0.65, 0.78, 0.98, 1]
        )
        content.add_widget(title)

        grid = GridLayout(cols=2, spacing=10, size_hint_y=0.7)

        btn_translate = Button(text="🌐 المترجم الفوري", background_color=[0.2, 0.5, 0.8, 1], bold=True)
        btn_search = Button(text="🔍 بحث ذكي مباشر", background_color=[0.2, 0.6, 0.7, 1], bold=True)
        btn_select = Button(text="🎯 تحديد وتحليل الشاشة", background_color=[0.6, 0.3, 0.8, 1], bold=True)
        btn_voice = Button(text="🎙️ محادثة صوتية", background_color=[0.2, 0.7, 0.4, 1], bold=True)

        popup = Popup(title="Gemini Overlay Tools", content=content, size_hint=(0.9, 0.55))

        def trigger_tool(prompt_prefix):
            popup.dismiss()
            self.text_input.text = prompt_prefix
            self.text_input.focus = True

        btn_translate.bind(on_release=lambda x: trigger_tool("ترجم الشاشة/النص التالي إلى العربية: "))
        btn_search.bind(on_release=lambda x: trigger_tool("ابحث عن ومعلومات تفصيلية حول: "))
        btn_select.bind(on_release=lambda x: trigger_tool("قم بتحديد وتفكيك وتحليل المحتوى التالي: "))
        btn_voice.bind(on_release=lambda x: (popup.dismiss(), self.toggle_voice_input(None)))

        grid.add_widget(btn_translate)
        grid.add_widget(btn_search)
        grid.add_widget(btn_select)
        grid.add_widget(btn_voice)

        content.add_widget(grid)

        close_btn = Button(text="إغلاق", size_hint_y=0.15, background_color=[0.5, 0.5, 0.5, 1])
        close_btn.bind(on_release=popup.dismiss)
        content.add_widget(close_btn)

        popup.open()

    def open_redeem_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        code_input = TextInput(
            hint_text="ادخل كود التفعيل المخصص",
            multiline=False,
            size_hint_y=0.4
        )
        status_lbl = Label(text="", size_hint_y=0.2, color=[1, 0.3, 0.3, 1])
        btn_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.4)

        popup = Popup(title="تفعيل كود الترقية", content=content, size_hint=(0.85, 0.4))

        def process_code(btn):
            code = code_input.text.strip()
            if not code:
                status_lbl.text = "يرجى كتابة الكود"
                return
            success, result = subscription_service.redeem_code(self.user_email, code)
            if success:
                status_lbl.color = [0.3, 1, 0.3, 1]
                status_lbl.text = f"تم بنجاح! ترقية الحساب إلى {result}"
                self.update_user_header(self.user_email)
            else:
                status_lbl.color = [1, 0.3, 0.3, 1]
                status_lbl.text = f"فشل: {result}"

        submit_btn = Button(text="تفعيل", background_color=[0.2, 0.8, 0.3, 1])
        submit_btn.bind(on_release=process_code)
        close_btn = Button(text="إغلاق")
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
