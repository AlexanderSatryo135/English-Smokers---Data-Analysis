import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Page configuration
st.set_page_config(page_title="Smoking Data Analysis", page_icon="📊", layout="wide")

# Load data 
@st.cache_data
def load_data():
    return pd.read_csv('smoking.csv')

df = load_data()

# App Title
st.title("Smoking Data Analysis")
st.write("This application visualizes the data analysis results from the `main.ipynb` notebook.")

# --- Display Dataset ---
st.header("1. Full Dataset")
st.write("Complete data from `smoking.csv`:")
st.dataframe(df)

st.divider()

# --- Visualization 1: Smoking Status by Gender and Marital Status ---
st.header("2. Smoking Status by Gender and Marital Status")
cross_tab = pd.crosstab([df["gender"], df["marital_status"]], df["smoke"])

fig1, ax1 = plt.subplots(figsize=(12, 6))
cross_tab.plot(kind='bar', color=['skyblue', 'salmon'], ax=ax1)

ax1.set_title('Smoking Status by Gender and Marital Status', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Gender & Marital Status', fontsize=12)
ax1.set_ylabel('Count', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig1)

st.divider()

# --- Visualization 2: Preferred Tobacco Type by Age Group (English Smokers) ---
st.header("3. Preferred Tobacco Type by Age Group (English Smokers)")
young_types = df[(df["smoke"] == "Yes") & (df["age"].between(18, 25)) & (df["nationality"] == "English")]["type"].value_counts()
adult_types = df[(df["smoke"] == "Yes") & (df["age"].between(26, 40)) & (df["nationality"] == "English")]["type"].value_counts()

combined_data1 = pd.DataFrame({
    '18 - 25 Years': young_types,
    '26 - 40 Years': adult_types
}).fillna(0)

fig2, ax2 = plt.subplots(figsize=(10, 6))
combined_data1.plot(kind='bar', color=['skyblue', 'salmon'], width=0.7, ax=ax2)

for container in ax2.containers:
    ax2.bar_label(container, fmt='%.0f', padding=3)

ax2.set_title('Preferred Tobacco Type by Age Group (English Smokers)', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Tobacco Type', fontsize=12)
ax2.set_ylabel('Count', fontsize=12)
ax2.tick_params(axis='x', rotation=0)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig2)

st.divider()


# --- Visualization 3: Top 10 Smoking Patterns (Weekend / Weekday Amount) by Age Group ---
st.header("4. Top 10 Smoking Patterns by Age Group")
st.write("Number of cigarettes smoked on weekends vs weekdays.")

young_amt = df[(df["smoke"] == "Yes") & (df["age"].between(18, 25)) & (df["nationality"] == "English")][["amt_weekends", "amt_weekdays"]].value_counts()
young_amt.index = [f"{wnd} / {wdy}" for wnd, wdy in young_amt.index]

adult_amt = df[(df["smoke"] == "Yes") & (df["age"].between(26, 40)) & (df["nationality"] == "English")][["amt_weekends", "amt_weekdays"]].value_counts()
adult_amt.index = [f"{wnd} / {wdy}" for wnd, wdy in adult_amt.index]

combined_data2 = pd.DataFrame({
    '18 - 25 Years': young_amt,
    '26 - 40 Years': adult_amt
}).fillna(0)

combined_data2['Total'] = combined_data2['18 - 25 Years'] + combined_data2['26 - 40 Years']
combined_data2 = combined_data2.sort_values(by='Total', ascending=False).head(10).drop(columns=['Total'])

fig3, ax3 = plt.subplots(figsize=(12, 6))
combined_data2.plot(kind='bar', color=['skyblue', 'salmon'], width=0.7, ax=ax3)

for container in ax3.containers:
    ax3.bar_label(container, fmt='%.0f', padding=3)

ax3.set_title('Top 10 Smoking Patterns (Weekend / Weekday Amount) by Age Group', fontsize=14, fontweight='bold', pad=15)
ax3.set_xlabel('Amount (Weekends / Weekdays)', fontsize=12)
ax3.set_ylabel('Count (People)', fontsize=12)
ax3.tick_params(axis='x', rotation=45)
ax3.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig3)

st.divider()

# --- Visualization 4: Smokers Count by Gross Income ---
st.header("5. Smokers Count by Gross Income")

low_income_smokers = df[(df["gross_income"] == "5,200 to 10,400") & (df["smoke"] == "Yes")].shape[0]
mid_income_smokers = df[(df["gross_income"] == "10,400 to 15,600") & (df["smoke"] == "Yes")].shape[0]

income_labels = ['5,200 to 10,400', '10,400 to 15,600']
counts = [low_income_smokers, mid_income_smokers]

fig4, ax4 = plt.subplots(figsize=(8, 5))
bars = ax4.bar(income_labels, counts, color=['mediumseagreen', 'orange'], width=0.5)

ax4.bar_label(bars, fmt='%d', padding=3, fontsize=11)
ax4.set_title('Smokers Count by Gross Income', fontsize=14, fontweight='bold', pad=15)
ax4.set_xlabel('Gross Income Group', fontsize=12)
ax4.set_ylabel('Number of Smokers', fontsize=12)
ax4.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig4)