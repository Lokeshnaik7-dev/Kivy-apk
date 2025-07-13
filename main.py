from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import shutil, os
import openai
from openai_key import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

UPLOAD_DIR = "videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class VideoAIApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.video = Video(source="", state="stop")
        self.add_widget(self.video)

        self.filechooser = FileChooserIconView()
        self.filechooser.bind(on_selection=self.upload_video)
        self.add_widget(self.filechooser)

        self.chat_input = TextInput(hint_text="Ask something...", multiline=False, size_hint_y=0.1)
        self.add_widget(self.chat_input)

        self.chat_button = Button(text="Ask AI", size_hint_y=0.1)
        self.chat_button.bind(on_release=self.ask_ai)
        self.add_widget(self.chat_button)

        self.response_label = Label(text="AI Response will appear here", size_hint_y=0.2)
        self.add_widget(self.response_label)

    def upload_video(self, instance, selection):
        if selection:
            filename = selection[0]
            dest = os.path.join(UPLOAD_DIR, os.path.basename(filename))
            shutil.copy(filename, dest)
            self.video.source = dest
            self.video.state = "play"

    def ask_ai(self, instance):
        query = self.chat_input.text
        if query.strip():
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            self.response_label.text = response['choices'][0]['message']['content']

class MyApp(App):
    def build(self):
        return VideoAIApp()

if __name__ == "__main__":
    MyApp().run()