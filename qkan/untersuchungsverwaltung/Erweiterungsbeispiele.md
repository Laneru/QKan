# Erweiterungsbeispiele für KostenermittlungTool

## 1. Persistente Speicherung in Datenbank

```python
def save_project_to_db(self, project_data):
    """Speichere Auftrag in PostgreSQL Tabelle"""
    try:
        # Erstelle Tabelle falls nicht vorhanden
        create_table_query = """
        CREATE TABLE IF NOT EXISTS auftraege (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            datum DATE NOT NULL,
            status VARCHAR(50) DEFAULT 'Entwurf',
            beschreibung TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        
        CREATE TABLE IF NOT EXISTS auftrag_haltungen (
            id SERIAL PRIMARY KEY,
            auftrag_id INTEGER REFERENCES auftraege(id) ON DELETE CASCADE,
            haltungsname VARCHAR(255) NOT NULL,
            added_at TIMESTAMP DEFAULT NOW()
        );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()
        
        # Einfügen des Auftrags
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
        
        auftrag_id = self.cur.fetchone()[0]
        self.conn.commit()
        
        # Füge Haltungen hinzu
        for haltung in project_data.get('haltungen', []):
            haltung_query = """
            INSERT INTO auftrag_haltungen (auftrag_id, haltungsname)
            VALUES (%s, %s)
            """
            self.cur.execute(haltung_query, (auftrag_id, haltung))
        
        self.conn.commit()
        
        QMessageBox.information(
            self, 
            "Erfolg",
            f"Auftrag mit ID {auftrag_id} gespeichert"
        )
        
        return auftrag_id
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        QMessageBox.critical(
            self,
            "Fehler beim Speichern",
            f"Fehler: {str(e)}"
        )
        return None


def load_projects_from_db(self):
    """Lade alle Aufträge aus der Datenbank"""
    try:
        query = """
        SELECT id, name, datum, status, beschreibung
        FROM auftraege
        ORDER BY updated_at DESC
        """
        
        self.cur.execute(query)
        auftraege = self.cur.fetchall()
        
        self.projects_data = {}
        for auftrag in auftraege:
            auftrag_id, name, datum, status, beschreibung = auftrag
            
            # Lade Haltungen
            haltungen_query = """
            SELECT haltungsname FROM auftrag_haltungen
            WHERE auftrag_id = %s
            """
            self.cur.execute(haltungen_query, (auftrag_id,))
            haltungen = [h[0] for h in self.cur.fetchall()]
            
            self.projects_data[name] = {
                'id': auftrag_id,
                'name': name,
                'datum': datum.isoformat(),
                'status': status,
                'beschreibung': beschreibung,
                'haltungen': haltungen
            }
        
        self.refresh_projects_table()
        
    except Exception as e:
        QMessageBox.warning(
            self,
            "Fehler beim Laden",
            f"Konnte Aufträge nicht laden: {str(e)}"
        )
```

---

## 2. Erweiterte Auftragsauswahl Dialog

```python
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout
)

class AuftragAuswahlDialog(QDialog):
    """Dialog zur Auswahl eines existierenden Auftrags"""
    
    def __init__(self, auftraege_data, parent=None):
        super().__init__(parent)
        self.auftraege_data = auftraege_data
        self.selected_project = None
        self.init_ui()
        self.setWindowTitle("Auftrag auswählen")
        self.resize(600, 400)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Aufträge-Tabelle
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Name", "Datum", "Status", "Beschreibung"
        ])
        
        row = 0
        for name, data in self.auftraege_data.items():
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(data['name']))
            self.table.setItem(row, 1, QTableWidgetItem(data['datum']))
            self.table.setItem(row, 2, QTableWidgetItem(data['status']))
            self.table.setItem(row, 3, QTableWidgetItem(data['beschreibung']))
            row += 1
        
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        btn_select = QPushButton("Auswählen")
        btn_select.clicked.connect(self.select_project)
        button_layout.addWidget(btn_select)
        
        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def select_project(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Info", "Bitte einen Auftrag auswählen")
            return
        
        # Hole Auftragsname aus Tabelle
        project_names = list(self.auftraege_data.keys())
        self.selected_project = project_names[current_row]
        self.accept()


def open_auftrag_dialog(self):
    """Öffne Auftragsauswahl-Dialog"""
    if not self.projects_data:
        QMessageBox.info(self, "Info", "Keine Aufträge vorhanden")
        return
    
    dialog = AuftragAuswahlDialog(self.projects_data, self)
    if dialog.exec_():
        self.select_project(dialog.selected_project)
```

