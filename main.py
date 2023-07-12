from configparser import ConfigParser
from tkinter import messagebox
from tkinter import *
import requests
import funcs
import time
import datetime
from datetime import datetime


# Getting url and api key from 'config.ini' file
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']
url = config['url']['url']


def search_histoty():
    new_window = Toplevel(root)
    new_window.title("Search History")
    new_window.configure(bg="white", padx=10, pady=10)
    new_window.resizable(False, False)
    
    new_window.grid_rowconfigure(0, weight=1)
    new_window.grid_columnconfigure(0, weight=1)
    
    search_histoty_frame = Frame(new_window, bg="#15317E", pady=5, padx=30)
    search_histoty_frame.grid(row=0, sticky="nsew")
    search_histoty_frame.grid_rowconfigure(0, weight=1)
    search_histoty_frame.grid_columnconfigure(0, weight=1)

    
    text = StringVar()
    history = funcs.Show_search_history()
    search = ""
    for _ in history:
        search += _
    text.set(search)

    Empty = "Database is Empty! +_+"
    if len(text.get()) == 0:
        text.set(Empty)

    text = Label(search_histoty_frame,
                   textvariable=text,
                   fg="white", bg='#15317E',
                   bd=3, font=('mincho', 13), pady=10)
    text.grid(sticky="nsew")

    erase_history = Button(search_histoty_frame, anchor=CENTER,
           relief=RAISED,
           text="Delete Search Results",
           bg="#15317E", fg="#FFFFFF", bd=3,
           pady=4, command=lambda: [funcs.Erase_data(),
                                    new_window.destroy()])
    erase_history.grid(sticky="ews")


def clear_search_bar(*args, **kwargs):
    search_bar.delete(0, END)


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (city, country, temp_celcius, temp_fahrenheit, icons, weather, description_weather, time,
        #  sunrise, sunset, min_temp, max_temp)
        city = json['name']
        country = json['sys']['country']
        temp_celcius = json['main']['temp'] - 273.15
        temp_fahrenheit = temp_celcius * 9 / 5 + 32
        icons = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        description_weather = json['weather'][0]['description']
        time = json['timezone']
        sunrise = json["sys"]["sunrise"]
        sunset = json["sys"]["sunset"]
        min_temp = json["main"]["temp_min"]
        max_temp = json["main"]["temp_max"]

        final = (city, country, temp_celcius, temp_fahrenheit, icons, weather, description_weather, time,
                 sunrise, sunset, min_temp, max_temp)
        funcs.Data_Base((city, country, temp_celcius,
                        temp_fahrenheit, weather, time))
        return final

    else:
        return None


def search():
    try:
        city = search_text.get()
        weather = get_weather(city)
        # weather = (city,country, temp_celcius, temp_fahrenheit, icons, weather, description_weather)
        search_bar.delete(0, END)
        search_bar.insert(0, f'Result for {city.title()}:')

        location["text"] = "{}, {}".format(weather[0], weather[1])
        temperature['text'] = '{:.2f}°C, {:.2f}°F'.format(
            weather[2], weather[3])
        weather_detail['text'] = "{}, {}".format(weather[5], weather[6])
        image['file'] = "icons/{}.png".format(weather[4])
        sunrise["text"] = "Sunrise: {} am".format(datetime.utcfromtimestamp(
            weather[8] + int(weather[7])).strftime('%c')[11:16])
        sunset["text"] = "Sunset: {} pm".format(datetime.utcfromtimestamp(
            weather[9] + int(weather[7] - 43200)).strftime('%c')[11:16])
        max_temp["text"] = "High temperature: {:.2f}°C, {:.2f}°F".format(
            int(weather[11]) - 273.15, (int(weather[11])-273.15)*9/5 + 32)
        min_temp["text"] = "Low temperature: {:.2f}°C, {:.2f}°F".format(
            int(weather[10]) - 273.15, (int(weather[10])-273.15)*9/5 + 32)

        while True:
            city_current_time['text'] = funcs.utc_con(int(weather[7]))
            root.update_idletasks()
            root.update()
            time.sleep(0.5)

    except TypeError:
        messagebox.showerror(
            "Error", "Can't find city \"{}\"".format(city))


root = Tk()
root.title("Weather App")
width, height = 700, 500
root.geometry(f"{width}x{height}")
root.configure(bg="white", padx=1, pady=1)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)


