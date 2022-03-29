import random
import unicornhathd

MAX_PYTHONS = 64


class Visualizer:
    """ manages a bunch of snakes. """

    def __init__(self):
        self.width, self.height = unicornhathd.get_shape()
        self.pythons = set([])
        unicornhathd.brightness(0.5)

    @staticmethod
    def hex_to_rgb(color):
        color = color.lstrip('#')
        color = (color[0:2], color[2:4], color[4:6])
        return [int(x, 16) for x in color]

    def add_python(self, color, length=3, direction='left'):
        """ adds a new snake. """
        color = Visualizer.hex_to_rgb(color)

        if len(self.pythons) < MAX_PYTHONS:
            self.pythons.add(Python(unicornhathd, color, length=length, direction=direction))
        else:
            raise Exception("python nest is full!")

    @staticmethod
    def filter_python(python):
        """ indicates if the python is alive and well. """
        return python.active

    def close(self):
        unicornhathd.off()

    def render(self):
        """ draws and updates all pythons in the visualizer. """
        unicornhathd.clear()

        for python in self.pythons:
            python.update()
            python.draw()

        self.pythons = set(filter(Visualizer.filter_python, self.pythons))
        unicornhathd.show()


class Python:
    """ Pythons slither across the LED matrix gracefully: code adapted from Pimoroni examples. """

    def __init__(self, canvas, color, length=3, direction='left'):
        self.position = Python.start_position(direction)
        self.velocity = self.get_velocity(direction)
        self.active = True
        self.length = length
        self.tail = []
        self.color_head = (color[0], color[1], color[2])
        self.color_tail = (int(color[0] / 4), int(color[1] / 4), int(color[2] / 4))
        self.canvas = canvas

    @staticmethod
    def start_position(direction):
        x, y = 0, 0

        if direction in ['left', 'right']:
            y = random.randint(0, 15)
            if direction == 'left':
                x = 15
            else:
                x = 0

        if direction in ['up', 'down']:
            x = random.randint(0, 15)
            if direction == 'up':
                y = 0
            else:
                y = 15

        return x, y

    def get_color(self, x, y):
        """ gets the color of the head or tail, depending on the given coordinates. """
        if (x, y) == self.position:
            return self.color_head
        elif (x, y) in self.tail:
            return self.color_tail

    def draw(self):
        """ renders the snake onto the unicorn hat HD. """
        none_drawable = True

        for position in [self.position] + self.tail:
            x, y = position

            if 0 <= x < 16 and 0 <= y < 16:
                r, g, b = self.get_color(x, y)
                self.canvas.set_pixel(x, y, r, g, b)
                none_drawable = False

        if none_drawable:
            self.active = False

    @staticmethod
    def get_velocity(direction):
        if direction == 'left':
            return -1, 0

        if direction == 'right':
            return 1, 0

        if direction == 'up':
            return 0, 1

        if direction == 'down':
            return 0, -1

    def update(self):
        """ updates a snake position and optionally changes its direction. """
        x, y = self.position
        v_x, v_y = self.velocity
        x += v_x
        y += v_y

        if (x, y) in self.tail:
            return False

        self.tail.append(self.position)
        self.tail = self.tail[-self.length:]
        self.position = (x, y)

        return True
