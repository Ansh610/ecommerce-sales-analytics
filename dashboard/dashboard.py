import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# ---------------- AUTO REFRESH ----------------

st_autorefresh(interval=60000, key="refresh")

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")

st.title("🛒 E-commerce Sales Analytics Dashboard")

# ---------------- DATABASE CONNECTION ----------------

df = pd.read_csv("data/ecommerce_data.csv")

# ---------------- FEATURE ENGINEERING ----------------

df["revenue"] = df["price"] * df["quantity"]
df["order_date"] = pd.to_datetime(df["order_date"])

# simulated cost + profit
df["cost"] = df["price"] * 0.7
df["profit"] = df["revenue"] - (df["cost"] * df["quantity"])

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["order_date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["order_date"].max()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

df = df[
    (df["order_date"] >= pd.to_datetime(start_date)) &
    (df["order_date"] <= pd.to_datetime(end_date)) &
    (df["category"].isin(category_filter))
]

# ---------------- KPI METRICS ----------------

total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()
avg_order_value = total_revenue / total_orders

k1, k2, k3, k4 = st.columns(4)

k1.markdown(
f"""
<div style="background: linear-gradient(90deg,#00C9FF,#92FE9D);
padding:20px;border-radius:10px;text-align:center">
<h3>Total Revenue</h3>
<h2>${total_revenue:,.0f}</h2>
</div>
""",
unsafe_allow_html=True)

k2.markdown(
f"""
<div style="background: linear-gradient(90deg,#f7971e,#ffd200);
padding:20px;border-radius:10px;text-align:center">
<h3>Total Orders</h3>
<h2>{total_orders}</h2>
</div>
""",
unsafe_allow_html=True)

k3.markdown(
f"""
<div style="background: linear-gradient(90deg,#667eea,#764ba2);
padding:20px;border-radius:10px;text-align:center">
<h3>Total Customers</h3>
<h2>{total_customers}</h2>
</div>
""",
unsafe_allow_html=True)

k4.markdown(
f"""
<div style="background: linear-gradient(90deg,#ff6a00,#ee0979);
padding:20px;border-radius:10px;text-align:center">
<h3>Avg Order Value</h3>
<h2>${avg_order_value:,.2f}</h2>
</div>
""",
unsafe_allow_html=True)

st.markdown("---")

# ---------------- REVENUE TREND ----------------

st.subheader("📈 Revenue Trend")

monthly_revenue = df.groupby(df["order_date"].dt.to_period("M"))["revenue"].sum()
monthly_revenue.index = monthly_revenue.index.astype(str)

fig1 = px.line(
    x=monthly_revenue.index,
    y=monthly_revenue.values,
    markers=True,
    labels={"x":"Month","y":"Revenue"},
    color_discrete_sequence=["#00BFFF"]
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CATEGORY CHARTS ----------------

col1, col2 = st.columns(2)

category_rev = df.groupby("category")["revenue"].sum().reset_index()

with col1:

    st.subheader("Revenue by Category")

    fig2 = px.bar(
        category_rev,
        x="category",
        y="revenue",
        color="category",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:

    st.subheader("Revenue Share")

    fig3 = px.pie(
        category_rev,
        names="category",
        values="revenue",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------

st.subheader("🏆 Top Products")

top_products = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="product",
    y="revenue",
    color="product",
    color_discrete_sequence=px.colors.qualitative.Set2
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- PROFIT ANALYSIS ----------------

st.subheader("💰 Profit by Category")

profit_data = df.groupby("category")["profit"].sum().reset_index()

fig_profit = px.bar(
    profit_data,
    x="category",
    y="profit",
    color="category",
    color_discrete_sequence=px.colors.qualitative.Dark2
)

st.plotly_chart(fig_profit, use_container_width=True)

# ---------------- SALES HEATMAP ----------------

# ---------------- DARK THEME SALES HEATMAP ----------------

st.subheader("🔥 Sales Activity Heatmap")

heatmap_df = df.copy()

heatmap_df["weekday"] = heatmap_df["order_date"].dt.day_name()
heatmap_df["week"] = heatmap_df["order_date"].dt.isocalendar().week

heatmap_data = heatmap_df.groupby(["weekday", "week"])["revenue"].sum().reset_index()

pivot = heatmap_data.pivot_table(
    index="weekday",
    columns="week",
    values="revenue",
    aggfunc="sum"
)

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
pivot = pivot.reindex(days)

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(14,4))

sns.heatmap(
    pivot,
    cmap="mako",
    linewidths=0.2,
    linecolor="#1f1f1f",
    ax=ax
)

ax.set_title("Sales Activity by Week & Day", fontsize=14, color="white")

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

st.pyplot(fig)

plt.close(fig)
# ---------------- AI INSIGHTS ----------------

st.markdown("---")

st.subheader("🧠 Business Insights")

top_category = category_rev.sort_values("revenue", ascending=False).iloc[0]["category"]
top_product = top_products.iloc[0]["product"]

st.markdown(
f"""
<div style="background-color:#0E1117;padding:20px;border-radius:10px;
border-left:5px solid #00BFFF">

<h4 style="color:#00BFFF">Key Insights</h4>

<ul>
<li><b>{top_category}</b> is the highest revenue generating category.</li>
<li>The best performing product is <b>{top_product}</b>.</li>
<li>Average order value is <b>${avg_order_value:,.2f}</b>.</li>
<li>There are <b>{total_customers}</b> active customers.</li>
</ul>

</div>
""",
unsafe_allow_html=True
)

# ---------------- DOWNLOAD REPORT ----------------

st.subheader("⬇ Download Reports")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="ecommerce_report.csv",
    mime="text/csv",
)

# PDF report

def generate_pdf():

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(100, 750, "E-commerce Sales Report")
    c.drawString(100, 720, f"Total Revenue: ${total_revenue:,.0f}")
    c.drawString(100, 700, f"Total Orders: {total_orders}")
    c.drawString(100, 680, f"Total Customers: {total_customers}")

    c.save()

    buffer.seek(0)

    return buffer

pdf = generate_pdf()

st.download_button(
    label="Download PDF Report",
    data=pdf,
    file_name="sales_report.pdf",
    mime="application/pdf"
)

# ---------------- DATA PREVIEW ----------------

st.subheader("Dataset Preview")

st.dataframe(df.head(100))