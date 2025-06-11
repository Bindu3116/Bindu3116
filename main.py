from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import webbrowser
from textblob import TextBlob
import random
import os

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
    "happy": (0.85, 0.65, 0.13, 1),
    "sad": (0.4, 0.6, 1, 1),
    "angry": (1, 0.3, 0.3, 1),
    "relaxed": (0.5, 1, 0.5, 1),
    "neutral": (0.8, 0.8, 0.8, 1)
}

# 🧠 Sentiment analysis to determine mood
def get_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    lowered = text.lower()

    # 🔁 Keyword override logic
    if "relaxed" in lowered or "calm" in lowered or "peaceful" in lowered:
        return "relaxed"

    if polarity > 0.5:
        return "happy"
    elif polarity > 0.0:
        return "relaxed"
    elif polarity < -0.6:
        return "angry"
    elif polarity < -0.2:
        return "sad"
    else:
        return "neutral"


# 📱 Main app layout
class MoodBeats(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # UI widgets
        self.input = TextInput(hint_text="How are you feeling today?", size_hint_y=0.2, multiline=False)
        self.emoji_image = Image(size_hint_y=0.3)
        self.result_label = Label(text="", font_size=24, size_hint_y=0.2, color=(1, 1, 1, 1))
        self.song_label = Label(text="", font_size=18, size_hint_y=0.2, color=(1, 1, 1, 1))
        self.link_label = Label(text="", font_size=16, markup=True, size_hint_y=0.1)
        self.link_label.bind(on_ref_press=self.open_link)

        btn = Button(text="Get Mood Music", size_hint_y=0.2)
        btn.bind(on_press=self.analyze_mood)

        # Add to layout
        self.add_widget(self.input)
        self.add_widget(btn)
        self.add_widget(self.emoji_image)
        self.add_widget(self.result_label)
        self.add_widget(self.song_label)
        self.add_widget(self.link_label)

        self.current_song_link = ""

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def open_link(self, instance, ref):
        if self.current_song_link:
            webbrowser.open(self.current_song_link)

    def analyze_mood(self, instance):
        text = self.input.text.strip()
        if not text:
            self.result_label.text = "Please enter something!"
            return

        mood = get_mood(text)
        song, link = random.choice(mood_songs[mood])

        self.result_label.text = f"Detected Mood: {mood.capitalize()}"
        self.song_label.text = f"🎵 Song Suggestion:\n{song}"

        # Adjust text color for better visibility on bright backgrounds
        if mood == "happy":
            self.result_label.color = (0, 0, 0, 1)  # black
            self.song_label.color = (0, 0, 0, 1)
            self.link_label.color = (0, 0, 1, 1)    # dark blue
        else:
            self.result_label.color = (1, 1, 1, 1)  # white
            self.song_label.color = (1, 1, 1, 1)
            self.link_label.color = (0, 1, 1, 1)    # cyan
        self.link_label.text = f"[ref=link][color=00ffff]{link}[/color][/ref]"
        self.current_song_link = link

        # Change background color
        self.bg_color.rgba = mood_colors[mood]

        # Load emoji image safely (works in .app too)
        base_path = os.path.abspath(os.path.dirname(__file__))
        emoji_path = os.path.join(base_path, "emoji", f"{mood}.png")

        if os.path.exists(emoji_path):
            self.emoji_image.source = emoji_path
            self.emoji_image.reload()
        else:
            print(f"⚠️ Emoji image not found: {emoji_path}")
            self.emoji_image.source = ""

# 🚀 Launch the app
class MoodBeatsApp(App):
    def build(self):
        return MoodBeats()

if __name__ == '__main__':
    MoodBeatsApp().run()
