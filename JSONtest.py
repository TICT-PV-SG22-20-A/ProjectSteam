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
    root.title('SteamStats')

    bar_color = '#171A21'
    menu_bar_color = '#3e7ea7'
    background_color = '#1B3E54'
    box_color = '#4E6A84'
    background_color2 = '#29455B'

    steamlogo = tkinter.PhotoImage(file = 'steam.png')

    bar = tkinter.Label(root,height = 5,width = 400, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 2,sticky = 'w')
    box1 = tkinter.Label(root,width = 40,anchor = 'n', height = 30,fg = 'white', bg = background_color)
    box1.grid(row = 2, column = 1)
    tkinter.Label(root, width = 400, height = 30, bg = background_color2).grid(row = 2, column = 2)
    tkinter.Label(root, width = 40, height = 40, bg = menu_bar_color).grid(row = 3, column = 1)
    tkinter.Label(root, width = 400, height = 40, bg = box_color).grid(row = 3, column = 2)
    tkinter.Label(root, image = steamlogo, border = 0 ).place(x = 5, y = 5)

    steam_data_dict = convert_to_dict(steam_data)

    ten_first_names = '\n\nFirst 10 games in the JSON file: \n\n\n\n\n\n'

    for x in range(10):
        ten_first_names = ten_first_names + (steam_data_dict[x]['name']) + '\n'

    tkinter.Label(box1, text = ten_first_names,font = 'Motiva-Sans 12',bg = background_color, fg ='white').place(x=25,y=0)





    root.mainloop()





create_dashboard()
