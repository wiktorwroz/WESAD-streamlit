# 📋 Instrukcja: Nurse Stress ML Analysis

## Jak uruchomić analizę Nurse Stress dla kolegi

### 📥 KROK 1: Pobierz plik z GitHub

**Opcja A: Pobierz bezpośrednio z GitHub**
1. Przejdź do: https://github.com/wiktorwroz/WESAD-streamlit
2. Kliknij na plik: `nurse_stress_ml_analysis.ipynb`
3. Kliknij przycisk **"Raw"** (surowy)
4. Zaznacz cały tekst (Cmd+A / Ctrl+A) i skopiuj (Cmd+C / Ctrl+C)
5. Wklej do nowego pliku `.ipynb` na swoim komputerze

**Opcja B: Sklonuj całe repozytorium**
```bash
git clone https://github.com/wiktorwroz/WESAD-streamlit.git
cd WESAD-streamlit
```

---

### 📦 KROK 2: Przygotuj środowisko

**Wymagane pakiety Python:**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly streamlit jupyter notebook
```

**Lub zainstaluj wszystkie naraz:**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly streamlit jupyter notebook scipy
```

---

### 📊 KROK 3: Przygotuj dane

**Wymagane pliki danych:**

1. **`nurse_features.csv`** - dane Nurse (już przetworzone cechy)
   - Musi zawierać kolumny: `id`, `datetime`, oraz cechy fizjologiczne (EDA, HR, TEMP)

2. **`wesad_features_full.csv`** - dane WESAD (opcjonalnie, jeśli chcesz porównanie)
   - Możesz pominąć, jeśli chcesz tylko analizę Nurse

**Gdzie umieścić pliki:**
- Utwórz katalog `data/` w tym samym miejscu co notebook
- Umieść pliki: `data/nurse_features.csv` i `data/wesad_features_full.csv`

**Lub zmień ścieżki w notebooku:**
- W KROK 1 znajdź linie z `pd.read_csv(...)` i zmień ścieżki na swoje

---

### 🚀 KROK 4: Uruchom notebook

**Opcja A: Jupyter Notebook**
```bash
jupyter notebook nurse_stress_ml_analysis.ipynb
```

**Opcja B: JupyterLab**
```bash
jupyter lab nurse_stress_ml_analysis.ipynb
```

**Opcja C: VS Code**
- Otwórz plik `.ipynb` w VS Code
- Wybierz kernel Python

---

### 📝 KROK 5: Uruchom komórki

**Ważne: Uruchamiaj komórki po kolei!**

1. **KROK 1**: Wczytaj dane Nurse
2. **KROK 2**: Przygotuj dane (opcjonalnie: wyciągnij cechy fizjologiczne)
3. **KROK 3**: Eksploracja danych
4. **KROK 4**: Przygotowanie do ML
5. **KROK 5**: Trenowanie modeli ML
6. **KROK 6**: Ewaluacja modeli
7. **KROK 7**: Porównanie z WESAD (opcjonalnie)
8. **KROK 8**: Wizualizacja PCA (opcjonalnie)
9. **KROK 9**: Generowanie Streamlit app

**💡 Wskazówka:** Jeśli nie masz danych WESAD, możesz pominąć KROK 7 i KROK 8.

---

### 🎨 KROK 6: Uruchom aplikację Streamlit

**Po uruchomieniu KROK 9, na końcu notebooka zobaczysz instrukcje:**

```bash
cd "ścieżka/do/katalogu/results"
streamlit run nurse_wesad_profile_comparison_streamlit.py
```

**Lub jeśli chcesz uruchomić dashboard dla inwestorów:**
```bash
cd "ścieżka/do/katalogu/results"
streamlit run nursewell_business_dashboard.py
```

**Gdzie znaleźć ścieżkę:**
- W notebooku, w KROK 9, zobaczysz dokładną ścieżkę do `results_dir`
- Skopiuj ją i użyj w terminalu

---

### ⚠️ Rozwiązywanie problemów

**Problem: "FileNotFoundError: nurse_features.csv"**
- **Rozwiązanie:** Sprawdź, czy plik istnieje w katalogu `data/` lub zmień ścieżkę w KROK 1

**Problem: "ModuleNotFoundError: No module named 'X'"**
- **Rozwiązanie:** Zainstaluj brakujący moduł: `pip install X`

**Problem: "KROK 7 nie działa - brak danych WESAD"**
- **Rozwiązanie:** To normalne! Pomiń KROK 7 i KROK 8, jeśli nie masz danych WESAD

**Problem: "Streamlit nie znajduje plików"**
- **Rozwiązanie:** Upewnij się, że uruchamiasz Streamlit z katalogu `results/`, gdzie są zapisane pliki CSV

**Problem: "Kernel crashed"**
- **Rozwiązanie:** 
  - Zmniejsz liczbę przetwarzanych osób w KROK 2.5 (np. `person_ids[:5]`)
  - Zmniejsz rozmiar okien czasowych
  - Zwiększ pamięć RAM lub użyj mniejszej próbki danych

---

### 📊 Co zawiera notebook?

1. **Analiza danych Nurse:**
   - Eksploracja danych
   - Ekstrakcja cech fizjologicznych (EDA, HR, TEMP)
   - Cechy zaawansowane (SCR, tonic level, skewness, kurtosis)

2. **Modele ML:**
   - Random Forest
   - Gradient Boosting
   - Logistic Regression
   - Extra Trees
   - CatBoost

3. **Ewaluacja:**
   - Metryki: Accuracy, F1, Precision, Recall, ROC-AUC
   - Wizualizacje: Confusion Matrix, ROC Curve, Feature Importance

4. **Porównanie z WESAD (opcjonalnie):**
   - Porównanie profili fizjologicznych
   - Odległości do centroidów WESAD (baseline vs stress)
   - Wizualizacja PCA 2D

5. **Streamlit App:**
   - Interaktywna aplikacja do porównania profili
   - Dashboard dla inwestorów

---

### 💡 Wskazówki

- **Uruchamiaj komórki po kolei** - niektóre komórki zależą od wyników poprzednich
- **Sprawdzaj output** - każdy KROK wyświetla informacje o postępie
- **Zapisuj wyniki** - notebook automatycznie zapisuje pliki CSV i PKL w katalogu `results/`
- **Jeśli coś nie działa** - sprawdź, czy wszystkie wymagane pliki danych są dostępne

---

### 📞 Kontakt

Jeśli masz pytania lub problemy:
- Sprawdź output w notebooku - zawiera szczegółowe komunikaty błędów
- Upewnij się, że masz wszystkie wymagane pliki danych
- Sprawdź, czy wszystkie pakiety są zainstalowane

---

### ✅ Checklist przed uruchomieniem

- [ ] Pobrano plik `nurse_stress_ml_analysis.ipynb`
- [ ] Zainstalowano wszystkie wymagane pakiety Python
- [ ] Przygotowano plik `nurse_features.csv` (lub zmieniono ścieżki)
- [ ] Utworzono katalog `results/` (lub notebook go utworzy automatycznie)
- [ ] Otworzono notebook w Jupyter/VS Code
- [ ] Gotowy do uruchomienia komórek po kolei!

---

**Powodzenia! 🚀**

