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
    root.geometry('1140x960')
    root.title('SteamStats')
    root.overrideredirect(True) # haalt de titlebar weg, nodig als je een overlay wilt maken


    root.update()

    positionRight = int(root.winfo_screenwidth() / 2 - 0.5*root.winfo_width())
    positionDown = int(root.winfo_screenheight() / 2 - 0.5 * root.winfo_height())

    root.geometry("+{}+{}".format(positionRight, positionDown))


    bar = tkinter.Frame(root,height = 80,width = 1140, bg = bar_color)
    bar.grid(row = 1, column =1, columnspan = 3)

    global box1 # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    global box2
    global box3
    global box4
    global box5
    box1 = tkinter.Frame(root,width = 500, height = 480, bg = background_color)
    box1.grid(row = 2, column = 1)
    box2 = tkinter.Frame(root, width = 640, height = 480, bg = background_color2)
    box2.grid(row = 2, column = 2, columnspan = 2)
    box3 = tkinter.Frame(root, width = 500, height = 400, bg = background_color)
    box3.grid(row = 3, column = 1)
    box4 = tkinter.Frame(root, width = 320, height = 400, bg = box_color)
    box4.grid(row = 3, column = 2)
    box5 = tkinter.Frame(root, width=320, height=400, bg=menu_bar_color, )
    box5.grid(row=3, column=3)



    def terminate_window():
        'sluit het window'
        root.destroy()

    tkinter.Button(bar,text = 'X', fg = 'white', bg =  bar_color,width = 2, height = 1, border = 0, command = terminate_window, activebackground=box_color).place(x = 1120, y = 0)


