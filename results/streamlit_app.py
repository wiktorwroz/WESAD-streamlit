import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Automatyczne wykrywanie lokalizacji plików
def get_results_dir():
    """Automatycznie wykrywa lokalizację folderu results"""
    possible_paths = [
        Path.cwd() / "results",
        Path(__file__).parent / "results" if '__file__' in globals() else None,
        Path(__file__).parent.parent / "results" if '__file__' in globals() else None,
    ]
    possible_paths = [p for p in possible_paths if p is not None]
    
    for path in possible_paths:
        if path.exists() and (path / "analysis_results.json").exists():
            return path
    
    return Path.cwd() / "results"

# Wczytaj wyniki analizy
@st.cache_data
def load_analysis_results():
    results_dir = get_results_dir()
    results_file = results_dir / "analysis_results.json"
    if not results_file.exists():
        st.error(f"❌ Nie znaleziono pliku: {results_file}")
        st.info(f"💡 Sprawdź czy plik istnieje w: {results_dir}")
        st.stop()
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_resource
def load_label_encoder():
    results_dir = get_results_dir()
    encoder_file = results_dir / "label_encoder.pkl"
    if not encoder_file.exists():
        st.error(f"❌ Nie znaleziono pliku: {encoder_file}")
        st.info(f"💡 Sprawdź czy plik istnieje w: {results_dir}")
        st.stop()
    with open(encoder_file, 'rb') as f:
        return pickle.load(f)

# Wczytaj dane
try:
    results = load_analysis_results()
    label_encoder = load_label_encoder()
    results_dir = get_results_dir()
except Exception as e:
    st.error(f"❌ Błąd podczas wczytywania danych: {e}")
    st.info(f"💡 Sprawdź czy pliki znajdują się w: {get_results_dir()}")
    st.info("💡 Upewnij się, że uruchomiłeś komórkę generującą pliki w notebooku!")
    st.stop()

# Konfiguracja strony
st.set_page_config(page_title="WESAD Analysis Results", layout="wide")
st.title("📊 Wyniki Analizy Klasyfikacji Emocji - WESAD Dataset")
st.markdown("---")

# Sidebar z informacjami
with st.sidebar:
    st.header("📋 Informacje o Analizie")
    st.metric("Liczba próbek train", results['data_info']['n_train_after_smote'])
    st.metric("Liczba próbek test", results['data_info']['n_test'])
    st.metric("Liczba cech", results['data_info']['n_features'])
    st.metric("Liczba klas", results['data_info']['n_classes'])
    
    st.markdown("---")
    st.subheader("Klasy")
    for label, code in results['label_encoder_mapping'].items():
        st.write(f"**{label}**: {code}")

# Sekcja 1: Rozkład klas
st.header("📊 Rozkład Klas")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Train (przed SMOTE)")
    df_before = pd.DataFrame(list(results['class_distribution_before_smote'].items()), 
                            columns=['Klasa', 'Liczba próbek'])
    st.bar_chart(df_before.set_index('Klasa'))
    st.dataframe(df_before, use_container_width=True)

with col2:
    st.subheader("Train (po SMOTE)")
    df_after = pd.DataFrame(list(results['class_distribution_after_smote'].items()), 
                           columns=['Klasa', 'Liczba próbek'])
    st.bar_chart(df_after.set_index('Klasa'))
    st.dataframe(df_after, use_container_width=True)

with col3:
    st.subheader("Test")
    df_test = pd.DataFrame(list(results['class_distribution_test'].items()), 
                          columns=['Klasa', 'Liczba próbek'])
    st.bar_chart(df_test.set_index('Klasa'))
    st.dataframe(df_test, use_container_width=True)

# Sekcja 2: Porównanie modeli
st.header("🏆 Porównanie Modeli")

metrics_df = pd.DataFrame(results['model_metrics']).T
metrics_df = metrics_df.round(4)
st.subheader("Metryki Globalne")
st.dataframe(metrics_df, use_container_width=True)

