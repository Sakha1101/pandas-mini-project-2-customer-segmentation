# Customer Segmentation Analysis

## Objective
Segment customers based on value and behavior to identify:
- High-value customers
- At-risk customers
- Low-value customers
- Regular customers

## Dataset
This project uses a messy retail customer dataset with:
- 700+ rows
- Missing values
- Mixed date formats
- Wrong data types
- Inconsistent text categories
- Outliers
- Duplicate rows

## Workflow
1. Load dataset
2. Remove duplicate rows
3. Clean text columns
4. Fix data types
5. Handle missing values
6. Create new features:
   - Avg_Order_Value
   - Age_Group
   - Recency_Days
7. Segment customers
8. Build summary table

## Segmentation Logic
- At Risk: Recency_Days > 120
- High Value: Total_Purchase above median and Recency_Days < 60
- Low Value: Total_Purchase below median and Number_of_Orders below median
- Regular: Remaining customers

## Output Files
- customer_segmentation_analysis.py
- customer_segmentation_cleaned.csv
- customer_segment_summary.csv

## Tools Used
- Python
- Pandas
- NumPy

## Business Value
This analysis helps a business:
- identify inactive customers
- protect revenue from churn
- target high-value customers
- plan retention and re-engagement campaigns
