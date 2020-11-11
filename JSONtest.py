import json
import tkinter
from operator import itemgetter




steam_data = open('steam_data.json','r')


def convert_to_list(data):
    'converts the raw JSON file to a list of dictionaries'

    data = (data.read())
    data_list = json.loads(data)

    return data_list

def sort_list_alphabetically(list):
    'returns the list sorted on the name of keys alphabetically'

    sortedList = sorted(list, key= itemgetter('name'))
    return sortedList

def create_dashboard():
    'create the dashboard'

    global root # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    root = tkinter.Tk()
    root.geometry('1000x1000')
    root.title('SteamStats')
    root.overrideredirect(True) # haalt de titlebar weg, nodig voor een overlay denk ik

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth*2.5)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight * 2.5)

    root.geometry("+{}+{}".format(positionRight, positionDown))


    bar_color = '#171A21'
    menu_bar_color = '#3e7ea7'
    background_color = '#1B3E54'
    box_color = '#4E6A84'
    background_color2 = '#29455B'

    bar = tkinter.Label(root,height = 5,width = 400, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 2,sticky = 'w')

    global box1 # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie

    box1 = tkinter.Label(root,width = 40,anchor = 'n', height = 30,fg = 'white', bg = background_color)
    box1.grid(row = 2, column = 1)
    box2 = tkinter.Label(root, width = 400, height = 30, bg = background_color2)
    box2.grid(row = 2, column = 2)
    box3 = tkinter.Label(root, width = 40, height = 40, bg = menu_bar_color)
    box3.grid(row = 3, column = 1)
    box4 = tkinter.Label(root, width = 400, height = 40, bg = box_color)
    box4.grid(row = 3, column = 2)

    def terminate_window():
        root.destroy()

    tkinter.Button(bar,text = 'X', fg = 'white', bg =  bar_color,width = 2, height = 1, border = 0, command = terminate_window, activebackground=box_color).place(x = 975, y = 0)





def fill_dashboard(list):
    'add a logo and text to the dashboard'


    background_color = '#1B3E54'
    steamlogo = tkinter.PhotoImage(file = 'steam.png')

    ten_first_names = '\n\nFirst 10 games in the JSON file: \n\n\n\n\n\n'

    for x in range(10):
        ten_first_names = ten_first_names + (list[x]['name']) + '\n'

    tkinter.Label(box1, text = ten_first_names,font = 'Arial 12',bg = background_color, fg ='white').place(x=25,y=0)
    tkinter.Label(root, image = steamlogo, border = 0 ).place(x = 10, y = 10)


    root.mainloop() # als ik de mainloop start buiten de functie waar het logo wordt geplaatst, dan laadt het logo niet.





create_dashboard()
fill_dashboard(convert_to_list(steam_data))