def fill_dashboard(list):
    'add data to the dashboard'


    def make_bar_plot_ratings():

        ratings= []

        for x in range(len(list)):
                positive_percentage = (round(int(list[x]['positive_ratings']) / int(
                    (int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
                ratings.append(positive_percentage)

        count_list = []
        for x in range(0,100,10):
            temp_list = []
            for i in range(len(ratings)):
                if(x+10>ratings[i]>=x):
                     temp_list.append(ratings[i])
            count_list.append((len(temp_list)))

        x = ['0-10%','10-20%','20-30%','30-40%','40-50%','50-60%','60-70%','70-80%','80-90%','90-100%']
        values = count_list

        plt.figure(figsize=(6.4, 4.8))
        plt.style.use('ggplot')
        x_pos = [i for i, _ in enumerate(x)]
        plt.bar(x_pos, values, color='#aed6f5')
        plt.xlabel("")
        plt.ylabel("Number of Games")
        plt.xticks(rotation=25)

        plt.xticks(x_pos, x)
        ax = plt.gca()
        ax.set_facecolor('#29455B')
        plt.savefig('chart.png')


    def make_bar_plot_release_year():
        release_dates = []
        for x in range(len(list)):
            release_dates.append(list[x]['release_date'].split('-')[0])

        unique_release_dates = []
        for x in range(len(release_dates)):
            if(release_dates[x]not in unique_release_dates):
                unique_release_dates.append(release_dates[x])
        unique_release_dates = sorted(unique_release_dates)

        value_list = []
        for x in range(len(unique_release_dates)):
            value_list.append(release_dates.count(unique_release_dates[x]))

        x = unique_release_dates[:-1]
        values = value_list[:-1]

        plt.figure(figsize=(6.4, 4.8))
        plt.style.use('ggplot')
        x_pos = [i for i, _ in enumerate(x)]
        plt.bar(x_pos, values, color='#aed6f5')
        plt.xlabel("")
        plt.ylabel("Number of Games Released")
        plt.xticks(rotation=45)

        plt.xticks(x_pos, x)
        ax = plt.gca()
        ax.set_facecolor('#29455B')

        plt.savefig('chart.png')

    def make_bar_plot_game_population():

        amount_of_players_list = []
        for entry in list:
            amount_of_players_list.append(int(int((entry['owners'].split('-')[0]))/10000))

        unique_amount_of_players_list = []

        for x in amount_of_players_list:
            if x not in unique_amount_of_players_list:
                unique_amount_of_players_list.append(x)
        unique_amount_of_players_list = (sorted(unique_amount_of_players_list))

        value_list = []
        for x in range(len(unique_amount_of_players_list)):
            value_list.append(amount_of_players_list.count(unique_amount_of_players_list[x]))

        plt.figure(figsize=(6.4, 4.8))

        plt.style.use('ggplot')

        unique_amount_of_players_list.append(unique_amount_of_players_list[-1]*2)

        for x in range(len(unique_amount_of_players_list)):
            if unique_amount_of_players_list[x]/1000 >=1:
                unique_amount_of_players_list[x] = f'{int(unique_amount_of_players_list[x]/1000)}k'
        x = unique_amount_of_players_list[1:]
        values = value_list

        x_pos = [i for i, _ in enumerate(x)]

        plt.bar(x_pos, values, color = '#aed6f5')
        plt.xlabel("Highest Estimate of Size Playerbase (in 10000 people)")
        plt.ylabel("Number of Games")

        plt.xticks(x_pos, x)
        ax = plt.gca()
        ax.set_facecolor('#29455B')

        plt.savefig('chart.png')


    def get_average_playtime_piechart(limit):
        'maak een average playtime piechart'
        name = 'Highest Average Playtime'
        playtime_dict = {}
        for entry in list:
            if (int(entry['positive_ratings']) + int(entry['negative_ratings']) > 1000):
                playtime_dict[entry['name']] = entry['average_playtime']

        playtime_dict = sorted(playtime_dict.items(), key=itemgetter(1))
        playtime_dict.reverse()

        playtime_dict = playtime_dict[:limit]

        make_piechart(playtime_dict,name)


    def get_genre_piechart(limit):
        'maak een genre distributie piechart'
        name = 'Genre Popularity Distribution'

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



        make_piechart(genre_tags_list,name)

    def make_piechart(dict,name):
        'maak de piechart image'

        labels = []
        sizes = []

        for entry in dict:
            labels.append(entry[0])
            sizes.append(entry[1])


        fig1, ax1 = plt.subplots()

        centre_circle = plt.Circle((0, 0), 0.70, fc='#29455B')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        fig.set_facecolor('#29455B')


        colors = ['#222630','#1f2947','#171A21', '#3e7ea7', '#1B3E54', '#4E6A84','#aed6f5']

        explode = []

        for x in range(len(labels)):
            explode.append(0.05)


        if(name =='Highest Average Playtime'):
            for x in range(len(sizes)):
                sizes[x] = int(sizes[x]/60)

            def make_autopct(values):
                def my_autopct(pct):
                    total = sum(values)
                    val = int(round(pct * total / 100.0))
                    return '{v:d}h'.format(p=pct, v=val)

                return my_autopct

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct=make_autopct(sizes),
                                                startangle=90,
                                                pctdistance=0.85, explode=explode)
        else:
            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct= '%1.1f%%',
                                                startangle=90,
                                                pctdistance=0.85, explode=explode)
        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')
        ax1.axis('equal')
        plt.savefig('chart.png')


    global steamlogo
    global dislikeIcon
    global likeIcon
    global pieChart
    global statsLogo


    steamlogo = tkinter.PhotoImage(file='steam.png')
    statsLogo = tkinter.PhotoImage(file = 'stats.png')
    likeIcon = tkinter.PhotoImage(file = 'icon_thumbsUp.png')
    dislikeIcon = tkinter.PhotoImage(file ='icon_thumbsDown.png')


    try:
        pieChart = tkinter.PhotoImage(file='chart.png')
    except:
        get_genre_piechart(5)
        pieChart = tkinter.PhotoImage(file='chart.png')


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

        lowest_rated_games = '\n\nLeast liked steam games:\n\n\n'

        for x in range(12):
            lowest_rated_games = lowest_rated_games + f'{sorted_ratings_list[x][0]} - {sorted_ratings_list[x][1]}%' + '\n'

        return lowest_rated_games

    tkinter.Label(root, image=steamlogo, border=0).place(x=10, y=10)
    tkinter.Label(image = statsLogo, borderwidth = 0).place(y = 20, x = 200)


    ten_first_names = '\n\nFirst 10 games in the JSON file: \n\n\n\n'


    for x in range(10):
        ten_first_names = ten_first_names + (list[x]['name']) + '\n'

    global lowest_rated_textbox


    lowest_rated_textbox = tkinter.Text(box5, height=21, width=34, bg=menu_bar_color, fg='white', font='Arial 12', wrap='word')
    lowest_rated_textbox.place(x=5, y=9)
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

    top_rated_textbox = tkinter.Text(box4, height = 21, width = 34, bg = box_color, fg = 'white',font='Arial 12', wrap = 'word')
    top_rated_textbox.place(x = 5, y = 9)
    top_rated_textbox.tag_configure("center", justify='center')
    top_rated_textbox.insert(tkinter.END, get_top_rated_games(50000), 'center')


    rated_games_entry = tkinter.Entry(box3, width=10, bg = background_color, fg = 'white')
    rated_games_entry.insert(0,50000)
    rated_games_entry.place(x=190, y=240)
    tkinter.Label(box3, text = 'Minimum amount of ratings:', bg = background_color, fg = 'white').place(x =175, y =200)
    tkinter.Button(box3,width =5,height = 1,bg = background_color2,fg = 'white', command = refresh_rated_games, text = 'reload').place(x = 270, y = 237)


    pieChartImage = tkinter.Label(box2, image = pieChart, bg = background_color,borderwidth = 0)
    pieChartImage.pack()
    tkinter.Label(box1, text = ten_first_names,font='Arial 12', bg=background_color, fg='white').place(x=132,y=70)







    def update_pie_info():
        'refresh de piechart'

        chartName = tkvar.get()

        pie_limit = limit_box.get()

        try:
            pie_limit = int(pie_limit)
        except:
            pie_limit = int(5)

        if(pie_limit < 1):
            pie_limit = int(5)
        if(chartName == 'Game Rating Distribution (like/dislike ratio)'):
            make_bar_plot_ratings()
        if(chartName == 'Game Releases per Year (2019&2020 excluded)'):
            make_bar_plot_release_year()
        if(chartName == 'Game Playerbase Distribution          '):
            make_bar_plot_game_population()
        if(chartName == 'Genre Popularity Distribution'):
            get_genre_piechart(pie_limit)
        if(chartName == 'Highest Average Playtime'):
            get_average_playtime_piechart(pie_limit)
        global pieChart
        pieChart = tkinter.PhotoImage(file='chart.png')
        pieChartImage.config(image = pieChart)

    limit_box = tkinter.Entry(box2, bd=2, width=2, bg=background_color2, fg='white')
    limit_box.place(x=200, y=6)
    limit_box.insert(0, 5)
    tkinter.Button(box2, command = update_pie_info, text = 'reload', width = 6,bg = background_color2, fg = 'white').place(x=3,y=450)



    options = ['Genre Popularity Distribution','Game Playerbase Distribution          ','Game Rating Distribution (like/dislike ratio)', 'Highest Average Playtime', 'Game Releases per Year (2019&2020 excluded)']

    tkvar = tkinter.StringVar(box2)
    tkvar.set(options[0])

    menu = tkinter.OptionMenu(box2, tkvar, *options)
    menu.config(bg=background_color2, fg = 'white', activebackground = background_color, activeforeground = 'white')
    menu["menu"].config(bg=background_color2, fg = 'white', borderwidth = 0, activebackground = background_color,activeforeground = 'white')
    menu["highlightthickness"] = 0
    menu.place(x=3,y=3)


    tkinter.Label(box4, image = likeIcon, borderwidth = 0).place(x =6,y = 10)
    tkinter.Label(box5, image = dislikeIcon, borderwidth = 0).place(x =6,y = 10)



def launch_dashboard():
    'launch dashboard'
    root.mainloop()


create_dashboard()
fill_dashboard(convert_to_list(steam_data))

launch_dashboard()