# Wykres porównawczy
fig, ax = plt.subplots(figsize=(12, 6))
metrics_df.plot(kind='bar', ax=ax, rot=45)
ax.set_ylabel('Wartość metryki')
ax.set_title('Porównanie modeli: Accuracy, Balanced Accuracy, Macro F1')
ax.legend(title='Metryka', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 1)
plt.tight_layout()
st.pyplot(fig)

# Sekcja 3: Najlepszy model
if results['best_model']:
    st.header("🥇 Najlepszy Model")
    best = results['best_model']
    col1, col2, col3 = st.columns(3)
    col1.metric("Model", best['name'])
    col2.metric("Balanced Accuracy", f"{best['balanced_accuracy']:.4f}")
    col3.metric("Macro F1", f"{best['macro_f1']:.4f}")

# Sekcja 4: Confusion Matrices
st.header("📈 Confusion Matrices")
model_names = list(results['confusion_matrices'].keys())
selected_model = st.selectbox("Wybierz model:", model_names)

if selected_model:
    cm = np.array(results['confusion_matrices'][selected_model])
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm_normalized, annot=True, fmt='.2%', cmap='Blues',
                xticklabels=results['data_info']['classes'],
                yticklabels=results['data_info']['classes'],
                ax=ax, cbar_kws={'label': 'Procent'})
    ax.set_title(f'Confusion Matrix - {selected_model}', fontsize=14, fontweight='bold')
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')
    plt.tight_layout()
    st.pyplot(fig)
    
    cm_df = pd.DataFrame(cm, 
                         index=results['data_info']['classes'],
                         columns=results['data_info']['classes'])
    st.dataframe(cm_df, use_container_width=True)

# Sekcja 5: Per-class metrics
st.header("📊 Metryki Per-Class")
selected_model_metrics = st.selectbox("Wybierz model (dla metryk per-class):", model_names, key='metrics')

if selected_model_metrics and selected_model_metrics in results['per_class_metrics']:
    per_class = results['per_class_metrics'][selected_model_metrics]
    per_class_df = pd.DataFrame(per_class).T
    st.dataframe(per_class_df, use_container_width=True)
    
    # Wykres Precision i Recall
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    per_class_df[['precision', 'recall']].plot(kind='bar', ax=axes[0], rot=0)
    axes[0].set_title('Precision i Recall per Class')
    axes[0].set_ylabel('Wartość')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].set_ylim(0, 1)
    
    per_class_df['f1_score'].plot(kind='bar', ax=axes[1], rot=0, color='green')
    axes[1].set_title('F1-Score per Class')
    axes[1].set_ylabel('F1-Score')
    axes[1].grid(True, alpha=0.3, axis='y')
    axes[1].set_ylim(0, 1)
    
    plt.tight_layout()
    st.pyplot(fig)

# Sekcja 6: Podsumowanie
st.header("📝 Podsumowanie")
if results.get('best_model'):
    best_name = results['best_model']['name']
    best_bal_acc = results['best_model']['balanced_accuracy']
    best_macro_f1 = results['best_model']['macro_f1']
    best_acc = results['best_model']['accuracy']
    summary_text = f"""### Analiza Klasyfikacji Emocji - WESAD Dataset

**Najlepszy model:** {best_name}

**Wyniki:**
- **Balanced Accuracy:** {best_bal_acc:.4f}
- **Macro F1:** {best_macro_f1:.4f}
- **Accuracy:** {best_acc:.4f}

**Metody:**
- Subject-wise split (80% train, 20% test)
- SMOTE dla balansowania klas
- Agregacja: amusement + stress → emotion
- Segmentacja: sliding window (5s okna, 50% overlap)
"""
else:
    summary_text = """### Analiza Klasyfikacji Emocji - WESAD Dataset

**Najlepszy model:** N/A

**Wyniki:**
- **Balanced Accuracy:** N/A
- **Macro F1:** N/A
- **Accuracy:** N/A

**Metody:**
- Subject-wise split (80% train, 20% test)
- SMOTE dla balansowania klas
- Agregacja: amusement + stress → emotion
- Segmentacja: sliding window (5s okna, 50% overlap)
"""
st.markdown(summary_text)
