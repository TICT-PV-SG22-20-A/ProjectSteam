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

    sorted_list = sorted(list, key= itemgetter('name'))
    return sorted_list

def create_dashboard():
    'create the dashboard'

    global root # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    root = tkinter.Tk()
    root.geometry('1000x1000')
    root.title('SteamStats')
    root.overrideredirect(True) # haalt de titlebar weg, nodig als je een overlay wilt maken

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

    bar = tkinter.Frame(root,height = 80,width = 1000, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 2,sticky = 'w')

    global box1 # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie

    box1 = tkinter.Frame(root,width = 400, height = 400, bg = background_color)
    box1.grid(row = 2, column = 1)
    box2 = tkinter.Frame(root, width = 600, height = 400, bg = background_color2)
    box2.grid(row = 2, column = 2)
    box3 = tkinter.Frame(root, width = 400, height = 600, bg = menu_bar_color)
    box3.grid(row = 3, column = 1)
    box4 = tkinter.Frame(root, width = 600, height = 600, bg = box_color)
    box4.grid(row = 3, column = 2)


    def terminate_window():
        root.destroy()

    tkinter.Button(bar,text = 'X', fg = 'white', bg =  bar_color,width = 2, height = 1, border = 0, command = terminate_window, activebackground=box_color).place(x = 980, y = 0)



def fill_dashboard(list):
    'add a logo and text to the dashboard'

    global steamlogo # als ik dit logo niet global maak dan laadt hij niet bij het runnen van de mainloop
    steamlogo = tkinter.PhotoImage(file='steam.png')

    tkinter.Label(root, image=steamlogo, border=0).place(x=10, y=10)

    background_color = '#1B3E54'

    ten_first_names = '\n\nFirst 10 games in the JSON file: \n\n\n\n'

    for x in range(10):
        ten_first_names = ten_first_names + (list[x]['name']) + '\n'

    entry_text = tkinter.Label(box1, text = ten_first_names,font = 'Arial 12',bg = background_color, fg ='white')
    entry_text.pack(padx=85, pady =44)


def launch_dashboard():
    root.mainloop()


create_dashboard()
fill_dashboard(convert_to_list(steam_data))
launch_dashboard()

