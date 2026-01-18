# 🐳 Jak uruchomić Docker na Macu (Docker Desktop)

## 📋 Wymagania

- Docker Desktop zainstalowany i uruchomiony
- Terminal (wbudowany w Mac)

## 🚀 KROK PO KROKU

### 1. Sprawdź czy Docker działa

Otwórz Terminal i wpisz:
```bash
docker --version
```

Jeśli widzisz wersję (np. `Docker version 24.0.0`), Docker działa ✅

Jeśli nie:
- Otwórz **Docker Desktop** (ikonka wieloryba w górnym pasku)
- Poczekaj aż status zmieni się na "Docker Desktop is running"

### 2. Przejdź do katalogu z notebookami

```bash
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"
```

### 3. Zbuduj i uruchom Docker

**Opcja A: Docker Compose (NAJŁATWIEJSZE)**
```bash
docker-compose up --build
```

**Opcja B: Docker bezpośrednio**
```bash
# Zbuduj obraz
docker build -t wesad-analysis .

# Uruchom kontener
docker run -d \
  -p 8888:8888 \
  -v "$(pwd)/wesad_full_pro_analysis.ipynb:/workspace/wesad_full_pro_analysis.ipynb" \
  -v "$(pwd)/testy_stacjonarnosci.ipynb:/workspace/testy_stacjonarnosci.ipynb" \
  -v "$(pwd)/data:/workspace/data:ro" \
  -v "$(pwd)/results:/workspace/results" \
  --name wesad-analysis \
  wesad-analysis
```

### 4. Otwórz Jupyter Lab

Po uruchomieniu zobaczysz w terminalu coś takiego:
```
[I 2024-12-20 15:30:00.123 ServerApp] Jupyter Server 1.0.0 is running at:
[I 2024-12-20 15:30:00.123 ServerApp] http://0.0.0.0:8888/lab
```

**Kliknij w link** lub otwórz w przeglądarce:
```
http://localhost:8888
```

### 5. Użyj notebooków

- Otwórz `wesad_full_pro_analysis.ipynb`
- Otwórz `testy_stacjonarnosci.ipynb`
- Uruchamiaj komórki normalnie

### 6. Zatrzymaj Docker

W terminalu naciśnij: `Ctrl + C`

Lub w osobnym oknie terminala:
```bash
docker-compose down
```

## 🖥️ Docker Desktop - Interfejs graficzny

Możesz też użyć Docker Desktop do zarządzania:

1. **Otwórz Docker Desktop**
2. Przejdź do zakładki **"Containers"**
3. Zobaczysz kontener `wesad-analysis`
4. Możesz:
   - Zatrzymać/uruchomić kontener (przycisk ▶️/⏸️)
   - Zobaczyć logi (ikona 📋)
   - Otworzyć terminal w kontenerze (ikonka terminala)
   - Usunąć kontener (🗑️)

## 📊 Sprawdzenie statusu

```bash
# Zobacz uruchomione kontenery
docker ps

# Zobacz wszystkie kontenery (również zatrzymane)
docker ps -a

# Zobacz logi
docker logs wesad-analysis

# Zobacz użycie zasobów
docker stats wesad-analysis
```

## 🔧 Rozwiązywanie problemów

### Port 8888 zajęty
```bash
# Sprawdź co używa portu
lsof -i :8888

# Zmień port w docker-compose.yml na 8889
# Następnie otwórz: http://localhost:8889
```

### Docker Desktop nie działa
1. Otwórz Docker Desktop
2. Sprawdź czy status to "Docker Desktop is running"
3. Jeśli nie, kliknij "Start"

### Brak pamięci
1. Otwórz Docker Desktop
2. Settings (⚙️) → Resources
3. Zwiększ Memory (np. do 4GB lub 8GB)
4. Kliknij "Apply & Restart"

### Błędy podczas budowania
```bash
# Wyczyść cache i zbuduj ponownie
docker-compose build --no-cache
```

## 📝 Przykładowa sesja

```bash
# 1. Przejdź do katalogu
cd "/Users/turfian/Downloads/archive (4)/WESAD/wesad-prep/notebooks"

# 2. Uruchom Docker
docker-compose up --build

# 3. W przeglądarce: http://localhost:8888
# 4. Otwórz notebooki i pracuj

# 5. Gdy skończysz, zatrzymaj:
# W terminalu: Ctrl+C
# Lub w osobnym terminalu:
docker-compose down
```

## 🎯 Szybkie komendy

```bash
# Uruchom w tle
docker-compose up -d

# Zatrzymaj
docker-compose down

# Zatrzymaj i usuń volumes
docker-compose down -v

# Zobacz logi
docker-compose logs -f

# Zrestartuj
docker-compose restart
```

