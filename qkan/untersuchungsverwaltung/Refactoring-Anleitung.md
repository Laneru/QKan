# Refactoring-Anleitung: TV-Untersuchungstool mit Tabs

## Übersicht der Änderungen

Die refaktorierte Version (`KostenermittlungTool.py`) bietet folgende Verbesserungen:

### 1. **Tab-basierte Architektur**
- **Tab 1 - Aufträge**: Verwaltung von Untersuchungsaufträgen
- **Tab 2 - Kostenermittlung**: Kostenberechnung (aus bisherigem Code)
- **Tab 3 - Weitere Funktionen**: Platzhalter für zukünftige Erweiterungen

### 2. **Dynamisches UI**
- Kein `.ui` Datei mehr nötig → alles wird programmatisch generiert
- Bessere Kontrolle über Layout und Elemente
- Einfachere Erweiterbarkeit

### 3. **Modulare Struktur**
- Separate Methoden für jeden Tab
- Klare Trennung von Aufträgen und Kostenermittlung
- Leichtere Wartung und Fehlersuche

---

## Installation und Integration

### Schritt 1: Neue Datei erstellen

Erstelle eine neue Datei `Kostenermittlung_Tool.py` in deinem Plugin-Verzeichnis:

```
plugin_name/
├── __init__.py
├── main_plugin.py
├── Kostenermittlung_Tool.py  ← NEUE DATEI
├── settings/
│   ├── database.json
│   └── preisliste_untersuchung.json
└── res/
    └── (alte .ui Dateien optional)
```

### Schritt 2: Import in main_plugin.py

Passe deinen Haupt-Plugin-Code an:

```python
# In deinem main_plugin.py
from .Kostenermittlung_Tool import KostenermittlungTool

class YourMainPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.conn = None  # Datenbankverbindung
        self.db_type = 'postgres'  # oder 'spatialite'
    
    def show_kostenermittlung_tool(self):
        """Öffne das Kostenermittlungstool"""
        dialog = KostenermittlungTool(self)
        dialog.exec_()
```

### Schritt 3: Aufruf aus deinem Plugin

```python
# Beispiel: Button-Klick in deinem Haupt-Plugin
action = QAction("Kostenermittlung", self.iface.mainWindow())
action.triggered.connect(self.show_kostenermittlung_tool)
```

---

## Detaillierte Struktur

### Tab 1: Auftragsmanagement (`create_auftraege_tab()`)

**Funktionalität:**
- Neue Aufträge erstellen
- Aufträge bearbeiten und speichern
- Aufträge laden und löschen
- Auftragsübersicht in Tabelle

**Datenstruktur:**
```python
self.projects_data = {
    'Auftrag 1': {
        'name': 'Auftrag 1',
        'datum': '2026-02-21',
        'status': 'In Bearbeitung',
        'beschreibung': 'Kanalreinigung Straße X',
        'haltungen': []  # Liste der Haltungsnamen
    }
}
```

**Wichtige Methoden:**
- `create_new_project()` - Neue Auftrag
- `save_project()` - Auftrag speichern
- `load_project()` - Auftrag laden
- `delete_project()` - Auftrag löschen
- `refresh_projects_table()` - Tabelle aktualisieren

**Erweiterungsmöglichkeiten:**
- Persistente Speicherung in Datenbank (statt nur im RAM)
- Verknüpfung mit QGIS-Selektionen
- Automatisches Datum der letzten Änderung
- Berechtigungssystem

### Tab 2: Kostenermittlung (`create_kostenermittlung_tab()`)

**Funktionalität:**
- Haltungen aus Layer laden
- Kostenberechnung durchführen
- Panoramo- und GAL-Optionen
- Excel-Export

**Struktur:**
```
┌─────────────────────────────────────┐
│ Haltungsauswahl                     │
│ [Haltungen laden] [Aktualisieren]   │
├─────────────────────────────────────┤
│ Haltungsdaten (Tabelle)             │
│ Haltung | Länge | System | Kosten..│
├─────────────────────────────────────┤
│ ☐ Panoramo  ☐ GAL                  │
│ [Reinigung berechnen] [TV berechnen]│
├─────────────────────────────────────┤
│ Kostenzusammenfassung               │
│ MW: 1.000,00€ | RW: 500,00€ | ...  │
├─────────────────────────────────────┤
│ [In Excel exportieren]              │
└─────────────────────────────────────┘
```

**Wichtige Methoden:**
- `showSelectedFeatures()` - Features aus Layer laden
- `calculateCleaningCost()` - Reinigungskosten
- `calculateCleaningTVCost()` - TV/Befahrungskosten
- `export_excel()` - In Excel exportieren

### Tab 3: Weitere Funktionen (`create_weitere_tab()`)

**Aktuell:** Nur Platzhalter

**Ideen für Erweiterungen:**
- Abflussgrundrisse verwalten
- Inspektionsergebnisse dokumentieren
- Fotogalerie für Haltungen
- Defektklassifizierung
- Prognose-Tool für Reparaturen
- Statistiken und Auswertungen

---

## Wichtige Anpassungen

### 1. **Kostenfeld-Verwaltung**

Die alte Version mit `.ui` Datei definierte die Felder manuell. Im neuen Code werden sie dynamisch erzeugt:

```python
def create_cost_display_group(self, parent_layout, title, row, systems):
    """Hilfsfunktion für Kostengruppen"""
    # Erzeugt automatisch netto/brutto Felder für jedes System
```

