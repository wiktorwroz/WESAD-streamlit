# ===============================
# 1️⃣ Importy
# ===============================
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# ===============================
# 2️⃣ Wczytanie przetworzonych danych
# ===============================
pkl_path = "/Users/turfian/Downloads/archive (4)/WESAD/S2/S2.pkl"
with open(pkl_path, "rb") as f:
    data = pickle.load(f)  # zakładam, że to DataFrame z czasem i cechami

# Sprawdzenie kolumn
print(data.columns)

# ===============================
# 3️⃣ Wybór top 4 cech (przykład ręczny, możesz zmienić)
# ===============================
top_features = ["TEMP", "HR", "EDA", "BVP"]  # zmień jeśli Shapley wskaże inne
time_col = "time"  # zakładam, że masz kolumnę z czasem
label_col = "label"  # zakładam, że baseline/emotion w tej kolumnie

# ===============================
# 4️⃣ Wykresy liniowe trendów
# ===============================
sns.set(style="whitegrid")
plt.figure(figsize=(15,10))

for i, feat in enumerate(top_features):
    plt.subplot(2,2,i+1)
    for grp, grp_data in data.groupby(label_col):
        plt.plot(grp_data[time_col], grp_data[feat], label=grp)
    plt.title(feat)
    plt.xlabel("Time")
    plt.ylabel(feat)
    plt.legend()

plt.tight_layout()
plt.show()

# ===============================
# 5️⃣ Streamlit (komórka na końcu notebooka)
# ===============================
st.title("Trend czasowy wybranych cech WESAD")
st.write("Top 4 cechy wybrane metodą interpretowalności (Shapley lub manualnie)")

selected_feature = st.selectbox("Wybierz cechę do wyświetlenia", top_features)

for grp, grp_data in data.groupby(label_col):
    st.line_chart(pd.DataFrame({
        selected_feature: grp_data[selected_feature].values
    }, index=grp_data[time_col]), use_container_width=True)