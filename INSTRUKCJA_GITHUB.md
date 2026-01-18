# 📤 Instrukcja wgrania plików na GitHub

## Pliki do wgrania:
1. `wesad_full_pro_analysis.ipynb`
2. `testy_stacjonarnosci.ipynb`

## Krok po kroku:

### 1. Sprawdź status repozytorium
```bash
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"
git status
```

### 2. Dodaj pliki do Git
```bash
git add wesad_full_pro_analysis.ipynb
git add testy_stacjonarnosci.ipynb
```

### 3. Sprawdź co zostanie dodane
```bash
git status
```

### 4. Utwórz commit z opisem zmian
```bash
git commit -m "Dodano: wesad_full_pro_analysis.ipynb i testy_stacjonarnosci.ipynb

- wesad_full_pro_analysis.ipynb: Pełny pipeline analizy WESAD z LOSO CV, SMOTE, GradientBoosting/ExtraTrees
- testy_stacjonarnosci.ipynb: Testy stacjonarności sygnałów fizjologicznych"
```

### 5. Wgraj na GitHub
```bash
git push origin main
```

## Alternatywnie - wszystko w jednym kroku:

```bash
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"
git add wesad_full_pro_analysis.ipynb testy_stacjonarnosci.ipynb
git commit -m "Dodano: wesad_full_pro_analysis.ipynb i testy_stacjonarnosci.ipynb"
git push origin main
```

## Jeśli nie masz jeszcze repozytorium na GitHub:

### 1. Utwórz nowe repozytorium na GitHub.com
- Zaloguj się na GitHub
- Kliknij "New repository"
- Nazwij np. "wesad-analysis" lub "wesad-prep"
- **NIE** inicjalizuj z README (jeśli już masz lokalne repo)

### 2. Połącz lokalne repo z GitHubem (jeśli jeszcze nie jest połączone):
```bash
git remote add origin https://github.com/TWOJA_NAZWA/wesad-analysis.git
git branch -M main
git push -u origin main
```

## Uwagi:
- Pliki `.ipynb` mogą być duże - GitHub obsługuje je dobrze
- Jeśli pliki są bardzo duże (>100MB), rozważ użycie Git LFS
- Sprawdź czy `.gitignore` nie ignoruje plików `.ipynb`

## Sprawdzenie po wgraniu:
1. Otwórz swoje repozytorium na GitHub.com
2. Sprawdź czy pliki są widoczne
3. GitHub automatycznie renderuje notebooki Jupyter - możesz je przeglądać bezpośrednio w przeglądarce!

