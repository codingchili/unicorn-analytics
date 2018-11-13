#!/usr/bin/env python

import random
import time

import unicornhathd


class Visualizer:
    """ manages a bunch of snakes. """
    
    def __init__(self):
        self.idth, self.height = unicornhathd.get_shape()
        self.pythons = set([])

    @staticmethod
    def hex_to_rgb(color):
        color = color.lstrip('#')
        color = (color[0:2], color[2:4], color[4:6])
        return [int(x, 16) for x in color]

    def add_python(self, color, length=3):
        """ adds a new snake. """
        color = Visualizer.hex_to_rgb(color)
        self.pythons.add(Python(unicornhathd, color, length=length))

    @staticmethod
    def filter_python(python):
        """ indicates if the python is alive and well. """
        return not python.remove

    def close(self):
        unicornhathd.off()

    def render(self):
        """ draws and updates all pythons in the visualizer. """
        unicornhathd.clear()
            
        for python in self.pythons:
            python.update(dir)
            python.draw()

        self.pythons = set(filter(Visualizer.filter_python, self.pythons))
        unicornhathd.show()
       

class Python:
    """ Pythons slither across the LED matrix gracefully: code adapted from Pimoroni examples. """
    
    def __init__(self, canvas, color, length=3):
        self.position = (0, random.randint(0, 16))
        self.velocity = (1, 0)

        self.remove = False
        self.grow_speed = 1
        self.length = length
        self.tail = []
        self.colour_head = (color[0], color[1], color[2])
        self.colour_tail = (int(color[0] / 3), int(color[1] / 3), int(color[2] / 3))
        self.canvas = canvas

    def get_colour(self, x, y):
        """ gets the color of the head or tail, depending on the given coordinates. """
        if (x, y) == self.position:
            return self.colour_head
        elif (x, y) in self.tail:
            return self.colour_tail

    def draw(self):
        """ renders the snake onto the unicorn hat HD. """
        none_drawable = True

        for position in [self.position] + self.tail:
            x, y = position

            if x < 16 and y < 16:
                r, g, b = self.get_colour(x, y)
                self.canvas.set_pixel(x, y, r, g, b)
                none_drawable = False

        if none_drawable:
            self.remove = True

    def update(self, direction=''):
        """ updates a snake position and optionally changes its direction. """
        x, y = self.position

        if direction == 'left' and self.velocity != (1, 0):
            self.velocity = (-1, 0)

        if direction == 'right' and self.velocity != (-1, 0):
            self.velocity = (1, 0)

        if direction == 'up' and self.velocity != (0, -1):
            self.velocity = (0, 1)

        if direction == 'down' and self.velocity != (0, 1):
            self.velocity = (0, -1)

        v_x, v_y = self.velocity
        x += v_x
        y += v_y

        if (x, y) in self.tail:
            return False

        self.tail.append(self.position)
        self.tail = self.tail[-self.length:]
        self.position = (x, y)

        return True

