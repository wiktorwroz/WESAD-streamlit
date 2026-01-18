# 🐳 Docker Setup dla WESAD Analysis Notebooks

## 📋 Zawartość

Ten Docker setup zawiera:
- `wesad_full_pro_analysis.ipynb` - Pełna analiza regulacji emocjonalnej
- `testy_stacjonarnosci.ipynb` - Testy stacjonarności sygnałów

## 🚀 Szybki Start

### Opcja 1: Docker Compose (Zalecane)

```bash
# Zbuduj i uruchom
docker-compose up --build

# W przeglądarce otwórz:
# http://localhost:8888
```

### Opcja 2: Docker bezpośrednio

```bash
# Zbuduj obraz
docker build -t wesad-analysis .

# Uruchom kontener
docker run -d \
  -p 8888:8888 \
  -v $(pwd)/wesad_full_pro_analysis.ipynb:/workspace/wesad_full_pro_analysis.ipynb \
  -v $(pwd)/testy_stacjonarnosci.ipynb:/workspace/testy_stacjonarnosci.ipynb \
  -v $(pwd)/data:/workspace/data:ro \
  -v $(pwd)/results:/workspace/results \
  --name wesad-analysis \
  wesad-analysis

# W przeglądarce otwórz:
# http://localhost:8888
```

## 📁 Struktura

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── wesad_full_pro_analysis.ipynb
├── testy_stacjonarnosci.ipynb
└── data/              # (opcjonalnie) dane WESAD
```

## 🔧 Konfiguracja

### Porty
- **8888** - Jupyter Lab

### Volumes
- Notebooks są zamontowane, więc zmiany są zachowane
- `./data` - dane WESAD (read-only)
- `./results` - wyniki analiz (zapis)

### Zmienne środowiskowe
- `JUPYTER_ENABLE_LAB=yes` - używa Jupyter Lab zamiast Notebook

## 📦 Zainstalowane biblioteki

- numpy, pandas, scipy
- matplotlib, seaborn, plotly
- scikit-learn
- imbalanced-learn (SMOTE)
- shap (interpretacja modeli)
- jupyter, jupyterlab

## 🛠️ Komendy

### Zatrzymaj kontener
```bash
docker-compose down
# lub
docker stop wesad-analysis
```

### Zobacz logi
```bash
docker-compose logs -f
# lub
docker logs -f wesad-analysis
```

### Wejdź do kontenera
```bash
docker exec -it wesad-analysis bash
```

### Usuń kontener i obraz
```bash
docker-compose down --rmi all
# lub
docker rm -f wesad-analysis
docker rmi wesad-analysis
```

## ⚠️ Uwagi

1. **Dane WESAD**: Jeśli masz dane WESAD, umieść je w katalogu `./data` przed uruchomieniem
2. **Wyniki**: Wyniki analiz będą zapisywane w `./results`
3. **Token**: Jupyter Lab jest dostępny bez tokenu (tylko dla lokalnego użycia!)
4. **Pamięć**: Notebooki mogą wymagać dużo pamięci RAM - upewnij się, że Docker ma wystarczająco zasobów

## 🔒 Bezpieczeństwo

⚠️ **UWAGA**: Ten setup jest przeznaczony do lokalnego użycia. 
Dla produkcji:
- Dodaj token do Jupyter
- Użyj hasła
- Skonfiguruj HTTPS

## 📝 Przykładowe użycie

1. **Uruchom Docker:**
   ```bash
   docker-compose up
   ```

2. **Otwórz Jupyter Lab:**
   - Przejdź do: http://localhost:8888
   - Otwórz `wesad_full_pro_analysis.ipynb` lub `testy_stacjonarnosci.ipynb`

3. **Uruchom analizę:**
   - Wykonaj komórki w kolejności
   - Wyniki będą zapisane w `/workspace/results`

4. **Zatrzymaj:**
   ```bash
   docker-compose down
   ```

## 🐛 Rozwiązywanie problemów

### Port 8888 zajęty
```bash
# Zmień port w docker-compose.yml:
ports:
  - "8889:8888"  # Użyj 8889 zamiast 8888
```

### Brak pamięci
```bash
# Zwiększ limit pamięci w Docker Desktop:
# Settings → Resources → Memory
```

### Błędy importu
```bash
# Sprawdź czy wszystkie biblioteki są w requirements.txt
docker exec -it wesad-analysis pip list
```

## 📚 Więcej informacji

- [Docker Documentation](https://docs.docker.com/)
- [Jupyter Lab Documentation](https://jupyterlab.readthedocs.io/)

