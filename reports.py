import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


data = pd.read_excel("C:\\Users\\ACER\\IdeaProjects\\exceldata.xlsx")


data['Product Name'] = data['Product Name'].str.lower().str.strip()


product_stock = data.groupby('Product Name')['Stock Value'].sum()


total_stock_value = product_stock.sum()

stock_percentage = (product_stock / total_stock_value) * 100


fig, ((ax1, ax2), (ax4, ax3)) = plt.subplots(2, 2, figsize=(10, 8))

ax1.bar(product_stock.index, product_stock)
ax1.set_title("Stock Statistic")
ax1.set_ylabel("Stock Values")
ax1.tick_params(axis='x', rotation=90)  


ax2.pie(stock_percentage, labels=product_stock.index, autopct='%1.1f%%', startangle=140)
ax2.set_title("Stock Distribution")
ax2.axis('equal') 


ax3.bar(data['Supplier'], data['Product Name'], color='skyblue')
ax3.set_ylabel("Product Name")
ax3.set_xlabel("Supplier")
ax3.set_title("Suppliers Distribution")
ax3.tick_params(axis='x', rotation=90) 


for product_name, product_data in data.groupby('Product Name'):
    product_data = product_data.set_index('Year')
    ax4.scatter(product_data.index, product_data['Sales per Year'], label=product_name)

years = [2021, 2022, 2023, 2024]
ax4.set_xticks(years)
ax4.set_xticklabels(years)
ax4.set_xlabel("Year")
ax4.set_ylabel("Sales per Year")
ax4.set_title("Sales per Year Distribution")
ax4.legend()  


plt.tight_layout()


root = tk.Tk()
root.title("Data Visualization")


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create function for button click
def button_click():
    print("Button clicked")

# Add button at the bottom of the window
button = tk.Button(root, text="Click Me", command=button_click,background="black")
button.pack(side=tk.BOTTOM)

# Run tkinter main loop
root.mainloop()
