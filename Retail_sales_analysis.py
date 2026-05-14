import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

n = 8000

products = {
    "Electronics": ["Laptop", "Monitor", "Keyboard", "Mouse", "Headphones"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Sofa", "Table"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Hoodie"],
    "Grocery": ["Rice Bag", "Cooking Oil", "Snacks", "Coffee", "Cereal"]
}

regions = ["East", "West", "South", "North", "Central"]
segments = ["Consumer", "Corporate", "Home Office"]
payment_methods = ["Credit Card", "Debit Card", "PayPal", "Cash", "UPI"]
shipping_modes = ["Standard", "Express", "Same Day"]
loyalty_levels = ["Bronze", "Silver", "Gold", "Platinum"]
order_priorities = ["Low", "Medium", "High", "Critical"]
return_status = ["Returned", "Not Returned"]

rows = []

start_date = datetime(2024, 1, 1)

for i in range(1, n + 1):
    category = random.choice(list(products.keys()))
    product = random.choice(products[category])
    quantity = np.random.randint(1, 10)

    unit_price = round(np.random.uniform(10, 1200), 2)
    discount = round(np.random.uniform(0, 0.30), 2)

    revenue = round(quantity * unit_price * (1 - discount), 2)
    cost = round(revenue * np.random.uniform(0.45, 0.80), 2)
    profit = round(revenue - cost, 2)
    profit_margin = round((profit / revenue) * 100, 2) if revenue != 0 else 0

    order_date = start_date + timedelta(days=np.random.randint(0, 730))
    delivery_days = np.random.randint(1, 10)
    ship_date = order_date + timedelta(days=delivery_days)

    rows.append({
        "OrderID": f"ORD{i:05d}",
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "ShipDate": ship_date.strftime("%Y-%m-%d"),
        "CustomerID": f"CUST{np.random.randint(1000, 9999)}",
        "CustomerName": f"Customer_{np.random.randint(1, 2000)}",
        "Segment": random.choice(segments),
        "Gender": random.choice(["Male", "Female"]),
        "AgeGroup": random.choice(["18-25", "26-35", "36-45", "46-60", "60+"]),
        "LoyaltyLevel": random.choice(loyalty_levels),
        "Country": "USA",
        "State": random.choice(["Texas", "California", "New York", "Florida", "Washington", "Illinois"]),
        "City": random.choice(["Dallas", "Austin", "Seattle", "Chicago", "New York", "Miami", "San Francisco"]),
        "Region": random.choice(regions),
        "ProductID": f"PROD{np.random.randint(100, 999)}",
        "ProductName": product,
        "Category": category,
        "SubCategory": product,
        "Brand": random.choice(["NovaTech", "UrbanMart", "PrimeGoods", "ValuePlus", "FreshLine"]),
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Discount": discount,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "ProfitMargin": profit_margin,
        "PaymentMethod": random.choice(payment_methods),
        "ShippingMode": random.choice(shipping_modes),
        "DeliveryDays": delivery_days,
        "OrderPriority": random.choice(order_priorities),
        "ReturnStatus": random.choices(return_status, weights=[12, 88])[0],
        "CustomerRating": np.random.randint(1, 6)
    })

df = pd.DataFrame(rows)

df.to_csv("retail_sales_data.csv", index=False)

print("Dataset created successfully")
print(df.head())
print(df.shape)

print(df.columns)
print(df.info())
print(df.describe())


#creating missing values as our synthetic data is complete
df.loc[50:80, "CustomerRating"] = np.nan
df.loc[120:150, "Profit"] = np.nan
print(df.isnull().sum())

##DATA CLEANING##

#Handling missing values
df["Profit"] = df["Profit"].fillna(df["Profit"].mean())
df["CustomerRating"] = df["CustomerRating"] = df["CustomerRating"].fillna(df["CustomerRating"].median())
print(df[["Profit", "CustomerRating"]].isnull().sum())


#Handiling duplicates
print(df.duplicated().sum())

df = df.drop_duplicates()
print(df.shape)

#Outliner detection
print(df["Revenue"].describe())
print(df["Profit"].describe())

q1 = df["Revenue"].quantile(0.25)
q3 = df["Revenue"].quantile(0.75)
iqr = q3 - q1

lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

outliners = df[(df["Revenue"] < lower_limit) | (df["Revenue"] > upper_limit)]
print(outliners.shape)
print(outliners[["OrderID", "ProductName", "Revenue", "Profit",]].head())


#Featureing Data (Here we are creating new features based on existing data to enhance our analysis)

#Add a new feature "DiscountLevel" based on the "Discount" column
df['DiscountLevel'] = pd.cut(df['Discount'],bins = [-0.01, 0.10, 0.20, 0.30], labels = ["Low Discount", "Medium Discount", "High Discount"])

# data month year
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month 
df["Quarter"] = df["OrderDate"].dt.quarter


#Save Enhanced Dataset
df.to_csv("Retail_sales_cleaned.csv", index = False)

print("Cleaned dataset saved successfully")
print(df.shape)


