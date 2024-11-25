from tkinter import * #provides tool for building GUI
import requests # handle HTTP requests to fetch weather from openweatherAPI
import json
import datetime # format sunrise and sunset time from API
import os #manages file path for images
from PIL import ImageTk, Image #processes images

# Initialize Tkinter
root = Tk()
root.title("Weather App") #set title
root.geometry("450x700") #size of window
root['background'] = "white" #background color

# Add your OpenWeatherMap API key here
api_key = "e664097df37cf78483647531b3de9390"

# File Paths for Images
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.png")
sun_path = os.path.join(current_dir, "sun.png")
moon_path = os.path.join(current_dir, "moon.png")
search_icon_path = os.path.join(current_dir, "search_icon.png")  # Search icon for button

# Load and display logo
try:
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((150, 100), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = Label(root, image=logo_img, bg="white")
    logo_label.image = logo_img  # Prevent garbage collection
    logo_label.place(x=150, y=10)
except Exception as e:
    print(f"Error loading logo: {e}")

# Date and Time labels
dt = datetime.datetime.now()
date = Label(root, text=dt.strftime('%A'), bg='white', font=("bold", 15))
date.place(x=10, y=120)
month = Label(root, text=dt.strftime('%d %B'), bg='white', font=("bold", 15))
month.place(x=100, y=120)
hour = Label(root, text=dt.strftime('%I:%M %p'), bg='white', font=("bold", 15))
hour.place(x=10, y=150)

# Add dynamic time-based theme
def update_theme():
    try:
        if 8 <= dt.hour <= 17:  # Daytime
            theme_img = Image.open(sun_path)
        else:  # Nighttime
            theme_img = Image.open(moon_path)

        theme_img = theme_img.resize((100, 100), Image.Resampling.LANCZOS)
        theme_img = ImageTk.PhotoImage(theme_img)
        theme_label = Label(root, image=theme_img, bg="white")
        theme_label.place(x=175, y=160)
        theme_label.image = theme_img  # Prevent garbage collection
    except Exception as e:
        print(f"Error loading theme image: {e}")

update_theme()

# Search Bar with Search Icon
city_name_var = StringVar()
city_entry = Entry(root, textvariable=city_name_var, width=35)
city_entry.place(x=60, y=270)  # Moved down to avoid collision

# Search Button with Icon
try:
    search_img = Image.open(search_icon_path)
    search_img = search_img.resize((40, 40), Image.Resampling.LANCZOS)
    search_img = ImageTk.PhotoImage(search_img)
    search_button = Button(root, image=search_img, command=lambda: fetch_weather(), bg="white", borderwidth=0)
    search_button.place(x=370, y=265)  # Positioned search button to the right of the search bar
    search_button.image = search_img  # Prevent garbage collection
except Exception as e:
    print(f"Error loading search button image: {e}")
    
# fetches weather data from API
def fetch_weather():
    city = city_name_var.get()
    if not city:
        print("Please enter a city name!")
        return

    try:
        # API Call
        api_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        )
        api_request.raise_for_status()
        api = api_request.json()

        # Extract Data
        y = api['main']
        current_temp = y['temp']
        humidity = y['humidity']

        x = api['coord']
        longitude = x['lon']
        latitude = x['lat']

        z = api['sys']
        country = z['country']
        city_name = api['name']

        # Update Labels
        lable_temp.configure(text=f"{current_temp}°C")
        lable_humidity.configure(text=f"{humidity}%")
        lable_lon.configure(text=f"{longitude}")
        lable_lat.configure(text=f"{latitude}")
        lable_country.configure(text=f"{country}")
        lable_citi.configure(text=f"{city_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Error: Invalid city name or API response.")

# Labels for Data/ display weather data
lable_citi = Label(root, text="City: ...", bg='white', font=("bold", 15))
lable_citi.place(x=10, y=340)
lable_country = Label(root, text="Country: ...", bg='white', font=("bold", 15))
lable_country.place(x=135, y=340)
lable_lon = Label(root, text="Lon: ...", bg='white', font=("Helvetica", 15))
lable_lon.place(x=25, y=370)
lable_lat = Label(root, text="Lat: ...", bg='white', font=("Helvetica", 15))
lable_lat.place(x=95, y=370)

lable_temp = Label(root, text="...", bg='white', font=("Helvetica", 60), fg='black')
lable_temp.place(x=150, y=420)

humi = Label(root, text="Humidity:", bg='white', font=("bold", 15))
humi.place(x=3, y=510)
lable_humidity = Label(root, text="...", bg='white', font=("bold", 15))
lable_humidity.place(x=107, y=510)

note = Label(root, text="All temperatures in degree Celsius", bg='white', font=("italic", 10))
note.place(x=95, y=600)

# Run Tkinter Mainloop
root.mainloop()
