# application for task 3
import pyglet
from pyglet import shapes
from recognizer import Recognizer
import sys
import config as c
from pynput.keyboard import Key, Controller
from Game import Game


keyboard = Controller()

# recognizer = Recognizer()
# recognizer.main()

title = "HarryPotter"
window = pyglet.window.Window(c.Window.WINDOW_WIDTH * 2, c.Window.WINDOW_HEIGHT, title)

game = Game()

line = []

@window.event
def on_draw():
    window.clear()
    game.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        line.clear()
    elif symbol == pyglet.window.key.S:
        game.startScreen = False
        game.random_image()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)



@window.event
def on_mouse_release(x, y, button, modifiers):
    window.clear()
    if pyglet.window.mouse.LEFT:
        result, score = game.recognizer.recognize(line)
        print(result[0])
        if result[0] == game.currentGesture:
            print("success")
            game.random_image()
        line.clear()




@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    game.draw()
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])
        point = shapes.Circle(x, y, radius=5, color=(255, 225, 255), batch=game.batch)
        point.draw()


pyglet.app.run()