#KPI(Key Performance Indicator) Calculation
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = df["OrderID"].nunique()
avg_order_value = total_revenue / total_orders
avg_profit_margin = df["ProfitMargin"].mean()


print("Total Revenue:", total_revenue)
print("Total Profit:", total_profit)
print("Total Orders:", total_orders)
print("Average Order Value:", avg_order_value)
print("Average Profit Margin:", avg_profit_margin)

#Top Revenue Products
top_products = df.groupby('ProductName')["Revenue"].sum().sort_values(ascending=False)
print(top_products)

#Regional Revenue
regional_revenue = df.groupby("Region")["Revenue"].sum().sort_values(ascending = False)
print(regional_revenue)

#most profitable category
category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
print(category_profit)

#chart 1 top products by revenue
import matplotlib.pyplot as plt

top_products.head(10).plot(kind = "bar")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Product Name")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#revenue by region
regional_revenue.plot(kind = "bar")
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Total Revenue")
plt.xticks(rotation = 0)
plt.tight_layout()
plt.show()

# 3 Profit by category
category_profit.plot(kind="bar")
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation = 0)
plt.tight_layout()
plt.show()


#Top Preforming Regions:
Profitable_regions = df.groupby("Region")[["Revenue", "Profit"]].sum().sort_values(by = "Revenue", ascending=False)
print(Profitable_regions)
Profitable_regions.plot(kind = "bar")
plt.title("Revenue and Profit by Region")
plt.xlabel("Region")
plt.ylabel("Total Revenue and Profit")
plt.xticks(rotation = 0)
plt.tight_layout()
plt.show()

#customer segment analysis
segment_analysis = df.groupby("Segment")[["Revenue", "Profit"]].mean().sort_values(by = "Revenue", ascending=False)
print(segment_analysis)
#segment_analysis.plot(kind = "bar")
# plt.title("Average Performace per Segment")
# plt.xlabel("Segment")
# plt.ylabel("Total Revenue and Profit")
# plt.xticks(rotation = 0)
# plt.tight_layout()
# plt.show()
#Return Analysis
return_analysis = df.groupby("ReturnStatus")["Profit"].mean()
print(return_analysis)

rating_profit = df.groupby("CustomerRating")["Profit"].mean()
print(rating_profit)

#Monthly Revenue Trend Analysis
monthly_revenue = df.groupby(df["OrderDate"].dt.to_period("M"))["Revenue"].sum()
print(monthly_revenue)


df["OrderDate"] = pd.to_datetime(df["OrderDate"])
monthly_profit = df.groupby(df["OrderDate"].dt.to_period("M"))["Profit"].sum()
print(monthly_profit)

#Yearly Revenue Analysis
yearly_revenue = df.groupby("Year")["Revenue"].sum()
print(yearly_revenue)
yearly_revenue.plot(kind="bar")
plt.title("Yearly Revenue Comparison")
plt.xlabel("Year")
plt.ylabel("Total Revenue")
plt.xticks(rotation = 0)
plt.tight_layout()
plt.show()

#Quarterly Revenue Analysis
quarterly_revenue = df.groupby("Quarter")["Revenue"].sum()
print(quarterly_revenue)
quarterly_revenue.plot(kind="bar")
plt.title("Quarterly Revenue Comparison")
plt.xlabel("Quarter")
plt.ylabel
plt.ylabel
plt.xticks(rotation = 0)
plt.tight_layout()
plt.show()

#Discount Impact Analysis
discount_analysis = df.groupby("DiscountLevel")[["Revenue", "Profit", "ProfitMargin"]].mean()
print(discount_analysis)

#Shipping Performance Analysis
shipping_analysis = df.groupby("ShippingMode")[["Revenue", "Profit", "DeliveryDays", "CustomerRating"]].mean()
print(shipping_analysis)

#correlation
correlation =  df[["Revenue","Profit","Discount","DeliveryDays","CustomerRating"]].corr()
print(correlation)

import matplotlib.pyplot as plt

plt.imshow(correlation)
plt.colorbar()

plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45)
plt.yticks(range(len(correlation.columns)), correlation.columns)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

#FINAL BUSSINESS INSIGHTS
# Revenue and profit showed strong positive correlation, indicating that higher revenue-generating products contributed significantly to overall profitability.

# North region generated the highest revenue and profit, while West region showed comparatively weaker business performance.

# Corporate customers demonstrated the highest average revenue and profitability, suggesting that the corporate segment represents high-value customers.

# Higher discount levels were associated with lower average revenue and profit, indicating that excessive discounting may not effectively improve business performance.

# Same Day shipping generated slightly higher average revenue and profit, while customer ratings remained relatively similar across shipping modes.

# Quarterly trend analysis showed stronger revenue performance during Q2 and Q3, whereas Q4 demonstrated comparatively weaker sales activity.

# Missing values, duplicate records, and revenue outliers were identified and handled during the data cleaning and preprocessing stage to improve overall data quality

import os
print(os.getcwd())