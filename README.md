# CV Parser mit KI-Bewertung

Eine moderne Anwendung zur automatischen Analyse von Lebensläufen mittels künstlicher Intelligenz. Die Anwendung bewertet CVs basierend auf Stellenanforderungen und erstellt ein Matching-Score.

## Features

- PDF-Lebenslauf-Parsing
- KI-basierte Textanalyse mit deutschem Sprachmodell
- Automatische Bewertung basierend auf Stellenanforderungen
- Moderne Benutzeroberfläche
- Mehrsprachige Unterstützung (Deutsch)

## Installation

1. Python-Umgebung einrichten (Python 3.8+ erforderlich):
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Frontend-Abhängigkeiten installieren:
```bash
cd frontend
npm install
```

## Verwendung

1. Backend starten:
```bash
uvicorn main:app --reload
```

2. Frontend starten:
```bash
cd frontend
npm start
```

Die Anwendung ist dann unter http://localhost:3000 verfügbar. 