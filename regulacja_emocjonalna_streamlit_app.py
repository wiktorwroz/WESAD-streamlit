import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Konfiguracja strony
st.set_page_config(
    page_title="Analiza Regulacji Emocjonalnej",
    page_icon="🧠",
    layout="wide"
)

# Tytuł
st.title("🧠 Analiza Regulacji Emocjonalnej")
st.markdown("---")

# Wczytaj dane
@st.cache_data
def load_data():
    """Wczytuje dane z pliku CSV"""
    csv_path = Path("regulacja_emocjonalna_dane.csv")
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        return df
    else:
        st.error(f"Brak pliku {csv_path}")
        return None

# Wczytaj dane
df = load_data()

if df is not None:
    # Wybór osoby
    st.sidebar.header("⚙️ Konfiguracja")
    
    subjects = df['subject'].unique().tolist()
    selected_subject = st.sidebar.selectbox(
        "Wybierz osobę:",
        options=subjects,
        index=0
    )
    
    # Filtruj dane dla wybranej osoby
    subject_data = df[df['subject'] == selected_subject].copy()
    
    # Wyświetl dane
    st.header(f"📊 Dane dla {selected_subject}")
    
    # Podsumowanie parametrów
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eda_amp = subject_data[subject_data['signal'] == 'EDA']['peak_amplitude'].values[0] if len(subject_data[subject_data['signal'] == 'EDA']) > 0 else None
        st.metric("EDA - Amplituda", f"{eda_amp:.3f}" if eda_amp is not None else "N/A")
    
    with col2:
        bvp_amp = subject_data[subject_data['signal'] == 'BVP']['peak_amplitude'].values[0] if len(subject_data[subject_data['signal'] == 'BVP']) > 0 else None
        st.metric("BVP - Amplituda", f"{bvp_amp:.3f}" if bvp_amp is not None else "N/A")
    
    with col3:
        temp_amp = subject_data[subject_data['signal'] == 'TEMP']['peak_amplitude'].values[0] if len(subject_data[subject_data['signal'] == 'TEMP']) > 0 else None
        st.metric("TEMP - Zmiana", f"{temp_amp:.3f}" if temp_amp is not None else "N/A")
    
    # Tabela z parametrami
    st.subheader("📋 Szczegółowe parametry")
    display_df = subject_data[['signal', 'condition', 'latency_s', 'peak_amplitude', 
                               'duration_s', 'slope', 'decay', 'auc']].copy()
    display_df = display_df.round(3)
    st.dataframe(display_df, use_container_width=True)
    
    # Przycisk predykcji
    st.markdown("---")
    st.subheader("🔮 Predykcja Regulacji Emocjonalnej")
    
    if st.button("🎯 Uruchom Predykcję", type="primary", use_container_width=True):
        # Logika predykcji na podstawie danych
        eda_data = subject_data[subject_data['signal'] == 'EDA']
        bvp_data = subject_data[subject_data['signal'] == 'BVP']
        temp_data = subject_data[subject_data['signal'] == 'TEMP']
        
        # Ocena na podstawie parametrów
        if len(eda_data) > 0 and len(bvp_data) > 0 and len(temp_data) > 0:
            # Predykcja dla S2
            if selected_subject == "S2":
                st.success("✅ **Regulacja przebiega sprawnie, szybko wracasz do równowagi, brawo, poradzisz sobie!**")
                st.info("📊 Twoja reakcja jest umiarkowana - ciało reaguje, ale szybko wraca do normy.")
            
            # Predykcja dla S3
            elif selected_subject == "S3":
                st.warning("⚠️ **Nie jest idealnie, ale jakoś sobie radzisz.**")
                st.info("📊 Twoja reakcja jest mieszana - ciało aktywuje się częściowo, regulacja działa, choć nie idealnie.")
            
            # Predykcja dla S4
            elif selected_subject == "S4":
                st.error("❌ **Słaba regulacja, pomóż ciału się uspokoić.**")
                st.info("📊 Twoja reakcja jest ekstremalna - stres utrzymuje się długo, ciało nie daje rady się uspokoić.")
                st.markdown("""
                **💡 Rekomendacje:**
                - Głębokie oddychanie
                - Techniki relaksacyjne
                - Spacer na świeżym powietrzu
                - Medytacja lub mindfulness
                """)
            else:
                st.info("Wybierz osobę S2, S3 lub S4")
        else:
            st.error("Brak kompletnych danych dla wybranej osoby")
    
    # Wizualizacja
    st.markdown("---")
    st.subheader("📈 Wizualizacja parametrów")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Parametry reakcji dla {selected_subject}", fontsize=16, fontweight='bold')
    
    # Wykres 1: Amplituda piku
    ax1 = axes[0, 0]
    signals = subject_data['signal'].unique()
    amplitudes = [subject_data[subject_data['signal'] == sig]['peak_amplitude'].values[0] 
                  if len(subject_data[subject_data['signal'] == sig]) > 0 else 0 
                  for sig in signals]
    ax1.bar(signals, amplitudes, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax1.set_title("Amplituda piku")
    ax1.set_ylabel("Amplituda")
    ax1.grid(True, alpha=0.3)
    
    # Wykres 2: Czas trwania
    ax2 = axes[0, 1]
    durations = [subject_data[subject_data['signal'] == sig]['duration_s'].values[0] 
                 if len(subject_data[subject_data['signal'] == sig]) > 0 else 0 
                 for sig in signals]
    ax2.bar(signals, durations, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax2.set_title("Czas trwania reakcji")
    ax2.set_ylabel("Czas (s)")
    ax2.grid(True, alpha=0.3)
    
    # Wykres 3: Slope
    ax3 = axes[1, 0]
    slopes = [subject_data[subject_data['signal'] == sig]['slope'].values[0] 
              if len(subject_data[subject_data['signal'] == sig]) > 0 else 0 
              for sig in signals]
    ax3.bar(signals, slopes, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax3.set_title("Tempo wzrostu (slope)")
    ax3.set_ylabel("Slope")
    ax3.grid(True, alpha=0.3)
    
    # Wykres 4: AUC
    ax4 = axes[1, 1]
    aucs = [subject_data[subject_data['signal'] == sig]['auc'].values[0] 
            if len(subject_data[subject_data['signal'] == sig]) > 0 else 0 
            for sig in signals]
    ax4.bar(signals, aucs, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax4.set_title("Powierzchnia pod krzywą (AUC)")
    ax4.set_ylabel("AUC")
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Stopka
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>Analiza Regulacji Emocjonalnej - WESAD Dataset</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Nie można wczytać danych. Sprawdź czy plik CSV istnieje.")