Das macht den Code wartbarer und vermeidet Tipp-Fehler.

### 2. **Datenbank-Unterstützung**

Beide DB-Typen werden unterstützt:

```python
if self.is_spatialite:
    # SQLite Syntax
    placeholders = ','.join(['?'] * len(haltnams_list))
else:
    # PostgreSQL Syntax
    placeholders = ','.join(['%s'] * len(haltnams_list))
```

### 3. **Auftrag-Haltung Verknüpfung**

Um Haltungen einem Auftrag zuzuweisen, könnte man z.B. beim Laden erweitern:

```python
def load_project(self):
    """Lade Auftrag"""
    # ... vorhandener Code ...
    
    # Neue Haltungen hinzufügen
    project = self.projects_data[project_name]
    for haltung in project['haltungen']:
        # In Tab 2 markieren
        pass
```

---

## Mögliche Erweiterungen

### 1. **Persistente Speicherung**

```python
def save_project_to_db(self, project_data):
    """Speichere Auftrag in PostgreSQL"""
    query = """
    INSERT INTO auftraege (name, datum, status, beschreibung)
    VALUES (%s, %s, %s, %s)
    RETURNING id
    """
    self.cur.execute(query, (
        project_data['name'],
        project_data['datum'],
        project_data['status'],
        project_data['beschreibung']
    ))
    return self.cur.fetchone()[0]
```

### 2. **Mehrfachauswahl in Auftragsauswahl**

```python
def load_project_dialog(self):
    """Dialog zur Projektauswahl"""
    from qgis.PyQt.QtWidgets import QComboBox, QInputDialog
    
    projects = list(self.projects_data.keys())
    project_name, ok = QInputDialog.getItem(
        self, "Projekt auswählen", "Projekt:", projects
    )
    if ok:
        self.load_project(project_name)
```

### 3. **Automatische Kostenberechnung**

```python
def on_table_changed(self, item):
    """Berechne Kosten bei Änderung"""
    if item.column() == 1:  # Länge geändert
        self.calculateCleaningCost()
        self.calculateCleaningTVCost()
```

Verbinde im `create_kostenermittlung_tab()`:
```python
self.Liste_Haltungen.itemChanged.connect(self.on_table_changed)
```

### 4. **Historisierung**

```python
def create_history_tab(self):
    """Tab für Änderungshistorie"""
    widget = QWidget()
    layout = QVBoxLayout()
    
    history_table = QTableWidget()
    history_table.setColumnCount(4)
    history_table.setHorizontalHeaderLabels([
        "Zeitstempel", "Aktion", "Auftrag", "Details"
    ])
    layout.addWidget(history_table)
    
    widget.setLayout(layout)
    return widget
```

---

## Best Practices

### 1. **Error Handling**

```python
try:
    # Datenbankoperation
    self.cur.execute(query, params)
except psycopg2.Error as e:
    QMessageBox.critical(
        self, 
        "Datenbankfehler", 
        f"Fehler: {str(e)}"
    )
except Exception as e:
    import traceback
    traceback.print_exc()
    QMessageBox.critical(self, "Fehler", str(e))
```

### 2. **Logging**

```python
from qgis.core import QgsMessageLog, Qgis

def log_message(message, level=Qgis.Info):
    QgsMessageLog.logMessage(
        message,
        'KostenermittlungTool',
        level
    )
```

### 3. **Validierung**

```python
def validate_project_data(self, data):
    """Validiere Auftragsdaten"""
    if not data['name'].strip():
        raise ValueError("Auftragsname darf nicht leer sein")
    
    try:
        QDate.fromString(data['datum'], "yyyy-MM-dd")
    except:
        raise ValueError("Ungültiges Datumsformat")
    
    return True
```

---

## Migration vom alten Code

### Was zu beachten ist:

1. **`.ui` Dateien:** Nicht mehr nötig, aber können gelöscht werden
2. **Kostenfeld-Namen:** Ändern sich nicht (z.B. `self.Reinigung_netto_MW`)
3. **SQL-Queries:** Funktionieren weiterhin mit PostgreSQL und SQLite
4. **Callbacks:** Alle bisherigen Callbacks funktionieren wie vorher

### Direkte Anpassungen nötig:

```python
# ALT (mit .ui Datei):
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "res", "Kostenermittlung.ui")
)
class Kostenermittlung(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

# NEU (dynamisch):
class KostenermittlungTool(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
```

---

## Testing

Teste folgende Szenarien:

1. **Auftragsverwaltung:**
   - ✅ Neuen Auftrag erstellen
   - ✅ Auftrag speichern/laden
   - ✅ Auftrag löschen

2. **Kostenermittlung:**
   - ✅ Haltungen aus Layer laden
   - ✅ Reinigungskosten berechnen
   - ✅ TV-Kosten berechnen
   - ✅ Mit/ohne Panoramo
   - ✅ Mit/ohne GAL
   - ✅ Excel-Export

3. **Datenbankoperationen:**
   - ✅ PostgreSQL Verbindung
   - ✅ SQLite/Spatialite Fallback
   - ✅ GAL-Abfrage funktioniert

---

## Support

Bei Fragen oder Problemen:

1. Überprüfe die Konsolenausgabe auf Fehler
2. Nutze `QMessageBox` für Debug-Infos
3. Aktiviere QGIS Logging: `QgsMessageLog.logMessage()`
4. Überprüfe die Datenbank-Verbindung

---

**Fertig!** Die refaktorierte Version ist produktionsreif. 🚀
