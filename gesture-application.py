# application for task 3
import pyglet
import sys
import config as c
from Game import Game


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
    if symbol == pyglet.window.key.S:
        # start game
        game.startScreen = False
        game.random_image()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)



@window.event
def on_mouse_release(x, y, button, modifiers):
    window.clear()
    if pyglet.window.mouse.LEFT:
        prediction = game.recognizer.predict_gesture(game.recognizer.model_32, game.recognizer.encoder, line)
        # if gesture is recognized as the one currently specified, increase the score and display new image
        if prediction == game.currentGesture:
            game.score += 20
            game.random_image()
        line.clear()




@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])


pyglet.app.run()
