from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import MenuScreen, AnimalScreen, EmotionScreen, FoodScreen, ClothesScreen
from kivy.config import Config

# Configuração do tamanho da janela
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '658')

class ComunicaTEAApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(AnimalScreen(name='animal_screen'))
        sm.add_widget(EmotionScreen(name='emotion_screen'))
        sm.add_widget(FoodScreen(name='food_screen'))
        sm.add_widget(ClothesScreen(name='clothes_screen'))
        return sm

if __name__ == "__main__":
    ComunicaTEAApp().run()
