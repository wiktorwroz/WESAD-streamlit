# 🔹 STREAMLIT APP - DEMO MONITOROWANIA STRESU
# Uruchom: streamlit run streamlit_stress_demo.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm

# Konfiguracja strony
st.set_page_config(
    page_title="Monitorowanie Stresu - Demo",
    page_icon="📊",
    layout="wide"
)

# Tytuł
st.title("📊 Monitorowanie Stresu - Aplikacja Demo")
st.markdown("---")

# KROK 2: Definicja 2 sztywnych profili użytkownika
PROFILES = {
    "Profil 1 - Chwilowy stres": {
        "HR_mean": 85,
        "HRV_RMSSD": 28,
        "HRV_SDNN": 42,
        "TEMP_mean": 36.8,
        "description": "Reakcja krótkoterminowa, powrót do normy możliwy",
        "interpretation": "Wzorzec odpowiada chwilowej reakcji stresowej"
    },
    "Profil 2 - Przewlekłe przeciążenie": {
        "HR_mean": 95,
        "HRV_RMSSD": 15,
        "HRV_SDNN": 25,
        "TEMP_mean": 37.2,
        "description": "Brak pełnej regeneracji, trwałe obciążenie",
        "interpretation": "Wzorzec wskazuje na możliwe przewlekłe przeciążenie"
    }
}

# Wartości referencyjne (normalne zakresy)
REFERENCE_VALUES = {
    "HR_mean": {"normal": (60, 100), "label": "HR (bpm)"},
    "HRV_RMSSD": {"normal": (25, 50), "label": "HRV RMSSD (ms)"},
    "HRV_SDNN": {"normal": (30, 60), "label": "HRV SDNN (ms)"},
    "TEMP_mean": {"normal": (36.0, 37.0), "label": "Temperatura (°C)"}
}

# KROK 3: UI - wybór profilu
st.header("🔍 Wybór Profilu Użytkownika")

selected_profile = st.radio(
    "Wybierz profil do analizy:",
    options=list(PROFILES.keys()),
    horizontal=True
)

st.markdown("---")

# Pobierz dane wybranego profilu
profile_data = PROFILES[selected_profile]

# Wyświetl tabelę z parametrami
st.subheader("📋 Parametry Fizjologiczne")

# Przygotuj DataFrame do wyświetlenia
params_df = pd.DataFrame([
    {
        "Parametr": "HR_mean",
        "Wartość": profile_data["HR_mean"],
        "Jednostka": "bpm",
        "Status": "⚠️ Podwyższony" if profile_data["HR_mean"] > 80 else "✅ Normalny"
    },
    {
        "Parametr": "HRV_RMSSD",
        "Wartość": profile_data["HRV_RMSSD"],
        "Jednostka": "ms",
        "Status": "⚠️ Obniżony" if profile_data["HRV_RMSSD"] < 25 else "✅ Normalny"
    },
    {
        "Parametr": "HRV_SDNN",
        "Wartość": profile_data["HRV_SDNN"],
        "Jednostka": "ms",
        "Status": "⚠️ Obniżony" if profile_data["HRV_SDNN"] < 30 else "✅ Normalny"
    },
    {
        "Parametr": "TEMP_mean",
        "Wartość": profile_data["TEMP_mean"],
        "Jednostka": "°C",
        "Status": "⚠️ Podwyższona" if profile_data["TEMP_mean"] > 37.0 else "✅ Normalna"
    }
])

st.dataframe(params_df, use_container_width=True)

# Wykres - Radar Plot
st.subheader("📈 Wizualizacja Profilu")

# Przygotuj dane do radar plotu
features = list(REFERENCE_VALUES.keys())
values = [profile_data[feat] for feat in features]
labels = [REFERENCE_VALUES[feat]["label"] for feat in features]

# Normalizacja wartości do zakresu 0-100 dla wizualizacji
normalized_values = []
for i, feat in enumerate(features):
    val = values[i]
    ref_min, ref_max = REFERENCE_VALUES[feat]["normal"]
    # Normalizuj: 0 = ref_min, 100 = ref_max
    normalized = ((val - ref_min) / (ref_max - ref_min)) * 100
    normalized = np.clip(normalized, 0, 150)  # Ogranicz do 150%
    normalized_values.append(normalized)

# Radar plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
angles += angles[:1]  # Zamknij okrąg
normalized_values += normalized_values[:1]

