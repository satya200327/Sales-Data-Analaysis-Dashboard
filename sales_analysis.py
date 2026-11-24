"""
Sales Data Analysis Project
Run: python sales_analysis.py
The script reads sales_data.csv and creates summary CSV files and charts in output/.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_FILE)
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# 2. Clean data
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df = df.drop_duplicates()
df = df.dropna(subset=["Order_ID", "Order_Date", "Product", "Quantity", "Unit_Price"])
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0)
df = df.dropna(subset=["Quantity", "Unit_Price"])
df["Revenue"] = (df["Quantity"] * df["Unit_Price"]) - df["Discount"]

# 3. Key business metrics
total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()
average_order_value = total_revenue / total_orders if total_orders else 0

print("\n--- BUSINESS SUMMARY ---")
print(f"Total revenue: Rs. {total_revenue:,.2f}")
print(f"Number of orders: {total_orders}")
print(f"Units sold: {total_units:,.0f}")
print(f"Average order value: Rs. {average_order_value:,.2f}")

# 4. Grouped analysis
product_sales = df.groupby("Product", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
city_sales = df.groupby("City", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
category_sales = df.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
monthly_sales = (
    df.assign(Month=df["Order_Date"].dt.to_period("M").astype(str))
      .groupby("Month", as_index=False)["Revenue"].sum()
)

product_sales.to_csv(OUTPUT_DIR / "product_sales.csv", index=False)
city_sales.to_csv(OUTPUT_DIR / "city_sales.csv", index=False)
category_sales.to_csv(OUTPUT_DIR / "category_sales.csv", index=False)
monthly_sales.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)

print("\n--- PRODUCT-WISE REVENUE ---")
print(product_sales.to_string(index=False))
print("\n--- CITY-WISE REVENUE ---")
print(city_sales.to_string(index=False))
print("\n--- CATEGORY-WISE REVENUE ---")
print(category_sales.to_string(index=False))
print("\n--- MONTHLY REVENUE ---")
print(monthly_sales.to_string(index=False))

# 5. Visualizations
sns.set_theme(style="whitegrid")

plt.figure(figsize=(9, 5))
sns.barplot(data=product_sales, x="Product", y="Revenue")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_product.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
sns.barplot(data=city_sales, x="City", y="Revenue")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_city.png", dpi=150)
plt.close()

plt.figure(figsize=(9, 5))
sns.lineplot(data=monthly_sales, x="Month", y="Revenue", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

print(f"\nDone! Summary files and charts are saved in: {OUTPUT_DIR}")
