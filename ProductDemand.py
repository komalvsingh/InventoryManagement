import pandas as pd

import seaborn as sns
import plotly.express as px  # Import Plotly
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

data = pd.read_excel("C:\\Users\\ACER\\IdeaProjects\\exceldata.xlsx")
data.dropna()

# Create a scatter plot using Plotly
fig = px.scatter(data, x="Sales per Year", y="Product Name", size="Sales per Year")
fig.show()
x = data[["Sales per Year","Year"]]
y = data["Sales per Year"]
xtrain,xtest,ytrain,ytest= train_test_split(x,y,test_size=0.2,random_state=42)
model = DecisionTreeRegressor()
model.fit(xtrain,ytrain)
DecisionTreeRegressor()
