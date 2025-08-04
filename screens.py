from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import json
import os

Builder.load_file('layout.kv')

class AnimalButton(Button):
    image_source = StringProperty()
    sound_source = StringProperty()

    def __init__(self, image_source, sound_source, **kwargs):
        super(AnimalButton, self).__init__(**kwargs)
        self.image_source = image_source
        self.sound_source = sound_source
        self.touch_count = 0

    def play_sound_and_animate(self):
        # Tocar som
        sound = SoundLoader.load(self.sound_source)
        if sound:
            sound.play()
        
        # Incrementar contador de toques
        self.touch_count += 1
        self.save_progress()
        
        # Feedback visual simples - mudar cor temporariamente
        original_color = self.background_color
        self.background_color = (0.4, 0.9, 0.7, 1)  # Cor mais clara
        
        # Restaurar cor original após 0.2 segundos
        def restore_color(dt):
            self.background_color = original_color
        
        Clock.schedule_once(restore_color, 0.2)

    def save_progress(self):
        # Salvar progresso em arquivo JSON
        progress_file = 'progress.json'
        progress_data = {}
        
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
            except:
                progress_data = {}
        
        # Salvar contador para este card
        card_id = f"{self.image_source}_{self.sound_source}"
        progress_data[card_id] = self.touch_count
        
        with open(progress_file, 'w') as f:
            json.dump(progress_data, f)

class MenuScreen(Screen):
    pass

class ProgressScreen(Screen):
    def __init__(self, **kwargs):
        super(ProgressScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        # Atualizar a tela quando entrar nela
        self.create_progress_view()
    
    def create_progress_view(self):
        layout = self.ids.progress_layout
        layout.clear_widgets()
        
        # Carregar dados de progresso
        progress_data = self.load_progress_data()
        
        if not progress_data:
            # Se não há dados, mostrar mensagem
            no_data_label = Label(
                text="Nenhum progresso registrado ainda.\nToque nos cards para começar!",
                font_size='18sp',
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=100
            )
            layout.add_widget(no_data_label)
        else:
            # Mostrar estatísticas
            title_label = Label(
                text="Estatísticas de Uso",
                font_size='24sp',
                bold=True,
                color=(1, 0.9, 0.3, 1),
                size_hint_y=None,
                height=60
            )
            layout.add_widget(title_label)
            
            # Ordenar por número de toques
            sorted_items = sorted(progress_data.items(), key=lambda x: x[1], reverse=True)
            
            for card_id, touch_count in sorted_items:
                # Extrair nome do card do ID
                card_name = self.get_card_name(card_id)
                
                item_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=50,
                    padding=[10, 5]
                )
                
                name_label = Label(
                    text=f"{card_name}",
                    font_size='16sp',
                    color=(1, 1, 1, 1),
                    size_hint_x=0.7
                )
                
                count_label = Label(
                    text=f"Toques: {touch_count}",
                    font_size='16sp',
                    color=(0.2, 0.8, 0.6, 1),
                    size_hint_x=0.3
                )
                
                item_layout.add_widget(name_label)
                item_layout.add_widget(count_label)
                layout.add_widget(item_layout)
    
    def load_progress_data(self):
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def get_card_name(self, card_id):
        # Mapear IDs para nomes amigáveis
        name_mapping = {
            'img/cavalo.webp_songs/cavalo.mp3': 'Cavalo',
            'img/gato.webp_songs/gato.mp3': 'Gato',
            'img/leao.webp_songs/leao.mp3': 'Leão',
            'img/elefante.webp_songs/elefante.mp3': 'Elefante',
            'img/feliz.webp_songs/feliz.mp3': 'Feliz',
            'img/triste.webp_songs/triste.mp3': 'Triste',
            'img/raiva.webp_songs/raiva.mp3': 'Raiva',
            'img/surpreso.webp_songs/surpreso.mp3': 'Surpreso',
            'img/maca.webp_songs/maca.mp3': 'Maçã',
            'img/banana.webp_songs/banana.mp3': 'Banana',
            'img/pizza.webp_songs/pizza.mp3': 'Pizza',
            'img/sorvete.webp_songs/sorvete.mp3': 'Sorvete',
            'img/camisa.webp_songs/camisa.mp3': 'Camisa',
            'img/calca.webp_songs/calca.mp3': 'Calça',
            'img/sapato.webp_songs/sapato.mp3': 'Sapato',
            'img/chapeu.webp_songs/chapeu.mp3': 'Chapéu',
            'img/telefone.webp_songs/telefone.mp3': 'Telefone',
            'img/carro.webp_songs/carro.mp3': 'Carro',
            'img/casa.webp_songs/casa.mp3': 'Casa',
            'img/livro.webp_songs/livro.mp3': 'Livro'
        }
        return name_mapping.get(card_id, card_id)

