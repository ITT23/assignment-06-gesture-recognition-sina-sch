# gesture input program for first task
import pyglet
from pyglet import shapes
from recognizer import Recognizer
import sys
import config as c

recognizer = Recognizer(c.Gestures.FIVE)
recognizer.main()

title = "OneDollarRecognizer"
window = pyglet.window.Window(c.Window.WINDOW_WIDTH, c.Window.WINDOW_HEIGHT, title)

line = []
result_text = pyglet.text.Label("Gesture:   ", x=c.Window.WINDOW_WIDTH-150, y=c.Window.WINDOW_HEIGHT-20, anchor_x='center', anchor_y='center', font_size=20)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        line.clear()
        window.clear()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)

@window.event
def on_mouse_release(x, y, button, modifiers):
    window.clear()
    if button & pyglet.window.mouse.LEFT:
        if len(line) > 0:
            result, score = recognizer.recognize(line)
            print("RESULT", result[0], score)
            line.clear()
            result_text.text = "Gesture:   " + result[0]
            result_text.draw()
            result_text.text = "Gesture:   "




@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])
        point = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
        point.draw()

 
pyglet.app.run()