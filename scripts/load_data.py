"""
Amazon Product Analysis
Step 1 : Load Dataset

Author : Jitendra More
"""

import os
import pandas as pd

print("=" * 60)
print(" AMAZON PRODUCT DATA ANALYSIS ")
print("=" * 60)

# =====================================
# Create Output Folders
# =====================================

os.makedirs("output", exist_ok=True)
os.makedirs("output/charts", exist_ok=True)
os.makedirs("output/reports", exist_ok=True)

# =====================================
# Load Dataset
# =====================================

DATA_PATH = "data/amazon.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print("\n✅ Dataset Loaded Successfully")

except FileNotFoundError:
    print("\n❌ Dataset not found.")
    exit()

# =====================================
# Dataset Shape
# =====================================

print("\nDataset Shape")
print("-" * 60)
print(df.shape)

# =====================================
# First 5 Records
# =====================================

print("\nFirst 5 Records")
print("-" * 60)
print(df.head())

# =====================================
# Last 5 Records
# =====================================

print("\nLast 5 Records")
print("-" * 60)
print(df.tail())

# =====================================
# Dataset Information
# =====================================

print("\nDataset Information")
print("-" * 60)
df.info()

# =====================================
# Column Names
# =====================================

print("\nColumn Names")
print("-" * 60)

for column in df.columns:
    print(column)

# =====================================
# Missing Values
# =====================================

print("\nMissing Values")
print("-" * 60)
print(df.isnull().sum())

# =====================================
# Duplicate Rows
# =====================================

print("\nDuplicate Rows")
print("-" * 60)
print(df.duplicated().sum())

# =====================================
# Dataset Summary
# =====================================

print("\nDataset Summary")
print("-" * 60)
print(df.describe(include="all"))

print("\n" + "=" * 60)
print("LOAD DATA COMPLETED")
print("=" * 60)