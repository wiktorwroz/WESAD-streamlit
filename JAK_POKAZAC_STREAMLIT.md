# 🚀 Jak pokazać aplikację Streamlit koleżance/koleże

## 📋 Dostępne aplikacje Streamlit

W projekcie WESAD masz kilka aplikacji Streamlit:

1. **`wesad_full_pro_streamlit_app.py`** - Główna aplikacja z analizą cech
2. **`results/streamlit_prediction_app.py`** - Aplikacja do predykcji emocji

## 🎯 Szybki start - Lokalnie (na tym samym komputerze)

### Opcja 1: Uruchomienie lokalne (najprostsze)

```bash
# 1. Przejdź do katalogu z aplikacją
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"

# 2. Uruchom aplikację
streamlit run wesad_full_pro_streamlit_app.py

# LUB dla aplikacji predykcji:
streamlit run results/streamlit_prediction_app.py
```

**Co się stanie:**
- Aplikacja otworzy się w przeglądarce pod adresem: `http://localhost:8501`
- Koleżanka/kolega może otworzyć ten sam adres na swoim komputerze (jeśli jest w tej samej sieci)

### Opcja 2: Udostępnienie w sieci lokalnej

```bash
# Uruchom z dostępem z sieci
streamlit run wesad_full_pro_streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

**Następnie:**
1. Sprawdź swój adres IP:
   ```bash
   # Na Mac:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   
2. Koleżanka/kolega otwiera w przeglądarce:
   ```
   http://TWOJ_IP:8501
   ```
   Np. `http://192.168.1.100:8501`

## 🌐 Opcja 3: Streamlit Cloud (darmowe, online)

### Krok 1: Przygotuj repozytorium GitHub

```bash
# Jeśli jeszcze nie masz na GitHubie:
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"
git init
git add wesad_full_pro_streamlit_app.py
git add results/streamlit_prediction_app.py
git add results/*.pkl results/*.json results/*.csv
git commit -m "Add Streamlit app"
git remote add origin https://github.com/TWOJE_KONTO/WESAD-streamlit.git
git push -u origin main
```

### Krok 2: Utwórz plik requirements.txt

```bash
# W katalogu z aplikacją
cat > requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
EOF
```

### Krok 3: Wdróż na Streamlit Cloud

1. Przejdź do: https://share.streamlit.io
2. Zaloguj się przez GitHub
3. Kliknij "New app"
4. Wybierz repozytorium i plik: `wesad_full_pro_streamlit_app.py`
5. Kliknij "Deploy"

**Gotowe!** Aplikacja będzie dostępna pod adresem:
```
https://TWOJE-KONTO.streamlit.app
```

## 📱 Opcja 4: Ngrok (tunelowanie, szybkie rozwiązanie)

### Instalacja ngrok

```bash
# Pobierz z: https://ngrok.com/download
# Lub przez Homebrew:
brew install ngrok
```

### Uruchomienie

```bash
# Terminal 1: Uruchom Streamlit
streamlit run wesad_full_pro_streamlit_app.py

# Terminal 2: Utwórz tunel
ngrok http 8501
```

**Ngrok da Ci publiczny URL**, np.:
```
https://abc123.ngrok.io
```

Koleżanka/kolega może otworzyć ten link w przeglądarce!

## 🐳 Opcja 5: Docker (dla zaawansowanych)

Jeśli masz Docker, możesz uruchomić aplikację w kontenerze:

```bash
# Zbuduj obraz
docker build -t wesad-streamlit -f Dockerfile.streamlit .

# Uruchom kontener
docker run -p 8501:8501 wesad-streamlit
```

## ✅ Sprawdzenie czy wszystko działa

### Przed pokazaniem:

1. **Sprawdź czy Streamlit jest zainstalowany:**
   ```bash
   streamlit --version
   ```

2. **Sprawdź czy pliki istnieją:**
   ```bash
   ls -la wesad_full_pro_streamlit_app.py
   ls -la results/streamlit_prediction_app.py
   ```

3. **Sprawdź czy są potrzebne pliki danych:**
   ```bash
   ls -la results/analysis_results.json
   ls -la results/*.pkl
   ls -la wesad_features_full.csv
   ```

## 🎬 Najprostszy sposób (dla szybkiego pokazania)

```bash
# 1. Otwórz Terminal
# 2. Wpisz:
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"
streamlit run wesad_full_pro_streamlit_app.py

# 3. Aplikacja otworzy się automatycznie w przeglądarce
# 4. Koleżanka/kolega może otworzyć ten sam adres (jeśli jest w sieci)
#    lub możesz użyć ngrok dla publicznego dostępu
```

## 🔧 Rozwiązywanie problemów

### Błąd: "streamlit: command not found"
```bash
pip install streamlit
# lub
pip3 install streamlit
```

### Błąd: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Port 8501 zajęty
```bash
# Użyj innego portu:
streamlit run wesad_full_pro_streamlit_app.py --server.port 8502
```

### Aplikacja nie znajduje plików
- Upewnij się, że uruchamiasz z właściwego katalogu
- Sprawdź ścieżki w kodzie aplikacji

## 📝 Notatki

- **Lokalnie:** Najszybsze, ale tylko na tym samym komputerze lub w sieci lokalnej
- **Ngrok:** Szybkie rozwiązanie dla publicznego dostępu (darmowe, ale URL zmienia się przy każdym uruchomieniu)
- **Streamlit Cloud:** Najlepsze dla stałego dostępu (darmowe, stały URL)

## 🎯 Rekomendacja

Dla szybkiego pokazania koleżance/koleże:
1. Użyj **ngrok** (najszybsze)
2. Lub **Streamlit Cloud** (jeśli chcesz stały link)

Dla lokalnego pokazania:
1. Uruchom lokalnie i udostępnij przez sieć lokalną

