#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("Libraries imported successfully!")


# In[2]:


df = pd.read_csv('C:/Users/shraw/OneDrive/Desktop/EV_analytics_project/global_ev_adoption_behavior_2026.csv')

print("Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
df.head()


# In[3]:


print("=== DATA TYPES ===")
print(df.dtypes)

print("\n=== NULL VALUES ===")
print(df.isnull().sum())

print("\n=== BASIC STATISTICS ===")
df.describe()


# In[4]:


# === DATA CLEANING ===

# 1. Fill education_level nulls with mode (most common value)
df['education_level'].fillna(df['education_level'].mode()[0], inplace=True)

# 2. Fill charging_station_accessibility nulls with median
df['charging_station_accessibility'].fillna(df['charging_station_accessibility'].median(), inplace=True)

# 3. Fill ev_knowledge_score nulls with median
df['ev_knowledge_score'].fillna(df['ev_knowledge_score'].median(), inplace=True)

# Verify nulls are gone
print("Nulls after cleaning:")
print(df.isnull().sum().sum(), "total nulls remaining")
print("\nShape after cleaning:", df.shape)


# In[5]:


# Clean version without warnings
df['education_level'] = df['education_level'].fillna(df['education_level'].mode()[0])
df['charging_station_accessibility'] = df['charging_station_accessibility'].fillna(df['charging_station_accessibility'].median())
df['ev_knowledge_score'] = df['ev_knowledge_score'].fillna(df['ev_knowledge_score'].median())

print("Data cleaning complete!")
print("Total nulls remaining:", df.isnull().sum().sum())


# In[6]:


# === VISUALIZATION 1: EV Adoption Likelihood Distribution ===

adoption_counts = df['ev_adoption_likelihood'].value_counts()

plt.figure(figsize=(8, 6))
plt.pie(adoption_counts, 
        labels=adoption_counts.index, 
        autopct='%1.1f%%',
        colors=['#2ecc71', '#f39c12', '#e74c3c'],
        startangle=90)
plt.title('EV Adoption Likelihood Distribution', fontsize=16, fontweight='bold')
plt.savefig('ev_adoption_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 1 saved!")


# In[7]:


# === VISUALIZATION 2: EV Adoption by City Type ===

plt.figure(figsize=(10, 6))
city_adoption = df.groupby(['city_type', 'ev_adoption_likelihood']).size().unstack()
city_adoption.plot(kind='bar', 
                   color=['#e74c3c', '#2ecc71', '#f39c12'],
                   edgecolor='white',
                   figsize=(10, 6))
plt.title('EV Adoption Likelihood by City Type', fontsize=16, fontweight='bold')
plt.xlabel('City Type', fontsize=12)
plt.ylabel('Number of People', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='Adoption Likelihood')
plt.savefig('ev_adoption_by_city.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 2 saved!")


# In[8]:


# === VISUALIZATION 3: Average Annual Income by EV Adoption Likelihood ===

plt.figure(figsize=(8, 6))
income_adoption = df.groupby('ev_adoption_likelihood')['annual_income'].mean().sort_values(ascending=False)

bars = plt.bar(income_adoption.index, 
               income_adoption.values,
               color=['#2ecc71', '#f39c12', '#e74c3c'],
               edgecolor='white',
               width=0.5)

# Add value labels on top of each bar
for bar, value in zip(bars, income_adoption.values):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 500,
             f'₹{value:,.0f}', ha='center', va='bottom', fontweight='bold')

plt.title('Average Annual Income by EV Adoption Likelihood', fontsize=16, fontweight='bold')
plt.xlabel('EV Adoption Likelihood', fontsize=12)
plt.ylabel('Average Annual Income', fontsize=12)
plt.savefig('income_by_adoption.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 3 saved!")


# In[9]:


# === VISUALIZATION 4: Fuel Expense by Vehicle Type ===

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, 
            x='current_vehicle_type', 
            y='fuel_expense_per_month',
            palette='Set2')
plt.title('Fuel Expense Distribution by Vehicle Type', fontsize=16, fontweight='bold')
plt.xlabel('Vehicle Type', fontsize=12)
plt.ylabel('Fuel Expense Per Month', fontsize=12)
plt.xticks(rotation=15)
plt.savefig('fuel_expense_by_vehicle.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 4 saved!")


# In[10]:


# === VISUALIZATION 5: Correlation Heatmap ===

plt.figure(figsize=(14, 10))
numeric_cols = df.select_dtypes(include=[np.number])
correlation = numeric_cols.corr()

sns.heatmap(correlation,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            linewidths=0.5,
            annot_kws={'size': 8})
plt.title('Correlation Heatmap of Numeric Features', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 5 saved!")


# In[11]:


# === VISUALIZATION 6: EV Knowledge Score by Education Level ===

plt.figure(figsize=(10, 6))
edu_knowledge = df.groupby('education_level')['ev_knowledge_score'].mean().sort_values(ascending=False)

bars = plt.bar(edu_knowledge.index,
               edu_knowledge.values,
               color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'],
               edgecolor='white',
               width=0.5)

for bar, value in zip(bars, edu_knowledge.values):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

plt.title('Average EV Knowledge Score by Education Level', fontsize=16, fontweight='bold')
plt.xlabel('Education Level', fontsize=12)
plt.ylabel('Average EV Knowledge Score', fontsize=12)
plt.xticks(rotation=15)
plt.savefig('knowledge_by_education.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 6 saved!")


# In[12]:


# === EXPORT CLEANED DATA FOR POWER BI ===

df.to_csv('C:/Users/shraw/OneDrive/Desktop/EV_analytics_project/ev_cleaned_data.csv', index=False)

print("Cleaned data exported successfully!")
print("Total rows exported:", len(df))
print("Total columns exported:", len(df.columns))


# In[ ]:




