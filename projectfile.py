import schedule
import time
import smtplib
import requests,json
import tkinter as tk
from tkinter import messagebox
api_key = "af468ad6524b03946c6e4915a608fac0"
sender_email="weatherdata.py@gmail.com"
sender_email_password="dbgl jfyu oyuo vvkl"
def get_and_send():
    reciver_email=email_entry.get()
    city_name=city_entry.get()
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response=requests.get(complete_url)
    x=response.json()
    if x["cod"]!=404:
        y=x["main"]
        current_temperature=round(y["temp"]-273.15,2)
        current_pressure=y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        #message
        subject=f"Weather Update for {city_name.capitalize()}"
        message=(
		f"Subject: {subject}\n\n"
		f"Dear Recipient\n\n"
		f"Please find below the latest weather update for {city_name.capitalize()}:\n\n"
		" Temperature (in Celsius unit) = " +
					str(current_temperature) +
		"\n atmospheric pressure (in hPa unit) = " +
					str(current_pressure) +
		"\n humidity (in percentage) = " +
					str(current_humidity) +
		"\n description = " +
				    str(weather_description))
        msg1=message
        if "rain" in weather_description.lower():
            msg1=msg1+"\n\nNOTE:Rain is forcasted today.Do remember to carry your umbrella."
        msg1=msg1+"\n\nThank you for your attention\n\n"+"Best Regards,\n"+"Automated weather notification system."
        #email sending
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(sender_email,sender_email_password)
        s.sendmail(sender_email,reciver_email,msg1)
        s.quit()
        print("script succsessfully ran")
    else:
        print("City Not Found!!!")
def schedule_task():
    time=rem_time.get()
    '''l=time.split(".")
    h=0
    m=0
    s=0

    if(len(l)==1):
        h=int(l[0])
    elif(len(l)==2):
        h=int(l[0])
        m=int(l[1])
    elif(len(l)==3):
        h=int(l[0])
        m=int(l[1])
        s=int(l[2])'''
    try:
        schedule.every().day.at(time).do(get_and_send)
        print("daily alert set")
        check_scheduletasks()
    except:
        print("Invalid time format. please use (HH:MM)")
        messagebox.showerror("INVALID TIME FORMAT (HH:MM)")
def check_scheduletasks():
    schedule.run_pending()
    root.after(1000,check_scheduletasks)


root = tk.Tk()
root.title("Weather Notification System")
root.geometry("400x400")

# Add Labels and Entry fields
tk.Label(root, text="Enter City Name:").pack(pady=10)
city_entry = tk.Entry(root, width=30)
city_entry.pack()

tk.Label(root, text="Enter Receiver's Email:").pack(pady=10)
email_entry = tk.Entry(root, width=30)
email_entry.pack()
send_button = tk.Button(root, text="Send Weather Email",command=get_and_send)
send_button.pack(pady=20)
tk.Label(root,text="Daily remainder time (24 hour format)(ex:HH:MM):").pack(pady=10)
rem_time=tk.Entry(root, width=10)
rem_time.pack()
daily_button=tk.Button(root, text="Set Daily Alert",command=schedule_task)
daily_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
