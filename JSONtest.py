import json
import tkinter
from operator import itemgetter

steam_data = open('steam_data.json','r')

bar_color = '#171A21'
menu_bar_color = '#3e7ea7'
background_color = '#1B3E54'
box_color = '#4E6A84'
background_color2 = '#29455B'

def convert_to_list(data):
    'converts the raw JSON file to a list of dictionaries'

    data = (data.read())
    data_list = json.loads(data)

    return data_list

def sort_list_alphabetically(list):
    'returns the list sorted on the name of games alphabetically'

    sorted_list = sorted(list, key= itemgetter('name'))
    return sorted_list

def create_dashboard():
    'create the dashboard'

    global root # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    root = tkinter.Tk()
    root.geometry('1200x1000')
    root.title('SteamStats')
    root.overrideredirect(True) # haalt de titlebar weg, nodig als je een overlay wilt maken

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth*2.5)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight * 2.5)

    root.geometry("+{}+{}".format(positionRight, positionDown))


    bar = tkinter.Frame(root,height = 80,width = 1200, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 3)

    global box1 # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    global box4
    global box5
    box1 = tkinter.Frame(root,width = 400, height = 400, bg = background_color)
    box1.grid(row = 2, column = 1)
    box2 = tkinter.Frame(root, width = 800, height = 400, bg = background_color2)
    box2.grid(row = 2, column = 2, columnspan = 2)
    box3 = tkinter.Frame(root, width = 400, height = 600, bg = background_color)
    box3.grid(row = 3, column = 1)
    box4 = tkinter.Frame(root, width = 400, height = 600, bg = box_color)
    box4.grid(row = 3, column = 2)
    box5 = tkinter.Frame(root, width=400, height=600, bg=menu_bar_color, )
    box5.grid(row=3, column=3)





    def terminate_window():
        root.destroy()

    tkinter.Button(bar,text = 'X', fg = 'white', bg =  bar_color,width = 2, height = 1, border = 0, command = terminate_window, activebackground=box_color).place(x = 1180, y = 0)



def fill_dashboard(list):
    'add a logo and text to the dashboard'

    global steamlogo # als ik dit logo niet global maak dan laadt hij niet bij het runnen van de mainloop
    global dislikeIcon
    global likeIcon
    steamlogo = tkinter.PhotoImage(file='steam.png')
    likeIcon = tkinter.PhotoImage(file = 'icon_thumbsUp.png')
    dislikeIcon = tkinter.PhotoImage(file ='icon_thumbsDown.png')

    def get_top_rated_games(ratings):
        ratings_dict = {}

        for x in range(len(list)):
            if(int(int(list[x]['positive_ratings'])+int(list[x]['negative_ratings'])) > int(ratings)):
                positive_percentage = (round(int(list[x]['positive_ratings']) / int((int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
                ratings_dict[list[x]['name']] = positive_percentage


        sorted_ratings_list = sorted(ratings_dict.items(), key = itemgetter(1))
        sorted_ratings_list.reverse()

        best_rated_games = 'Most liked steam games:\n\n\n'

        for x in range(12):
            best_rated_games = best_rated_games + f'{sorted_ratings_list[x][0]} - {sorted_ratings_list[x][1]}%' + '\n'

        return best_rated_games

    def get_lowest_rated_games(ratings):
        ratings_dict = {}

        for x in range(len(list)):
            if (int(int(list[x]['positive_ratings']) + int(list[x]['negative_ratings'])) > int(ratings)):
                positive_percentage = (round(int(list[x]['positive_ratings']) / int(
                    (int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
                ratings_dict[list[x]['name']] = positive_percentage

        sorted_ratings_list = sorted(ratings_dict.items(), key=itemgetter(1))

        lowest_rated_games = 'Most disliked steam games:\n\n\n'

        for x in range(12):
            lowest_rated_games = lowest_rated_games + f'{sorted_ratings_list[x][0]} - {sorted_ratings_list[x][1]}%' + '\n'

        return lowest_rated_games

    tkinter.Label(root, image=steamlogo, border=0).place(x=10, y=10)

    print(list[0])

    ten_first_names = '\n\nFirst 10 games in the JSON file: \n\n\n\n'


    for x in range(10):
        ten_first_names = ten_first_names + (list[x]['name']) + '\n'



    global lowest_rated_textbox


    lowest_rated_textbox = tkinter.Text(box5, height=30, width=43, bg=menu_bar_color, fg='white', font='Arial 12', wrap='word')
    lowest_rated_textbox.place(x=5, y=5)
    lowest_rated_textbox.tag_configure("center", justify='center')
    lowest_rated_textbox.insert(tkinter.END, get_lowest_rated_games(50000), 'center')
    tkinter.Label(box5, text='Minimum amount of ratings:', bg=menu_bar_color, fg='white').place(x=120, y=360)
    lowest_rated_games_entry = tkinter.Entry(box5, width=10)
    lowest_rated_games_entry.place(x=170, y=390)


    def refresh_lowest_rated_games():
        entry = lowest_rated_games_entry.get()

        try:
            if entry  == '':
                entry = 50000

            if (int(entry) > 100000):
                entry = 100000


            lowest_rated_textbox.delete(1.0, tkinter.END)
            lowest_rated_textbox.insert(tkinter.END, get_lowest_rated_games(entry), 'center')

        except ValueError:
            print("not a number")


    tkinter.Button(box5,width =5, command = refresh_lowest_rated_games, text = 'reload').place(x = 180, y = 430)





    global top_rated_textbox

    top_rated_textbox = tkinter.Text(box4, height = 30, width = 43, bg = box_color, fg = 'white',font='Arial 12', wrap = 'word')
    top_rated_textbox.place(x = 5, y = 5)
    top_rated_textbox.tag_configure("center", justify='center')
    top_rated_textbox.insert(tkinter.END, get_top_rated_games(50000), 'center')
    tkinter.Label(box4, text = 'Minimum amount of ratings:', bg = box_color, fg = 'white').place(x = 120, y =360)
    top_rated_games_entry = tkinter.Entry(box4, width = 10)
    top_rated_games_entry.place(x = 170, y = 390)



    def refresh_top_rated_games():
        entry = top_rated_games_entry.get()

        try:
            if entry  == '':
                entry = 50000

            if (int(entry) > 100000):
                entry = 100000


            top_rated_textbox.delete(1.0, tkinter.END)
            top_rated_textbox.insert(tkinter.END, get_top_rated_games(entry), 'center')

        except ValueError:
            print("not a number")




    tkinter.Button(box4,width =5, command = refresh_top_rated_games, text = 'reload').place(x = 180, y = 430)
    entry_text = tkinter.Label(box1, text=ten_first_names, font='Arial 12', bg=background_color, fg='white')
    entry_text.pack(padx=85, pady=44)






def launch_dashboard():
    root.mainloop()





create_dashboard()
fill_dashboard(convert_to_list(steam_data))
launch_dashboard()

