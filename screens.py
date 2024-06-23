from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_file('layout.kv')

class AnimalButton(Button):
    image_source = StringProperty()
    sound_source = StringProperty()

    def __init__(self, image_source, sound_source, **kwargs):
        super(AnimalButton, self).__init__(**kwargs)
        self.image_source = image_source
        self.sound_source = sound_source

    def play_sound(self, instance):
        sound = SoundLoader.load(self.sound_source)
        if sound:
            sound.play()

class MenuScreen(Screen):
    pass

class AnimalScreen(Screen):
    def __init__(self, **kwargs):
        super(AnimalScreen, self).__init__(**kwargs)
        layout = self.ids.layout
        animals = [
            {"image": "img/cavalo.webp", "sound": "songs/cavalo.mp3"},
            {"image": "img/gato.webp", "sound": "songs/gato.mp3"},
            {"image": "img/leao.webp", "sound": "songs/leao.mp3"},
            {"image": "img/elefante.webp", "sound": "songs/elefante.mp3"},
        ]

        for animal in animals:
            button = AnimalButton(image_source=animal["image"], sound_source=animal["sound"])
            button.bind(on_press=button.play_sound)
            layout.add_widget(button)

class EmotionScreen(Screen):
    def __init__(self, **kwargs):
        super(EmotionScreen, self).__init__(**kwargs)
        layout = self.ids.layout
        emotions = [
            {"image": "img/feliz.webp", "sound": "songs/feliz.mp3"},
            {"image": "img/triste.webp", "sound": "songs/triste.mp3"},
            {"image": "img/raiva.webp", "sound": "songs/raiva.mp3"},
            {"image": "img/surpreso.webp", "sound": "songs/surpreso.mp3"},
        ]

        for emotion in emotions:
            button = AnimalButton(image_source=emotion["image"], sound_source=emotion["sound"])
            button.bind(on_press=button.play_sound)
            layout.add_widget(button)

class FoodScreen(Screen):
    def __init__(self, **kwargs):
        super(FoodScreen, self).__init__(**kwargs)
        layout = self.ids.layout
        foods = [
            {"image": "img/maca.webp", "sound": "songs/maca.mp3"},
            {"image": "img/banana.webp", "sound": "songs/banana.mp3"},
            {"image": "img/pizza.webp", "sound": "songs/pizza.mp3"},
            {"image": "img/sorvete.webp", "sound": "songs/sorvete.mp3"},
        ]

        for food in foods:
            button = AnimalButton(image_source=food["image"], sound_source=food["sound"])
            button.bind(on_press=button.play_sound)
            layout.add_widget(button)

class ClothesScreen(Screen):
    def __init__(self, **kwargs):
        super(ClothesScreen, self).__init__(**kwargs)
        layout = self.ids.layout
        clothes = [
            {"image": "img/camisa.webp", "sound": "songs/camisa.mp3"},
            {"image": "img/calca.webp", "sound": "songs/calca.mp3"},
            {"image": "img/sapato.webp", "sound": "songs/sapato.mp3"},
            {"image": "img/chapeu.webp", "sound": "songs/chapeu.mp3"},
        ]

        for cloth in clothes:
            button = AnimalButton(image_source=cloth["image"], sound_source=cloth["sound"])
            button.bind(on_press=button.play_sound)
            layout.add_widget(button)
