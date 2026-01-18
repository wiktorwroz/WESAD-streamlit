
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja strony
st.set_page_config(
    page_title="Galaxy vs Nurse Stress Comparison",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tytuł
st.title("📊 Porównanie Galaxy Wearables vs Nurse Stress")
st.markdown("---")

# Wczytaj dane
@st.cache_data
def load_data():
    """Wczytaj dane z CSV"""
    data_path = Path("../results/galaxy_nurse_combined_features.csv")
    if not data_path.exists():
        # Alternatywna ścieżka
        data_path = Path("galaxy_nurse_combined_features.csv")
    
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    else:
        st.error(f"❌ Nie znaleziono pliku danych: {data_path}")
        st.info("💡 Uruchom najpierw komórki analizy, aby utworzyć plik CSV")
        return None

# Wczytaj dane
df = load_data()

if df is not None and not df.empty:
    # Sidebar - wybór opcji
    st.sidebar.header("⚙️ Opcje wizualizacji")
    
    # Wybór typu wykresu
    chart_type = st.sidebar.selectbox(
        "Wybierz typ wykresu:",
        ["Bar Chart (Baseline vs Stress)", "Radar Chart", "Heatmapa zmian", "Porównanie trendów"]
    )
    
    # Wybór cech
    if 'label' in df.columns and 'dataset' in df.columns:
        feature_cols = [col for col in df.columns if col not in ['label', 'dataset', 'condition']]
        selected_features = st.sidebar.multiselect(
            "Wybierz cechy do porównania:",
            options=feature_cols,
            default=feature_cols[:10] if len(feature_cols) > 10 else feature_cols
        )
    else:
        selected_features = []
        st.sidebar.warning("⚠️ Brak kolumn 'label' lub 'dataset' w danych")
    
    # Główna zawartość
    if chart_type == "Bar Chart (Baseline vs Stress)":
        st.header("📊 Bar Chart: Baseline vs Stress")
        
        if len(selected_features) > 0 and 'label' in df.columns and 'dataset' in df.columns:
            # Przygotuj dane
            df_plot = df[df['label'].isin(['baseline', 'stress'])].copy()
            
            # Oblicz średnie per dataset × label
            summary = df_plot.groupby(['dataset', 'label'])[selected_features].mean().reset_index()
            
            # Utwórz wykres
            fig, axes = plt.subplots(1, len(selected_features), figsize=(4*len(selected_features), 6))
            if len(selected_features) == 1:
                axes = [axes]
            
            for idx, feat in enumerate(selected_features):
                ax = axes[idx]
                baseline_galaxy = summary[(summary['dataset'] == 'Galaxy') & (summary['label'] == 'baseline')][feat].values[0] if len(summary[(summary['dataset'] == 'Galaxy') & (summary['label'] == 'baseline')]) > 0 else 0
                stress_galaxy = summary[(summary['dataset'] == 'Galaxy') & (summary['label'] == 'stress')][feat].values[0] if len(summary[(summary['dataset'] == 'Galaxy') & (summary['label'] == 'stress')]) > 0 else 0
                baseline_nurse = summary[(summary['dataset'] == 'Nurse') & (summary['label'] == 'baseline')][feat].values[0] if len(summary[(summary['dataset'] == 'Nurse') & (summary['label'] == 'baseline')]) > 0 else 0
                stress_nurse = summary[(summary['dataset'] == 'Nurse') & (summary['label'] == 'stress')][feat].values[0] if len(summary[(summary['dataset'] == 'Nurse') & (summary['label'] == 'stress')]) > 0 else 0
                
                x = np.arange(2)
                width = 0.35
                
                ax.bar(x - width/2, [baseline_galaxy, baseline_nurse], width, label='Baseline', color='#2ecc71')
                ax.bar(x + width/2, [stress_galaxy, stress_nurse], width, label='Stress', color='#e74c3c')
                
                ax.set_xlabel('Dataset')
                ax.set_ylabel(feat)
                ax.set_title(feat)
                ax.set_xticks(x)
                ax.set_xticklabels(['Galaxy', 'Nurse'])
                ax.legend()
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("⚠️ Wybierz cechy do porównania lub sprawdź czy dane zawierają kolumny 'label' i 'dataset'")
    
    elif chart_type == "Radar Chart":
        st.header("🕸️ Radar Chart: Profil stresu")
        
        if len(selected_features) > 0 and 'label' in df.columns and 'dataset' in df.columns:
            # Przygotuj dane
            df_plot = df[df['label'].isin(['baseline', 'stress'])].copy()
            summary = df_plot.groupby(['dataset', 'label'])[selected_features].mean().reset_index()
            
            # Normalizuj wartości (0-1) dla lepszej wizualizacji
            for feat in selected_features:
                max_val = summary[feat].max()
                min_val = summary[feat].min()
                if max_val > min_val:
                    summary[f'{feat}_norm'] = (summary[feat] - min_val) / (max_val - min_val)
                else:
                    summary[f'{feat}_norm'] = 0.5
            
            # Utwórz radar chart używając plotly
            fig = go.Figure()
            
            for dataset in ['Galaxy', 'Nurse']:
                for label in ['baseline', 'stress']:
                    subset = summary[(summary['dataset'] == dataset) & (summary['label'] == label)]
                    if len(subset) > 0:
                        values = [subset[f'{feat}_norm'].values[0] for feat in selected_features]
                        fig.add_trace(go.Scatterpolar(
                            r=values + [values[0]],  # Zamknij wykres
                            theta=selected_features + [selected_features[0]],
                            fill='toself',
                            name=f'{dataset} - {label}'
                        ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Radar Chart: Porównanie profili stresu"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Wybierz cechy do porównania")
    
    elif chart_type == "Heatmapa zmian":
        st.header("🔥 Heatmapa: Zmiany względne (stress vs baseline)")
        
        if len(selected_features) > 0 and 'label' in df.columns and 'dataset' in df.columns:
            # Oblicz zmiany procentowe
            df_plot = df[df['label'].isin(['baseline', 'stress'])].copy()
            summary = df_plot.groupby(['dataset', 'label'])[selected_features].mean().reset_index()
            
            changes_data = []
            for dataset in ['Galaxy', 'Nurse']:
                baseline_row = summary[(summary['dataset'] == dataset) & (summary['label'] == 'baseline')]
                stress_row = summary[(summary['dataset'] == dataset) & (summary['label'] == 'stress')]
                
                if len(baseline_row) > 0 and len(stress_row) > 0:
                    for feat in selected_features:
                        baseline_val = baseline_row[feat].values[0]
                        stress_val = stress_row[feat].values[0]
                        if baseline_val != 0 and not np.isnan(baseline_val) and not np.isnan(stress_val):
                            change_pct = ((stress_val - baseline_val) / baseline_val) * 100
                            changes_data.append({
                                'dataset': dataset,
                                'feature': feat,
                                'change_pct': change_pct
                            })
            
            if len(changes_data) > 0:
                changes_df = pd.DataFrame(changes_data)
                pivot_df = changes_df.pivot(index='feature', columns='dataset', values='change_pct')
                
                fig, ax = plt.subplots(figsize=(10, max(6, len(selected_features)*0.5)))
                sns.heatmap(pivot_df, annot=True, fmt='.1f', cmap='RdBu_r', center=0, 
                           cbar_kws={'label': 'Zmiana procentowa (%)'}, ax=ax)
                ax.set_title('Heatmapa zmian procentowych (stress vs baseline)')
                ax.set_ylabel('Cecha')
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("⚠️ Nie można obliczyć zmian procentowych")
        else:
            st.warning("⚠️ Wybierz cechy do porównania")
    
    elif chart_type == "Porównanie trendów":
        st.header("📈 Porównanie trendów zmian")
        
        if len(selected_features) > 0 and 'label' in df.columns and 'dataset' in df.columns:
            # Oblicz zmiany procentowe
            df_plot = df[df['label'].isin(['baseline', 'stress'])].copy()
            summary = df_plot.groupby(['dataset', 'label'])[selected_features].mean().reset_index()
            
            trends_data = []
            for dataset in ['Galaxy', 'Nurse']:
                baseline_row = summary[(summary['dataset'] == dataset) & (summary['label'] == 'baseline')]
                stress_row = summary[(summary['dataset'] == dataset) & (summary['label'] == 'stress')]
                
                if len(baseline_row) > 0 and len(stress_row) > 0:
                    for feat in selected_features:
                        baseline_val = baseline_row[feat].values[0]
                        stress_val = stress_row[feat].values[0]
                        if baseline_val != 0 and not np.isnan(baseline_val) and not np.isnan(stress_val):
                            change_pct = ((stress_val - baseline_val) / baseline_val) * 100
                            trends_data.append({
                                'dataset': dataset,
                                'feature': feat,
                                'change_pct': change_pct
                            })
            
            if len(trends_data) > 0:
                trends_df = pd.DataFrame(trends_data)
                
                # Wykres liniowy
                fig, ax = plt.subplots(figsize=(12, 6))
                for dataset in ['Galaxy', 'Nurse']:
                    subset = trends_df[trends_df['dataset'] == dataset]
                    ax.plot(subset['feature'], subset['change_pct'], marker='o', label=dataset, linewidth=2, markersize=8)
                
                ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
                ax.set_xlabel('Cecha', fontsize=12)
                ax.set_ylabel('Zmiana procentowa (%)', fontsize=12)
                ax.set_title('Porównanie trendów zmian (stress vs baseline)', fontsize=14, fontweight='bold')
                ax.legend(fontsize=11)
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
                
                # Tabela porównawcza
                st.subheader("📋 Tabela porównawcza zmian procentowych")
                pivot_trends = trends_df.pivot(index='feature', columns='dataset', values='change_pct')
                st.dataframe(pivot_trends.style.background_gradient(cmap='RdBu_r', axis=None), use_container_width=True)
            else:
                st.warning("⚠️ Nie można obliczyć trendów")
        else:
            st.warning("⚠️ Wybierz cechy do porównania")
    
    # Sekcja z podobieństwami i różnicami
    st.markdown("---")
    st.header("📋 Najważniejsze podobieństwa i różnice")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ PODOBIEŃSTWA")
        st.markdown("""
        1. **Kierunki zmian HRV**: Oba datasety wykazują spadek HRV (RMSSD, SDNN) podczas stresu
        2. **Trendy temperatury**: Zmiany TEMP w podobnym kierunku (chociaż amplituda różna)
        3. **Fizjologiczna odpowiedź**: Oba datasety pokazują typowe fizjologiczne odpowiedzi na stres
        """)
    
    with col2:
        st.subheader("⚠️ RÓŻNICE")
        st.markdown("""
        1. **Charakter stresu**: 
           - **Galaxy** = stres chwilowy (laboratoryjny, TSST/SSST)
           - **Nurse** = stres chroniczny (realne miejsce pracy)
        2. **Amplituda zmian**: 
           - **Galaxy**: Większe procentowe zmiany cech
           - **Nurse**: Mniejsze procentowe zmiany (adaptacja)
        3. **Populacja**: 
           - **Galaxy**: Kontrolowane warunki, młodsza populacja
           - **Nurse**: Realne warunki, starsza populacja zawodowa
        """)
    
    # Statystyki
    st.markdown("---")
    st.header("📊 Statystyki danych")
    
    if 'label' in df.columns and 'dataset' in df.columns:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Łączna liczba próbek", len(df))
        
        with col2:
            galaxy_count = len(df[df['dataset'] == 'Galaxy'])
            st.metric("Galaxy", galaxy_count)
        
        with col3:
            nurse_count = len(df[df['dataset'] == 'Nurse'])
            st.metric("Nurse", nurse_count)
        
        with col4:
            if 'label' in df.columns:
                baseline_count = len(df[df['label'] == 'baseline'])
                stress_count = len(df[df['label'] == 'stress'])
                st.metric("Baseline", baseline_count)
        
        # Rozkład etykiet
        st.subheader("Rozkład etykiet per dataset")
        if 'label' in df.columns:
            crosstab = pd.crosstab(df['dataset'], df['label'])
            st.dataframe(crosstab, use_container_width=True)

else:
    st.error("❌ Brak danych do wizualizacji")
    st.info("💡 Uruchom najpierw komórki analizy, aby utworzyć plik CSV z danymi")
    
    st.markdown("### 📝 Instrukcje:")
    st.markdown("""
    1. Uruchom wszystkie komórki analizy w notebooku `galaxy_nurse_stress_comparison.ipynb`
    2. Upewnij się, że plik `../results/galaxy_nurse_combined_features.csv` został utworzony
    3. Odśwież tę stronę Streamlit
    """)
