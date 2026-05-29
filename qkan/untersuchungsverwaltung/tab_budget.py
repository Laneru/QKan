# untersuchungsverwaltung/tab_budget.py
import json
from qgis.PyQt.QtWidgets import (
    QMessageBox, QTableWidgetItem, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QGroupBox, QGridLayout, QLabel, QLineEdit, QComboBox
)
from qgis.PyQt.QtCore import Qt

class BudgetManager:
    """Verwaltet die Logik für den Tab 'Haushaltsmittel'"""
    
    def __init__(self, dialog):
        self.dialog = dialog
        self.current_id = None
        
    def add_budget(self):
        jahr = self.dialog.budget_jahr.currentText()
        kst = self.dialog.budget_kst.text().strip()
        sk = self.dialog.budget_sk.text().strip()
        budget_str = self.dialog.budget_betrag.text().strip().replace(',', '.')
        
        if not kst or not sk or not budget_str:
            QMessageBox.warning(self.dialog, "Fehler", "Bitte Kostenstelle, Sachkonto und Budget ausfüllen.")
            return
            
        try:
            budget = float(budget_str)
        except ValueError:
            QMessageBox.warning(self.dialog, "Fehler", "Budget muss eine Zahl sein.")
            return
            
        try:
            if self.current_id is None: # NEU
                if self.dialog.is_spatialite:
                    self.dialog.cur.execute("INSERT INTO untersuchungs_haushaltsmittel (jahr, kostenstelle, sachkonto, budget_gesamt) VALUES (?, ?, ?, ?)", (jahr, kst, sk, budget))
                else:
                    self.dialog.cur.execute("INSERT INTO public.untersuchungs_haushaltsmittel (jahr, kostenstelle, sachkonto, budget_gesamt) VALUES (%s, %s, %s, %s)", (jahr, kst, sk, budget))
            else: # UPDATE
                if self.dialog.is_spatialite:
                    self.dialog.cur.execute("UPDATE untersuchungs_haushaltsmittel SET jahr=?, kostenstelle=?, sachkonto=?, budget_gesamt=? WHERE id=?", (jahr, kst, sk, budget, self.current_id))
                else:
                    self.dialog.cur.execute("UPDATE public.untersuchungs_haushaltsmittel SET jahr=%s, kostenstelle=%s, sachkonto=%s, budget_gesamt=%s WHERE id=%s", (jahr, kst, sk, budget, self.current_id))
                    
            self.dialog.conn.commit()
            
            # Formular leeren
            self.dialog.budget_kst.clear()
            self.dialog.budget_sk.clear()
            self.dialog.budget_betrag.clear()
            self.current_id = None
            self.dialog.btn_budget_save.setText("Hinzufügen")
            
            self.refresh_budget_table()
        except Exception as e:
            self.dialog.conn.rollback()
            QMessageBox.critical(self.dialog, "Fehler", f"Konnte Budget nicht speichern (evtl. existiert Kombination bereits):\n{e}")

    def edit_budget(self, row_data):
        self.current_id = row_data[0]
        self.dialog.budget_jahr.setCurrentText(str(row_data[1]))
        self.dialog.budget_kst.setText(row_data[2])
        self.dialog.budget_sk.setText(row_data[3])
        self.dialog.budget_betrag.setText(f"{row_data[4]:.2f}")
        self.dialog.btn_budget_save.setText("Änderungen speichern")

    def delete_budget(self, record_id):
        reply = QMessageBox.question(self.dialog, "Löschen", "Budget-Eintrag wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if self.dialog.is_spatialite:
                    self.dialog.cur.execute("DELETE FROM untersuchungs_haushaltsmittel WHERE id=?", (record_id,))
                else:
                    self.dialog.cur.execute("DELETE FROM public.untersuchungs_haushaltsmittel WHERE id=%s", (record_id,))
                self.dialog.conn.commit()
                self.refresh_budget_table()
            except Exception as e:
                self.dialog.conn.rollback()
                QMessageBox.critical(self.dialog, "Fehler", f"Fehler beim Löschen:\n{e}")

    def get_kosten_fuer_kst_sk(self, kst, sk, jahr):
        """Summiert alle Kosten über abgeschlossene Aufträge im Jahr für eine bestimmte KST/SK-Kombi."""
        if not self.dialog.cur:
            return 0.0

        summe = 0.0
        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute("""
                    SELECT
                        details_rw, details_sw, details_mw,
                        ist_kosten_rw, ist_kosten_sw, ist_kosten_mw,
                        modus,
                        k_rw_reinigung, k_rw_tv, k_rw_gal,
                        k_sw_reinigung, k_sw_tv, k_sw_gal,
                        k_mw_reinigung, k_mw_tv, k_mw_gal
                    FROM untersuchungsauftraege
                    WHERE status = 'Abgeschlossen'
                    AND abschlussdatum LIKE ?
                """, (f"{jahr}-%",))
            else:
                self.dialog.cur.execute("""
                    SELECT
                        details_rw, details_sw, details_mw,
                        ist_kosten_rw, ist_kosten_sw, ist_kosten_mw,
                        modus,
                        k_rw_reinigung, k_rw_tv, k_rw_gal,
                        k_sw_reinigung, k_sw_tv, k_sw_gal,
                        k_mw_reinigung, k_mw_tv, k_mw_gal
                    FROM public.untersuchungsauftraege
                    WHERE status = 'Abgeschlossen'
                    AND EXTRACT(YEAR FROM abschlussdatum) = %s
                """, (jahr,))

            auftraege = self.dialog.cur.fetchall()

            for a in auftraege:
                (det_rw, det_sw, det_mw,
                ist_rw, ist_sw, ist_mw,
                modus,
                k_rw_rein, k_rw_tv, k_rw_gal,
                k_sw_rein, k_sw_tv, k_sw_gal,
                k_mw_rein, k_mw_tv, k_mw_gal) = a

                # Hilfsfunktion: JSON parsen sicher
                def _parse(json_str):
                    if not json_str:
                        return {}
                    try:
                        return json.loads(json_str)
                    except Exception:
                        return {}

                d_rw = _parse(det_rw)
                d_sw = _parse(det_sw)
                d_mw = _parse(det_mw)

                # 1) Projektmodus: Ist-Kosten je System, wenn Projekt-KST/SK passen
                if modus == "Projekt":
                    # RW
                    if d_rw.get('kst_projekt') == kst and d_rw.get('sk_projekt') == sk:
                        summe += float(ist_rw or 0)
                    # SW
                    if d_sw.get('kst_projekt') == kst and d_sw.get('sk_projekt') == sk:
                        summe += float(ist_sw or 0)
                    # MW
                    if d_mw.get('kst_projekt') == kst and d_mw.get('sk_projekt') == sk:
                        summe += float(ist_mw or 0)

                # 2) Normalmodus: Kosten je System/Art, wenn Normal-KST/SK passen
                # RW
                if d_rw.get('kst_reinigung') == kst and d_rw.get('sk_normal') == sk:
                    summe += float(k_rw_rein or 0)
                if d_rw.get('kst_tv') == kst and d_rw.get('sk_normal') == sk:
                    summe += float(k_rw_tv or 0)
                if d_rw.get('kst_gal') == kst and d_rw.get('sk_normal') == sk:
                    summe += float(k_rw_gal or 0)

                # SW
                if d_sw.get('kst_reinigung') == kst and d_sw.get('sk_normal') == sk:
                    summe += float(k_sw_rein or 0)
                if d_sw.get('kst_tv') == kst and d_sw.get('sk_normal') == sk:
                    summe += float(k_sw_tv or 0)
                if d_sw.get('kst_gal') == kst and d_sw.get('sk_normal') == sk:
                    summe += float(k_sw_gal or 0)

                # MW
                if d_mw.get('kst_reinigung') == kst and d_mw.get('sk_normal') == sk:
                    summe += float(k_mw_rein or 0)
                if d_mw.get('kst_tv') == kst and d_mw.get('sk_normal') == sk:
                    summe += float(k_mw_tv or 0)
                if d_mw.get('kst_gal') == kst and d_mw.get('sk_normal') == sk:
                    summe += float(k_mw_gal or 0)

            return summe
        except Exception as e:
            self.dialog.conn.rollback()
            print("[BUDGET-ERROR]", e)
            return 0.0


    def refresh_budget_table(self):
        if not self.dialog.cur: return
        try:
            selected_jahr = self.dialog.budget_jahr_filter.currentText()
            
            if self.dialog.is_spatialite:
                self.dialog.cur.execute("SELECT id, jahr, kostenstelle, sachkonto, budget_gesamt FROM untersuchungs_haushaltsmittel WHERE jahr=? ORDER BY kostenstelle, sachkonto", (selected_jahr,))
            else:
                self.dialog.cur.execute("SELECT id, jahr, kostenstelle, sachkonto, budget_gesamt FROM public.untersuchungs_haushaltsmittel WHERE jahr=%s ORDER BY kostenstelle, sachkonto", (selected_jahr,))
            
            rows = self.dialog.cur.fetchall()
            self.dialog.budget_table.setRowCount(len(rows))
            
            for row_idx, row_data in enumerate(rows):
                kst = row_data[2]
                sk = row_data[3]
                budget = float(row_data[4])
                
                # IST-Kosten berechnen (nur abgeschlossene Aufträge!)
                ist_kosten = self.get_kosten_fuer_kst_sk(kst, sk, selected_jahr)
                rest = budget - ist_kosten
                
                self.dialog.budget_table.setItem(row_idx, 0, QTableWidgetItem(kst))
                self.dialog.budget_table.setItem(row_idx, 1, QTableWidgetItem(sk))
                self.dialog.budget_table.setItem(row_idx, 2, QTableWidgetItem(f"{budget:.2f} €"))
                self.dialog.budget_table.setItem(row_idx, 3, QTableWidgetItem(f"{ist_kosten:.2f} €"))
                
                item_rest = QTableWidgetItem(f"{rest:.2f} €")
                # Farblich markieren, wenn Budget überschritten
                if rest < 0:
                    item_rest.setForeground(Qt.red)
                elif rest < (budget * 0.1): # Warnung wenn < 10%
                    item_rest.setForeground(Qt.darkYellow)
                    
                self.dialog.budget_table.setItem(row_idx, 4, item_rest)
                
                btn_widget = QWidget()
                l = QHBoxLayout(btn_widget)
                l.setContentsMargins(0,0,0,0)
                btn_edit = QPushButton("Bearbeiten")
                btn_del = QPushButton("Löschen")
                btn_edit.clicked.connect(lambda chk, d=row_data: self.edit_budget(d))
                btn_del.clicked.connect(lambda chk, id=row_data[0]: self.delete_budget(id))
                l.addWidget(btn_edit)
                l.addWidget(btn_del)
                self.dialog.budget_table.setCellWidget(row_idx, 5, btn_widget)
                
        except Exception as e:
            self.dialog.conn.rollback()
            print("Ladefehler Budget:", e)
