from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"

# ---------------- LOAD AND PREPARE DATA ----------------
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE)

    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    data = data.drop_duplicates()
    data = data.dropna(
        subset=["Order_ID", "Order_Date", "Product", "Quantity", "Unit_Price"]
    )

    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["Unit_Price"] = pd.to_numeric(data["Unit_Price"], errors="coerce")
    data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce").fillna(0)
    data = data.dropna(subset=["Quantity", "Unit_Price"])

    # Revenue = (Quantity x Unit Price) - Discount
    data["Revenue"] = (
        data["Quantity"] * data["Unit_Price"] - data["Discount"]
    )
    data["Month"] = data["Order_Date"].dt.to_period("M").astype(str)
    return data

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("🔎 Dashboard Filters")

cities = sorted(df["City"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
products = sorted(df["Product"].dropna().unique().tolist())

selected_cities = st.sidebar.multiselect("Select city", cities, default=cities)
selected_categories = st.sidebar.multiselect(
    "Select category", categories, default=categories
)
selected_products = st.sidebar.multiselect(
    "Select product", products, default=products
)

filtered = df[
    df["City"].isin(selected_cities)
    & df["Category"].isin(selected_categories)
    & df["Product"].isin(selected_products)
].copy()

# ---------------- DASHBOARD TITLE ----------------
st.title("📊 Sales Analytics Dashboard")
st.caption("Explore retail sales performance using the supplied sample dataset.")

if filtered.empty:
    st.warning("No records match the selected filters. Change the filters in the sidebar.")
    st.stop()

# ---------------- KPI CARDS ----------------
total_revenue = filtered["Revenue"].sum()
total_orders = filtered["Order_ID"].nunique()
total_units = filtered["Quantity"].sum()
average_order_value = total_revenue / total_orders if total_orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Units Sold", f"{total_units:,.0f}")
c4.metric("Average Order Value", f"₹{average_order_value:,.0f}")

st.divider()

# ---------------- PREPARE CHART DATA ----------------
product_sales = (
    filtered.groupby("Product", as_index=False)["Revenue"]
    .sum().sort_values("Revenue", ascending=False)
)
city_sales = (
    filtered.groupby("City", as_index=False)["Revenue"]
    .sum().sort_values("Revenue", ascending=False)
)
category_sales = (
    filtered.groupby("Category", as_index=False)["Revenue"]
    .sum().sort_values("Revenue", ascending=False)
)
monthly_sales = (
    filtered.groupby("Month", as_index=False)["Revenue"]
    .sum().sort_values("Month")
)

# ---------------- CHARTS ----------------
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Product")

    fig_product = px.bar(
        product_sales,
        x="Product",
        y="Revenue",
        color="Product",
        text_auto=".2s",
        title="Product-wise Revenue"
    )

    
    fig_product.update_layout(showlegend=False, xaxis_title="Product",
                              yaxis_title="Revenue (₹)")
    st.plotly_chart(fig_product, use_container_width=True)
    

with right:
    st.subheader("Revenue by City")
    fig_city = px.bar(
        city_sales, x="City", y="Revenue",
        color="City", text_auto=".2s",
        title="City-wise Revenue"
    )
    fig_city.update_layout(showlegend=False, xaxis_title="City",
                           yaxis_title="Revenue (₹)")
    st.plotly_chart(fig_city, use_container_width=True)

left2, right2 = st.columns(2)

with left2:
    st.subheader("Revenue by Category")
    fig_category = px.pie(
        category_sales, names="Category", values="Revenue",
        hole=0.4, title="Category-wise Revenue"
    )
    st.plotly_chart(fig_category, use_container_width="stretch")

with right2:
    st.subheader("Monthly Revenue Trend")
    fig_month = px.line(
        monthly_sales, x="Month", y="Revenue",
        markers=True, title="Monthly Revenue"
    )
    fig_month.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹)")
    st.plotly_chart(fig_month, use_container_width=True)

# ---------------- DATA TABLE AND DOWNLOAD ----------------
st.divider()
st.subheader("Filtered Sales Records")
st.dataframe(
    filtered.sort_values("Order_Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download filtered sales data (CSV)",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.caption("Note: This is sample practice data, not actual company/customer data.")