class AnimalScreen(Screen):
    def __init__(self, **kwargs):
        super(AnimalScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        # Recriar botões quando entrar na tela
        self.create_buttons()
    
    def create_buttons(self):
        layout = self.ids.layout
        # Limpa o layout antes de adicionar novos botões
        layout.clear_widgets()
        
        animals = [
            {"image": "img/cavalo.webp", "sound": "songs/cavalo.mp3"},
            {"image": "img/gato.webp", "sound": "songs/gato.mp3"},
            {"image": "img/leao.webp", "sound": "songs/leao.mp3"},
            {"image": "img/elefante.webp", "sound": "songs/elefante.mp3"},
        ]

        for animal in animals:
            button = AnimalButton(image_source=animal["image"], sound_source=animal["sound"])
            self.load_progress(button)
            layout.add_widget(button)

    def load_progress(self, button):
        # Carregar progresso salvo
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
                    card_id = f"{button.image_source}_{button.sound_source}"
                    if card_id in progress_data:
                        button.touch_count = progress_data[card_id]
            except:
                pass

class EmotionScreen(Screen):
    def __init__(self, **kwargs):
        super(EmotionScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        # Recriar botões quando entrar na tela
        self.create_buttons()
    
    def create_buttons(self):
        layout = self.ids.layout
        # Limpa o layout antes de adicionar novos botões
        layout.clear_widgets()
        
        emotions = [
            {"image": "img/feliz.webp", "sound": "songs/feliz.mp3"},
            {"image": "img/triste.webp", "sound": "songs/triste.mp3"},
            {"image": "img/raiva.webp", "sound": "songs/raiva.mp3"},
            {"image": "img/surpreso.webp", "sound": "songs/surpreso.mp3"},
        ]

        for emotion in emotions:
            button = AnimalButton(image_source=emotion["image"], sound_source=emotion["sound"])
            self.load_progress(button)
            layout.add_widget(button)

    def load_progress(self, button):
        # Carregar progresso salvo
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
                    card_id = f"{button.image_source}_{button.sound_source}"
                    if card_id in progress_data:
                        button.touch_count = progress_data[card_id]
            except:
                pass

class FoodScreen(Screen):
    def __init__(self, **kwargs):
        super(FoodScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        # Recriar botões quando entrar na tela
        self.create_buttons()
    
    def create_buttons(self):
        layout = self.ids.layout
        # Limpa o layout antes de adicionar novos botões
        layout.clear_widgets()
        
        foods = [
            {"image": "img/maca.webp", "sound": "songs/maca.mp3"},
            {"image": "img/banana.webp", "sound": "songs/banana.mp3"},
            {"image": "img/pizza.webp", "sound": "songs/pizza.mp3"},
            {"image": "img/sorvete.webp", "sound": "songs/sorvete.mp3"},
        ]

        for food in foods:
            button = AnimalButton(image_source=food["image"], sound_source=food["sound"])
            self.load_progress(button)
            layout.add_widget(button)

    def load_progress(self, button):
        # Carregar progresso salvo
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
                    card_id = f"{button.image_source}_{button.sound_source}"
                    if card_id in progress_data:
                        button.touch_count = progress_data[card_id]
            except:
                pass

class ClothesScreen(Screen):
    def __init__(self, **kwargs):
        super(ClothesScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        # Recriar botões quando entrar na tela
        self.create_buttons()
    
    def create_buttons(self):
        layout = self.ids.layout
        # Limpa o layout antes de adicionar novos botões
        layout.clear_widgets()
        
        clothes = [
            {"image": "img/camisa.webp", "sound": "songs/camisa.mp3"},
            {"image": "img/calca.webp", "sound": "songs/calca.mp3"},
            {"image": "img/sapato.webp", "sound": "songs/sapato.mp3"},
            {"image": "img/chapeu.webp", "sound": "songs/chapeu.mp3"},
        ]

        for cloth in clothes:
            button = AnimalButton(image_source=cloth["image"], sound_source=cloth["sound"])
            self.load_progress(button)
            layout.add_widget(button)

    def load_progress(self, button):
        # Carregar progresso salvo
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
                    card_id = f"{button.image_source}_{button.sound_source}"
                    if card_id in progress_data:
                        button.touch_count = progress_data[card_id]
            except:
                pass

class ObjectsScreen(Screen):
    def __init__(self, **kwargs):
        super(ObjectsScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        # Recriar botões quando entrar na tela
        self.create_buttons()
    
    def create_buttons(self):
        layout = self.ids.layout
        # Limpa o layout antes de adicionar novos botões
        layout.clear_widgets()
        
        objects = [
            {"image": "img/telefone.webp", "sound": "songs/telefone.mp3"}, # Nova imagem de telefone
            {"image": "img/carro.webp", "sound": "songs/carro.mp3"},        # Imagem de carro
            {"image": "img/casa.webp", "sound": "songs/casa.mp3"},          # Imagem de casa
            {"image": "img/livro.webp", "sound": "songs/livro.mp3"},        # Nova imagem de livro
        ]

        for obj in objects:
            button = AnimalButton(image_source=obj["image"], sound_source=obj["sound"])
            self.load_progress(button)
            layout.add_widget(button)

    def load_progress(self, button):
        # Carregar progresso salvo
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress_data = json.load(f)
                    card_id = f"{button.image_source}_{button.sound_source}"
                    if card_id in progress_data:
                        button.touch_count = progress_data[card_id]
            except:
                pass