ax.plot(angles, normalized_values, 'o-', linewidth=2, label=selected_profile, color='#2E86AB')
ax.fill(angles, normalized_values, alpha=0.25, color='#2E86AB')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylim(0, 150)
ax.set_yticks([0, 50, 100, 150])
ax.set_yticklabels(['0%', '50%', '100%', '150%'], fontsize=9)
ax.grid(True)
ax.set_title('Profil Fizjologiczny', fontsize=13, fontweight='bold', pad=20)

st.pyplot(fig)

# KROK 4: Automatyczna interpretacja
st.markdown("---")
st.subheader("🔬 Ocena Stanu")

st.info(f"**{profile_data['interpretation']}**")

st.markdown(f"*{profile_data['description']}*")

# Ostrzeżenie
st.warning("⚠️ **To nie jest diagnoza medyczna** – jedynie informacja oparta na danych fizjologicznych. W przypadku problemów zdrowotnych skonsultuj się z lekarzem.")

# KROK 5: INTERAKCJA UŻYTKOWNIKA
st.markdown("---")
st.subheader("💬 Twoja Opinia")

# 1. Potwierdzenie
feedback = st.radio(
    "Czy opis profilu zgadza się z Twoim odczuciem?",
    options=["Zgadza się", "Nie do końca", "Nie zgadza się"],
    horizontal=True
)

# 2. Objawy (checkboxy)
st.markdown("**Jakie objawy odczuwasz? (można wybrać kilka)**")
symptoms = {
    "Napięcie": st.checkbox("Napięcie", key="symptom_tension"),
    "Zmęczenie": st.checkbox("Zmęczenie", key="symptom_fatigue"),
    "Rozdrażnienie": st.checkbox("Rozdrażnienie", key="symptom_irritation"),
    "Brak objawów": st.checkbox("Brak objawów", key="symptom_none")
}

# 3. Subiektywny poziom stresu
stress_level = st.slider(
    "Jak oceniasz swój poziom stresu? (0 = brak, 10 = bardzo wysoki)",
    min_value=0,
    max_value=10,
    value=5,
    step=1
)

# Wizualizacja poziomu stresu
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    stress_color = "#ff4444" if stress_level >= 7 else "#ffaa00" if stress_level >= 4 else "#44ff44"
    st.markdown(f"<div style='background-color: {stress_color}; padding: 10px; border-radius: 5px; text-align: center;'>"
                f"<strong>Poziom stresu: {stress_level}/10</strong></div>", 
                unsafe_allow_html=True)

# KROK 6: Reakcja aplikacji na feedback
st.markdown("---")
st.subheader("🤖 Analiza Feedbacku")

if feedback:
    selected_symptoms = [s for s, checked in symptoms.items() if checked]
    
    # Logika analizy
    if feedback == "Zgadza się":
        st.success("✅ **Profil potwierdzony** – aplikacja może lepiej personalizować informacje zwrotne.")
        if selected_symptoms and "Brak objawów" not in selected_symptoms:
            st.info(f"Odczuwane objawy: {', '.join(selected_symptoms)}. Zalecana obserwacja i ewentualne techniki relaksacyjne.")
    elif feedback == "Nie do końca":
        st.warning("⚠️ **Częściowa zgodność** – rozbieżność między danymi fizjologicznymi a odczuciem. Zalecana obserwacja i możliwe czynniki wpływające (sen, nawodnienie, aktywność fizyczna).")
    elif feedback == "Nie zgadza się":
        st.error("❌ **Rozbieżność między danymi fizjologicznymi a odczuciem** – zalecana obserwacja. Mogą występować czynniki wpływające na odczyty (np. leki, stan zdrowia, warunki pomiaru).")
    
    if stress_level >= 7:
        st.warning("🔴 Wysoki poziom stresu subiektywnego. Rozważ techniki relaksacyjne, odpoczynek lub konsultację specjalistyczną.")
    elif stress_level <= 2:
        st.success("🟢 Niski poziom stresu – dobry stan ogólny.")

# KROK 7 i 8: Sekcja końcowa
st.markdown("---")
st.markdown("### 📖 O Aplikacji")

st.markdown("""
Aplikacja pokazuje, jak połączenie danych z wearables i subiektywnego feedbacku użytkownika może poprawić interpretację stresu i wspierać samoświadomość.

**Monitorowanie** wzorców fizjologicznych może pomóc w **obserwacji** własnych reakcji na stres i wspierać lepsze zarządzanie codziennym napięciem.

**Pamiętaj:** To narzędzie edukacyjne i wspierające świadomość – nie zastępuje profesjonalnej opieki medycznej.
""")
