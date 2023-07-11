from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
import math

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.circle_button = Button(self.root, text='circle', command=self.circle)
        self.circle_button.grid(row=0, column=2)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=3)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=4)
        
        self.save_button = Button(self.root, text='save', command=self.save)
        self.save_button.grid(row=0, column=5)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=6)

        self.clicks = 0
        self.centre_x = 0
        self.centre_y = 0
        self.radius = 0

        self.c = Canvas(self.root, bg='white', width=800, height=600)
        self.c.grid(row=1, columnspan=6)

        self.setup()
        self.root.mainloop()


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.circle_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<Button-1>', self.circle_draw)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def circle(self):
        self.activate_button(self.circle_button)
        self.circle_on = True

    def save(self):
    	filename = asksaveasfilename() 
    	self.c.update()
    	self.c.postscript(file=filename, colormode='color')

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode


    def paint(self, event):
        if(self.circle_on == False):
            self.line_width = self.choose_size_button.get()
            paint_color = 'white' if self.eraser_on else self.color
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y

    def circle_draw(self, event):
        if(self.circle_on == True):
            if(self.clicks == 0):
                self.centre_x = event.x;
                self.centre_y = event.y;
                print("C")
                print(self.centre_x, self.centre_y)

            if(self.clicks == 1):
                self.radius = math.sqrt((self.centre_x - event.x) ** 2 
                                       +(self.centre_y - event.y) ** 2)
                print("R")
                print(self.radius)

            self.clicks = 1

            self.line_width = self.choose_size_button.get()
            paint_color = 'white' if self.eraser_on else self.color
            two_pi = 2 * math.pi
            for i in range(0,100):
                self.c.create_line(self.centre_x + self.radius * math.cos(two_pi * i / 100 ),
                                   self.centre_y + self.radius * math.sin(two_pi * i / 100),
                                   self.centre_x + self.radius * math.cos(two_pi * (i+1) / 100),
                                   self.centre_y + self.radius * math.sin(two_pi * (i+1) / 100),
                                    width=self.line_width, fill = paint_color,
                                    capstyle=ROUND, smooth=TRUE,splinesteps=36)

            self.centre_x = event.x
            self.centre_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
