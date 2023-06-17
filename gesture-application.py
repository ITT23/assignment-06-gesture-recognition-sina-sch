# application for task 3
import pyglet
from pyglet import shapes
from recognizer import Recognizer
import sys
import config as c
from pynput.keyboard import Key, Controller


keyboard = Controller()

recognizer = Recognizer()
recognizer.main()


width = c.Window.WINDOW_WIDTH
height = c.Window.WINDOW_HEIGHT
title = "RockPaperScissors"
window = pyglet.window.Window(width, height, title)

line = []

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        line.clear()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)



@window.event
def on_mouse_release(x, y, button, modifiers):
    window.clear()
    if pyglet.window.mouse.LEFT:
        result = recognizer.recognize(line)
        print("RESULT", result)
        line.clear()
        print(line)

        gesture = result[0]
        if gesture == "caret":
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
        elif gesture == "v":
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
        elif gesture == "rectangle":
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)



@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if pyglet.window.mouse.LEFT:

        line.append([int(x), int(y)])#recognizer.get_point(int(x), int(height-y)))
        #print(line)
        #line_shape = pyglet.shapes.Line(x, y, x+dx, y+dy, width=1, color=(255, 255, 255))
        point = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
        point.draw()


pyglet.app.run()
