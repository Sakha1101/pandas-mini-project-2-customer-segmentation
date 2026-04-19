"""
Customer Segmentation Analysis
Mini Project 2
"""

import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv("customer_segmentation_mini_project_2.csv")

# 2. Remove exact duplicate rows
df = df.drop_duplicates().copy()

# 3. Clean text columns
text_columns = ["City", "Product_Category", "Payment_Method"]
for col in text_columns:
    df[col] = df[col].astype("string").str.strip().str.lower()

df["Product_Category"] = df["Product_Category"].replace({
    "eletronics": "electronics",
    "home appliance": "home appliances"
})

df["City"] = df["City"].str.title()
df["Product_Category"] = df["Product_Category"].str.title()
df["Payment_Method"] = df["Payment_Method"].str.title()

# 4. Fix data types
df["Age"] = df["Age"].astype("string").str.extract(r"(\d+)", expand=False)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")

df["Number_of_Orders"] = df["Number_of_Orders"].replace({"five": "5"})
df["Number_of_Orders"] = df["Number_of_Orders"].astype("string").str.extract(r"(\d+)", expand=False)
df["Number_of_Orders"] = pd.to_numeric(df["Number_of_Orders"], errors="coerce").astype("Int64")

df["Last_Purchase_Date"] = pd.to_datetime(
    df["Last_Purchase_Date"],
    errors="coerce",
    format="mixed",
    dayfirst=True
)

# 5. Handle missing values
df["Age"] = df["Age"].fillna(df["Age"].median()).astype("Int64")
df["City"] = df["City"].fillna(df["City"].mode()[0])
df["Total_Purchase"] = df["Total_Purchase"].fillna(df["Total_Purchase"].median())
df["Number_of_Orders"] = df["Number_of_Orders"].fillna(df["Number_of_Orders"].median()).astype("Int64")

# 6. Feature engineering
df["Avg_Order_Value"] = np.where(
    df["Number_of_Orders"] == 0,
    0,
    (df["Total_Purchase"] / df["Number_of_Orders"]).round(2)
)

age_conditions = [
    df["Age"] <= 25,
    (df["Age"] > 25) & (df["Age"] <= 45),
    df["Age"] > 45
]
age_labels = ["Young", "Adult", "Senior"]
df["Age_Group"] = np.select(age_conditions, age_labels, default="Unknown")

df["Recency_Days"] = (pd.Timestamp("today").normalize() - df["Last_Purchase_Date"]).dt.days
df["Recency_Days"] = df["Recency_Days"].clip(lower=0)
df["Recency_Days"] = df["Recency_Days"].fillna(999)

# 7. Customer segmentation
purchase_median = df["Total_Purchase"].median()
orders_median = df["Number_of_Orders"].median()

segment_conditions = [
    df["Recency_Days"] > 120,
    (df["Total_Purchase"] > purchase_median) & (df["Recency_Days"] < 60),
    (df["Total_Purchase"] < purchase_median) & (df["Number_of_Orders"] < orders_median)
]
segment_labels = ["At Risk", "High Value", "Low Value"]
df["Customer_Segment"] = np.select(segment_conditions, segment_labels, default="Regular")

# 8. Segment summary
df_segment = (
    df.groupby("Customer_Segment", as_index=False)
      .agg(
          Count_Customers=("Customer_ID", "nunique"),
          Revenue=("Total_Purchase", "sum"),
          Avg_Recency=("Recency_Days", "mean")
      )
)

df_segment["Revenue"] = df_segment["Revenue"].round(2)
df_segment["Avg_Recency"] = df_segment["Avg_Recency"].round(0)

total_customers = df_segment["Count_Customers"].sum()
total_revenue = df_segment["Revenue"].sum()

df_segment["Customer_%"] = (df_segment["Count_Customers"] / total_customers * 100).round(2)
df_segment["Revenue_%"] = (df_segment["Revenue"] / total_revenue * 100).round(2)

df_segment = df_segment.sort_values(by="Revenue", ascending=False).reset_index(drop=True)

print("\nCleaned Dataset Preview:")
print(df.head())

print("\nSegment Summary:")
print(df_segment)

df.to_csv("customer_segmentation_cleaned.csv", index=False)
df_segment.to_csv("customer_segment_summary.csv", index=False)

print("\nFiles saved:")
print("- customer_segmentation_cleaned.csv")
print("- customer_segment_summary.csv")
