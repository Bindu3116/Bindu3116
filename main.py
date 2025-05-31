from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from textblob import TextBlob
import random

# 🎵 Mood-based song suggestions
mood_songs = {
    "happy": [("Happy - Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs")],
    "sad": [("Fix You - Coldplay", "https://youtu.be/k4V3Mo61fJM")],
    "angry": [("In The End - Linkin Park", "https://youtu.be/eVTXPUF4Oz4")],
    "relaxed": [("Weightless - Marconi Union", "https://youtu.be/UfcAVejslrU")],
    "neutral": [("Let It Be - The Beatles", "https://youtu.be/QDYfEBY9NM4")]
}

# 🎨 Background colors for each mood
mood_colors = {
    "happy": (1, 1, 0, 1),       # Yellow
    "sad": (0.4, 0.6, 1, 1),     # Blue
    "angry": (1, 0.3, 0.3, 1),   # Red
    "relaxed": (0.5, 1, 0.5, 1), # Green
    "neutral": (0.8, 0.8, 0.8, 1)# Gray
}

# 🧠 Sentiment analysis function
def get_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "happy"
    elif polarity > 0.1:
        return "relaxed"
    elif polarity < -0.3:
        return "angry"
    elif polarity < -0.1:
        return "sad"
    else:
        return "neutral"

# 📱 Main App Layout
class MoodBeats(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Background canvas
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # UI Elements
        self.input = TextInput(hint_text="How are you feeling today?", size_hint_y=0.2, multiline=False)
        self.result_label = Label(text="", font_size=24)
        self.song_label = Label(text="", font_size=18)
        self.link_label = Label(text="", font_size=16, markup=True)

        btn = Button(text="Get Mood Music", size_hint_y=0.2)
        btn.bind(on_press=self.analyze_mood)

        # Add widgets to layout
        self.add_widget(self.input)
        self.add_widget(btn)
        self.add_widget(self.result_label)
        self.add_widget(self.song_label)
        self.add_widget(self.link_label)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def analyze_mood(self, instance):
        text = self.input.text
        if not text.strip():
            self.result_label.text = "Please enter something!"
            return

        mood = get_mood(text)
        emoji = {
            "happy": "😄",
            "sad": "😢",
            "angry": "😡",
            "relaxed": "😌",
            "neutral": "😐"
        }[mood]

        song, link = random.choice(mood_songs[mood])

        self.result_label.text = f"Detected Mood: {mood.capitalize()} {emoji}"
        self.song_label.text = f"🎵 Suggested Song: {song}"
        self.link_label.text = f"[ref=link][color=00ffff]{link}[/color][/ref]"

        # Change background color
        r, g, b, a = mood_colors[mood]
        self.bg_color.rgba = (r, g, b, a)

# 🚀 App Runner
class MoodBeatsApp(App):
    def build(self):
        return MoodBeats()

if __name__ == '__main__':
    MoodBeatsApp().run()
