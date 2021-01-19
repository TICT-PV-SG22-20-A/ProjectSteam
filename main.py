import json
import threading
import tkinter
from operator import itemgetter
import matplotlib.pyplot as plt
from random import randint
import time
from datetime import datetime, date
import random

#!disclaimer!

#de tkinter elementen lijken random tussen alle functies verstopt te zitten zonder enige logica daar achter
#dat klopt, maar nadat ik het meerdere keren heb proberen op te ruimen,
#en elke daar mijn programma mee heb weten te breken, heb ik geaccepteerd dat het hem gewoon niet gaat worden.



#alles wat met de GPIO package werkt staat in een 'try' omdat GPIO niet op pc gedownload kan worden maar het
#programma wel op pc moet kunnen werken
try:
    import RPi.GPIO as GPIO
    # Stelt de modus in hoe de pins worden gelezen en zet error meldingen uit
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(0)
    # Knop pin
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # Servo pin
    GPIO.setup(25, GPIO.OUT)
    # LED strip pins
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)
    # Shift register pins
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    # Afstand sensor pins
    GPIO.setup( 20, GPIO.OUT )
    GPIO.setup( 21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

except ModuleNotFoundError:
    print('input/output is not available for this device')



bar_color = '#171A21'
menu_bar_color = '#3e7ea7'
background_color = '#1B3E54'
box_color = '#4E6A84'
background_color2 = '#29455B'


def convert_to_list(data):
    'maakt van de json file een lijst van dictionaries'

    data = (data.read())
    data_list = json.loads(data)

    return data_list


def sort_list_alphabetically(list):
    'sorteert de lijst van dictionaries alphabetisch op de naam van de games, gebruikt een vereenvoudigde vorm van quicksort'


    #maak 3 lists voor nummers lager, hetzelfde en hoger dan de 'pivot'
    lower = []
    same = []
    higher = []

    #exit conditie
    if len(list) < 2:
        return list

    #de willekeurig geselecteerde pivot, dit werkt beter dan altijd het 1e element in de lijst te nemen
    pivot = list[randint(0, len(list) - 1)]['name']

    #vul de 3 lists met waardes
    for entry in list:
        if entry['name'] < pivot:
            lower.append(entry)
        elif entry['name'] > pivot:
            higher.append(entry)
        elif entry['name'] == pivot:
            same.append(entry)

    #deze functie is recursief en blijft zichzelf dus verdelen in steeds kleinere lists totdat voor elke sub-list de
    #exit condition bereikt is.
    return sort_list_alphabetically(lower) + same + sort_list_alphabetically(higher)


def create_dashboard():
    'maak het dashboard'

    global root  # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie

    #geef de condities voor het root-scherm
    root = tkinter.Tk()
    root.geometry('1140x960')
    root.title('SteamStats')
    root.resizable(False, False)

    #refresh het root scherm zodat ik de width en hight af kan lezen
    root.update()
    #gebruik de width en high van het root scherm om de window in het midden van een beeldscherm te positioneren
    positionRight = int(root.winfo_screenwidth() / 2 - 0.5 * root.winfo_width())
    positionDown = int(root.winfo_screenheight() / 2 - 0.5 * root.winfo_height())
    root.geometry("+{}+{}".format(positionRight, positionDown))



    # ik maak deze global omdat ik hier toegang tot moet hebben buiten de functie
    global box1
    global box2
    global box3
    global box4
    global box5

    #de GUI grid
    bar = tkinter.Frame(root, height=80, width=1140, bg=bar_color)
    bar.grid(row=1, column=1, columnspan=3)
    box1 = tkinter.Frame(root, width=500, height=480, bg=background_color)
    box1.grid(row=2, column=1)
    box2 = tkinter.Frame(root, width=640, height=480, bg=background_color2)
    box2.grid(row=2, column=2, columnspan=2)
    box3 = tkinter.Frame(root, width=500, height=400, bg=background_color)
    box3.grid(row=3, column=1)
    box4 = tkinter.Frame(root, width=320, height=400, bg=box_color)
    box4.grid(row=3, column=2)
    box5 = tkinter.Frame(root, width=320, height=400, bg=menu_bar_color, )
    box5.grid(row=3, column=3)


def fill_dashboard(list):
    'voegt data toe aan het dashboarad'

    def make_bar_plot_ratings():
        'maakt een bar grafiek genaamd "game rating distribution" en sla hem op als .png'

        ratings = []

        #reken like/dislike ratios uit
        for x in range(len(list)):
            positive_percentage = (round(int(list[x]['positive_ratings']) / int(
                (int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
            ratings.append(positive_percentage)

        count_list = []
        #tel hoe vaak een ratio tussen x en x+10 voorkomt
        for x in range(0, 100, 10):
            temp_list = []
            for i in range(len(ratings)):
                if (x + 10 > ratings[i] >= x):
                    temp_list.append(ratings[i])
            count_list.append((len(temp_list)))

        #matplotlib stuff:
        x = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
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
        'maakt een bar grafiek genaamd "game releases per year" en sla hem op als .png'

        #split alle release years in een list
        release_dates = []
        for x in range(len(list)):
            release_dates.append(list[x]['release_date'].split('-')[0])

        #kijk welke release years allemaal voorkomen in de JSON file
        unique_release_dates = []
        for x in range(len(release_dates)):
            if (release_dates[x] not in unique_release_dates):
                unique_release_dates.append(release_dates[x])
        unique_release_dates = sorted(unique_release_dates)

        #een lijst van de unieke release year counts
        value_list = []
        for x in range(len(unique_release_dates)):
            value_list.append(release_dates.count(unique_release_dates[x]))

        #2019 is incompleet, dus die halen we er af
        x = unique_release_dates[:-1]
        values = value_list[:-1]

        #matplotlib stuff
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
        'maakt een bar grafiek genaamd "game playerbase distribution" en sla hem op als .png'

        #een list van de hoogste estimate playersize per game / 10000
        #gedeeld door 10000 omdat het anders niet op de x-as past
        amount_of_players_list = []
        for entry in list:
            amount_of_players_list.append(int(int((entry['owners'].split('-')[0])) / 10000))

        #een list van de verschillende hoogste estimated playersize cutoffs
        unique_amount_of_players_list = []

        for x in amount_of_players_list:
            if x not in unique_amount_of_players_list:
                unique_amount_of_players_list.append(x)
        unique_amount_of_players_list = (sorted(unique_amount_of_players_list))

        #een list met counts van de estimated playersize cutoffs
        value_list = []
        for x in range(len(unique_amount_of_players_list)):
            value_list.append(amount_of_players_list.count(unique_amount_of_players_list[x]))


        #more matplotlib stuff
        plt.figure(figsize=(6.4, 4.8))

        plt.style.use('ggplot')

        unique_amount_of_players_list.append(unique_amount_of_players_list[-1] * 2)

        #text past niet op de x-as dus moest iets verzinnen om de getallen kleiner te maken
        for x in range(len(unique_amount_of_players_list)):
            if unique_amount_of_players_list[x] / 1000 >= 1:
                unique_amount_of_players_list[x] = f'{int(unique_amount_of_players_list[x] / 1000)}k'
        x = unique_amount_of_players_list[1:]
        values = value_list

        x_pos = [i for i, _ in enumerate(x)]

        #matplotlib stuff
        plt.bar(x_pos, values, color='#aed6f5')
        plt.xlabel("Highest Estimate of Size Playerbase (in 10000 people)")
        plt.ylabel("Number of Games")

        plt.xticks(x_pos, x)
        ax = plt.gca()
        ax.set_facecolor('#29455B')

        plt.savefig('chart.png')

    def get_average_playtime_piechart(limit):
        'loop door de data om de piechart "highest average playtime" te maken, alleen voor games vanaf 1000 ratings'

        name = 'Highest Average Playtime'
        playtime_dict = {}
        #alleen beschikbaar voor games met meer dan 1000 ratings om spam te voorkomen
        for entry in list:
            if (int(entry['positive_ratings']) + int(entry['negative_ratings']) > 1000):
                playtime_dict[entry['name']] = entry['average_playtime']

        #gebruik itemgetter om te sorteren op average_playtime
        playtime_dict = sorted(playtime_dict.items(), key=itemgetter(1))
        playtime_dict.reverse()


        #geef de data door aan de make_piechart functie
        make_piechart(playtime_dict, name, limit,'playtime')

    def get_genre_piechart(limit):
        'loop door de data om de piechart "genre popularity distribution" te maken'

        name = 'Genre Popularity Distribution'

        #maak een lijst met alle genre tags(steamspy_tags) in de JSON file
        genre_tags = []
        for entry in list:
            tags = (entry['steamspy_tags'].split(';'))
            for tag in tags:
                genre_tags.append(tag)

        #maak een list met unieke genre tags, en count hoeveel elke voorkomt
        genre_tags_dict = {}
        for x in set(genre_tags):
            genre_tags_dict[x] = genre_tags.count(x)

        genre_tags_list = sorted(genre_tags_dict.items(), key=itemgetter(1))
        genre_tags_list.reverse()

        #geef de data door aan de make_piechart functie
        make_piechart(genre_tags_list, name, limit,'genre')

    def make_piechart(dict, name,limit,type):
        'maak de piechart .png, wordt gebruikt door de get_genre_piechart en get_average_playtime_piechart functies'



        labels = []
        sizes = []

        #gebruik de data uit de dict om labels en sizes toe te wijzen
        for entry in dict:
            labels.append(entry[0])
            sizes.append(entry[1])

        if(type == 'genre' and limit < len(labels)):
            #bereken wat het toaal van alle genres is die niet op de chart passen (other)
            remainder = (sum(sizes[limit-1:]))

            labels = labels[:limit-1]
            sizes = sizes[:limit-1]
            sizes.append(remainder)

            #label voor het totaal van alle genres die niet op de chart passen
            labels.append('other')
        else:
            labels = labels[:limit]
            sizes = sizes[:limit]

        #matplotlib stuff
        fig1, ax1 = plt.subplots()

        centre_circle = plt.Circle((0, 0), 0.70, fc='#29455B')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        fig.set_facecolor('#29455B')


        #ik vond het een leuk idee om te kijken of ik iets zou kunnen maken dat automatisch hex-kleurcodes genereert
        #in matchende kleur tinten(allemaal blauw achtig).
        colors = []
        counter = random.randint(0,4)
        while(len(colors)!= len(labels)):

            if counter > 4:
                counter = 0

            if(counter==0):
                colors.append('#{:06x}'.format(random.randint(0x3e7e90, 0x3e7eff)))
            elif(counter==1):
                colors.append('#{:06x}'.format(random.randint(0x222630, 0x22264f)))
            elif(counter==2):
                colors.append('#{:06x}'.format(random.randint(0x507b95, 0x507bff)))
            elif(counter==3):
                colors.append('#{:06x}'.format(random.randint(0x2a4b5, 0x2a4ff)))
            elif(counter==4):
                colors.append('#{:06x}'.format(random.randint(0x1a3140, 0x1a3177)))

            counter += 1


        #meer matplotlib dingen om het er uniek uit te laten zien
        explode = []

        for x in range(len(labels)):
            explode.append(0.05)

        if (name == 'Highest Average Playtime'):
            for x in range(len(sizes)):
                sizes[x] = int(sizes[x] / 60)

            #om de text in de piecharts aan te passen
            def make_autopct(values):
                def my_autopct(pct):
                    total = sum(values)
                    val = int(round(pct * total / 100.0))
                    return '{v:d}h'.format(p=pct, v=val)

                return my_autopct


            #matplotlib stuff
            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct=make_autopct(sizes),
                                                startangle=90,
                                                pctdistance=0.85, explode=explode)
        else:
            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',
                                                startangle=90,
                                           pctdistance=0.85, explode=explode)

        for text in texts:
            text.set_color('black')
        for autotext in autotexts:
            autotext.set_color('white')
        ax1.axis('equal')
        plt.savefig('chart.png')

        #dit gaat kennelijk niet automatisch en was mijn programma aan het crashen
        plt.close()


    #images laden niet tenzij ze global zijn
    global steamlogo
    global dislikeIcon
    global likeIcon
    global pieChart
    global statsLogo
    global help_1
    global help_2
    global help_3
    global help_4
    global information

    #laden van images
    steamlogo = tkinter.PhotoImage(file='steam.png')
    statsLogo = tkinter.PhotoImage(file='stats.png')
    likeIcon = tkinter.PhotoImage(file='icon_thumbsUp.png')
    dislikeIcon = tkinter.PhotoImage(file='icon_thumbsDown.png')
    help_1 = tkinter.PhotoImage(file='help_1.png')
    help_2 = tkinter.PhotoImage(file='help_2.png')
    help_3 = tkinter.PhotoImage(file='help_3.png')
    help_4 = tkinter.PhotoImage(file='help_4.png')
    information = tkinter.PhotoImage(file='information.png')


    #als er geen chart file aanwezig is, maak er dan 1 aan
    try:
        pieChart = tkinter.PhotoImage(file='chart.png')
    except:
        get_genre_piechart(5)
        pieChart = tkinter.PhotoImage(file='chart.png')



    def get_top_rated_games(ratings):
        'geeft een string van de hoogst beordeelde games terug, "ratings" is hoeveel ratings een game minimaal moet hebben'

        ratings_dict = {}

        #check of een game voldoet aan het minimum aantal ratings, zo ja, maak een dictionary met z'n naam+ratio
        for x in range(len(list)):
            if (int(int(list[x]['positive_ratings']) + int(list[x]['negative_ratings'])) > int(ratings)):
                positive_percentage = (round(int(list[x]['positive_ratings']) / int(
                    (int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100))
                ratings_dict[list[x]['name']] = positive_percentage

        sorted_ratings_list = sorted(ratings_dict.items(), key=itemgetter(1))
        sorted_ratings_list.reverse()

        best_rated_games = '\n\nMost liked steam games:\n\n\n'

        #zet de 12 games met de hoogste rating in een string
        for x in range(12):
            best_rated_games = best_rated_games + f'{sorted_ratings_list[x][0]} - {sorted_ratings_list[x][1]}%' + '\n'

        return best_rated_games

    def get_lowest_rated_games(ratings):
        'geeft een string van de laagst beordeelde games terug, "ratings" is hoeveel ratings een game minimaal moet hebben'
        ratings_dict = {}

        #werkt hetzelfde als get_top_rated_games maar dan omgekeerd

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


    def led_strip(percentages):
        # Zet de LED strip op kleuren op basis van procenten.
        def apa102_send_bytes(bytes):
            for byte in bytes:
                for bit in byte:
                    if bit == 1:
                        GPIO.output(26, GPIO.HIGH)
                    if bit == 0:
                        GPIO.output(26, GPIO.LOW)
                    GPIO.output(19, GPIO.HIGH)
                    GPIO.output(19, GPIO.LOW)

        def apa102(colors):
            # Er worden eerst 4 bytes van nullen gestuurd om de LED strip te laten weten dat dit het begin is.
            nullen = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
            apa102_send_bytes(nullen)
            # Er wordt nu voor 8 LED lampjes de juiste bits meegegeven per kleur.
            nieuwe_bytes = []
            for i in colors:
                # Dit begint met 1 byte van 1tjes.
                nieuwe_bytes.append([1, 1, 1, 1, 1, 1, 1, 1])
                for b in i:
                    # Hier wordt een getal kleur code omgezet in binair
                    color_byte = []
                    getal = f'{b:08b}'
                    for nummer in getal:
                        color_byte.append(int(nummer))
                    nieuwe_bytes.append(color_byte)
            # Stuurt de LED informatie door
            apa102_send_bytes(nieuwe_bytes)
            # de functie eindigt met 4 bytes van 1tjes. Dit verteld de LED strip dat dit het einde is.
            eenen = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1]]
            apa102_send_bytes(eenen)
        # kleur codes voor de gebruikte kleuren
        red = [0, 0, 5]
        green = [0, 5, 0]
        # Hier wordt de list uitgelezen op een waarde onder op boven de 60.
        # Onder de 60 is slecht en dan wordt het ledje rood, er boven is goed en dus groen.
        kleuren = []
        for getal in percentages:
            if getal < 60:
                kleuren.append(red)
            elif getal >= 60:
                kleuren.append(green)
        # De kleur informatie van alle 8 ledjes wordt doorgestuurd.
        apa102(kleuren)

    def servo(procent):
        # Zet de Servo op positie op basis van een procent
        def pulse(delay1, delay2):
            # Zet de pin van de servo aan voor een bepaalde tijd. Zo komt de servo in exact de goede positie.
            GPIO.output(25, GPIO.HIGH)
            time.sleep(delay1)
            GPIO.output(25, GPIO.LOW)
            time.sleep(delay2)

        def servo_pulse(position):
            # berekent op bais van een getal tussen 0 en 100, hoelang de servo aangezet moet worden.
            tijd = round(((position / 100) * 2 + 0.5) / 1000, 10)
            # mijn servo weigert een getal boven de 0.0024, daar wordt hier rekening mee gehouden.
            if tijd == 0.0025:
                tijd = 0.0024
            # Roept de pulse functie aan om het berekende tijd uit te voeren.
            pulse(tijd, 0.02)

        servo_pulse(procent)


    def get_average_like_dislike_ratio():
        'geeft de gemiddelde like/dislike ratio terug van alle games op steam'

        ratings = []  # list met like/dislike percentages van games
        for x in range(len(list)):
            rating = round(int(list[x]['positive_ratings']) / int(
                (int(list[x]['positive_ratings']) + int(list[x]['negative_ratings']))) * 100)
            ratings.append(rating)

        #bereken gemiddelde
        average_like_dislike_ratio = sum(ratings)/len(ratings)
        return average_like_dislike_ratio



    def get_standard_deviation_like_dislike_ratio():
        'geeft de standaard afwijking van het like/dislike ratio van alle games terug'

        average = get_average_like_dislike_ratio()

        #maak een lijst met onafgeronde like/dislike ratios
        ratings = []
        for x in range(len(list)):
            rating = int(list[x]['positive_ratings'])/(int(list[x]['positive_ratings'])+int(list[x]['negative_ratings']))*100
            ratings.append(rating)

        #bereken de afstand van het gemiddelde voor elke waarde
        distances_from_average = []

        for rating in ratings:
            distance_from_average = rating - average
            distances_from_average.append(distance_from_average)

        #doe de afstanden van het gemiddelde in het kwadraat
        distances_from_average_sq = []

        for distance_from_average in distances_from_average:
            distance_from_average_sq = distance_from_average**2
            distances_from_average_sq.append(distance_from_average_sq)

        #bereken het gemiddelde van de afstanden van het gemiddelde(variantie)
        variance = sum(distances_from_average_sq)/len(distances_from_average_sq)

        #neem de wortel van dit gemiddelde
        standard_deviation = variance**0.5

        return standard_deviation

    def get_random_8_games():

        random_8_games = '\n8 random games with their like/dislike ratio:\n\n'

        ratings = []  # list met like/dislike percentages van games

        #selecteer 8 willekeurige games met hun like/dislike ratio en stop het in een string
        for x in range(8):
            random_ID = randint(0, len(list) - 1)
            rating = round(int(list[random_ID]['positive_ratings']) / int(
                (int(list[random_ID]['positive_ratings']) + int(list[random_ID]['negative_ratings']))) * 100)
            random_8_games = random_8_games + (f"{list[random_ID]['name']} - {rating}%\n")
            ratings.append(rating)

        try:
            # Roept de servo functie aan met het eerste percentage van de ratings lijst
            servo(ratings[0])
            # Roept de LED strip functie aan met alle percentages van de lijst
            led_strip(ratings)
        except NameError:
            pass

        return random_8_games


    def get_first_ten_names_sorted_alphabetically():

        ten_first_names_sorted_alphabetically = '\nFirst 10 games in the JSON file (sorted alphabetically): \n\n'

        #gebruik de sort_list_alphabetitically functie om de lijst alphabetisch om game naam te sorteren
        alpha_list = sort_list_alphabetically(list)


        #voeg de 10 eerste games toe aan een string
        for x in range(10):
            ten_first_names_sorted_alphabetically += alpha_list[x]['name'] + '\n'

        return ten_first_names_sorted_alphabetically


    #tkinter voodoo
    global lowest_rated_textbox

    lowest_rated_textbox = tkinter.Text(box5, height=21, width=34, bg=menu_bar_color, fg='white', font='Arial 12',
                                        wrap='word', border=0)
    lowest_rated_textbox.place(x=5, y=9)
    lowest_rated_textbox.tag_configure("center", justify='center')
    lowest_rated_textbox.insert(tkinter.END, get_lowest_rated_games(50000), 'center')

    # plaats het logo links boven
    tkinter.Label(root, image=steamlogo, border=0).place(x=10, y=10)
    tkinter.Label(image=statsLogo, borderwidth=0).place(y=20, x=200)

    def refresh_rated_games():
        'laadt opnieuw de lijsten in'

        #laadt de lijsten opnieuw gebaseerd op het nieuwe nummer minimale ratings
        entry = rated_games_entry.get()

        try:
            if entry == '':
                entry = 20000

            if (int(entry) > 100000):
                entry = 100000

            lowest_rated_textbox.delete(1.0, tkinter.END)
            lowest_rated_textbox.insert(tkinter.END, get_lowest_rated_games(entry), 'center')

            top_rated_textbox.delete(1.0, tkinter.END)
            top_rated_textbox.insert(tkinter.END, get_top_rated_games(entry), 'center')

        except ValueError:
            print("not a number")


    #tkinter voodoo
    global top_rated_textbox

    top_rated_textbox = tkinter.Text(box4, height=21, width=34, bg=box_color, fg='white', font='Arial 12', wrap='word',
                                     border=0)
    top_rated_textbox.place(x=5, y=9)
    top_rated_textbox.tag_configure("center", justify='center')
    top_rated_textbox.insert(tkinter.END, get_top_rated_games(50000), 'center')

    rated_games_entry = tkinter.Entry(box3, width=10, bg=background_color, fg='white')
    rated_games_entry.insert(0, 50000)
    rated_games_entry.place(x=190, y=220)
    tkinter.Label(box3, text='Minimum amount of ratings:', bg=background_color, fg='white').place(x=169, y=180)
    tkinter.Button(box3, width=5, height=1, bg=background_color2, fg='white', command=refresh_rated_games,
                   text='reload').place(x=265, y=217)

    pieChartImage = tkinter.Label(box2, image=pieChart, bg=background_color, borderwidth=0)
    pieChartImage.pack()


    tkinter.Label(box1, text=get_first_ten_names_sorted_alphabetically(), font='Arial 10', bg=background_color,
                  fg='white').place(x=85, y=25)

    random_8_textbox = tkinter.Text(root, height=11, width=65, bg=background_color, fg='white', font='Arial 10',
                                    wrap='word', border=0)
    random_8_textbox.place(x=20, y=330)
    random_8_textbox.tag_configure("center", justify='center')
    random_8_textbox.insert(tkinter.END, get_random_8_games(), 'center')

    def update_pie_info():
        'refresh de piechart'


        #genereer een nieuwe piechart gebaseerd op de geselecteerde titel,limit
        chartName = tkvar.get()

        pie_limit = limit_box.get()

        try:
            pie_limit = int(pie_limit)
        except:
            pie_limit = int(5)

        if (pie_limit < 1):
            pie_limit = int(5)
        if (chartName == 'Game Rating Distribution (like/dislike ratio)'):
            make_bar_plot_ratings()
        if (chartName == 'Game Releases per Year (2019&2020 excluded)'):
            make_bar_plot_release_year()
        if (chartName == 'Game Playerbase Distribution          '):
            make_bar_plot_game_population()
        if (chartName == 'Genre Popularity Distribution'):
            get_genre_piechart(pie_limit)
        if (chartName == 'Highest Average Playtime'):
            get_average_playtime_piechart(pie_limit)
        global pieChart
        pieChart = tkinter.PhotoImage(file='chart.png')
        pieChartImage.config(image=pieChart)


    #tkinter voodoo
    limit_box = tkinter.Entry(box2, bd=2, width=2, bg=background_color2, fg='white')
    limit_box.place(x=2, y=32)
    limit_box.insert(0, 5)
    tkinter.Button(box2, command=update_pie_info, text='reload', width=6, bg=background_color2, fg='white').place(x=3,
                                                                                                                  y=450)

    #selectie menu titels
    options = ['Genre Popularity Distribution', 'Game Playerbase Distribution          ',
               'Game Rating Distribution (like/dislike ratio)', 'Highest Average Playtime',
               'Game Releases per Year (2019&2020 excluded)']

    #tkinter voodoo
    tkvar = tkinter.StringVar(box2)
    tkvar.set(options[0])

    menu = tkinter.OptionMenu(box2, tkvar, *options)
    menu.config(bg=background_color2, fg='white', activebackground=background_color, activeforeground='white')
    menu["menu"].config(bg=background_color2, fg='white', borderwidth=0, activebackground=background_color,
                        activeforeground='white')
    menu["highlightthickness"] = 0
    menu.place(x=3, y=3)

    tkinter.Label(box4, image=likeIcon, borderwidth=0).place(x=6, y=10)
    tkinter.Label(box5, image=dislikeIcon, borderwidth=0).place(x=6, y=10)

    #label voor het gemiddelde like/dislike ratio van alle games op steam + standaard deviatie
    hard_stats = tkinter.Label(root, bg = bar_color, fg = 'white', text = f'Average like/dislike ratio for games on steam = {round(get_average_like_dislike_ratio(),2)}%      \u03C3 = {round(get_standard_deviation_like_dislike_ratio(),2)}%')
    hard_stats.place(x =630,y = 30)

    global check
    check = True

    def informationMenu():
        'toggled het informatiemenu'
        global check

        if (check):
            global h1
            global h2
            global h3
            global h4


            #verstop hard_stats om overlap te vermijden
            hard_stats['text'] = ''

            #plaats de help menu foto's
            h1 = tkinter.Label(root, image=help_1, borderwidth=0)
            h1.place(x=10, y=820)
            h2 = tkinter.Label(root, image=help_2, borderwidth=0)
            h2.place(x=650, y=10)
            h3 = tkinter.Label(root, image=help_3, borderwidth=0)
            h3.place(x=150, y=533)
            h4 = tkinter.Label(root, image=help_4, borderwidth=0)
            h4.place(x=280, y=810)

            check = False
        else:
            h1.destroy()
            h2.destroy()
            h3.destroy()
            h4.destroy()

            #help menu is weg, dus de hard_stats mogen terug
            hard_stats['text'] = f'Average like/dislike ratio for games on steam = {round(get_average_like_dislike_ratio(),2)}%      \u03C3 = {round(get_standard_deviation_like_dislike_ratio(),2)}%'


            check = True

    tkinter.Button(root, command=informationMenu, image=information, highlightthickness=0, bd=0, relief='flat').place(
        x=1080, y=20)

    def button_check():
        # Hier wordt naar de button gekeken als hij ingeklikt wordt. Daarna opent het help scherm
        try:
            # Voor het controleren als de knop niet ingedrukt blijft
            # Op deze manier wordt de functie maar 1 keer uitgevoerd als je 1 keer op de knop drukt.
            vorige = None
            while True:
                deze = GPIO.input(23)

                if vorige != deze:
                    if( GPIO.input(23) ):
                        informationMenu()
                vorige = deze
                # Controleer als de knop ingedrukt wordt elk volgende moment:
                time.sleep( 0.1 )
        except NameError:
            pass

    def led_shift():
        # Functie voor shift register met LED lampjes
        try:
            # Lijst van alle beschikbare LED lampjes
            LEDS = (1, 2, 3, 4, 5, 6, 7, 8)
            def shift(value, delay ):
                # Gaat elk led lampje af en wijst hier een bit aan toe via het shift register.
                for gpio in LEDS:
                    # op basis van de value worden er bits toegezen. Hoe de formule werkt is dat een getal
                    # omgezet wordt naar binair.
                    if value % 2 == 1:
                        GPIO.output(13, GPIO.HIGH)
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(5, GPIO.LOW)
                    else:
                        GPIO.output(13, GPIO.LOW)
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(5, GPIO.LOW)
                    value = value // 2
                # Stuurt de 8 gestuurde bitjes door naar het actieve gedeelte van het shift register.
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(6, GPIO.LOW)
                # Wacht om weer onieuw te beginnen
                time.sleep(delay)

            delay = 0.1
            while True:
                # Stuurt de getallen naar de functie om daarna in bits over te laten zetten
                # Op deze manier onstaat een soort trap effect.
                shift(1, delay)
                shift(2, delay)
                shift(4, delay)
                shift(8, delay)
                shift(16, delay)
                shift(32, delay)
                shift(64, delay)
                shift(128, delay)
                
        except NameError:
            pass
            
    def afstand_sensor():
        # functie voor afstand meten met de afstand sensor en uitvoeren van reload
        try:
            while True:
                # Stuurt het start bericht. Hierdoor wordt het geluid signaal gestart en gaat hij
                # wachten totdat het signaal weer binnenkomt.
                GPIO.output(20, GPIO.HIGH)
                time.sleep(0.00001)
                GPIO.output(20, GPIO.LOW)

                # Wacht tot het signaal binnenkomt en onthoudt dit moment.
                begin = None
                while True:
                    if GPIO.input(21) and begin == None:
                        begin = datetime.now().time()
                        break

                # wacht tot het signaal stopt en onthoudt dit moment.
                einde = None
                while True:
                    if not GPIO.input(21) and einde == None:
                        einde = datetime.now().time()
                        break

                # op basis van het verschil tussen begin en einde van het signaal kan de afstand gemeten worden.
                # dit wordt gedaan op basis van het snelheid van geluid.
                snelheid_geluid_per_seconde = 34300   
                duratie = (datetime.combine(date.min, einde) - datetime.combine(date.min, begin)).total_seconds()
                afstand = snelheid_geluid_per_seconde * duratie / 2
                # Controleert als de afstand onder de 4.5cm is. Als dit zo is worden de charts gereload.
                if afstand < 4.5:
                    led_shift()
                    update_pie_info()
                time.sleep(0.1)
                
        except NameError:
            pass

    # Start aparte threads voor 3 loops van de Raspberry Pi. Op deze manier kunnen de loops lopen terwijl,
    # de rest van de code door kan gaan.
    threading.Thread(target=button_check).start()
    threading.Thread(target=afstand_sensor).start()


def launch_dashboard():
    'launch dashboard'
    root.mainloop()


# ---------------------------------------------------------------------------------

#open JSON file
steam_data = open('steam_data.json', 'r')
#zet JSON file om naar iterable format
data_list = (convert_to_list(steam_data))
#maak de layout van het dashbooard
create_dashboard()
#vul het dasboard met alle data en interactieve onderdelen
fill_dashboard(data_list)
#launch
launch_dashboard()
