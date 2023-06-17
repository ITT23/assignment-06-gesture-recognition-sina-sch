# create dataset for second task
import pyglet
from pyglet import shapes
import sys
import config as c
import xml.etree.ElementTree as ET

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
            name = "pigtail"
            i = "10"
            gesture = ET.Element('Gesture')
            gesture.set('Name', name + i)
            gesture.set('Number', i)
            gesture.set('NumPts', str(len(line)))
            for point in line:
                item = ET.SubElement(gesture, 'Point')
                item.set('X', str(point[0]))
                item.set('Y', str(point[1]))
            # create a new XML file with the results
            mydata = ET.tostring(gesture)
            myfile = open("dataset/" + name + i + ".xml", "wb")
            myfile.write(mydata)

        window.clear()
        line.clear()



@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])
        line_shape = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
        line_shape.draw()
 
# run the pyglet application
pyglet.app.run()