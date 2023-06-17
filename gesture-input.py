# gesture input program for first task
import pyglet
from pyglet import shapes
from recognizer import Recognizer
import sys
import config as c

recognizer = Recognizer()
recognizer.main()

title = "OneDollarRecognizer"
window = pyglet.window.Window(c.Window.WINDOW_WIDTH, c.Window.WINDOW_HEIGHT, title)

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
    if button & pyglet.window.mouse.LEFT:
        if len(line) > 0:
            result = recognizer.recognize(line)
            print("RESULT", result[0])
            pyglet.text.Label(result[0],
                        font_name='Times New Roman',
                        font_size=36,
                        x=c.Window.WINDOW_WIDTH / 2,
                        y=c.Window.WINDOW_HEIGHT - c.Window.WINDOW_HEIGHT/3,
                        anchor_x='center',
                        anchor_y='center',
                        color=(255, 255, 255, 1)).draw()

        window.clear()
        line.clear()



@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])#recognizer.get_point(int(x), int(height-y)))
        #print(line)
        #line_shape = pyglet.shapes.Line(x, y, x+dx, y+dy, width=1, color=(255, 255, 255))
        line_shape = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
        line_shape.draw()
 
# run the pyglet application
pyglet.app.run()