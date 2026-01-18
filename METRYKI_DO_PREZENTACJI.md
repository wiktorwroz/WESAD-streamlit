# 📊 METRYKI DO WSTAWIENIA W PREZENTACJĘ

## SLIDE 8: WYNIKI - METRYKI

### Gdzie znaleźć wyniki:

1. **Otwórz notebook:** `wesad_full_pro_analysis.ipynb`
2. **Uruchom komórkę KROK 7** (LOSO Cross-Validation)
3. **Znajdź sekcję:** "PODSUMOWANIE WYNIKÓW LOSO CV"
4. **Skopiuj wartości** z tabeli dla każdego modelu

### Format do wstawienia:

```
Random Forest:
• Accuracy: 0.XXX ± 0.XXX
• F1-Score: 0.XXX ± 0.XXX
• ROC-AUC: 0.XXX ± 0.XXX

Gradient Boosting:
• Accuracy: 0.XXX ± 0.XXX
• F1-Score: 0.XXX ± 0.XXX
• ROC-AUC: 0.XXX ± 0.XXX

Extra Trees:
• Accuracy: 0.XXX ± 0.XXX
• F1-Score: 0.XXX ± 0.XXX
• ROC-AUC: 0.XXX ± 0.XXX
```

### Jeśli nie masz wyników LOSO CV:

Możesz użyć wyników z innych analiz jako referencji:
- Z pliku `results/analysis_results.json` (ale to są wyniki z innego zadania)
- Lub uruchomić KROK 7 w notebooku

---

## SLIDE 9: NAJWAŻNIEJSZE CECHY

### Gdzie znaleźć top cechy:

1. **Uruchom komórkę KROK 8** (SHAP Values) w notebooku
2. **Znajdź sekcję:** "Feature Importance" lub "Top Features"
3. **Skopiuj top 5-10 cech** z ich wagami/importance

### Format do wstawienia:

```
1. EDA_decay - szybkość powrotu do baseline (importance: 0.XXX)
2. EDA_peak_amplitude - intensywność reakcji (importance: 0.XXX)
3. BVP_hrv_rmssd - zmienność rytmu serca (importance: 0.XXX)
4. EDA_duration - czas trwania reakcji (importance: 0.XXX)
5. TEMP_variance - zmienność temperatury (importance: 0.XXX)
```

---

## DODATKOWE METRYKI DO DODANIA (opcjonalnie):

### SLIDE 6 - Statystyki danych:
- Liczba uczestników: 6
- Liczba cech: [sprawdź w notebooku - ml_df.shape[1]]
- Rozkład klas: [sprawdź w regulation_df - value_counts()]

### SLIDE 7 - Parametry modeli:
- Random Forest: 500 drzew, max_depth=None
- Gradient Boosting: learning_rate=0.1, n_estimators=100
- Extra Trees: n_estimators=100
- SMOTE: k_neighbors=5
- LOSO CV: 6 foldów (jeden per uczestnik)

---

## WIZUALIZACJE DO DODANIA:

1. **SLIDE 2:** Wykres rozkładu uczestników (bar chart)
2. **SLIDE 4:** Przykładowe wykresy sygnałów EDA/BVP/TEMP (time series)
3. **SLIDE 8:** Wykres porównujący modele (bar chart z accuracy/F1)
4. **SLIDE 9:** Wykres feature importance (horizontal bar chart)
5. **SLIDE 10:** Confusion matrix najlepszego modelu

---

## SZYBKI SPOSÓB NA WYNIKI:

Jeśli chcesz szybko uzyskać wyniki bez uruchamiania całego notebooka:

1. Otwórz terminal w katalogu z notebookiem
2. Uruchom:
   ```python
   python3 -c "
   import pandas as pd
   import json
   
   # Jeśli masz zapisane wyniki
   try:
       with open('results/analysis_results.json') as f:
           results = json.load(f)
       print('Wyniki z analysis_results.json:')
       for model, metrics in results['model_metrics'].items():
           print(f'{model}:')
           print(f'  Accuracy: {metrics[\"accuracy\"]:.3f}')
           print(f'  Balanced Accuracy: {metrics[\"balanced_accuracy\"]:.3f}')
           print(f'  Macro F1: {metrics[\"macro_f1\"]:.3f}')
   except:
       print('Uruchom notebook, aby uzyskać wyniki LOSO CV')
   "
   ```

---

## UWAGA:

Wyniki z `results/analysis_results.json` są z innego zadania (klasyfikacja baseline vs emotion), 
nie z analizy regulacji emocjonalnej (słaba/umiarkowana/dobra).

Dla prezentacji o regulacji emocjonalnej potrzebujesz wyników z KROK 7 w `wesad_full_pro_analysis.ipynb`.

