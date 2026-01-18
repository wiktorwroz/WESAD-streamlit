"""
Streamlit app for Galaxy & Nurse Individual Trends Analysis
Uruchomienie: streamlit run galaxy_nurse_individual_trends_streamlit.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Konfiguracja strony
st.set_page_config(
    page_title="Galaxy & Nurse - Indywidualne Trendy Stresu",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Galaxy & Nurse - Indywidualne Trendy Stresu")
st.markdown("""
### Analiza indywidualnych reakcji na stres
- **Galaxy**: Stres laboratoryjny (chwilowy)
- **Nurse**: Stres zawodowy (przewlekły)
""")

# Wczytaj dane (dostosuj ścieżkę)
@st.cache_data
def load_data():
    """Wczytuje przetworzone dane trendów."""
    results_path = Path("results/individual_trends_results.csv")
    if results_path.exists():
        return pd.read_csv(results_path)
    else:
        st.warning("⚠️ Plik z wynikami nie został znaleziony. Uruchom najpierw notebook.")
        return None

df_trends = load_data()

if df_trends is not None:
    # Sidebar - wybory
    st.sidebar.header("⚙️ Ustawienia")
    
    dataset_choice = st.sidebar.selectbox(
        "Wybierz dataset:",
        options=['Galaxy', 'Nurse', 'Oba'],
        index=2
    )
    
    if dataset_choice == 'Oba':
        df_filtered = df_trends
    else:
        df_filtered = df_trends[df_trends['dataset'] == dataset_choice]
    
    subjects_available = sorted(df_filtered['subject'].unique()) if not df_filtered.empty else []
    if subjects_available:
        subject_choice = st.sidebar.selectbox(
            "Wybierz uczestnika:",
            options=subjects_available,
            index=0
        )
    else:
        subject_choice = None
    
    features_available = sorted(df_filtered['feature'].unique()) if not df_filtered.empty else []
    if features_available:
        feature_choice = st.sidebar.multiselect(
            "Wybierz cechy (można wybrać wiele):",
            options=features_available,
            default=features_available[:3] if len(features_available) >= 3 else features_available
        )
    else:
        feature_choice = []
    
    # Główny panel
    if subject_choice and feature_choice:
        st.header(f"👤 Uczestnik: {subject_choice}")
        
        # Filtruj dane
        subject_data = df_filtered[
            (df_filtered['subject'] == subject_choice) & 
            (df_filtered['feature'].isin(feature_choice))
        ]
        
        if not subject_data.empty:
            # Przygotuj dane do wykresu
            plot_data = []
            for _, row in subject_data.iterrows():
                plot_data.append({
                    'Warunek': 'Baseline',
                    'Cecha': row['feature'],
                    'Wartość': row['baseline_mean']
                })
                plot_data.append({
                    'Warunek': 'Stress',
                    'Cecha': row['feature'],
                    'Wartość': row['stress_mean']
                })
            
            df_plot = pd.DataFrame(plot_data)
            
            # Wykres liniowy
            if HAS_PLOTLY:
                fig_line = px.line(
                    df_plot,
                    x='Warunek',
                    y='Wartość',
                    color='Cecha',
                    markers=True,
                    title=f"Trend: Baseline → Stress",
                    labels={'Wartość': 'Wartość cechy', 'Warunek': 'Warunek'}
                )
                fig_line.update_layout(height=400)
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Tabela zmian procentowych
            st.subheader("📈 Zmiany procentowe")
            changes_df = subject_data[['feature', 'baseline_mean', 'stress_mean', 'change_pct']].copy()
            changes_df.columns = ['Cecha', 'Baseline (średnia)', 'Stress (średnia)', 'Zmiana %']
            changes_df['Zmiana %'] = changes_df['Zmiana %'].round(2)
            changes_df['Baseline (średnia)'] = changes_df['Baseline (średnia)'].round(2)
            changes_df['Stress (średnia)'] = changes_df['Stress (średnia)'].round(2)
            st.dataframe(changes_df, use_container_width=True)
            
            # Opis trendu
            st.subheader("💡 Opis trendu")
            
            # Oblicz największe zmiany
            if len(changes_df) > 0:
                biggest_increase = changes_df.loc[changes_df['Zmiana %'].idxmax()]
                biggest_decrease = changes_df.loc[changes_df['Zmiana %'].idxmin()]
                
                description = f"""
**Profil uczestnika {subject_choice}:**

- **Największy wzrost**: {biggest_increase['Cecha']} (+{biggest_increase['Zmiana %']:.1f}%)
- **Największy spadek**: {biggest_decrease['Cecha']} ({biggest_decrease['Zmiana %']:.1f}%)

**Interpretacja:**
"""
                
                # Dodaj interpretację na podstawie zmian HRV
                hrv_features = [f for f in feature_choice if 'HRV' in f or 'pNN50' in f]
                if hrv_features:
                    hrv_changes = changes_df[changes_df['Cecha'].isin(hrv_features)]
                    if not hrv_changes.empty:
                        avg_hrv_change = hrv_changes['Zmiana %'].mean()
                        if avg_hrv_change < -10:
                            description += "- **Szybka reakcja stresowa**: Znaczny spadek HRV wskazuje na silną aktywację układu współczulnego\n"
                        elif avg_hrv_change > 10:
                            description += "- **Dobra regulacja**: Wzrost HRV może wskazywać na adaptację\n"
                
                temp_features = [f for f in feature_choice if 'TEMP' in f]
                if temp_features:
                    temp_changes = changes_df[changes_df['Cecha'].isin(temp_features)]
                    if not temp_changes.empty:
                        avg_temp_change = temp_changes['Zmiana %'].mean()
                        if avg_temp_change > 5:
                            description += "- **Wzrost temperatury**: Może wskazywać na reakcję stresową\n"
                
                st.markdown(description)
        else:
            st.warning(f"⚠️ Brak danych dla uczestnika {subject_choice} i wybranych cech.")
    else:
        st.info("👈 Wybierz uczestnika i cechy z panelu bocznego")

else:
    st.error("❌ Brak danych. Uruchom najpierw notebook aby wygenerować wyniki.")