# -----MENU-----#
menubar = Menu()
file_menu = Menu(menubar, tearoff=False)
file_menu.add_command(label="Search History", command=search_histoty)
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(menu=file_menu, label="File")
root.config(menu=menubar)

# -----HEADER-----#
header = Frame(root,
               bg="#15317E",
               pady=3)
header.grid(row=0, sticky="nsew")
header.grid_rowconfigure(1, weight=1)
header.grid_columnconfigure(0, weight=1)

# Intro Text
intro = Label(header,
              text="We show you weather",
              font=("mincho", 25, 'italic'),
              bg="#15317E",
              fg="#FFFFFF",
              padx=50)
intro.grid(row=0, column=0, sticky="nsew")


# Search Bar
search_text = StringVar()
search_bar = Entry(header,
                   textvariable=search_text,
                   font=("mincho", 10, "italic"),
                   bg="white",
                   fg='#15317E',
                   bd=0,
                   width=25,
                   highlightthickness=0)
search_bar.insert(0, "search here...")
search_bar.bind("<Button-1>", clear_search_bar)
search_bar.grid(row=0, column=1, sticky="nsew")

# Search Button
search_btn_icon = PhotoImage(file="icons/search_icon.png").subsample(2, 2)
search_btn = Button(header,
                    image=search_btn_icon,
                    cursor="hand2",
                    highlightthickness=0,
                    bd=0,
                    bg="#15317E",
                    activebackground="#15317E",
                    command=search)
search_btn.grid(row=0, column=2, sticky="nsew")


# -----BODY-----#
body = Frame(root,
             bg='white',
             # width=width,
             # height=400,
             padx=5,
             pady=5)
body.grid(row=1, sticky="nsew")
body.grid_rowconfigure(0, weight=1)
body.grid_columnconfigure(0, weight=1)

# Location
location = Label(body,
                 text="",
                 font=('mincho', 20, "bold"),
                 fg='#15317E',
                 bg="white")
location.grid()

# Time
city_current_time = Label(body,
                          text="",
                          fg='#15317E',
                          bg="white",
                          font=("SimSun", 14))
city_current_time.grid()

# Image
image = PhotoImage(file="")
weather_image = Label(body,
                      image=image,
                      bg="white")
weather_image.grid()

# Weather Info
weather_detail = Label(body,
                       text="",
                       fg='#15317E',
                       bg="white",
                       font=("mincho", 15))
weather_detail.grid()

# Temperature
temperature = Label(body,
                    text="",
                    fg='#15317E',
                    bg="white",
                    font=("SimSun-ExtB", 22))
temperature.grid()

# Sunrise Time
sunrise = Label(body,
                text="",
                fg='#15317E',
                bg="white",
                font=("mincho", 13))
sunrise.grid()

# Sunset Time
sunset = Label(body,
               text="",
               fg='#15317E',
               bg="white",
               font=("mincho", 13))
sunset.grid()

# Maximum Temperature
max_temp = Label(body,
                 text="",
                 fg='#15317E',
                 bg="white",
                 font=("mincho", 13))
max_temp.grid()

# Minimum Temperature
min_temp = Label(body,
                 text="",
                 fg='#15317E',
                 bg="white",
                 font=("mincho", 13))
min_temp.grid()


# -----FOOTER-----#
footer = Frame(root,
               bg="#15317E",
               # width=width,
               # height=50,
               pady=3)
footer.grid(row=2, sticky="ew")
footer.grid_rowconfigure(0, weight=1)
footer.grid_columnconfigure(0, weight=1)

footer_lable = Label(footer,
                     text="developed by amir")
footer_lable.grid()


root.mainloop()
