import json
import tkinter
from operator import itemgetter
import matplotlib.pyplot as plt




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
    root.geometry('1400x1200')
    root.title('SteamStats')
    root.overrideredirect(True) # haalt de titlebar weg, nodig als je een overlay wilt maken
    #root.attributes('-fullscreen', True)

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    root.update()

    positionRight = int(root.winfo_screenwidth() / 2 - 0.5*root.winfo_width())
    positionDown = int(root.winfo_screenheight() / 2 - 0.5 * root.winfo_height())

    root.geometry("+{}+{}".format(positionRight, positionDown))


    bar = tkinter.Frame(root,height = 80,width = 1400, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 3)

    global box1 # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    global box2
    global box3
    global box4
    global box5
    box1 = tkinter.Frame(root,width = 600, height = 600, bg = background_color)
    box1.grid(row = 2, column = 1)
    box2 = tkinter.Frame(root, width = 800, height = 600, bg = background_color2)
    box2.grid(row = 2, column = 2, columnspan = 2)
    box3 = tkinter.Frame(root, width = 600, height = 700, bg = background_color)
    box3.grid(row = 3, column = 1)
    box4 = tkinter.Frame(root, width = 400, height = 700, bg = box_color)
    box4.grid(row = 3, column = 2)
    box5 = tkinter.Frame(root, width=400, height=700, bg=menu_bar_color, )
    box5.grid(row=3, column=3)



    def terminate_window():
        root.destroy()

    tkinter.Button(bar,text = 'X', fg = 'white', bg =  bar_color,width = 2, height = 1, border = 0, command = terminate_window, activebackground=box_color).place(x = 1380, y = 0)

print()

def fill_dashboard(list):
    'add data to the dashboard'

    def get_genre_piechart(limit):
        genre_tags = []
        for entry in list:
            tags = (entry['steamspy_tags'].split(';'))
            for tag in tags:
                genre_tags.append(tag)

        genre_tags_dict = {}
        for x in set(genre_tags):
            genre_tags_dict[x] = genre_tags.count(x)

        genre_tags_list = sorted(genre_tags_dict.items(), key=itemgetter(1))
        genre_tags_list.reverse()

        genre_tags_list = genre_tags_list[:limit]

        tags = []
        count = []

        for entry in genre_tags_list:
            tags.append(entry[0])
            count.append(entry[1])

        labels = tags
        sizes = count

        fig1, ax1 = plt.subplots()

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        def make_autopct():
            def my_autopct(pct):
                total = sum(sizes)
                val = int(round(pct * total / 100.0))
                return '{p:.0f}%\n({v:d})'.format(p=pct, v=val)

            return my_autopct

        colors = ['#171A21', '#3e7ea7', '#1B3E54', '#4E6A84','#29455B', 'grey']




        ax1.pie(sizes, labels=labels, autopct=make_autopct(),
                shadow=True, startangle=90, colors = colors)
        ax1.axis('equal')
        plt.title(f"Steam genre distribution ",
                  bbox={'facecolor': '0.8', 'pad': 3}, loc='left')

        plt.savefig('piechart.png')

    get_genre_piechart(5)
    global steamlogo # als ik dit logo niet global maak dan laadt hij niet bij het runnen van de mainloop
    global dislikeIcon
    global likeIcon
    global pieChart
    steamlogo = tkinter.PhotoImage(file='steam.png')
    likeIcon = tkinter.PhotoImage(file = 'icon_thumbsUp.png')
    dislikeIcon = tkinter.PhotoImage(file ='icon_thumbsDown.png')
    pieChart = tkinter.PhotoImage(file='piechart.png')

    def get_top_rated_games(ratings):
        'geeft een string van de hoogst beordeelde games terug'

        ratings_dict = {}

        for x in range(len(list)):
            if(int(int(list[x]['positive_ratings'])+int(list[x]['negative_ratings'])) > int(ratings)):
                positive_percentage = (round(int(list[x]['positive_ratings']) / int((int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
                ratings_dict[list[x]['name']] = positive_percentage


        sorted_ratings_list = sorted(ratings_dict.items(), key = itemgetter(1))
        sorted_ratings_list.reverse()

        best_rated_games = '\n\nMost liked steam games:\n\n\n'

        for x in range(12):
            best_rated_games = best_rated_games + f'{sorted_ratings_list[x][0]} - {sorted_ratings_list[x][1]}%' + '\n'

        return best_rated_games

    def get_lowest_rated_games(ratings):
        'geeft een string van de laagst beordeelde games terug'
        ratings_dict = {}

        for x in range(len(list)):
            if (int(int(list[x]['positive_ratings']) + int(list[x]['negative_ratings'])) > int(ratings)):
                positive_percentage = (round(int(list[x]['positive_ratings']) / int(
                    (int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
                ratings_dict[list[x]['name']] = positive_percentage

        sorted_ratings_list = sorted(ratings_dict.items(), key=itemgetter(1))

        lowest_rated_games = '\n\nMost disliked steam games:\n\n\n'

        for x in range(12):
            lowest_rated_games = lowest_rated_games + f'{sorted_ratings_list[x][0]} - {sorted_ratings_list[x][1]}%' + '\n'

        return lowest_rated_games

    tkinter.Label(root, image=steamlogo, border=0).place(x=10, y=10)

    ten_first_names = '\n\nFirst 10 games in the JSON file: \n\n\n\n'


    for x in range(10):
        ten_first_names = ten_first_names + (list[x]['name']) + '\n'

    global lowest_rated_textbox


    lowest_rated_textbox = tkinter.Text(box5, height=28, width=43, bg=menu_bar_color, fg='white', font='Arial 12', wrap='word')
    lowest_rated_textbox.place(x=5, y=6)
    lowest_rated_textbox.tag_configure("center", justify='center')
    lowest_rated_textbox.insert(tkinter.END, get_lowest_rated_games(50000), 'center')



    def refresh_rated_games():
        'laad opnieuw de lijst in'

        entry = rated_games_entry.get()

        try:
            if entry  == '':
                entry = 20000

            if (int(entry) > 100000):
                entry = 100000


            lowest_rated_textbox.delete(1.0, tkinter.END)
            lowest_rated_textbox.insert(tkinter.END, get_lowest_rated_games(entry), 'center')

            top_rated_textbox.delete(1.0, tkinter.END)
            top_rated_textbox.insert(tkinter.END, get_top_rated_games(entry), 'center')

        except ValueError:
            print("not a number")



    global top_rated_textbox

    top_rated_textbox = tkinter.Text(box4, height = 28, width = 43, bg = box_color, fg = 'white',font='Arial 12', wrap = 'word')
    top_rated_textbox.place(x = 5, y = 6)
    top_rated_textbox.tag_configure("center", justify='center')
    top_rated_textbox.insert(tkinter.END, get_top_rated_games(50000), 'center')


    rated_games_entry = tkinter.Entry(box3, width=10)
    rated_games_entry.place(x=230, y=240)
    tkinter.Label(box3, text = 'Minimum amount of ratings:', bg = background_color, fg = 'white').place(x =220, y =200)
    tkinter.Button(box3,width =5,height = 1, command = refresh_rated_games, text = 'reload').place(x = 320, y = 237)


    tkinter.Label(box2, image = pieChart, bg = background_color,borderwidth = 30).pack()
    tkinter.Label(box1, text = ten_first_names,font='Arial 12', bg=background_color, fg='white').place(x=180,y=70)



def launch_dashboard():
    root.mainloop()


create_dashboard()
fill_dashboard(convert_to_list(steam_data))
launch_dashboard()

