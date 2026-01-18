#!/usr/bin/env python3
"""
Prosty test czy Streamlit działa
"""
import sys
import subprocess

print("=" * 80)
print("TEST STREAMLIT")
print("=" * 80)

# Sprawdź czy streamlit jest zainstalowany
try:
    import streamlit
    print(f"✅ Streamlit zainstalowany: {streamlit.__version__}")
except ImportError:
    print("❌ Streamlit nie jest zainstalowany!")
    print("   Zainstaluj: pip install streamlit")
    sys.exit(1)

# Sprawdź czy plik istnieje
import os
streamlit_file = "wesad_full_pro_streamlit_app.py"
if os.path.exists(streamlit_file):
    print(f"✅ Plik {streamlit_file} istnieje")
else:
    print(f"❌ Plik {streamlit_file} nie istnieje!")
    sys.exit(1)

# Sprawdź składnię
import ast
try:
    with open(streamlit_file, 'r') as f:
        ast.parse(f.read())
    print(f"✅ Składnia pliku {streamlit_file} jest poprawna")
except SyntaxError as e:
    print(f"❌ Błąd składniowy w {streamlit_file}: {e}")
    sys.exit(1)

# Sprawdź czy CSV istnieje
csv_file = "wesad_features_full.csv"
if os.path.exists(csv_file):
    print(f"✅ Plik {csv_file} istnieje")
    import pandas as pd
    try:
        df = pd.read_csv(csv_file)
        print(f"   Wierszy: {len(df)}, Kolumn: {len(df.columns)}")
        if 'subject' in df.columns:
            print(f"   Subjecty: {df['subject'].unique().tolist()}")
    except Exception as e:
        print(f"⚠️ Ostrzeżenie: Nie można wczytać CSV: {e}")
else:
    print(f"⚠️ Ostrzeżenie: Plik {csv_file} nie istnieje")
    print("   Aplikacja Streamlit pokaże komunikat o błędzie")

print("\n" + "=" * 80)
print("INSTRUKCJA URUCHOMIENIA:")
print("=" * 80)
print(f"\n1. Otwórz terminal")
print(f"2. Przejdź do katalogu:")
print(f"   cd \"{os.getcwd()}\"")
print(f"3. Uruchom Streamlit:")
print(f"   streamlit run {streamlit_file}")
print(f"\nAplikacja otworzy się w przeglądarce pod adresem: http://localhost:8501")
print("=" * 80)
