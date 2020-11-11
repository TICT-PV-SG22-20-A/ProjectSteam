import json
import tkinter

steam_data = open('steam_data.json','r')


def convert_to_dict(data):

    data = (data.read())
    data_dict = json.loads(data)

    return data_dict


def create_dashboard():
    root = tkinter.Tk()
    root.geometry('1000x1000')

    bar_color = '#171A21'
    menu_bar_color = '#3e7ea7'
    background_color = '#1B3E54'
    box_color = '#4E6A84'
    background_color2 = '#29455B'

    steamlogo = tkinter.PhotoImage(file = 'steam.png')

    bar = tkinter.Label(root,height = 5,width = 400, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 2,sticky = 'w')
    test = tkinter.Label(root, width = 40,anchor = 'n', height = 40,fg = 'white', bg = background_color)
    test.grid(row = 2, column = 1)
    tkinter.Label(root, width = 40, height = 40, bg = menu_bar_color).grid(row = 3, column = 1)
    tkinter.Label(root, width = 400, height = 40, bg = box_color).grid(row = 3, column = 2)
    tkinter.Label(root, width = 400, height = 40, bg = background_color2).grid(row = 2, column = 2)

    tkinter.Label(root, image = steamlogo, border = 0 ).place(x = 5, y = 5)

    root.mainloop()


create_dashboard()