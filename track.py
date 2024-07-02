import phonenumbers
from phonenumbers import geocoder,carrier
import folium
from opencage.geocoder import OpenCageGeocode
import tkinter as tk
from tkinter import messagebox
import subprocess



def track_number():
    number = phone_entry.get()
    key = "15b9601169804ada97227da2468b7a0c"

    try:
        check_number = phonenumbers.parse(number)
        number_location = geocoder.description_for_number(check_number, "en")

        geocoder_obj = OpenCageGeocode(key)
        query = str(number_location)
        results = geocoder_obj.geocode(query)

        service_provider = phonenumbers.parse(number)
        service_name = carrier.name_for_number(service_provider,"en")

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        map_location = folium.Map(location=[lat, lng], zoom_control=9)
        folium.Marker([lat, lng], popup=f"Location: {number_location}").add_to(map_location)
        map_location.save("mylocation.html")
        messagebox.showinfo("Success", "Location tracked successfully! Check mylocation.html for details.")

        # Update the frame with SIM card name and location
        sim_card_name_label.config(text=f"Service Provider: {service_name}")
        sim_card_location_label.config(text=f"Country: {number_location}")
        supplier_location_label.config(text=f"Location: {lat, lng}")

    except phonenumbers.phonenumberutil.NumberParseException:
        messagebox.showerror("Error", "Invalid phone number. Please enter a valid phone number.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def dashboard():
         root.destroy()
         subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])           


# GUI Setup
root = tk.Tk()
root.title("Phone Number Tracker")
root.configure(bg="white") 
root.geometry("700x400")

# Add a label "Track Suppliers"
track_label = tk.Label(root, text="Track Suppliers", font=("Arial", 28,"bold"), bg="white",fg="black")
track_label.pack(pady=10)
track_label.place(x=170,y=25)

phone_label = tk.Label(root, text="Enter Phone Number:",font=('Microsoft YaHei UI Light', 18),fg="#4B0082")
phone_label.pack(pady=5)
phone_label.place(x=30,y=111)

phone_entry = tk.Entry(root, width=35,bg="#E6E6FA")
phone_entry.pack(pady=10)
phone_entry.place(x=30,y=160,height=30)

submit_button = tk.Button(root, text="Submit", command=track_number, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
submit_button.pack(pady=10)
submit_button.place(x=130,y=280)

back_button = tk.Button(root, text="Back", command=dashboard, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
back_button.pack(pady=10)
back_button.place(x=250,y=280)

# Frame to display SIM card name and location
info_frame = tk.Frame(root, bg="#E6E6FA")
info_frame.pack(pady=20)
info_frame.place(x=350,y=110,width=300,height=150)

sim_card_name_label = tk.Label(info_frame, text="Service Provider: ", font=('Microsoft YaHei UI Light', 12), bg="#E6E6FA")
sim_card_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

sim_card_location_label = tk.Label(info_frame, text="Country: ", font=('Microsoft YaHei UI Light', 12), bg="#E6E6FA")
sim_card_location_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

supplier_location_label = tk.Label(info_frame, text="Location: ", font=('Microsoft YaHei UI Light', 12), bg="#E6E6FA")
supplier_location_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

root.mainloop()
