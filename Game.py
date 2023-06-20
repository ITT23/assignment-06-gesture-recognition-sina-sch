import os
import pyglet
import random
from unistroke_model import UniStroke
import config as c

class Game:
    def __init__(self):

        # get all background images with the corresponding gesture images
        rectangleImagePath = os.path.normpath("Images/rectangle.jpg")
        self.rectangleSprite = pyglet.sprite.Sprite(img=pyglet.image.load(rectangleImagePath))
        rectangleGestureImagePath = os.path.normpath("Images/rectangle_gesture.png")
        self.rectangleGestureSprite = pyglet.sprite.Sprite(img=pyglet.image.load(rectangleGestureImagePath), x=560, y=50)

        pigtailImagePath = os.path.normpath("Images/pigtail.jpg")
        self.pigtailSprite = pyglet.sprite.Sprite(img=pyglet.image.load(pigtailImagePath))
        pigtailGestureImagePath = os.path.normpath("Images/pigtail_gesture.png")
        self.pigtailGestureSprite = pyglet.sprite.Sprite(img=pyglet.image.load(pigtailGestureImagePath), x=600, y=250)

        checkImagePath = os.path.normpath("Images/check.png")
        self.checkSprite = pyglet.sprite.Sprite(img=pyglet.image.load(checkImagePath))
        checkGestureImagePath = os.path.normpath("Images/check_gesture.png")
        self.checkGestureSprite = pyglet.sprite.Sprite(img=pyglet.image.load(checkGestureImagePath), x=720, y=150)

        self.sprites = [self.rectangleSprite, self.pigtailSprite, self.checkSprite]
        self.gestureSprites  = [self.rectangleGestureSprite, self.pigtailGestureSprite, self.checkGestureSprite]

        # initial state of the game
        self.score = 0
        self.currentGesture = None
        self.currentGestureImage = None
        self.currentImage = None
        self.startScreen = True

        # init of recognizer (LSTM)
        self.recognizer = UniStroke()


    def draw(self):
        """draw labels for the startScreen if not started yet"""
        if self.startScreen:
            pyglet.text.Label("Welcome to Harry Potter and the Philosopher's Stone!",
                              font_name='Times New Roman',
                              font_size=26,
                              x=c.Window.WINDOW_WIDTH,
                              y=c.Window.WINDOW_HEIGHT - c.Window.WINDOW_HEIGHT/3,
                              anchor_x='center',
                              anchor_y='center').draw()
            pyglet.text.Label('Trace the specified lines and help Harry learn new spells!',
                            font_name='Times New Roman',
                            font_size=18,
                            x=c.Window.WINDOW_WIDTH,
                            y=c.Window.WINDOW_HEIGHT / 2,
                            anchor_x='center',
                            anchor_y='center').draw()
            pyglet.text.Label("Press 'S' to start the game",
                              font_name='Times New Roman',
                              font_size=18,
                              x=c.Window.WINDOW_WIDTH,
                              y=c.Window.WINDOW_HEIGHT / 2 - 50,
                              anchor_x='center',
                              anchor_y='center').draw()
        elif self.currentImage:
            self.currentImage.draw()
            self.currentGestureImage.draw()
            pyglet.text.Label('Score: ' +  str(self.score),
                              font_name='Times New Roman',
                              font_size=18,
                              x=100,
                              y=c.Window.WINDOW_HEIGHT - 50,
                              anchor_x='center',
                              anchor_y='center').draw()


    def random_image(self):
        """get a random image with a gesture"""
        random_idx = random.randint(0, 2)
        self.currentImage = self.sprites[random_idx]
        self.currentGesture = c.Gestures.THREE[random_idx]
        self.currentGestureImage = self.gestureSprites[random_idx]

