# 📦 Instrukcja dla koleżanki/kolegi - Jak uruchomić aplikację Streamlit

## ✅ Co musi mieć koleżanka/kolega

### 1. Pliki aplikacji (wszystkie w jednym folderze):

```
folder/
├── wesad_full_pro_streamlit_app.py    # Główna aplikacja
├── wesad_features_full.csv            # ⚠️ WAŻNE - dane CSV
└── results/                           # ⚠️ WAŻNE - folder z wynikami
    ├── analysis_results.json
    ├── best_model_logisticregression.pkl
    ├── label_encoder.pkl
    └── scaler.pkl
```

### 2. Python i biblioteki

```bash
# Zainstaluj Python 3.11+ (jeśli nie ma)
# Następnie zainstaluj biblioteki:
pip install streamlit pandas numpy scikit-learn matplotlib seaborn
```

## 🚀 Jak uruchomić

### Krok 1: Skopiuj wszystkie pliki

Koleżanka/kolega musi mieć:
- ✅ Plik `wesad_full_pro_streamlit_app.py`
- ✅ Plik `wesad_features_full.csv` (w tym samym folderze)
- ✅ Folder `results/` z plikami:
  - `analysis_results.json`
  - `best_model_logisticregression.pkl`
  - `label_encoder.pkl`
  - `scaler.pkl`

**WAŻNE:** Wszystkie pliki muszą być w tej samej strukturze folderów!

### Krok 2: Zainstaluj biblioteki

```bash
pip install streamlit pandas numpy scikit-learn matplotlib seaborn
```

### Krok 3: Uruchom aplikację

```bash
# Przejdź do folderu z plikami
cd folder_z_plikami

# Uruchom Streamlit
streamlit run wesad_full_pro_streamlit_app.py
```

Aplikacja otworzy się w przeglądarce pod adresem: `http://localhost:8501`

## 📋 Pakiet gotowy do wysłania

### Opcja 1: ZIP z wszystkimi plikami

```bash
# Na Twoim komputerze, stwórz pakiet:
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"
zip -r wesad_streamlit_app.zip \
  wesad_full_pro_streamlit_app.py \
  wesad_features_full.csv \
  results/
```

Wyślij plik `wesad_streamlit_app.zip` koleżance/koleże.

**Koleżanka/kolega:**
1. Rozpakuj ZIP
2. Zainstaluj biblioteki: `pip install streamlit pandas numpy scikit-learn matplotlib seaborn`
3. Uruchom: `streamlit run wesad_full_pro_streamlit_app.py`

### Opcja 2: GitHub (najlepsze)

```bash
# Stwórz repozytorium z wszystkimi plikami
git init
git add wesad_full_pro_streamlit_app.py
git add wesad_features_full.csv
git add results/
git commit -m "WESAD Streamlit app"
git remote add origin https://github.com/TWOJE_KONTO/wesad-streamlit.git
git push -u origin main
```

Koleżanka/kolega:
```bash
git clone https://github.com/TWOJE_KONTO/wesad-streamlit.git
cd wesad-streamlit
pip install streamlit pandas numpy scikit-learn matplotlib seaborn
streamlit run wesad_full_pro_streamlit_app.py
```

## ⚠️ Potencjalne problemy

### Problem 1: "File not found: wesad_features_full.csv"

**Rozwiązanie:**
- Upewnij się, że plik `wesad_features_full.csv` jest w tym samym folderze co `wesad_full_pro_streamlit_app.py`
- Sprawdź czy nazwa pliku jest dokładnie taka sama (wielkość liter ma znaczenie!)

### Problem 2: "ModuleNotFoundError: No module named 'streamlit'"

**Rozwiązanie:**
```bash
pip install streamlit
# lub
pip3 install streamlit
```

### Problem 3: "Nie znaleziono pliku analysis_results.json"

**Rozwiązanie:**
- Upewnij się, że folder `results/` jest w tym samym katalogu co aplikacja
- Sprawdź czy plik `results/analysis_results.json` istnieje

### Problem 4: "Port 8501 is already in use"

**Rozwiązanie:**
```bash
# Użyj innego portu:
streamlit run wesad_full_pro_streamlit_app.py --server.port 8502
```

## ✅ Checklist przed wysłaniem

- [ ] Plik `wesad_full_pro_streamlit_app.py` jest kompletny
- [ ] Plik `wesad_features_full.csv` istnieje i ma dane
- [ ] Folder `results/` zawiera wszystkie pliki:
  - [ ] `analysis_results.json`
  - [ ] `best_model_logisticregression.pkl`
  - [ ] `label_encoder.pkl`
  - [ ] `scaler.pkl`
- [ ] Struktura folderów jest poprawna (wszystko w jednym folderze)

## 🎯 Szybki test

Przed wysłaniem, przetestuj czy wszystko działa:

```bash
# 1. Stwórz testowy folder
mkdir test_streamlit
cd test_streamlit

# 2. Skopiuj pliki
cp ../wesad_full_pro_streamlit_app.py .
cp ../wesad_features_full.csv .
cp -r ../results .

# 3. Uruchom
streamlit run wesad_full_pro_streamlit_app.py
```

Jeśli działa u Ciebie, będzie działać u koleżanki/kolegi! ✅

