from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from random import randint, choice

class Fruit(Widget):
    def __init__(self, color, **kwargs):
        super(Fruit, self).__init__(**kwargs)
        self.size = (30, 30)  # Tamaño de la fruta
        self.color = color  # Color de la fruta
        with self.canvas:
            Color(*self.color)  # Aplica el color
            self.fruit = Ellipse(pos=self.pos, size=self.size)

    def update(self, speed):
        self.y -= speed  # Velocidad de caída
        self.fruit.pos = self.pos  # Actualiza la posición de la fruta
        if self.y < 0:
            self.parent.remove_widget(self)  # Elimina la fruta si cae

class Basket(Widget):
    def __init__(self, color, **kwargs):
        super(Basket, self).__init__(**kwargs)
        self.size = (100, 20)  # Tamaño del cesto
        self.color = color  # Color del cesto
        with self.canvas:
            Color(*self.color)  # Aplica el color
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_touch_move(self, touch):
        if touch.x < self.parent.width and touch.x > 0:
            self.x = touch.x - self.width / 2
            self.rect.pos = self.pos  # Actualiza la posición del cesto

class CatchGame(Widget):
    def __init__(self, **kwargs):
        super(CatchGame, self).__init__(**kwargs)
        self.fruit_colors = [
            (1, 0, 0),    # Rojo
            (0, 1, 0),    # Verde
            (0, 0, 1),    # Azul
            (1, 1, 0),    # Amarillo
            (1, 0.5, 0)   # Naranja
        ]
        self.basket_color = choice(self.fruit_colors)  # Color aleatorio para el cesto
        self.basket = Basket(color=self.basket_color)
        self.add_widget(self.basket)
        self.fruits = []
        self.score = 0  # Inicializa la puntuación
        self.speed = 7  # Velocidad inicial de caída
        self.score_label = Label(text=f'Score: {self.score}', size_hint=(1, 0.1), pos_hint={'top': 1})
        self.add_widget(self.score_label)
        Clock.schedule_interval(self.spawn_fruit, 1.0)  # Cada segundo

    def spawn_fruit(self, dt):
        fruit_color = choice(self.fruit_colors)  # Elige un color de fruta de la lista
        fruit = Fruit(color=fruit_color)  # Crea la fruta con el color elegido
        fruit.x = randint(0, self.width - fruit.width)  # Posición aleatoria en X
        fruit.y = self.height  # Posición inicial en Y
        self.fruits.append(fruit)
        self.add_widget(fruit)

    def update(self, dt):
        for fruit in self.fruits:
            fruit.update(self.speed)  # Actualiza la caída de la fruta con la velocidad
            if fruit.y < self.basket.y + self.basket.height and fruit.collide_widget(self.basket):
                # Comprueba si los colores son iguales
                if fruit.color == self.basket.color:
                    self.score += 1  # Aumenta la puntuación
                    self.score_label.text = f'Score: {self.score}'  # Actualiza la etiqueta de puntuación
                    self.speed += 0.5  # Aumenta la velocidad de caída cada vez que se atrapa una fruta
                else:
                    self.game_over()  # Fin del juego si el color no coincide

                self.fruits.remove(fruit)
                self.remove_widget(fruit)  # Elimina la fruta atrapada

            elif fruit.y < 0:
                self.fruits.remove(fruit)  # Elimina la fruta si cae
                self.remove_widget(fruit)  # Elimina la fruta si cae

    def game_over(self):
        # Muestra un mensaje de Game Over con la puntuación final
        content = Label(text=f'¡Fin del juego!\nPuntuación final: {self.score}', size_hint=(0.8, 0.4))
        popup = Popup(title='Game Over', content=content, size_hint=(0.8, 0.4))
        popup.open()
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 2)  # Cierra el juego después de 2 segundos

class CatchApp(App):
    def build(self):
        game = CatchGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # Actualiza la pantalla 60 veces por segundo
        return game

if __name__ == '__main__':
    CatchApp().run()
