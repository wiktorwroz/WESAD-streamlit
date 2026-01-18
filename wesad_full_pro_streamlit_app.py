import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Konfiguracja strony
st.set_page_config(
    page_title="WESAD Full Pro Analysis",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 WESAD - Full Pro Analysis Dashboard")
st.markdown("---")

# Funkcja do wczytywania danych z obsługą błędów
@st.cache_data
def load_data():
    """Wczytuje dane z pliku CSV z pełną obsługą błędów"""
    csv_path = Path("wesad_features_full.csv")
    
    # Sprawdź czy plik istnieje
    if not csv_path.exists():
        st.error(f"❌ **Plik nie istnieje:** `{csv_path.absolute()}`")
        st.info("💡 **Rozwiązanie:** Uruchom KROK 6 w notebooku `wesad_full_pro_analysis.ipynb`")
        return None
    
    # Spróbuj wczytać plik
    try:
        df = pd.read_csv(csv_path)
        
        # Sprawdź czy plik nie jest pusty
        if len(df) == 0:
            st.error("❌ **Plik CSV jest pusty!**")
            st.info("💡 Uruchom ponownie KROK 6 w notebooku")
            return None
        
        # Sprawdź czy ma kolumnę 'subject'
        if 'subject' not in df.columns:
            st.error("❌ **Brak kolumny 'subject' w pliku CSV!**")
            st.info("💡 Sprawdź czy plik został poprawnie wygenerowany w KROK 6")
            st.code(f"Dostępne kolumny: {', '.join(df.columns[:10])}...")
            return None
        
        return df
        
    except pd.errors.EmptyDataError:
        st.error("❌ **Plik CSV jest pusty!**")
        return None
    except pd.errors.ParserError as e:
        st.error(f"❌ **Błąd parsowania pliku CSV:** {e}")
        st.info("💡 Sprawdź czy plik nie jest uszkodzony")
        return None
    except Exception as e:
        st.error(f"❌ **Nieoczekiwany błąd:** {type(e).__name__}: {e}")
        st.exception(e)
        return None

# Wczytaj dane
df = load_data()

# Główna aplikacja
if df is not None:
    try:
        # Sidebar
        st.sidebar.header("⚙️ Konfiguracja")
        
        # Pobierz listę subjectów
        subjects = df['subject'].unique().tolist()
        subjects.sort()  # Posortuj alfabetycznie
        
        if len(subjects) == 0:
            st.error("❌ **Brak subjectów w danych!**")
        else:
            # Wybór subjecta
            selected_subject = st.sidebar.selectbox(
                "Wybierz osobę:",
                subjects,
                index=0
            )
            
            # Filtruj dane dla wybranego subjecta
            subject_data = df[df['subject'] == selected_subject]
            
            if len(subject_data) == 0:
                st.error(f"❌ **Brak danych dla subjecta {selected_subject}!**")
            else:
                subject_data = subject_data.iloc[0]
                
                # ========== GŁÓWNE METRYKI ==========
                st.header(f"📊 Analiza dla {selected_subject}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    eda_amp = subject_data.get('EDA_peak_amplitude', np.nan)
                    if not np.isnan(eda_amp):
                        st.metric("EDA Amplitude", f"{eda_amp:.3f}")
                    else:
                        st.metric("EDA Amplitude", "N/A")
                
                with col2:
                    hrv_rmssd = subject_data.get('BVP_hrv_rmssd', np.nan)
                    if not np.isnan(hrv_rmssd):
                        st.metric("HRV RMSSD", f"{hrv_rmssd:.3f}")
                    else:
                        st.metric("HRV RMSSD", "N/A")
                
                with col3:
                    eda_decay = subject_data.get('EDA_decay', np.nan)
                    if not np.isnan(eda_decay):
                        st.metric("EDA Decay", f"{eda_decay:.3f}")
                    else:
                        st.metric("EDA Decay", "N/A")
                
                with col4:
                    regulation_class = subject_data.get('regulation_class', 'N/A')
                    st.metric("Regulacja", regulation_class)
                
                # ========== WIZUALIZACJE ==========
                st.markdown("---")
                st.subheader("📈 Wizualizacje cech")
                
                try:
                    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
                    
                    # EDA features
                    eda_cols = [col for col in df.columns if col.startswith('EDA_') and col != 'EDA_peak_index']
                    if len(eda_cols) > 0:
                        eda_values = [subject_data.get(col, 0) for col in eda_cols[:5]]
                        axes[0, 0].bar(range(len(eda_values)), eda_values)
                        axes[0, 0].set_xticks(range(len(eda_values)))
                        axes[0, 0].set_xticklabels(
                            [col.replace('EDA_', '') for col in eda_cols[:5]], 
                            rotation=45, 
                            ha='right'
                        )
                        axes[0, 0].set_title('EDA Features')
                        axes[0, 0].grid(True, alpha=0.3)
                    else:
                        axes[0, 0].text(0.5, 0.5, 'Brak danych EDA', 
                                       ha='center', va='center', transform=axes[0, 0].transAxes)
                        axes[0, 0].set_title('EDA Features')
                    
                    # BVP/HRV features
                    bvp_cols = [col for col in df.columns if col.startswith('BVP_')]
                    if len(bvp_cols) > 0:
                        bvp_values = [subject_data.get(col, 0) for col in bvp_cols[:5]]
                        axes[0, 1].bar(range(len(bvp_values)), bvp_values)
                        axes[0, 1].set_xticks(range(len(bvp_values)))
                        axes[0, 1].set_xticklabels(
                            [col.replace('BVP_', '') for col in bvp_cols[:5]], 
                            rotation=45, 
                            ha='right'
                        )
                        axes[0, 1].set_title('BVP/HRV Features')
                        axes[0, 1].grid(True, alpha=0.3)
                    else:
                        axes[0, 1].text(0.5, 0.5, 'Brak danych BVP', 
                                       ha='center', va='center', transform=axes[0, 1].transAxes)
                        axes[0, 1].set_title('BVP/HRV Features')
                    
                    # Porównanie z innymi
                    if 'EDA_peak_amplitude' in df.columns:
                        axes[1, 0].bar(df['subject'], df['EDA_peak_amplitude'])
                        axes[1, 0].axhline(
                            y=subject_data.get('EDA_peak_amplitude', 0), 
                            color='r', 
                            linestyle='--', 
                            label='Wybrana osoba'
                        )
                        axes[1, 0].set_title('EDA Peak Amplitude - Porównanie')
                        axes[1, 0].set_ylabel('Amplituda')
                        axes[1, 0].legend()
                        axes[1, 0].grid(True, alpha=0.3)
                    else:
                        axes[1, 0].text(0.5, 0.5, 'Brak danych', 
                                       ha='center', va='center', transform=axes[1, 0].transAxes)
                    
                    # Regulation class distribution
                    if 'regulation_class' in df.columns:
                        regulation_counts = df['regulation_class'].value_counts()
                        axes[1, 1].bar(regulation_counts.index, regulation_counts.values)
                        axes[1, 1].set_title('Rozkład klas regulacji')
                        axes[1, 1].set_ylabel('Liczba osób')
                        axes[1, 1].grid(True, alpha=0.3)
                    else:
                        axes[1, 1].text(0.5, 0.5, 'Brak danych', 
                                       ha='center', va='center', transform=axes[1, 1].transAxes)
                    
                    plt.tight_layout()
                    st.pyplot(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ **Błąd podczas tworzenia wykresów:** {e}")
                    st.exception(e)
                
                # ========== TABELA Z CECHAMI (WIDOK TRANSPONOWANY) ==========
                st.markdown("---")
                st.subheader("📊 Wszystkie cechy (Cecha → Wartość)")
                
                try:
                    # Wyświetl w formie transponowanej (cecha -> wartość)
                    transposed_df = subject_data.to_frame().T
                    if 'subject' in transposed_df.columns:
                        transposed_df = transposed_df.drop(columns=['subject'])
                    st.dataframe(transposed_df, width='stretch', hide_index=True)
                        
                except Exception as e:
                    st.error(f"❌ **Błąd podczas wyświetlania tabeli:** {e}")
                    st.exception(e)
                
                # ========== PREDYKCJA REGULACJI ==========
                st.markdown("---")
                st.subheader("🔮 Predykcja Regulacji Emocjonalnej")
                
                if st.button("🎯 Uruchom Analizę", type="primary"):
                    regulation_class = subject_data.get('regulation_class', 'N/A')
                    
                    if regulation_class == 'dobra':
                        st.success("✅ **Dobra regulacja emocjonalna** - szybko wracasz do równowagi!")
                    elif regulation_class == 'umiarkowana':
                        st.warning("⚠️ **Umiarkowana regulacja** - możesz poprawić strategie regulacji.")
                    elif regulation_class == 'słaba':
                        st.error("❌ **Słaba regulacja** - rozważ techniki relaksacyjne i wsparcie.")
                    else:
                        st.info("ℹ️ Analiza w toku...")
    
    except Exception as e:
        st.error(f"❌ **Krytyczny błąd aplikacji:** {type(e).__name__}: {e}")
        st.exception(e)
        st.info("💡 **Spróbuj:**")
        st.info("1. Odśwież stronę (F5)")
        st.info("2. Sprawdź czy plik CSV jest poprawny")
        st.info("3. Uruchom ponownie KROK 6 w notebooku")

else:
    # Instrukcje gdy nie ma danych
    st.error("❌ **Nie można wczytać danych**")
    st.markdown("---")
    st.info("💡 **Instrukcja rozwiązania problemu:**")
    st.markdown("""
    1. **Otwórz notebook:** `wesad_full_pro_analysis.ipynb`
    2. **Uruchom komórki w kolejności:**
       - KROK 1: Import bibliotek
       - KROK 2: Funkcje pomocnicze
       - KROK 3: Ekstrakcja cech
       - KROK 5: Przetwarzanie sygnałów
       - KROK 6: Agregacja danych (generuje plik CSV)
    3. **Sprawdź czy plik został utworzony:**
       - `wesad_features_full.csv` w tym samym katalogu
    4. **Uruchom ponownie aplikację Streamlit**
    """)
    
    # Pokaż informacje o systemie
    with st.expander("🔍 Informacje diagnostyczne"):
        st.code(f"""
Python: {sys.version}
Katalog roboczy: {Path.cwd()}
Plik CSV: {Path('wesad_features_full.csv').absolute()}
Istnieje: {Path('wesad_features_full.csv').exists()}
        """)
