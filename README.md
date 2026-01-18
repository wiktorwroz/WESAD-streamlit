# WESAD - Full Pro Analysis Pipeline

## 📋 Opis projektu

Profesjonalna analiza multimodalnych sygnałów fizjologicznych z zestawu danych WESAD (Wearable Stress and Affect Detection). Projekt implementuje kompleksowy pipeline od surowych sygnałów do predykcji stanów emocjonalnych z wykorzystaniem zaawansowanych technik machine learning.

### Cel badania

Kompleksowa analiza regulacji emocjonalnej na podstawie sygnałów:
- **EDA** (Electrodermal Activity) - przewodnictwo skóry
- **BVP** (Blood Volume Pulse) - puls, HRV (Heart Rate Variability)
- **TEMP** (Temperature) - temperatura skóry
- **ACC** (Accelerometer) - akcelerometr (opcjonalnie)

## 🔬 Metodologia

### 1. Przygotowanie danych wejściowych

- Wczytanie wszystkich sygnałów dla wybranych osób (S2, S3, S4)
- Sprawdzenie i ujednolicenie długości sygnałów (forward-fill)
- Usunięcie ewidentnych anomalii i wartości nierealistycznych
- Przeskalowanie czasu do wspólnych timestampów

### 2. Filtracja i oczyszczanie sygnałów

- **EDA**: low-pass filter ~1 Hz
- **BVP**: low-pass filter ~4-5 Hz, bandpass 0.5-8 Hz
- **TEMP**: wygładzenie metodą rolling mean
- Wykrywanie artefaktów (ruch, skoki napięcia) - threshold 5 SD
- Usuwanie artefaktów metodą forward-fill lub interpolacji

### 3. Segmentacja sygnału

Podział danych na:
- **Baseline** (początek, ~30-60s spoczynku)
- **Stress/Emotion** (część protokołu)
- **Neutral** (jeśli dostępne)

Każdy segment opisany metadanymi: osoba, stan, czas.

### 4. Korekcja baseline

Dla każdej osoby i każdego sygnału:
- Wyznaczenie `baseline_mean` i `baseline_std`
- Sygnał skorygowany: `x_corrected = x - baseline_mean`
- Sygnał znormalizowany: `x_z = x_corrected / baseline_std`

### 5. Ekstrakcja cech (Feature Engineering)

Wygenerowanie cech z okien czasowych (5-10s, 50% nakładania):

#### Dla EDA:
- Amplitude peak
- Latency (czas do pierwszego piku)
- Rise time (czas wzrostu)
- Decay time (czas opadania)
- AUC (Area Under Curve)
- Tonic level (komponent wolnozmienny)
- Phasic response (komponent szybkozmienny)
- SCR count, mean amplitude, latency to first SCR

#### Dla BVP:
- Heart rate (mean, std)
- HRV SDNN (Standard Deviation of NN intervals)
- HRV RMSSD (Root Mean Square of Successive Differences)
- HRV pNN50 (percentage of NN intervals > 50ms)
- HRV LF/HF ratio (spektralne)

#### Dla TEMP:
- Slope (nachylenie trendu)
- Rolling mean
- Min/max change
- Delta 0-30s
- Variance

#### Dla ACC (opcjonalnie):
- Energy (suma kwadratów)
- Movement intensity (średnia z magnitude)
- Mean, std, max

### 6. Przygotowanie danych ML

- Usunięcie klas z < 20 próbek (parametr `MIN_CLASS_COUNT`)
- Train/test split z zachowaniem proporcji klas (`stratify`)
- Skalowanie (`StandardScaler`)
- Zamiana etykiet na numeryczne (`LabelEncoder`)

### 7. Modele ML

Wytrenowane i porównane modele:

1. **RandomForest** - baseline model
2. **LightGBM** - gradient boosting
3. **Logistic Regression** - model liniowy
4. **SVM** (Support Vector Machine) - kernel RBF
5. **MLP** (Multi-Layer Perceptron) - sieć neuronowa

Walidacja:
- **LOSO CV** (Leave-One-Subject-Out) dla RandomForest i LightGBM
- **Train/Test Split** dla pozostałych modeli

### 8. Ewaluacja modeli

Metryki:
- Accuracy
- Precision (macro)
- Recall (macro)
- F1-score (macro)
- ROC AUC (multi-class, weighted)

Wizualizacje:
- Confusion Matrix
- ROC Curves
- Feature Importance (SHAP)
- SHAP bar plot + beeswarm plot

### 9. Backtesting (Walidacja Time-Series)

Walidacja w stylu time-series:
- Dzielenie danych chronologicznie
- Każda iteracja: trening tylko na przeszłości
- Testowanie na przyszłości
- 5 foldów chronologicznych

### 10. Finalne predykcje i wykresy

- Predykcje na pełnej osi czasu
- Wykres "true vs predicted"
- Wykres aktywacji fizjologicznej przed/po stresie
- Confusion Matrix

## 🚀 Pipeline krok po kroku