---

## 3. Automatische Kostenberechnung bei Eingabe

```python
def enable_live_calculation(self):
    """Aktiviere Echtzeit-Kostenberechnung"""
    self.Liste_Haltungen.itemChanged.connect(self.on_table_item_changed)


def on_table_item_changed(self, item):
    """Callback wenn Tabelleneintrag geändert wird"""
    # Ignoriere bestimmte Spalten
    if item.column() == 0:  # Haltungsname - nicht berechnen
        return
    
    if item.column() == 1:  # Länge geändert
        self.calculateCleaningCost()
        self.calculateCleaningTVCost()
    
    if item.column() == 4:  # GAL-Anzahl geändert
        self.calculateCleaningTVCost()
```

---

## 4. Export mit zusätzlichen Metadaten

```python
def export_excel_with_metadata(self):
    """Exportiere mit Auftrags-Metadaten"""
    
    file_path, _ = QFileDialog.getSaveFileName(
        self,
        "Excel-Datei speichern",
        "",
        "Excel-Dateien (*.xlsx)"
    )
    
    if not file_path:
        return
    
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from datetime import datetime
        
        workbook = Workbook()
        
        # === Tab 1: Metadaten ===
        ws_meta = workbook.active
        ws_meta.title = "Metadaten"
        
        ws_meta['A1'] = "Auftragsinformationen"
        ws_meta['A1'].font = Font(size=14, bold=True)
        
        row = 3
        if self.current_project and self.current_project in self.projects_data:
            project = self.projects_data[self.current_project]
            
            ws_meta[f'A{row}'] = "Auftragsname:"
            ws_meta[f'B{row}'] = project['name']
            row += 1
            
            ws_meta[f'A{row}'] = "Datum:"
            ws_meta[f'B{row}'] = project['datum']
            row += 1
            
            ws_meta[f'A{row}'] = "Status:"
            ws_meta[f'B{row}'] = project['status']
            row += 1
            
            ws_meta[f'A{row}'] = "Beschreibung:"
            ws_meta[f'B{row}'] = project['beschreibung']
            row += 2
        
        # Zusammenfassung
        ws_meta[f'A{row}'] = "Kostenzusammenfassung"
        ws_meta[f'A{row}'].font = Font(size=12, bold=True)
        row += 1
        
        ws_meta[f'A{row}'] = "Reinigung MW netto:"
        ws_meta[f'B{row}'] = self.Reinigung_netto_MW.text()
        row += 1
        
        ws_meta[f'A{row}'] = "Reinigung MW brutto:"
        ws_meta[f'B{row}'] = self.Reinigung_brutto_MW.text()
        row += 1
        
        ws_meta[f'A{row}'] = "Befahrung MW netto:"
        ws_meta[f'B{row}'] = self.Befahrung_netto_MW.text()
        row += 1
        
        ws_meta[f'A{row}'] = "Befahrung MW brutto:"
        ws_meta[f'B{row}'] = self.Befahrung_brutto_MW.text()
        
        # === Tab 2: Haltungsdaten ===
        ws_data = workbook.create_sheet("Haltungen")
        
        headers = [
            "Haltungsname", "Länge", "System", "Dimension", "GALs",
            "Reinigung", "Reinigung+TV", "TV", "GAL", "Panoramo"
        ]
        
        for col, header in enumerate(headers, 1):
            cell = ws_data.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        
        for table_row in range(self.Liste_Haltungen.rowCount()):
            for col in range(self.Liste_Haltungen.columnCount()):
                item = self.Liste_Haltungen.item(table_row, col)
                value = item.text() if item else ""
                ws_data.cell(
                    row=table_row + 2,
                    column=col + 1,
                    value=value
                )
        
        # Auto-Breite
        for column in ws_data.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            ws_data.column_dimensions[column_letter].width = min(max_length + 2, 50)
        
        workbook.save(file_path)
        
        QMessageBox.information(
            self,
            "Erfolg",
            f"Datei gespeichert:\n{file_path}"
        )
        
        # Öffne die Datei
        import os
        import subprocess
        if os.name == 'nt':
            os.startfile(file_path)
        else:
            subprocess.Popen(['xdg-open', file_path])
            
    except Exception as e:
        QMessageBox.critical(
            self,
            "Fehler beim Export",
            f"Fehler: {str(e)}"
        )
```

---

## 5. Fortschrittsanzeige für lange Operationen

