import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------
# Load and Prepare the Data
# -------------------------------------------

# Load both sheets from the Excel file
file_path = "Data Analytics Internship Dataset - Bazaar.xlsx"
signup_data = pd.read_excel(file_path, sheet_name=0)  # User Signups
order_data = pd.read_excel(file_path, sheet_name=1)   # Order Details

# Convert date columns to datetime objects
signup_data["signup_date"] = pd.to_datetime(signup_data["signup_date"])
order_data["order_date"] = pd.to_datetime(order_data["order_date"])

# Extract week and month for temporal analysis
signup_data["signup_week"] = signup_data["signup_date"].dt.to_period("W").astype(str)
order_data["order_week"] = order_data["order_date"].dt.to_period("W").astype(str)
signup_data["signup_month"] = signup_data["signup_date"].dt.to_period("M").astype(str)
order_data["order_month"] = order_data["order_date"].dt.to_period("M").astype(str)

# -------------------------------------------
# 1. User Behavior Analysis
# -------------------------------------------

# (1) Count of users who signed up through paid channels
paid_users = signup_data[signup_data["acquisition_platform"].isin(["Google", "Facebook", "Tiktok"])].shape[0]
print(f"Users signed up through Paid Channels: {paid_users}")

# (2) Percentage of users who placed at least one order
users_with_orders = signup_data[signup_data["first_order_date"].notna()]["store_id"].nunique()
total_users = signup_data["store_id"].nunique()
conversion_rate = (users_with_orders / total_users) * 100 if total_users else 0
print(f"Percentage of users who placed at least one order: {conversion_rate:.2f}%")

# (3) Most common acquisition channel
top_channel = signup_data["acquisition_platform"].value_counts().idxmax()
print(f"Most users acquired via: {top_channel}")

# (4) Weekly Conversion Rate (Signup to First Order)
weekly_signups = signup_data.groupby("signup_week")["store_id"].nunique()
weekly_orders = order_data.groupby("order_week")["store_id"].nunique()
conversion_trend = (weekly_orders / weekly_signups).fillna(0) * 100

zoomed_trend = conversion_trend.iloc[8:20]  # Adjust indices as needed

# Plot the zoomed section
plt.figure(figsize=(10, 5))
plt.plot(zoomed_trend.index, zoomed_trend.values, marker="o", linestyle="-", color="blue")
plt.title("Weekly Signup-to-First-Order Conversion Rate (Focused View)")
plt.xlabel("Week")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# (5) Visualizing Signups by Acquisition Channel
plt.figure(figsize=(8, 5))
signup_data["acquisition_platform"].value_counts().plot(kind="bar", color=["#4caf50", "#2196f3", "#f44336", "#9c27b0", "#ff9800"])
plt.title("Signups by Acquisition Channel")
plt.xlabel("Acquisition Channel")
plt.ylabel("Number of Signups")
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 2. Orders and Revenue Analysis
# -------------------------------------------

# (6) Calculate Total Sales per Store Channel
order_data["ordered_quantity"] = order_data["ordered_quantity"].fillna(0)
order_data["updated_price"] = (order_data["amount_per_unit"] - order_data["item_discount"]).abs()
order_data["total_order_value"] = order_data["ordered_quantity"].abs() * order_data["updated_price"]

total_revenue = order_data["total_order_value"].sum()
sales_by_channel = order_data.groupby("store_channel")["total_order_value"].sum()

print(f"\nTotal Revenue (All Channels): ${total_revenue:,.2f}")
print("\nSales by Store Channel:\n")
for channel, value in sales_by_channel.items():
    print(f"{channel}: ${value:,.2f}")


# (7) Average Order Value (AOV)
total_orders = order_data["order_number"].nunique()
AOV = total_revenue / total_orders if total_orders else 0

print(f"\nTotal Orders: {total_orders}")
print(f"Average Order Value (AOV): ${AOV:.2f}")

# (8) Order Cancellation Rate
cancelled_orders = order_data[order_data["order_status"] == "CANCELLED"].shape[0]
cancelled_percentage = (cancelled_orders / total_orders) * 100 if total_orders else 0

print(f"\nCancelled Orders: {cancelled_orders}")
print(f"Cancellation Rate: {cancelled_percentage:.2f}%")

# (9) Daily Sales and Order Trend
daily_sales = order_data.groupby(order_data["order_date"].dt.date)["total_order_value"].sum()
daily_orders = order_data.groupby(order_data["order_date"].dt.date)["order_number"].nunique()

fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot Daily Sales
ax1.plot(daily_sales.index, daily_sales.values, color="blue", marker="o", label="Daily Sales")
ax1.set_xlabel("Date")
ax1.set_ylabel("Total Sales ($)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Plot Daily Orders on second y-axis
ax2 = ax1.twinx()
ax2.plot(daily_orders.index, daily_orders.values, color="red", marker="s", linestyle="--", label="Daily Orders")
ax2.set_ylabel("Total Orders", color="red")
ax2.tick_params(axis="y", labelcolor="red")

plt.title("Daily Trend: Sales vs. Orders")
fig.tight_layout()
plt.show()
