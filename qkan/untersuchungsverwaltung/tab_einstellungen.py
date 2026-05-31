# untersuchungsverwaltung/tab_einstellungen.py

import json
import os

import pandas as pd

from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QListWidgetItem,
    QFileDialog,
    QTableWidgetItem,
)
from qgis.PyQt.QtCore import Qt


class EinstellungenManager:
    """
    Verwaltet:
    - allgemeine Einstellungen
    - Listenverwaltung
    - PDF-Vorlagen
    - Plan-Ablagepfad
    - Preisverwaltung

    Preislogik:
    - dimensionsabhängig: Reinigung, Reinigung TV, TV, Panoramo
    - Einzelpreis: GAL, Panoramo SI
    """

    # ==================================================================
    # KONSTANTEN
    # ==================================================================

    PRICE_FILE_NAME = "preisliste_untersuchung.json"

    PRICE_CATEGORIES = [
        "Reinigung",
        "Reinigung TV",
        "TV",
        "GAL",
        "Panoramo",
        "Panoramo SI",
    ]

    SINGLE_PRICE_CATEGORIES = {
        "GAL",
        "Panoramo SI",
    }

    SINGLE_PRICE_KEY = "default"

    # ==================================================================
    # INITIALISIERUNG
    # ==================================================================

    def __init__(self, dialog):
        self.dialog = dialog
        self._preise_cache = None

        self.ensure_table_exists()

    # ==================================================================
    # TABELLENSTRUKTUR FÜR EINSTELLUNGEN
    # ==================================================================

    def ensure_table_exists(self):
        """Legt die Tabelle für Einstellungen an, falls sie noch nicht existiert."""
        if not self.dialog.cur:
            return

        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS untersuchungsverwaltung_einstellungen (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kategorie TEXT,
                        wert TEXT
                    )
                    """
                )
            else:
                self.dialog.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS public.untersuchungsverwaltung_einstellungen (
                        id SERIAL PRIMARY KEY,
                        kategorie VARCHAR(50),
                        wert TEXT
                    )
                    """
                )

            self.dialog.conn.commit()

        except Exception as e:
            self.dialog.conn.rollback()
            print(f"Fehler DB Einstellungen: {e}")

    # ==================================================================
    # PREISVERWALTUNG: DATEI / STRUKTUR
    # ==================================================================

    def get_price_file_path(self):
        """Liefert den Pfad zur Preisdatei im Tool-Ordner."""
        return os.path.join(os.path.dirname(__file__), self.PRICE_FILE_NAME)

    def get_default_price_structure(self):
        """Liefert die Standardstruktur der Preisdatei."""
        return {
            "Reinigung": {},
            "Reinigung TV": {},
            "TV": {},
            "GAL": {self.SINGLE_PRICE_KEY: 0.0},
            "Panoramo": {},
            "Panoramo SI": {self.SINGLE_PRICE_KEY: 0.0},
        }

    def _is_single_price_category(self, category):
        """Prüft, ob eine Kategorie nur einen Einzelpreis verwaltet."""
        return category in self.SINGLE_PRICE_CATEGORIES

    def _display_key_for_category(self, category, key):
        """
        Wandelt interne JSON-Schlüssel in UI-Anzeige um.
        Bei Einzelpreisen wird 'default' als 'Standard' angezeigt.
        """
        if self._is_single_price_category(category) and key == self.SINGLE_PRICE_KEY:
            return "Standard"
        return str(key)

    def _storage_key_for_category(self, category, displayed_key):
        """
        Wandelt UI-Eingaben zurück in JSON-Schlüssel.
        Bei Einzelpreisen wird immer 'default' gespeichert.
        """
        if self._is_single_price_category(category):
            return self.SINGLE_PRICE_KEY
        return str(displayed_key).strip()

    # ==================================================================
    # PREISVERWALTUNG: LADEN / SPEICHERN
    # ==================================================================

    def load_price_config(self):
        """
        Lädt die Preisdatei in den Cache.

        Struktur:
        {
            "Reinigung": {"300": 1.50},
            "Reinigung TV": {"300": 2.10},
            "TV": {"300": 3.50},
            "GAL": {"default": 19.59},
            "Panoramo": {"300": 2.80},
            "Panoramo SI": {"default": 37.51}
        }
        """
        file_path = self.get_price_file_path()
        data = self.get_default_price_structure()

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)

                for key in self.PRICE_CATEGORIES:
                    category_data = loaded.get(key, {})
                    if isinstance(category_data, dict):
                        data[key] = category_data

            except Exception as e:
                QMessageBox.warning(
                    self.dialog,
                    "Preisverwaltung",
                    f"Preisdatei konnte nicht geladen werden:\n{e}",
                )

        # Sicherstellen, dass Einzelpreiskategorien immer einen Default-Eintrag besitzen
        for category in self.SINGLE_PRICE_CATEGORIES:
            category_data = data.get(category, {})
            if not isinstance(category_data, dict):
                category_data = {}
            if self.SINGLE_PRICE_KEY not in category_data:
                category_data[self.SINGLE_PRICE_KEY] = 0.0
            data[category] = category_data

        self._preise_cache = data
        return data

    def save_price_config(self, data=None):
        """Speichert die Preisstruktur in die JSON-Datei."""
        if data is None:
            data = self._preise_cache or self.get_default_price_structure()

        file_path = self.get_price_file_path()

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self._preise_cache = data

        except Exception as e:
            QMessageBox.critical(
                self.dialog,
                "Preisverwaltung",
                f"Preisdatei konnte nicht gespeichert werden:\n{e}",
            )
            raise

    # ==================================================================
    # PREISVERWALTUNG: UI-INITIALISIERUNG
    # ==================================================================

    def init_preisverwaltung(self):
        """Initialisiert den Tab 'Preisverwaltung'."""
        if not hasattr(self.dialog, "preis_kategorie_combo"):
            return

        self.dialog.preis_kategorie_combo.clear()
        self.dialog.preis_kategorie_combo.addItems(self.PRICE_CATEGORIES)

        self.load_price_config()
        self.load_prices_into_table()

    def load_prices_into_table(self):
        if not hasattr(self.dialog, "preise_table"):
            return

        if self._preise_cache is None:
            self.load_price_config()

        category = self.dialog.preis_kategorie_combo.currentText()
        values = self._preise_cache.get(category, {})
        table = self.dialog.preise_table

        if self._is_single_price_category(category):
            price_value = values.get(self.SINGLE_PRICE_KEY, 0.0)
            table.setRowCount(1)
            table.setItem(0, 0, QTableWidgetItem("Standard"))
            table.setItem(0, 1, QTableWidgetItem(self._format_price(price_value)))
        else:
            # HIER: sortiert nach Dimension
            rows = sorted(
                values.items(),
                key=lambda kv: self._dimension_sort_key(kv[0])
            )
            table.setRowCount(len(rows))
            for row, (dimension, price) in enumerate(rows):
                table.setItem(row, 0, QTableWidgetItem(str(dimension)))
                table.setItem(row, 1, QTableWidgetItem(self._format_price(price)))

    def _dimension_sort_key(self, dim_str: str):
        """
        Erzeugt einen Sortierschlüssel für Dimensionen wie
        '200', '250/375', '600/900' usw., damit sie
        numerisch sinnvoll aufsteigend sortiert werden.
        """
        s = str(dim_str).strip()
        if "/" in s:
            parts = s.split("/")
            try:
                # sortiere zuerst nach erstem, dann nach zweitem Wert
                return (float(parts[0]), float(parts[1]))
            except ValueError:
                return (float("inf"), float("inf"))
        else:
            try:
                return (float(s), float("-inf"))
            except ValueError:
                return (float("inf"), float("-inf"))
        
    def add_price_row(self):
        """
        Fügt eine neue Zeile in der Preisverwaltung hinzu.

        Für Einzelpreiskategorien wird keine weitere Zeile angelegt,
        sondern nur die vorhandene Standardzeile fokussiert.
        """
        if not hasattr(self.dialog, "preise_table"):
            return

        category = self.dialog.preis_kategorie_combo.currentText()
        table = self.dialog.preise_table

        if self._is_single_price_category(category):
            if table.rowCount() == 0:
                table.setRowCount(1)
                table.setItem(0, 0, QTableWidgetItem("Standard"))
                table.setItem(0, 1, QTableWidgetItem("0.00"))
            table.setCurrentCell(0, 1)
            return

        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(""))
        table.setItem(row, 1, QTableWidgetItem("0.00"))
        table.setCurrentCell(row, 0)

    def delete_selected_price_row(self):
        """
        Löscht die ausgewählte Preiszeile.

        Bei Einzelpreiskategorien wird nicht die Zeile gelöscht,
        sondern der Preis auf 0.00 zurückgesetzt.
        """
        if not hasattr(self.dialog, "preise_table"):
            return

        category = self.dialog.preis_kategorie_combo.currentText()
        table = self.dialog.preise_table

        if self._is_single_price_category(category):
            if table.rowCount() == 0:
                table.setRowCount(1)
                table.setItem(0, 0, QTableWidgetItem("Standard"))
            table.setItem(0, 1, QTableWidgetItem("0.00"))
            table.setCurrentCell(0, 1)
            return

        row = table.currentRow()
        if row >= 0:
            table.removeRow(row)

    def reload_prices_from_json(self):
        """Lädt die Preisdatei neu und aktualisiert anschließend den KostenManager."""
        self.load_price_config()
        self.load_prices_into_table()

        if hasattr(self.dialog, "logic_kosten"):
            self.dialog.logic_kosten.load_cleaning_costs()

    def save_prices_from_table(self):
        """
        Liest die Preistabelle aus und speichert sie in die JSON-Datei.

        Besonderheiten:
        - GAL wird als Einzelpreis gespeichert
        - Panoramo SI wird als Einzelpreis gespeichert
        """
        if self._preise_cache is None:
            self.load_price_config()

        category = self.dialog.preis_kategorie_combo.currentText()
        table = self.dialog.preise_table

        if self._is_single_price_category(category):
            price_item = table.item(0, 1) if table.rowCount() > 0 else None
            price_text = price_item.text().strip() if price_item else "0.00"

            price_value = self._parse_price(price_text)
            if price_value is None:
                QMessageBox.warning(
                    self.dialog,
                    "Preisverwaltung",
                    f"Ungültiger Preis für '{category}': '{price_text}'",
                )
                return

            self._preise_cache[category] = {
                self.SINGLE_PRICE_KEY: price_value
            }

        else:
            category_data = {}

            for row in range(table.rowCount()):
                dim_item = table.item(row, 0)
                price_item = table.item(row, 1)

                dimension = dim_item.text().strip() if dim_item else ""
                price_text = price_item.text().strip() if price_item else ""

                if not dimension:
                    continue

                price_value = self._parse_price(price_text)
                if price_value is None:
                    QMessageBox.warning(
                        self.dialog,
                        "Preisverwaltung",
                        f"Ungültiger Preis in Zeile {row + 1}: '{price_text}'",
                    )
                    return

                storage_key = self._storage_key_for_category(category, dimension)
                category_data[storage_key] = price_value

            self._preise_cache[category] = category_data

        self.save_price_config(self._preise_cache)
        self.load_prices_into_table()

        if hasattr(self.dialog, "logic_kosten"):
            self.dialog.logic_kosten.load_cleaning_costs()

        QMessageBox.information(
            self.dialog,
            "Preisverwaltung",
            "Preise wurden gespeichert.",
        )

    # ==================================================================
    # PREISVERWALTUNG: HILFSMETHODEN
    # ==================================================================

    def _format_price(self, value):
        """Formatiert einen Preis für die Anzeige."""
        try:
            return f"{float(value):.2f}"
        except Exception:
            return "0.00"

    def _parse_price(self, value):
        """Wandelt eine Preiseingabe robust in float um."""
        try:
            cleaned = str(value).replace("€", "").replace(",", ".").strip()
            return float(cleaned)
        except Exception:
            return None

    # ==================================================================
    # PLAN-ABLAGEPFAD
    # ==================================================================

    def on_choose_plan_path(self):
        """Öffnet einen Dialog zur Auswahl des Basisordners für Pläne."""
        start_dir = self.get_single_value("Plan_Basis_Pfad") or os.path.expanduser("~")

        directory = QFileDialog.getExistingDirectory(
            self.dialog,
            "Basisordner für Pläne auswählen",
            start_dir,
        )

        if not directory:
            return

        directory = os.path.normpath(directory)

        if hasattr(self.dialog, "plan_path_line"):
            self.dialog.plan_path_line.setText(directory)

        self._save_single_value("Plan_Basis_Pfad", directory)

    def on_clear_plan_path(self):
        """Löscht den gespeicherten Plan-Basis-Pfad."""
        if hasattr(self.dialog, "plan_path_line"):
            self.dialog.plan_path_line.clear()

        self._save_single_value("Plan_Basis_Pfad", "")

    # ==================================================================
    # PDF-VORLAGEN
    # ==================================================================

    def init_pdf_template_editors(self):
        """Lädt gespeicherte HTML-Inhalte in die PDF-Editoren."""
        if not hasattr(self.dialog, "pdf_info_editor") or not hasattr(self.dialog, "pdf_beauf_editor"):
            return

        html_info = self.get_single_value("PDF_Info_HTML")
        if html_info:
            self.dialog.pdf_info_editor.set_html(html_info)

        html_beauf = self.get_single_value("PDF_Beauf_HTML")
        if html_beauf:
            self.dialog.pdf_beauf_editor.set_html(html_beauf)

    def save_pdf_templates(self):
        """Speichert die Inhalte der PDF-Template-Editoren."""
        try:
            if not hasattr(self.dialog, "pdf_info_editor") or not hasattr(self.dialog, "pdf_beauf_editor"):
                QMessageBox.warning(
                    self.dialog,
                    "PDF-Vorlagen",
                    "PDF-Editoren sind noch nicht initialisiert.",
                )
                return

            html_info = self.dialog.pdf_info_editor.get_html()
            html_beauf = self.dialog.pdf_beauf_editor.get_html()

            self._save_single_value("PDF_Info_HTML", html_info)
            self._save_single_value("PDF_Beauf_HTML", html_beauf)

        except Exception as e:
            QMessageBox.critical(
                self.dialog,
                "PDF-Vorlagen",
                f"Fehler beim Speichern der PDF-Vorlagen:\n{e}",
            )

    # ==================================================================
    # EINZELWERTE SPEICHERN / LADEN
    # ==================================================================

    def _save_single_value(self, kategorie, wert):
        """Speichert einen Einzelwert zu einer Kategorie."""
        if not self.dialog.cur:
            return

        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute(
                    "DELETE FROM untersuchungsverwaltung_einstellungen WHERE kategorie=?",
                    (kategorie,),
                )
                self.dialog.cur.execute(
                    "INSERT INTO untersuchungsverwaltung_einstellungen (kategorie, wert) VALUES (?, ?)",
                    (kategorie, wert),
                )
            else:
                self.dialog.cur.execute(
                    "DELETE FROM public.untersuchungsverwaltung_einstellungen WHERE kategorie=%s",
                    (kategorie,),
                )
                self.dialog.cur.execute(
                    "INSERT INTO public.untersuchungsverwaltung_einstellungen (kategorie, wert) VALUES (%s, %s)",
                    (kategorie, wert),
                )

            self.dialog.conn.commit()

        except Exception as e:
            self.dialog.conn.rollback()
            QMessageBox.critical(
                self.dialog,
                "Fehler",
                f"Konnte Wert nicht speichern:\n{e}",
            )

    def get_values(self, kategorie):
        """Liefert alle Werte einer Kategorie, ggf. als dekodierte JSON-Objekte."""
        if not self.dialog.cur:
            return []

        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute(
                    """
                    SELECT wert
                    FROM untersuchungsverwaltung_einstellungen
                    WHERE kategorie=?
                    ORDER BY wert
                    """,
                    (kategorie,),
                )
            else:
                self.dialog.cur.execute(
                    """
                    SELECT wert
                    FROM public.untersuchungsverwaltung_einstellungen
                    WHERE kategorie=%s
                    ORDER BY wert
                    """,
                    (kategorie,),
                )

            results = []
            for row in self.dialog.cur.fetchall():
                try:
                    results.append(json.loads(row[0]))
                except Exception:
                    results.append(row[0])

            return results

        except Exception:
            return []

    def get_single_value(self, kategorie):
        """Liefert den ersten Wert einer Kategorie als String."""
        vals = self.get_values(kategorie)
        return str(vals[0]).strip() if vals else ""

    def get_simple_list(self, kategorie):
        """Liefert eine flache Textliste für Auswahllisten und Comboboxen."""
        values = self.get_values(kategorie)
        flat_list = []

        for v in values:
            if isinstance(v, dict):
                if kategorie == "Sachbearbeiter":
                    flat_list.append(
                        f"{v.get('vorname', '')} {v.get('nachname', '')}".strip()
                    )
                elif kategorie == "Firmen":
                    flat_list.append(v.get("name", "").strip())
            else:
                flat_list.append(str(v))

        return flat_list

    # ==================================================================
    # FORMULARSTEUERUNG
    # ==================================================================

    def _clear_form_fields(self):
        """Leert alle Eingabefelder im Einstellungen-Tab."""
        field_names = [
            "einst_text_wert",
            "einst_sb_vorname",
            "einst_sb_nachname",
            "einst_sb_tel",
            "einst_sb_mail",
            "einst_firma_name",
            "einst_firma_plz",
            "einst_firma_ort",
            "einst_firma_str",
            "einst_firma_hnr",
            "einst_firma_tel",
            "einst_firma_mail",
        ]

        for name in field_names:
            widget = getattr(self.dialog, name, None)
            if widget is not None:
                widget.clear()

    def _set_dynamic_area_visible(self, visible=True):
        """Blendet den dynamischen Eingabebereich ein oder aus."""
        if hasattr(self.dialog, "einst_dyn_widget") and self.dialog.einst_dyn_widget is not None:
            self.dialog.einst_dyn_widget.setVisible(visible)
        elif hasattr(self.dialog, "einst_stack") and self.dialog.einst_stack is not None:
            self.dialog.einst_stack.setVisible(visible)

    # ==================================================================
    # KATEGORIEWECHSEL / LISTENLADEN
    # ==================================================================

    def on_kategorie_changed(self):
        """Reagiert auf einen Wechsel der Kategorie im Einstellungen-Tab."""
        kategorie = self.dialog.einst_kategorie.currentText()

        self._set_dynamic_area_visible(False)
        self._clear_form_fields()

        if kategorie == "Sachbearbeiter":
            self.dialog.einst_stack.setCurrentWidget(self.dialog.page_sachbearbeiter)
            self.dialog.btn_excel_import.hide()

        elif kategorie == "Firmen":
            self.dialog.einst_stack.setCurrentWidget(self.dialog.page_firmen)
            self.dialog.btn_excel_import.hide()

        elif kategorie == "Straße":
            self.dialog.einst_stack.setCurrentWidget(self.dialog.page_text)
            self.dialog.btn_excel_import.show()

        else:
            self.dialog.einst_stack.setCurrentWidget(self.dialog.page_text)
            self.dialog.btn_excel_import.hide()

        self._set_dynamic_area_visible(True)
        self.load_list()

    def load_list(self):
        """Lädt die aktuelle Kategorieliste in das QListWidget."""
        kategorie = self.dialog.einst_kategorie.currentText()
        self.dialog.einst_liste.clear()

        werte = self.get_values(kategorie)

        for w in werte:
            if isinstance(w, dict):
                if kategorie == "Sachbearbeiter":
                    display_text = (
                        f"{w.get('nachname', '')}, {w.get('vorname', '')} "
                        f"(Tel: {w.get('telefon', '-')})"
                    )
                elif kategorie == "Firmen":
                    display_text = f"{w.get('name', '')} (Ort: {w.get('ort', '-')})"
                else:
                    display_text = json.dumps(w, ensure_ascii=False)
            else:
                display_text = str(w)

            item = QListWidgetItem(display_text)
            item.setData(
                Qt.UserRole,
                w if isinstance(w, str) else json.dumps(w, ensure_ascii=False),
            )
            self.dialog.einst_liste.addItem(item)

        if hasattr(self.dialog, "btn_add"):
            selected = self.dialog.einst_liste.currentItem()
            self.dialog.btn_add.setText(
                "Speichern (Änderungen)" if selected else "Hinzufügen"
            )

    # ==================================================================
    # LISTENEINTRÄGE: HINZUFÜGEN / IMPORT / LÖSCHEN / SPEICHERN
    # ==================================================================

    def add_item(self):
        """Alias für save_item()."""
        self.save_item()

    def _insert_into_db(self, kategorie, wert):
        """Fügt einen neuen Eintrag in die Einstellungsdatenbank ein."""
        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute(
                    "INSERT INTO untersuchungsverwaltung_einstellungen (kategorie, wert) VALUES (?, ?)",
                    (kategorie, wert),
                )
            else:
                self.dialog.cur.execute(
                    "INSERT INTO public.untersuchungsverwaltung_einstellungen (kategorie, wert) VALUES (%s, %s)",
                    (kategorie, wert),
                )

            self.dialog.conn.commit()

        except Exception as e:
            self.dialog.conn.rollback()
            QMessageBox.critical(
                self.dialog,
                "Fehler",
                f"Konnte Wert nicht speichern:\n{e}",
            )

    def import_excel(self):
        """Importiert Straßen aus einer Excel-Datei."""
        kategorie = self.dialog.einst_kategorie.currentText()
        if kategorie != "Straße":
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self.dialog,
            "Excel-Datei auswählen",
            "",
            "Excel-Dateien (*.xlsx *.xls)",
        )
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            col_name = None
            for col in df.columns:
                if str(col).strip().lower() in ("straßenname", "strassenname"):
                    col_name = col
                    break

            if not col_name:
                QMessageBox.warning(
                    self.dialog,
                    "Fehler",
                    "Konnte keine Spalte namens 'Straßenname' finden.",
                )
                return

            unique_streets = df[col_name].dropna().astype(str).str.strip().unique()
            existing_streets = set(self.get_values("Straße"))

            import_count = 0
            for street in unique_streets:
                if street and street not in existing_streets:
                    self._insert_into_db("Straße", street)
                    import_count += 1

            QMessageBox.information(
                self.dialog,
                "Erfolg",
                f"Import abgeschlossen.\n{import_count} neue Straßen hinzugefügt.",
            )
            self.load_list()

        except Exception as e:
            QMessageBox.critical(
                self.dialog,
                "Fehler beim Import",
                f"Die Excel-Datei konnte nicht verarbeitet werden:\n{e}",
            )

    def delete_item(self):
        """Löscht den aktuell markierten Eintrag aus der Einstellungsdatenbank."""
        kategorie = self.dialog.einst_kategorie.currentText()
        selected = self.dialog.einst_liste.currentItem()

        if not selected:
            return

        wert_in_db = selected.data(Qt.UserRole)

        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute(
                    """
                    DELETE FROM untersuchungsverwaltung_einstellungen
                    WHERE kategorie=? AND wert=?
                    """,
                    (kategorie, wert_in_db),
                )
            else:
                self.dialog.cur.execute(
                    """
                    DELETE FROM public.untersuchungsverwaltung_einstellungen
                    WHERE kategorie=%s AND wert=%s
                    """,
                    (kategorie, wert_in_db),
                )

            self.dialog.conn.commit()
            self.load_list()

        except Exception as e:
            self.dialog.conn.rollback()
            QMessageBox.critical(
                self.dialog,
                "Fehler",
                f"Konnte Wert nicht löschen:\n{e}",
            )

    def save_item(self):
        """Speichert einen neuen oder geänderten Listeneintrag."""
        kategorie = self.dialog.einst_kategorie.currentText()

        if kategorie == "Sachbearbeiter":
            wert_dict = {
                "vorname": self.dialog.einst_sb_vorname.text().strip(),
                "nachname": self.dialog.einst_sb_nachname.text().strip(),
                "telefon": self.dialog.einst_sb_tel.text().strip(),
                "email": self.dialog.einst_sb_mail.text().strip(),
            }

            if not wert_dict["nachname"]:
                QMessageBox.warning(
                    self.dialog,
                    "Fehler",
                    "Nachname ist Pflicht!",
                )
                return

            wert = json.dumps(wert_dict, ensure_ascii=False)

        elif kategorie == "Firmen":
            wert_dict = {
                "name": self.dialog.einst_firma_name.text().strip(),
                "plz": self.dialog.einst_firma_plz.text().strip(),
                "ort": self.dialog.einst_firma_ort.text().strip(),
                "strasse": self.dialog.einst_firma_str.text().strip(),
                "hausnummer": self.dialog.einst_firma_hnr.text().strip(),
                "telefon": self.dialog.einst_firma_tel.text().strip(),
                "email": self.dialog.einst_firma_mail.text().strip(),
            }

            if not wert_dict["name"]:
                QMessageBox.warning(
                    self.dialog,
                    "Fehler",
                    "Firmenname ist Pflicht!",
                )
                return

            wert = json.dumps(wert_dict, ensure_ascii=False)

        else:
            wert = self.dialog.einst_text_wert.text().strip()
            if not wert:
                return

        selected = self.dialog.einst_liste.currentItem()

        if selected:
            self._update_in_db(kategorie, wert, selected.data(Qt.UserRole))
        else:
            self._insert_into_db(kategorie, wert)

        self.on_kategorie_changed()

    def _update_in_db(self, kategorie, neuer_wert, alter_wert):
        """Aktualisiert einen bestehenden Datenbankeintrag."""
        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute(
                    """
                    UPDATE untersuchungsverwaltung_einstellungen
                    SET wert=?
                    WHERE kategorie=? AND wert=?
                    """,
                    (neuer_wert, kategorie, alter_wert),
                )
            else:
                self.dialog.cur.execute(
                    """
                    UPDATE public.untersuchungsverwaltung_einstellungen
                    SET wert=%s
                    WHERE kategorie=%s AND wert=%s
                    """,
                    (neuer_wert, kategorie, alter_wert),
                )

            self.dialog.conn.commit()

        except Exception as e:
            self.dialog.conn.rollback()
            QMessageBox.critical(
                self.dialog,
                "Fehler",
                f"Konnte nicht aktualisieren:\n{e}",
            )

    # ==================================================================
    # LISTENAUSWAHL / FORMULARFÜLLUNG
    # ==================================================================

    def on_list_item_clicked(self):
        """Überträgt den markierten Eintrag in die Eingabefelder."""
        kategorie = self.dialog.einst_kategorie.currentText()
        selected = self.dialog.einst_liste.currentItem()

        if not selected:
            return

        data = selected.data(Qt.UserRole)

        if isinstance(data, str) and kategorie in ("Sachbearbeiter", "Firmen"):
            try:
                data = json.loads(data)
            except Exception:
                pass

        if kategorie == "Sachbearbeiter":
            self.dialog.einst_sb_vorname.setText(data.get("vorname", ""))
            self.dialog.einst_sb_nachname.setText(data.get("nachname", ""))
            self.dialog.einst_sb_tel.setText(data.get("telefon", ""))
            self.dialog.einst_sb_mail.setText(data.get("email", ""))

        elif kategorie == "Firmen":
            self.dialog.einst_firma_name.setText(data.get("name", ""))
            self.dialog.einst_firma_plz.setText(data.get("plz", ""))
            self.dialog.einst_firma_ort.setText(data.get("ort", ""))
            self.dialog.einst_firma_str.setText(data.get("strasse", ""))
            self.dialog.einst_firma_hnr.setText(data.get("hausnummer", ""))
            self.dialog.einst_firma_tel.setText(data.get("telefon", ""))
            self.dialog.einst_firma_mail.setText(data.get("email", ""))

        else:
            self.dialog.einst_text_wert.setText(str(data))

        if hasattr(self.dialog, "btn_add"):
            self.dialog.btn_add.setText("Speichern (Änderungen)")

    # ==================================================================
    # FACHLICHE HILFSMETHODEN
    # ==================================================================

    def get_kostenstelle_for(self, kategorie, system_kuerzel):
        """
        Liest Werte z.B. im Format 'MW=12345', 'RW:4711' oder 'SW 0815'
        und gibt den rechten Teil zurück.
        """
        werte = self.get_values(kategorie)

        for eintrag in werte:
            s = str(eintrag)
            for sep in ["=", ":", " "]:
                if sep in s:
                    left, right = s.split(sep, 1)
                    if left.strip().upper() == system_kuerzel.upper():
                        return right.strip()

        return ""