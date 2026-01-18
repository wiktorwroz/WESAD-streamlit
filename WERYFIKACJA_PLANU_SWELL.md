# WERYFIKACJA ZGODNOŚCI Z PLANEM - SWELL HRV Stress Analysis

## 📋 Plan vs Implementacja

### ✅ 1️⃣ Wczytanie danych
**Plan:**
- Pobierz dane raw z `data/raw/labels` (etykiety) i `data/raw/rri` (interwały RR)
- Sprawdź kolumny i uczestników (subject) oraz warunki (Condition)
- Oceń liczebność próbek w poszczególnych klasach stresu

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 8: Wczytuje etykiety z Excel (`data/raw/labels/hrv stress labels.xlsx`)
- ✅ Komórka 8: Wczytuje surowe dane RRI z `data/raw/rri/` (p1.txt - p25.txt)
- ✅ Komórka 8: Sprawdza kolumny etykiet i uczestników
- ✅ Komórka 9: Wizualizuje rozkład warunków per uczestnik

---

### ✅ 2️⃣ Przygotowanie danych HRV
**Plan:**
- Z plików RRI policz cechy HRV (RMSSD, SDNN, pNN50, LF/HF, MEAN_RR)
- Scal cechy z etykietami stresu i uczestnikami w jedną tabelę
- Upewnij się, że nie ma braków danych ani duplikatów

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 8: Funkcja `calculate_hrv_features()` oblicza:
  - RMSSD, SDNN (SDRR), pNN50, LF/HF, MEAN_RR, HR, VLF, LF, HF, TP, SD1, SD2, KURT, SKEW
- ✅ Komórka 8: Scalanie cech z etykietami (mapowanie z Excel)
- ✅ Komórka 12: Sprawdzenie brakujących wartości i wartości nieskończonych

---

### ⚠️ 3️⃣ Normalizacja
**Plan:**
- Globalna: normalizujesz wszystkie próbki razem (do modelu globalnego)
- Per-user: normalizujesz osobno dla każdego uczestnika (do modelu personalnego)
- StandardScaler

**Status:** ⚠️ **CZĘŚCIOWO ZAIMPLEMENTOWANE - WYMAGA POPRAWEK**
- ✅ Komórka 17 (Global Model): Normalizacja globalna z StandardScaler (fit na train, transform na test)
- ⚠️ Komórka 20 (Personal Model): Normalizacja powinna być wewnątrz pętli LOSO (fit na train per fold, transform na test per fold)
- ❌ **PROBLEM:** Normalizacja per-user powinna być wykonana **wewnątrz** pętli LOSO, a nie przed nią

**Wymagana poprawka:**
- W komórce 20: Normalizacja powinna być **wewnątrz** każdego LOSO fold (fit na `X_train_loso`, transform na `X_test_loso`)

---

### ✅ 4️⃣ Podział na zbiór treningowy i testowy
**Plan:**
- Globalny model: losowy podział wszystkich próbek, stratified po klasach stresu
- Personalny model: podział każdej osoby osobno, żeby trenować i testować indywidualnie
- Sprawdź, czy nie ma przecieku między train i test

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 8: Podział train/test per participant (70/30) - różne osoby w train i test
- ✅ Komórka 8: Weryfikacja braku wspólnych uczestników między train i test
- ✅ Komórka 20: LOSO (Leave-One-Subject-Out) dla modeli personalnych - osobny fold per uczestnik

---

### ✅ 5️⃣ Wybór cech do modelowania
**Plan:**
- Wybierz kluczowe cechy HRV (RMSSD, SDNN, pNN50, LF/HF, HR, MEAN_RR...)
- Jeśli brakuje cech, użyj wszystkich dostępnych featureów

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 15: Wybór featureów HRV z dostępnych kolumn
- ✅ Komórka 8: Obliczanie wszystkich potrzebnych featureów HRV

---

### ✅ 6️⃣ Trening modeli
**Plan:**
- Modele globalne: Logistic Regression, Random Forest, Gradient Boosting
- Modele personalne: te same algorytmy, ale osobno dla każdego uczestnika

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 17: Globalne modele (LR, RF, GB, XGBoost)
- ✅ Komórka 20: Personalne modele (LOSO - te same algorytmy per uczestnik)

---

### ✅ 7️⃣ Ewaluacja i metryki
**Plan:**
- Accuracy, F1-score, precision, recall, ROC-AUC
- Porównanie globalny vs personalny model
- Feature importance

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 17, 18: Ewaluacja globalnych modeli (accuracy, F1, precision, recall, ROC-AUC)
- ✅ Komórka 20, 21: Ewaluacja personalnych modeli (LOSO) i porównanie z globalnymi
- ✅ Komórka 23: Feature importance i SHAP values

---

### ✅ 8️⃣ Wnioski kliniczne / interpretacja
**Plan:**
- RMSSD/SDNN → niższy stres
- LF/HF → wyższy stres
- Różnice między uczestnikami → personalizacja może poprawić dokładność

**Status:** ✅ **ZAIMPLEMENTOWANE**
- ✅ Komórka 25: Wnioski kliniczne i interpretacja wyników

---

## ⚠️ PROBLEMY DO NAPRAWY

### 1. **Normalizacja w modelu personalnym (LOSO)**
- **Problem:** Normalizacja powinna być wewnątrz pętli LOSO (fit na train fold, transform na test fold)
- **Lokalizacja:** Komórka 20
- **Działanie:** Przenieś `StandardScaler` **wewnątrz** pętli LOSO

### 2. **Upewnić się, że używamy surowych danych RRI**
- **Problem:** Komórka 8 wczytuje surowe RRI, ale może być jeszcze stary kod CSV
- **Lokalizacja:** Komórka 8
- **Działanie:** Usunąć wszystkie pozostałości starego kodu CSV

---

## ✅ CO JEST DOBRE

1. ✅ Wczytywanie surowych danych RRI z `data/raw/rri/` i etykiet z Excel
2. ✅ Obliczanie featureów HRV z RRI (RMSSD, SDNN, pNN50, LF/HF, MEAN_RR, itd.)
3. ✅ Podział train/test per participant (różne osoby w train i test)
4. ✅ LOSO split dla modeli personalnych
5. ✅ Globalne i personalne modele (LR, RF, GB)
6. ✅ Pełna ewaluacja z metrykami (accuracy, F1, precision, recall, ROC-AUC)
7. ✅ Feature importance i SHAP values
8. ✅ Wnioski kliniczne

---

## 📝 REKOMENDACJE

1. **Napraw normalizację w LOSO** - najważniejsze!
2. **Usuń wszystkie pozostałości starego kodu CSV** z komórki 8
3. **Zweryfikuj**, czy dane rzeczywiście pochodzą z surowych RRI (nie z CSV)
4. **Upewnij się**, że normalizacja jest wykonywana **wewnątrz** każdego LOSO fold

