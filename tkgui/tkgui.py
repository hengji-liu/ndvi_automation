# try to use a window, so the user can click on the img to chose x,y
# also type in other numeric values to see the change instantly
from tkinter import *
from PIL import ImageTk, Image
from skimage.io import imread, imsave
from skimage.transform import resize


def mk_ori_img():
    image = imread(fname=r"..\IA Watson_15_August_16_E22 section_raw.jpg")
    imsave(fname=r"..\tmp\raw.jpg", arr=resize(image=image, output_shape=(512, 512)))


root = Tk()
mk_ori_img()
img = ImageTk.PhotoImage(Image.open(r'..\tmp\raw.jpg'))

# img
img_lbl = Label(root, image=img)
img_lbl.grid(row=0, columnspan=5)

# change quadrant
qd1 = Button(root, text="Quadrant 1")
qd1.grid(row=1, column=0)
qd2 = Button(root, text="Quadrant 2")
qd2.grid(row=1, column=1)
qd3 = Button(root, text="Quadrant 3")
qd3.grid(row=1, column=2)
qd4 = Button(root, text="Quadrant 4")
qd4.grid(row=1, column=3)
zoomout = Button(root, text="Zoom Out")
zoomout.grid(row=1, column=4)

# x, y
x = Label(root, text='x')
x.grid(row=2, column=0, sticky=E)
x_input = Entry(root)
x_input.grid(row=2, column=1)

y = Label(root, text='y')
y.grid(row=2, column=2, sticky=E)
y_input = Entry(root)
y_input.grid(row=2, column=3)

# net_x, net_y
net_x = Label(root, text='net_x')
net_x.grid(row=3, column=0, sticky=E)
net_x_input = Entry(root)
net_x_input.grid(row=3, column=1)

net_y = Label(root, text='net_y')
net_y.grid(row=3, column=2, sticky=E)
net_y_input = Entry(root)
net_y_input.grid(row=3, column=3)

# plot_x, plot_y
plot_x = Label(root, text='plot_x')
plot_x.grid(row=4, column=0, sticky=E)
plot_x_input = Entry(root)
plot_x_input.grid(row=4, column=1)

plot_y = Label(root, text='plot_y')
plot_y.grid(row=4, column=2, sticky=E)
plot_y_input = Entry(root)
plot_y_input.grid(row=4, column=3)

# offset_x, offset_y
offset_x = Label(root, text='offset_x')
offset_x.grid(row=5, column=0, sticky=E)
offset_x_input = Entry(root)
offset_x_input.grid(row=5, column=1)

offset_y = Label(root, text='offset_y')
offset_y.grid(row=5, column=2, sticky=E)
offset_y_input = Entry(root)
offset_y_input.grid(row=5, column=3)

# angle_deg
angle = Label(root, text='angle_deg')
angle.grid(row=6, column=0, sticky=E)
angle_input = Entry(root)
angle_input.grid(row=6, column=1)

# preview button
qd1 = Button(root, text="Preview")
qd1.grid(row=6, column=2, columnspan=3, sticky='we')

# status bar
status = Label(root, text="done", bd=1, relief=SUNKEN, anchor=W)
status.grid(row=18, columnspan=5, sticky='we')

root.mainloop()
