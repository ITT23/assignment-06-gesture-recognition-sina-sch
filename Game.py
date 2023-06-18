import os
import pyglet
import random
from recognizer import Recognizer
import config as c

class Game:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        starImagePath = os.path.normpath("Images/star.jpg")
        starImage = pyglet.image.load(starImagePath)

        pigtailImagePath = os.path.normpath("Images/pigtail.jpg")
        pigtailImage = pyglet.image.load(pigtailImagePath)

        checkImagePath = os.path.normpath("Images/check.png")
        checkImage = pyglet.image.load(checkImagePath)

        self.starSprite = pyglet.sprite.Sprite(img=starImage, batch=self.batch)
        self.pigtailSprite = pyglet.sprite.Sprite(img=pigtailImage, batch=self.batch)
        self.checkSprite = pyglet.sprite.Sprite(img=checkImage, batch=self.batch)
        self.sprites = [self.starSprite, self.pigtailSprite, self.checkSprite]

        self.currentGesture = None
        self.currentImage = None
        self.startScreen = True

        self.recognizer = Recognizer(c.Gestures.THREE)
        self.recognizer.main()


    def draw(self):
        """draw labels for the startScreen if not started yet"""
        if self.startScreen:
            pyglet.text.Label("Welcome to Harry Potter and the Philosopher's Stone",
                              font_name='Times New Roman',
                              font_size=26,
                              x=c.Window.WINDOW_WIDTH,
                              y=c.Window.WINDOW_HEIGHT - c.Window.WINDOW_HEIGHT/3,
                              anchor_x='center',
                              anchor_y='center',
                              batch=self.batch).draw()
            pyglet.text.Label('Your task is to draw the shape specified in the left corner.',
                            font_name='Times New Roman',
                            font_size=18,
                            x=c.Window.WINDOW_WIDTH,
                            y=c.Window.WINDOW_HEIGHT / 2,
                            anchor_x='center',
                            anchor_y='center',
                            batch=self.batch).draw()
            pyglet.text.Label("Press 'S' to start the game",
                              font_name='Times New Roman',
                              font_size=18,
                              x=c.Window.WINDOW_WIDTH,
                              y=c.Window.WINDOW_HEIGHT / 2 - 50,
                              anchor_x='center',
                              anchor_y='center',
                              batch=self.batch).draw()
        elif self.currentImage:
            self.currentImage.draw()
            pyglet.text.Label("Draw a " + self.currentGesture + '!',
                              font_name='Times New Roman',
                              font_size=18,
                              x=100,
                              y=c.Window.WINDOW_HEIGHT - 50,
                              anchor_x='center',
                              anchor_y='center',
                              batch=self.batch).draw()


    def random_image(self):
        random_idx = random.randint(0, 2)
        self.currentImage = self.sprites[random_idx]
        self.currentGesture = c.Gestures.THREE[random_idx]

