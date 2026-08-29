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
st.write("This application visualizes the data analysis results from the [`main.ipynb`](https://colab.research.google.com/drive/1ehjZYkU1qc51EdVp6xR9HbH3O-xkzq3X#scrollTo=797afeb4) notebook.")

# --- Display Dataset ---
st.header("1. Full Dataset")
st.write("Complete data from [`smoking.csv`](https://drive.google.com/drive/folders/1KRbSJ_G7LJsG6_saGdbLuYD4is-4Bv8A?usp=sharing):")
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
st.markdown("""
* **Overall Trend:** Non-smokers significantly outnumber smokers across every single gender and marital status category. 
* **Largest Demographic:** The dataset is heavily dominated by married females and married males, the vast majority of whom do not smoke.
* **Highest Smoker Count:** Interestingly, despite married individuals being the largest group overall, the highest number of active smokers is found among **Single Females** and **Single Males**.
* **Proportional Insight:** By comparing the height of the red bars (smokers) to the blue bars (non-smokers), single individuals show a noticeably higher proportion or likelihood of smoking compared to married individuals.""")

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
st.markdown("""
* **Dominant Preference:** "Packets" are the most popular tobacco type for both demographics, peaking significantly at 48 individuals in the 26-40 age group.
* **Age Group Discrepancy:** The 26-40 years demographic shows a much higher total count of smokers across almost all categories compared to the younger 18-25 group.
* **Hand-Rolled Trend:** There is a notable jump in the exclusive use of "Hand-Rolled" tobacco among the older demographic (15 users) compared to the younger demographic (only 2 users).
* **Least Popular Choice:** Mixing habits, particularly leaning towards "Both/Mainly Hand-Rolled", is the least common practice among both age groups.
""")

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
st.markdown("""
* **Consistent Habits:** The most prevalent smoking behavior is consistency. The top three patterns (20/20, 15/15, and 10/10) indicate that most individuals consume the exact same amount of cigarettes on weekends as they do on weekdays.
* **Heavy Consumption Peak:** The highest count belongs to the 20 cigarettes per day habit (equivalent to a standard full pack). This is overwhelmingly driven by the 26-40 age group (14 individuals).
* **Demographic Dominance:** Across every single one of the top 10 patterns, the older 26-40 demographic consistently outnumbers the younger 18-25 group.
* **Weekend Spikes:** While daily consistency is the norm, there are specific segments (like the "20.0 / 10.0" and "15.0 / 10.0" groups) representing social or leisure smokers who double their consumption during the weekend compared to regular workdays.
""")

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
st.markdown("""
* **Income Disparity:** There is a notable inverse relationship between the represented income brackets and the prevalence of smoking. 
* **Lower Income Peak:** The lower-income bracket (5,200 to 10,400) harbors a higher absolute number of active smokers (107 individuals).
* **Higher Income Drop:** As gross income moves up into the next bracket (10,400 to 15,600), the number of smokers noticeably drops to 83 individuals, suggesting a potential correlation between lower socioeconomic status and higher smoking rates within this specific data slice.
""")

st.divider()

st.header("Summary")
st.write("""
* **Demographic Vulnerability:** While married individuals make up the majority of the dataset, single individuals exhibit a proportionally higher tendency to smoke.
* **Consumption Habits:** Smokers generally maintain consistent habits throughout the week, with 20 cigarettes per day being the most common peak, especially among the 26-40 age group.
* **Product Preference:** "Packets" completely dominate the market preference across all observed age groups, while "Hand-Rolled" remains a niche choice.
* **Socioeconomic Correlation:** The data suggests an inverse relationship between income and smoking prevalence, with the lower-income bracket (5,200 to 10,400) containing the highest absolute number of smokers.
""")