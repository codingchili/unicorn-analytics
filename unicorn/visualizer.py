#!/usr/bin/env python

import os
import random
import time

from random import randint

import unicornhathd

class Visualizer:
    
    def __init__(self):
        self.idth, self.height = unicornhathd.get_shape()
        self.pythons = set([])


    def hex_to_rgb(self, hex):
        """ thanks to: https://gist.github.com/matthewkremer/3295567 """
        hex = hex.lstrip('#')
        hlen = len(hex)
        return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))


    def add_python(self, color, size=1):
        """ adds a new snake. """
        color = self.hex_to_rgb(color)
        self.pythons.add(Python(unicornhathd, color))

    
    def filter_python(self, python):
        return not python.remove


    def render(self):
        try:
            unicornhathd.clear()
                
            for python in self.pythons:
                python.update(dir)
                python.draw()

            self.pythons = set(filter(self.filter_python, self.pythons))
            unicornhathd.show()

        except KeyboardInterrupt:
            unicornhathd.off()
            pass
       

class Python:
    
    def __init__(self, canvas, color):
        self.position = (0, random.randint(0, 16))
        self.velocity = (1, 0)

        self.remove = False
        self.length = 3
        self.score = 0
        self.tail = []
        self.colour_head = (color[0], color[1], color[2])
        self.colour_tail = (color[0] / 3, color[1] / 3, color[2] / 3)
        self.canvas = canvas
        self.eaten = []
        self.grow_speed = 1

    def shrink(self):
        if self.length > 1:
            self.length -= 1
            self.tail = self.tail[-self.length:]
        if len(self.eaten) > 0:
            self.eaten.pop(0)

    def get_colour(self, x, y):
        if (x, y) == self.position:
            return self.colour_head
        elif (x, y) in self.tail:
            return self.colour_tail

    def draw(self):
        none_drawable = True

        for position in [self.position] + self.tail:
            x, y = position

            if x < 16 and y < 16:
                r, g, b = self.get_colour(x, y)
                self.canvas.set_pixel(x, y, r, g, b)
                none_drawable = False

        for idx, colour in enumerate(self.eaten):
            r, g, b = colour
            self.canvas.set_pixel(idx, 14, r >> 1, g >> 1, b >> 1)

        if none_drawable:
            self.remove = True

    def num_eaten(self):
        return len(self.eaten)

    def update(self, direction=''):
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
        c_x, c_y = self.canvas.get_shape()
        c_y -= 3 # 3 pixels along the top for score
       
        #x %= c_x
        #y %= c_y

        if (x, y) in self.tail:
            return False

        self.tail.append(self.position)
        self.tail = self.tail[-self.length:]
        self.position = (x, y)

        return True

visualizer = Visualizer()
while True:
    visualizer.render()
    time.sleep(0.1)
    visualizer.add_python('#ff00cc')