1. **Import bibliotek i konfiguracja** - ustawienie parametrów, ścieżek
2. **Funkcje pomocnicze** - filtracja, preprocessing, wykrywanie artefaktów
3. **Zaawansowana ekstrakcja cech** - EDA peaks, HRV, TEMP, ACC
4. **Wczytywanie danych WESAD** - z plików .pkl
5. **Przetwarzanie sygnałów** - filtracja, baseline, ekstrakcja cech
6. **Agregacja danych** - przygotowanie do ML
7. **Modele ML z LOSO CV** - RandomForest, LightGBM
8. **Rozszerzone modele ML** - Logistic Regression, SVM, MLP
9. **Interpretacja modeli** - SHAP values
10. **Backtesting** - walidacja time-series
11. **Finalne predykcje** - wykresy i wizualizacje
12. **Streamlit Dashboard** - interaktywna aplikacja

## 📊 Wykorzystywane sygnały

### EDA (Electrodermal Activity)
- Częstotliwość próbkowania: 4 Hz
- Filtracja: low-pass 1 Hz
- Cechy: SCR count, amplitude, latency, rise time, decay, AUC, tonic, phasic

### BVP (Blood Volume Pulse)
- Częstotliwość próbkowania: 64 Hz
- Filtracja: low-pass 4 Hz, bandpass 0.5-8 Hz
- Cechy: HR, HRV (SDNN, RMSSD, pNN50, LF/HF)

### TEMP (Temperature)
- Częstotliwość próbkowania: 4 Hz
- Filtracja: rolling mean
- Cechy: slope, delta, variance, trend

### ACC (Accelerometer)
- Częstotliwość próbkowania: 32 Hz
- Cechy: energy, movement intensity, statistics

## 🤖 Opis modeli

### RandomForest
- `n_estimators=500`
- `max_depth=None`
- LOSO cross-validation

### LightGBM
- `n_estimators=1000`
- `learning_rate=0.05`
- `num_leaves=31`
- Early stopping (50 rounds)
- LOSO cross-validation

### Logistic Regression
- `max_iter=1000`
- `multi_class='ovr'`
- Train/test split

### SVM
- `kernel='rbf'`
- `probability=True`
- Train/test split

### MLP
- `hidden_layer_sizes=(100, 50)`
- `max_iter=500`
- Early stopping
- Train/test split

## 📈 Wyniki

Wyniki są generowane automatycznie podczas wykonywania notebooka:

- **LOSO CV Results**: średnie wyniki dla każdego modelu
- **Extended Models Results**: wyniki dla Logistic Regression, SVM, MLP
- **Backtesting Results**: wyniki walidacji time-series
- **SHAP Feature Importance**: top 15 najważniejszych cech
- **Confusion Matrices**: dla każdego modelu
- **ROC Curves**: krzywe ROC dla multi-class

## 🎨 Wizualizacje

Notebook generuje następujące wykresy:

1. **Time series** - sygnały z zaznaczonymi pikami
2. **Radar charts** - cechy per subject
3. **Heatmaps** - korelacje cech
4. **Boxplots** - porównanie baseline vs stress
5. **ROC curves** - krzywe ROC
6. **SHAP plots** - bar plot i beeswarm plot
7. **Confusion matrices** - macierze pomyłek
8. **True vs Predicted** - porównanie predykcji

## 🖥️ Streamlit Dashboard

Interaktywna aplikacja Streamlit (`wesad_full_pro_streamlit_app.py`) z funkcjami:

1. **Upload sygnałów** - EDA, BVP, TEMP (opcjonalnie ACC)
2. **Preprocessing w tle** - baseline correction, filtracja, ekstrakcja cech
3. **Predykcja stanu** - baseline/stress/emotion
4. **Wyświetlanie**:
   - Wykresy sygnałów
   - Wykryte piki
   - Feature summary
   - Predykcja na osi czasu
   - Interpretacja SHAP

### Uruchomienie Streamlit:

```bash
streamlit run wesad_full_pro_streamlit_app.py
```

## 📦 Wymagania

Zainstaluj wymagane biblioteki:

```bash
pip install numpy pandas matplotlib seaborn scipy scikit-learn lightgbm shap plotly streamlit
```

Lub użyj pliku `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 📝 Struktura projektu

```
wesad-prep/
├── notebooks/
│   ├── wesad_full_pro_analysis.ipynb  # Główny notebook
│   └── wesad_full_pro_streamlit_app.py  # Aplikacja Streamlit
├── README.md                            # Ten plik
└── requirements.txt                     # Zależności
```

## 🔧 Parametry konfiguracyjne

Kluczowe parametry w notebooku:

- `SELECTED_SUBJECTS`: ["S2", "S3", "S4"]
- `WINDOW_SIZE_S`: 10 (rozmiar okna czasowego)
- `WINDOW_OVERLAP`: 0.5 (50% nakładania)
- `BASELINE_DURATION_S`: 30
- `ARTIFACT_THRESHOLD_SD`: 5.0
- `MIN_CLASS_COUNT`: 20
- `RANDOM_SEED`: 42

## 📚 Referencje

- WESAD Dataset: [Link do datasetu]
- HRV Analysis: Standardowe metryki HRV (SDNN, RMSSD, pNN50)
- SHAP: SHapley Additive exPlanations dla interpretowalności ML

## 👤 Autor

Projekt wykonany w ramach analizy danych WESAD.

## 📄 Licencja

[Określ licencję]

---

**Uwaga**: Upewnij się, że masz dostęp do danych WESAD przed uruchomieniem notebooka. Ścieżka do danych jest ustawiona w zmiennej `RAW_ROOT`.