```python
from qgis.PyQt.QtWidgets import QProgressDialog
from qgis.PyQt.QtCore import QTimer

def load_large_dataset(self):
    """Lade große Datenmengen mit Fortschrittsanzeige"""
    
    progress = QProgressDialog(
        "Daten werden geladen...",
        "Abbrechen",
        0,
        100,
        self
    )
    progress.setWindowModality(Qt.WindowModal)
    
    try:
        query = """
        SELECT haltnam, laenge, entwart, hoehe, breite
        FROM public.haltungen
        LIMIT 10000
        """
        
        self.cur.execute(query)
        
        # Hole Daten in Chunks
        chunk_size = 100
        all_rows = []
        
        while True:
            rows = self.cur.fetchmany(chunk_size)
            if not rows:
                break
            
            all_rows.extend(rows)
            progress.setValue(int(len(all_rows) / 100))
            
            # Ermögliche Abbruch
            if progress.wasCanceled():
                break
        
        progress.close()
        
        # Verarbeite Daten
        self.populate_table_from_rows(all_rows)
        
        QMessageBox.information(
            self,
            "Erfolg",
            f"{len(all_rows)} Datensätze geladen"
        )
        
    except Exception as e:
        progress.close()
        QMessageBox.critical(self, "Fehler", str(e))


def populate_table_from_rows(self, rows):
    """Fülle Tabelle mit Daten"""
    self.Liste_Haltungen.setRowCount(len(rows))
    
    for i, row in enumerate(rows):
        haltnam, laenge, entwart, hoehe, breite = row
        
        self.Liste_Haltungen.setItem(i, 0, QTableWidgetItem(haltnam))
        self.Liste_Haltungen.setItem(i, 1, QTableWidgetItem(str(laenge)))
        self.Liste_Haltungen.setItem(i, 2, QTableWidgetItem(entwart))
        
        h = int(hoehe) if hoehe else 0
        b = int(breite) if breite else 0
        dimension = f"{b}/{h}" if h != b else str(h)
        self.Liste_Haltungen.setItem(i, 3, QTableWidgetItem(dimension))
```

---

## 6. Validierung und Fehlerbehandlung

```python
def validate_project(self, project_data):
    """Validiere Projektdaten"""
    errors = []
    
    # Name validieren
    if not project_data.get('name', '').strip():
        errors.append("Auftragsname darf nicht leer sein")
    
    # Datum validieren
    try:
        from datetime import datetime
        datetime.strptime(project_data.get('datum', ''), '%Y-%m-%d')
    except:
        errors.append("Ungültiges Datumsformat (verwende YYYY-MM-DD)")
    
    # Status validieren
    valid_status = ["In Bearbeitung", "Abgeschlossen", "Pausiert", "Entwurf"]
    if project_data.get('status') not in valid_status:
        errors.append(f"Ungültiger Status. Erlaubt: {', '.join(valid_status)}")
    
    if errors:
        QMessageBox.warning(
            self,
            "Validierungsfehler",
            "\\n".join(errors)
        )
        return False
    
    return True


def save_project_validated(self):
    """Speichern mit Validierung"""
    project_data = {
        'name': self.auftrag_name.text().strip(),
        'datum': self.auftrag_datum.date().toString("yyyy-MM-dd"),
        'status': self.auftrag_status.currentText(),
        'beschreibung': self.auftrag_beschreibung.text()
    }
    
    if self.validate_project(project_data):
        self.save_project()
```

---

## 7. Logging und Debugging

```python
import logging
from qgis.core import QgsMessageLog, Qgis

# Konfiguriere Logger
logger = logging.getLogger('KostenermittlungTool')
logger.setLevel(logging.DEBUG)

# Handler für Datei
fh = logging.FileHandler('kostenermittlung.log')
fh.setLevel(logging.DEBUG)

# Handler für Konsole
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def log_action(self, action, details=""):
    """Protokolliere Aktion"""
    message = f"{action}: {details}"
    logger.info(message)
    
    # Auch in QGIS Log
    QgsMessageLog.logMessage(
        message,
        'KostenermittlungTool',
        Qgis.Info
    )


# Beispielnutzung
def save_project(self):
    try:
        # ... Speichern ...
        self.log_action("Projekt gespeichert", self.auftrag_name.text())
    except Exception as e:
        self.log_action("Fehler beim Speichern", str(e))
        logger.exception("Exception occurred")
```

---

Diese Erweiterungen kannst du nach Bedarf in dein Tool integrieren! 🚀
