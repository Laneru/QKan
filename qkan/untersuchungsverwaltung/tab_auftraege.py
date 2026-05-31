# untersuchungsverwaltung/tab_auftraege.py
import os
import shutil
import datetime
from qgis.PyQt.QtWidgets import (
    QMessageBox, QTableWidgetItem, QPushButton, QDialog, QVBoxLayout, 
    QFormLayout, QLineEdit, QComboBox, QCheckBox, QDateEdit, QHBoxLayout, 
    QTextEdit, QFileDialog, QGroupBox, QDialogButtonBox, QScrollArea, QWidget, QLabel
)
from qgis.PyQt.QtCore import QDate, Qt, QUrl, QSizeF
from qgis.PyQt.QtGui import QDesktopServices, QTextDocument
from qgis.PyQt.QtPrintSupport import QPrinter
import json

# Spaltenindizes der Tabelle untersuchungsauftraege (0‑basiert,
# passend zur CREATE TABLE-Reihenfolge in ensure_table_exists)
IDX_ID             = 0
IDX_PROJEKTNAME    = 1
IDX_STRASSE        = 2
IDX_ABSCHNITT      = 3
IDX_SACHBEARBEITER = 4
IDX_TELEFON        = 5
IDX_EMAIL          = 6
IDX_BEAUFTRAGT_AM  = 7
IDX_IB_BETEILIGUNG = 8
IDX_TYP_RW         = 9
IDX_TYP_SW         = 10
IDX_TYP_MW         = 11
IDX_DATEI          = 12
IDX_ZIELDATUM      = 13
IDX_GRUND          = 14
IDX_BEMERKUNG      = 15
IDX_IB_DATEN       = 16
IDX_DETAILS_RW     = 17
IDX_DETAILS_SW     = 18
IDX_DETAILS_MW     = 19
IDX_FIRMA          = 20
IDX_FIRMA_TEL      = 21
IDX_FIRMA_MAIL     = 22
IDX_STATUS         = 23
IDX_ABSCHLUSSDATUM = 24
IDX_MODUS          = 25
IDX_IST_RW         = 26   # ist_kosten_rw
IDX_IST_SW         = 27   # ist_kosten_sw
IDX_IST_MW         = 28   # ist_kosten_mw
IDX_K_RW_REIN      = 29
IDX_K_RW_TV        = 30
IDX_K_RW_GAL       = 31
IDX_K_SW_REIN      = 32
IDX_K_SW_TV        = 33
IDX_K_SW_GAL       = 34
IDX_K_MW_REIN      = 35
IDX_K_MW_TV        = 36
IDX_K_MW_GAL       = 37

class AuftragDialog(QDialog):
    """Das Popup-Fenster zum Anlegen und Bearbeiten eines Auftrags"""
    def __init__(self, parent, einstellungen_manager, row_data=None):
        super().__init__(parent)
        self.setWindowTitle("Auftrag bearbeiten" if row_data else "Neuer Auftrag")
        self.resize(700, 800)
        self.einstellungen = einstellungen_manager

        # --- Hilfsfunktion für sichere Float-Konvertierung ---
        def _safe_float(val):
            """
            Versucht, val in float zu wandeln.
            Bei None oder nicht-numerischem Inhalt wird 0.0 zurückgegeben.
            Akzeptiert auch Strings mit Komma als Dezimaltrennzeichen.
            """
            if val is None:
                return 0.0
            try:
                if isinstance(val, str):
                    val = val.strip().replace(",", ".")
                    if not val:
                        return 0.0
                return float(val)
            except (TypeError, ValueError):
                return 0.0

        # Hauptlayout mit Scroll-Bereich (damit das Fenster nicht aus dem Bildschirm ragt)
        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # --- Sachdaten ---
        group_sach = QGroupBox("Sachdaten")
        form_sach = QFormLayout()

        self.f_modus = QComboBox()
        self.f_modus.addItems(["Projekt", "Normale TV-Untersuchung"])
        form_sach.addRow("Art des Auftrags:", self.f_modus)

        self.f_projekt = QLineEdit()
        self.f_strasse = QComboBox()
        self.f_strasse.addItems(self.einstellungen.get_simple_list("Straße"))
        self.f_abschnitt = QLineEdit()
        self.f_bearbeiter = QComboBox()
        self.f_bearbeiter.addItems(self.einstellungen.get_simple_list("Sachbearbeiter"))
        self.f_bearbeiter.currentTextChanged.connect(self.on_sachbearbeiter_changed)

        self.f_telefon = QLineEdit()
        self.f_email = QLineEdit()

        # --- Firmen-Auswahl ---
        self.f_firma = QComboBox()
        self.f_firma.addItems(self.einstellungen.get_simple_list("Firmen"))

        from qgis.PyQt.QtCore import QTimer
        self.f_firma_timer = QTimer()
        self.f_firma_timer.setSingleShot(True)
        self.f_firma_timer.setInterval(300)
        self.f_firma_timer.timeout.connect(self.delayed_firma_fill)
        self.f_firma.currentTextChanged.connect(self.on_firma_timer)

        self.f_firma_tel = QLineEdit()
        self.f_firma_mail = QLineEdit()

        self.f_beauftragt = QDateEdit(QDate.currentDate())
        self.f_beauftragt.setCalendarPopup(True)
        self.f_ib = QCheckBox("Beteiligung Ingenieurbüro")

        form_sach.addRow("Projektname:", self.f_projekt)
        form_sach.addRow("Straße:", self.f_strasse)
        form_sach.addRow("Abschnitt:", self.f_abschnitt)
        form_sach.addRow("Sachbearbeiter:", self.f_bearbeiter)
        form_sach.addRow("Telefon:", self.f_telefon)
        form_sach.addRow("E-Mail:", self.f_email)
        form_sach.addRow("Beauftragte Firma:", self.f_firma)
        form_sach.addRow("Firma Telefon:", self.f_firma_tel)
        form_sach.addRow("Firma E-Mail:", self.f_firma_mail)
        form_sach.addRow("Beauftragt am:", self.f_beauftragt)
        form_sach.addRow("", self.f_ib)
        group_sach.setLayout(form_sach)
        layout.addWidget(group_sach)

        # --- DYNAMISCH: Ingenieurbüro Details ---
        self.group_ib_details = QGroupBox("Details Ingenieurbüro")
        form_ib = QFormLayout()

        form_ib.addRow(QLabel("<b>Bürodaten:</b>"))
        self.f_ib_name = QLineEdit()
        self.f_ib_staat = QLineEdit()
        self.f_ib_plz = QLineEdit()
        self.f_ib_ort = QLineEdit()
        self.f_ib_str = QLineEdit()
        self.f_ib_hnr = QLineEdit()
        form_ib.addRow("Name des Büros:", self.f_ib_name)
        form_ib.addRow("Staat:", self.f_ib_staat)
        form_ib.addRow("PLZ:", self.f_ib_plz)
        form_ib.addRow("Ort:", self.f_ib_ort)
        form_ib.addRow("Straße:", self.f_ib_str)
        form_ib.addRow("Hausnummer:", self.f_ib_hnr)

        form_ib.addRow(QLabel("<b>Verantwortliche Bauleitung:</b>"))
        self.f_ib_vname = QLineEdit()
        self.f_ib_nname = QLineEdit()
        self.f_ib_mobil = QLineEdit()
        self.f_ib_mail = QLineEdit()
        form_ib.addRow("Vorname:", self.f_ib_vname)
        form_ib.addRow("Nachname:", self.f_ib_nname)
        form_ib.addRow("Mobilfunknummer:", self.f_ib_mobil)
        form_ib.addRow("E-Mail:", self.f_ib_mail)

        self.group_ib_details.setLayout(form_ib)
        self.group_ib_details.setVisible(False)
        self.f_ib.toggled.connect(self.group_ib_details.setVisible)
        layout.addWidget(self.group_ib_details)

        # --- Untersuchungsdaten ---
        group_unt = QGroupBox("Untersuchungsdaten")
        form_unt = QFormLayout()

        h_kanaltyp = QHBoxLayout()
        self.f_typ_rw = QCheckBox("RW")
        self.f_typ_sw = QCheckBox("SW")
        self.f_typ_mw = QCheckBox("MW")
        h_kanaltyp.addWidget(self.f_typ_rw)
        h_kanaltyp.addWidget(self.f_typ_sw)
        h_kanaltyp.addWidget(self.f_typ_mw)
        form_unt.addRow("Kanaltyp:", h_kanaltyp)

        h_datei = QHBoxLayout()
        self.f_datei = QLineEdit()
        self.f_datei.setReadOnly(True)
        btn_datei = QPushButton("...")
        btn_datei.setFixedWidth(40)
        btn_datei.clicked.connect(self.select_file)
        btn_open = QPushButton("Öffnen")
        btn_open.setFixedWidth(60)
        btn_open.clicked.connect(self.open_file)
        h_datei.addWidget(self.f_datei)
        h_datei.addWidget(btn_datei)
        h_datei.addWidget(btn_open)
        form_unt.addRow("Umfang (Datei):", h_datei)

        self.f_zieldatum = QDateEdit(QDate.currentDate().addDays(14))
        self.f_zieldatum.setCalendarPopup(True)
        self.f_grund = QComboBox()
        self.f_grund.addItems(self.einstellungen.get_simple_list("Grund der Untersuchung"))
        self.f_bemerkung = QTextEdit()
        self.f_bemerkung.setFixedHeight(60)

        form_unt.addRow("Zieldatum:", self.f_zieldatum)
        form_unt.addRow("Grund:", self.f_grund)
        form_unt.addRow("Bemerkung:", self.f_bemerkung)
        group_unt.setLayout(form_unt)
        layout.addWidget(group_unt)

        # --- DYNAMISCH: Details für RW, SW, MW ---
        self.group_rw, self.w_rw = self.create_typ_details_widget("Regenwasser (RW)")
        self.group_sw, self.w_sw = self.create_typ_details_widget("Schmutzwasser (SW)")
        self.group_mw, self.w_mw = self.create_typ_details_widget("Mischwasser (MW)")

        layout.addWidget(self.group_rw)
        layout.addWidget(self.group_sw)
        layout.addWidget(self.group_mw)

        def handle_system_toggle(system, group, widgets, checked):
            group.setVisible(checked)
            print(f"[CHECKBOX-DEBUG] System {system} toggled: checked={checked}, modus={self.f_modus.currentText()!r}")
            if checked and self.f_modus.currentText() == "Normale TV-Untersuchung":
                print(f"[CHECKBOX-DEBUG] -> fill_kst_for_system({system}) wird aufgerufen")
                self.fill_kst_for_system(system, widgets)

        self.f_typ_rw.toggled.connect(
            lambda chk, s="RW", g=self.group_rw, w=self.w_rw: handle_system_toggle(s, g, w, chk)
        )
        self.f_typ_sw.toggled.connect(
            lambda chk, s="SW", g=self.group_sw, w=self.w_sw: handle_system_toggle(s, g, w, chk)
        )
        self.f_typ_mw.toggled.connect(
            lambda chk, s="MW", g=self.group_mw, w=self.w_mw: handle_system_toggle(s, g, w, chk)
        )

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # --- Abschluss & Kosten ---
        group_abschluss = QGroupBox("Abschluss & Kosten")
        form_abschluss = QFormLayout()

        self.f_status = QComboBox()
        self.f_status.addItems(["In Bearbeitung", "Pausiert", "Abgeschlossen", "Storniert"])

        self.f_abschlussdatum = QDateEdit(QDate.currentDate())
        self.f_abschlussdatum.setCalendarPopup(True)
        self.f_abschlussdatum.setEnabled(False)

        form_abschluss.addRow("Status:", self.f_status)
        form_abschluss.addRow("Abschlussdatum:", self.f_abschlussdatum)

        self.lbl_projekt_kosten = QLabel("<b>Tatsächliche Kosten (Projekt):</b>")
        form_abschluss.addRow(self.lbl_projekt_kosten)

        self.lbl_ist_rw = QLabel("Regenwasser (€):")
        self.lbl_ist_sw = QLabel("Schmutzwasser (€):")
        self.lbl_ist_mw = QLabel("Mischwasser (€):")

        self.f_ist_rw = QLineEdit("0.00")
        self.f_ist_sw = QLineEdit("0.00")
        self.f_ist_mw = QLineEdit("0.00")

        form_abschluss.addRow(self.lbl_ist_rw, self.f_ist_rw)
        form_abschluss.addRow(self.lbl_ist_sw, self.f_ist_sw)
        form_abschluss.addRow(self.lbl_ist_mw, self.f_ist_mw)

        self.lbl_normale_kosten = QLabel("<b>Normale Untersuchung – Kosten je System und Art:</b>")
        form_abschluss.addRow(self.lbl_normale_kosten)

        self.lbl_norm_rw = QLabel("RW Reinigung / TV / GAL/HAL:")
        self.lbl_norm_sw = QLabel("SW Reinigung / TV / GAL/HAL:")
        self.lbl_norm_mw = QLabel("MW Reinigung / TV / GAL/HAL:")

        self.k_rw_reinigung = QLineEdit("0.00")
        self.k_rw_tv        = QLineEdit("0.00")
        self.k_rw_gal       = QLineEdit("0.00")
        self.k_sw_reinigung = QLineEdit("0.00")
        self.k_sw_tv        = QLineEdit("0.00")
        self.k_sw_gal       = QLineEdit("0.00")
        self.k_mw_reinigung = QLineEdit("0.00")
        self.k_mw_tv        = QLineEdit("0.00")
        self.k_mw_gal       = QLineEdit("0.00")

        form_abschluss.addRow(
            self.lbl_norm_rw,
            self._h_triple(self.k_rw_reinigung, self.k_rw_tv, self.k_rw_gal)
        )
        form_abschluss.addRow(
            self.lbl_norm_sw,
            self._h_triple(self.k_sw_reinigung, self.k_sw_tv, self.k_sw_gal)
        )
        form_abschluss.addRow(
            self.lbl_norm_mw,
            self._h_triple(self.k_mw_reinigung, self.k_mw_tv, self.k_mw_gal)
        )

        self.f_status.currentTextChanged.connect(
            lambda text: self.f_abschlussdatum.setEnabled(text == "Abgeschlossen")
        )

        group_abschluss.setLayout(form_abschluss)
        layout.addWidget(group_abschluss)

        self.f_modus.currentTextChanged.connect(self.on_modus_changed)
        self.on_modus_changed(self.f_modus.currentText())

        self.buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        main_layout.addWidget(self.buttons)

        # --- Vorbefüllen (Bearbeiten-Modus) ---
        if row_data:
            self.f_projekt.setText(row_data[IDX_PROJEKTNAME] or "")
            self.f_strasse.setCurrentText(row_data[IDX_STRASSE] or "")
            self.f_abschnitt.setText(row_data[IDX_ABSCHNITT] or "")
            self.f_bearbeiter.setCurrentText(row_data[IDX_SACHBEARBEITER] or "")
            self.f_telefon.setText(row_data[IDX_TELEFON] or "")
            self.f_email.setText(row_data[IDX_EMAIL] or "")

            if row_data[IDX_BEAUFTRAGT_AM]:
                self.f_beauftragt.setDate(
                    QDate.fromString(str(row_data[IDX_BEAUFTRAGT_AM]), "yyyy-MM-dd")
                )

            self.f_ib.setChecked(bool(row_data[IDX_IB_BETEILIGUNG]))
            self.f_typ_rw.setChecked(bool(row_data[IDX_TYP_RW]))
            self.f_typ_sw.setChecked(bool(row_data[IDX_TYP_SW]))
            self.f_typ_mw.setChecked(bool(row_data[IDX_TYP_MW]))

            self.f_datei.setText(row_data[IDX_DATEI] or "")
            if row_data[IDX_ZIELDATUM]:
                self.f_zieldatum.setDate(
                    QDate.fromString(str(row_data[IDX_ZIELDATUM]), "yyyy-MM-dd")
                )
            self.f_grund.setCurrentText(row_data[IDX_GRUND] or "")
            self.f_bemerkung.setPlainText(row_data[IDX_BEMERKUNG] or "")

            self.load_ib_data(row_data[IDX_IB_DATEN])
            self.load_typ_data(self.w_rw, row_data[IDX_DETAILS_RW])
            self.load_typ_data(self.w_sw, row_data[IDX_DETAILS_SW])
            self.load_typ_data(self.w_mw, row_data[IDX_DETAILS_MW])

            firma_name = row_data[IDX_FIRMA] or ""
            idx = self.f_firma.findText(firma_name)
            if idx >= 0:
                self.f_firma.setCurrentIndex(idx)
            else:
                self.f_firma.setCurrentText(firma_name)

            self.f_firma_tel.setText(row_data[IDX_FIRMA_TEL] or "")
            self.f_firma_mail.setText(row_data[IDX_FIRMA_MAIL] or "")

            if row_data[IDX_STATUS]:
                status_idx = self.f_status.findText(str(row_data[IDX_STATUS]))
                if status_idx >= 0:
                    self.f_status.setCurrentIndex(status_idx)

            if row_data[IDX_ABSCHLUSSDATUM]:
                self.f_abschlussdatum.setDate(
                    QDate.fromString(str(row_data[IDX_ABSCHLUSSDATUM]), "yyyy-MM-dd")
                )

            if row_data[IDX_MODUS]:
                modus_str = str(row_data[IDX_MODUS])
                idx = self.f_modus.findText(modus_str)
                if idx >= 0:
                    self.f_modus.setCurrentIndex(idx)

            # --- robustes Vorbefüllen der Ist-Kosten ---
            if len(row_data) > IDX_IST_RW and row_data[IDX_IST_RW] is not None:
                self.f_ist_rw.setText(f"{_safe_float(row_data[IDX_IST_RW]):.2f}")
            if len(row_data) > IDX_IST_SW and row_data[IDX_IST_SW] is not None:
                self.f_ist_sw.setText(f"{_safe_float(row_data[IDX_IST_SW]):.2f}")
            if len(row_data) > IDX_IST_MW and row_data[IDX_IST_MW] is not None:
                self.f_ist_mw.setText(f"{_safe_float(row_data[IDX_IST_MW]):.2f}")

            # Normal-Kosten RW
            if len(row_data) > IDX_K_RW_REIN and row_data[IDX_K_RW_REIN] is not None:
                self.k_rw_reinigung.setText(f"{_safe_float(row_data[IDX_K_RW_REIN]):.2f}")
            if len(row_data) > IDX_K_RW_TV and row_data[IDX_K_RW_TV] is not None:
                self.k_rw_tv.setText(f"{_safe_float(row_data[IDX_K_RW_TV]):.2f}")
            if len(row_data) > IDX_K_RW_GAL and row_data[IDX_K_RW_GAL] is not None:
                self.k_rw_gal.setText(f"{_safe_float(row_data[IDX_K_RW_GAL]):.2f}")

            # Normal-Kosten SW
            if len(row_data) > IDX_K_SW_REIN and row_data[IDX_K_SW_REIN] is not None:
                self.k_sw_reinigung.setText(f"{_safe_float(row_data[IDX_K_SW_REIN]):.2f}")
            if len(row_data) > IDX_K_SW_TV and row_data[IDX_K_SW_TV] is not None:
                self.k_sw_tv.setText(f"{_safe_float(row_data[IDX_K_SW_TV]):.2f}")
            if len(row_data) > IDX_K_SW_GAL and row_data[IDX_K_SW_GAL] is not None:
                self.k_sw_gal.setText(f"{_safe_float(row_data[IDX_K_SW_GAL]):.2f}")

            # Normal-Kosten MW
            if len(row_data) > IDX_K_MW_REIN and row_data[IDX_K_MW_REIN] is not None:
                self.k_mw_reinigung.setText(f"{_safe_float(row_data[IDX_K_MW_REIN]):.2f}")
            if len(row_data) > IDX_K_MW_TV and row_data[IDX_K_MW_TV] is not None:
                self.k_mw_tv.setText(f"{_safe_float(row_data[IDX_K_MW_TV]):.2f}")
            if len(row_data) > IDX_K_MW_GAL and row_data[IDX_K_MW_GAL] is not None:
                self.k_mw_gal.setText(f"{_safe_float(row_data[IDX_K_MW_GAL]):.2f}")

    def _h_pair(self, w1, w2):
        l = QHBoxLayout()
        container = QWidget()
        l.addWidget(w1)
        l.addWidget(w2)
        l.setContentsMargins(0, 0, 0, 0)
        container.setLayout(l)
        return container

    def _h_triple(self, w1, w2, w3):
        l = QHBoxLayout()
        container = QWidget()
        l.addWidget(w1)
        l.addWidget(w2)
        l.addWidget(w3)
        l.setContentsMargins(0, 0, 0, 0)
        container.setLayout(l)
        return container

    def on_modus_changed(self, text):
        is_projekt = (text == "Projekt")

        # 1) Abschlussblock

        # Projekt-Istkosten (Label + QLineEdit) – nur bei Projekt sichtbar
        for lbl, edit in [
            (self.lbl_ist_rw, self.f_ist_rw),
            (self.lbl_ist_sw, self.f_ist_sw),
            (self.lbl_ist_mw, self.f_ist_mw),
        ]:
            lbl.setVisible(is_projekt)
            edit.setVisible(is_projekt)
        self.lbl_projekt_kosten.setVisible(is_projekt)

        # Normal-Kosten (Label + QLineEdit) – nur bei Normal sichtbar
        self.lbl_normale_kosten.setVisible(not is_projekt)
        for lbl, edits in [
            (self.lbl_norm_rw, [self.k_rw_reinigung, self.k_rw_tv, self.k_rw_gal]),
            (self.lbl_norm_sw, [self.k_sw_reinigung, self.k_sw_tv, self.k_sw_gal]),
            (self.lbl_norm_mw, [self.k_mw_reinigung, self.k_mw_tv, self.k_mw_gal]),
        ]:
            lbl.setVisible(not is_projekt)
            for e in edits:
                e.setVisible(not is_projekt)

        # 2) Detail-Tabs: NUR Sichtbarkeit der KST/SK-Felder umschalten
        for system, widgets, chk in [
            ("RW", self.w_rw, self.f_typ_rw.isChecked()),
            ("SW", self.w_sw, self.f_typ_sw.isChecked()),
            ("MW", self.w_mw, self.f_typ_mw.isChecked()),
        ]:
            # KST/SK-Label+Felder im Tab je nach Modus zeigen/verstecken
            self.set_kst_sk_visibility(widgets, is_projekt)
            # KEIN fill_kst_for_system() mehr hier!


    def fill_kst_for_system(self, system, widgets):
        """Füllt im Normalmodus die KST/SK-Felder eines Systems aus den Einstellungen."""

        # Rohwerte aus Einstellungen holen
        kst_rein = self.get_kst_for("KST_Reinigung", system)
        kst_tv   = self.get_kst_for("KST_TV", system)
        kst_gal  = self.get_kst_for("KST_GAL", system)
        sk       = self.einstellungen.get_single_value(f"SK_Normal_{system}")

        print(f"[KST-DEBUG] System {system}:")
        print(f"  Einstellungen -> Reinigung: {kst_rein!r}, TV: {kst_tv!r}, GAL/HAL: {kst_gal!r}, SK: {sk!r}")

        # Vorherige Inhalte der Felder auslesen (um zu sehen, ob wirklich leer)
        prev_rein = widgets['kst_reinigung'].text()
        prev_tv   = widgets['kst_tv'].text()
        prev_gal  = widgets['kst_gal'].text()
        prev_sk   = widgets['sk_normal'].text()

        print(f"  Vorher in QLineEdit:")
        print(f"    kst_reinigung: {prev_rein!r}")
        print(f"    kst_tv:        {prev_tv!r}")
        print(f"    kst_gal:       {prev_gal!r}")
        print(f"    sk_normal:     {prev_sk!r}")

        # Nur setzen, wenn das Feld noch leer ist (deine bisherige Logik)
        if not prev_rein:
            widgets['kst_reinigung'].setText(kst_rein)
            print(f"  -> kst_reinigung gesetzt auf {kst_rein!r} (aus Einstellungen)")
        else:
            print(f"  -> kst_reinigung NICHT gesetzt (bereits Wert vorhanden)")

        if not prev_tv:
            widgets['kst_tv'].setText(kst_tv)
            print(f"  -> kst_tv gesetzt auf {kst_tv!r} (aus Einstellungen)")
        else:
            print(f"  -> kst_tv NICHT gesetzt (bereits Wert vorhanden)")

        if not prev_gal:
            widgets['kst_gal'].setText(kst_gal)
            print(f"  -> kst_gal gesetzt auf {kst_gal!r} (aus Einstellungen)")
        else:
            print(f"  -> kst_gal NICHT gesetzt (bereits Wert vorhanden)")

        if not prev_sk:
            widgets['sk_normal'].setText(sk)
            print(f"  -> sk_normal gesetzt auf {sk!r} (aus Einstellungen)")
        else:
            print(f"  -> sk_normal NICHT gesetzt (bereits Wert vorhanden)")

        print("-" * 60)


    def get_kst_for(self, kategorie, system_kuerzel):
        """
        Liefert die Kostenstelle für RW/SW/MW aus den Einstellungen.

        Fall A: Einträge im Format 'RW=4711', 'SW=4722', ...
                -> rechte Seite passend zum Kürzel zurückgeben.
        Fall B: Einträge sind nur Zahlen ('4711', '4722', '4733') in fester Reihenfolge
                (RW, SW, MW) -> indexbasiert zuordnen.
        Fall C: Nur ein Wert vorhanden -> gleicher Wert für alle Systeme.
        """
        werte = self.einstellungen.get_values(kategorie)
        print(f"[KST-GET] Kategorie={kategorie!r}, System={system_kuerzel!r}, Werte={werte!r}")

        if not werte:
            return ""

        index_map = {"RW": 0, "SW": 1, "MW": 2}
        idx = index_map.get(system_kuerzel.upper(), 0)

        # 1) benannte Einträge RW=..., SW=..., MW=...
        for eintrag in werte:
            s = str(eintrag)
            for sep in ("=", ":", " "):
                if sep in s:
                    left, right = s.split(sep, 1)
                    if left.strip().upper() == system_kuerzel.upper():
                        val = right.strip()
                        print(f"[KST-GET] -> benannter Eintrag: {s!r} -> {val!r}")
                        return val

        # 2) Fallback: reine Zahlenliste in fester Reihenfolge (RW, SW, MW)
        if 0 <= idx < len(werte):
            val = str(werte[idx]).strip()
            print(f"[KST-GET] -> indexbasierter Eintrag: werte[{idx}]={werte[idx]!r} -> {val!r}")
            return val

        # 3) zusätzlicher Fallback: nur EIN Wert -> gleicher Wert für alle Systeme
        if len(werte) == 1:
            val = str(werte[0]).strip()
            print(f"[KST-GET] -> globaler Eintrag (1 Wert): {werte[0]!r} -> {val!r}")
            return val

        print("[KST-GET] -> kein passender Eintrag gefunden")
        return ""

    def configure_system_widgets(self, w, system_kuerzel, is_projekt):
        """
        Passt die Sichtbarkeit/Felder je System (RW/SW/MW) an den Modus an
        und setzt bei 'Normal' automatisch die Kostenstellen aus den Einstellungen.
        """
        # Modus: Projekt -> nur 'preis_projekt' zeigen, die drei o.g. Normal-Preise ausblenden
        w['preis_projekt'].setVisible(is_projekt)
        w['preis_reinigung'].setVisible(not is_projekt)
        w['preis_tv'].setVisible(not is_projekt)
        w['preis_galhal'].setVisible(not is_projekt)
        
        # Bei normaler TV-Untersuchung: Kostenstellen automatisch setzen
        if not is_projekt:
            # RW/SW/MW-Kürzel verwenden
            kst_tv = self.einstellungen.get_kostenstelle_for("KST_TV", system_kuerzel)
            kst_rein = self.einstellungen.get_kostenstelle_for("KST_Reinigung", system_kuerzel)
            kst_gal = self.einstellungen.get_kostenstelle_for("KST_GALHAL", system_kuerzel)
            
            # Einfach: die TV-Kostenstelle in das KST-Feld schreiben, der Rest wird für die Berechnung genutzt
            # (oder du legst separate KST-Felder an, wenn du das granular in der DB haben willst)
            w['kst'].setText(kst_tv or w['kst'].text())
        # Bei Projekt: KST/SK manuell vom Nutzer eingeben


    def create_typ_details_widget(self, title):
        """Erzeugt dynamisch den Block für RW, SW oder MW"""
        group = QGroupBox(f"Untersuchungs-Details {title}")
        layout = QFormLayout()
        
        w = {}  # Dictionary für alle Felder
        
        # --- Untersuchungsarten ---
        w['norm'] = QCheckBox("Normale Kanal-TV-Untersuchung")
        w['pano'] = QCheckBox("Kanal-TV mit 3D Kugelbildscanner (Panoramo)")
        w['si']   = QCheckBox("Schachtinspektion (Panoramo SI)")
        w['gal']  = QCheckBox("GAL-Untersuchung mit Ortung/Aufmaß")
        w['hal']  = QCheckBox("HAL-Untersuchung mit Ortung/Aufmaß")
        
        for key in ['norm', 'pano', 'si', 'gal', 'hal']:
            layout.addRow("", w[key])
        
        # --- Dynamische Längen-/Anzahl-Felder ---
        w['laenge_tv'] = QLineEdit()
        w['laenge_tv'].setPlaceholderText("Haltungslänge in Metern")
        w['laenge_tv'].setVisible(False)
        layout.addRow("Haltungslänge (TV/Panoramo):", w['laenge_tv'])
        
        w['anzahl_si'] = QLineEdit()
        w['anzahl_si'].setPlaceholderText("Anzahl Schächte")
        w['anzahl_si'].setVisible(False)
        layout.addRow("Anzahl Schächte (Panoramo SI):", w['anzahl_si'])
        
        w['anzahl_gal'] = QLineEdit()
        w['anzahl_gal'].setPlaceholderText("Anzahl GAL")
        w['anzahl_gal'].setVisible(False)
        layout.addRow("Anzahl GAL:", w['anzahl_gal'])
        
        w['anzahl_hal'] = QLineEdit()
        w['anzahl_hal'].setPlaceholderText("Anzahl HAL")
        w['anzahl_hal'].setVisible(False)
        layout.addRow("Anzahl HAL:", w['anzahl_hal'])
        
        # --- KST/SK-Felder: getrennt nach Projekt / Normal ---

        # Projekt: eine KST/SK pro System
        w['lbl_kst_projekt'] = QLabel("Kostenstelle (Projekt):")
        w['kst_projekt'] = QLineEdit()
        layout.addRow(w['lbl_kst_projekt'], w['kst_projekt'])

        w['lbl_sk_projekt'] = QLabel("Sachkonto (Projekt):")
        w['sk_projekt'] = QLineEdit()
        layout.addRow(w['lbl_sk_projekt'], w['sk_projekt'])

        # Normale Untersuchung: 3 KST (Reinigung/TV/GAL) + 1 SK
        w['lbl_kst_reinigung'] = QLabel("KST Reinigung:")
        w['kst_reinigung'] = QLineEdit()
        layout.addRow(w['lbl_kst_reinigung'], w['kst_reinigung'])

        w['lbl_kst_tv'] = QLabel("KST TV/Panoramo/SI:")
        w['kst_tv'] = QLineEdit()
        layout.addRow(w['lbl_kst_tv'], w['kst_tv'])

        w['lbl_kst_gal'] = QLabel("KST GAL/HAL:")
        w['kst_gal'] = QLineEdit()
        layout.addRow(w['lbl_kst_gal'], w['kst_gal'])

        w['lbl_sk_normal'] = QLabel("Sachkonto (Normal):")
        w['sk_normal'] = QLineEdit()
        layout.addRow(w['lbl_sk_normal'], w['sk_normal'])
        
        # --- Events für dynamisches Ein-/Ausblenden ---
        w['norm'].toggled.connect(lambda chk: self.toggle_tv_laenge(w))
        w['pano'].toggled.connect(lambda chk: self.toggle_tv_laenge(w))
        w['si'].toggled.connect(lambda chk: w['anzahl_si'].setVisible(chk))
        w['gal'].toggled.connect(lambda chk: w['anzahl_gal'].setVisible(chk))
        w['hal'].toggled.connect(lambda chk: w['anzahl_hal'].setVisible(chk))
        
        group.setLayout(layout)
        group.setVisible(False)
        return group, w

    def set_kst_sk_visibility(self, w, is_projekt):
        """Blendet die KST/SK-Felder in den Detail-Tabs je nach Modus ein/aus."""
        # Projekt-Felder: sichtbar nur im Projektmodus
        for key in ['lbl_kst_projekt', 'kst_projekt',
                    'lbl_sk_projekt', 'sk_projekt']:
            w[key].setVisible(is_projekt)

        # Normal-Felder: sichtbar nur bei normaler Untersuchung
        for key in ['lbl_kst_reinigung', 'kst_reinigung',
                    'lbl_kst_tv', 'kst_tv',
                    'lbl_kst_gal', 'kst_gal',
                    'lbl_sk_normal', 'sk_normal']:
            w[key].setVisible(not is_projekt)

    def toggle_tv_laenge(self, w):
        """Zeigt das gemeinsame Haltungslängen-Feld für 'norm' ODER 'pano' an"""
        show_laenge = w['norm'].isChecked() or w['pano'].isChecked()
        w['laenge_tv'].setVisible(show_laenge)

    def load_typ_data(self, widgets, json_str):
        if not json_str:
            return
        try:
            d = json.loads(json_str)
            widgets['norm'].setChecked(bool(d.get('norm', 0)))
            widgets['pano'].setChecked(bool(d.get('pano', 0)))
            widgets['si'].setChecked(bool(d.get('si', 0)))
            widgets['gal'].setChecked(bool(d.get('gal', 0)))
            widgets['hal'].setChecked(bool(d.get('hal', 0)))
            

            # Projekt-KST/SK
            widgets['kst_projekt'].setText(d.get('kst_projekt', ''))
            widgets['sk_projekt'].setText(d.get('sk_projekt', ''))

            # Normal-KST/SK
            widgets['kst_reinigung'].setText(d.get('kst_reinigung', ''))
            widgets['kst_tv'].setText(d.get('kst_tv', ''))
            widgets['kst_gal'].setText(d.get('kst_gal', ''))
            widgets['sk_normal'].setText(d.get('sk_normal', ''))
            widgets['laenge_tv'].setText(d.get('laenge_tv', ''))
            widgets['anzahl_si'].setText(d.get('anzahl_si', ''))
            widgets['anzahl_gal'].setText(d.get('anzahl_gal', ''))
            widgets['anzahl_hal'].setText(d.get('anzahl_hal', ''))
        except Exception as e:
            print(f"[TYP-LOAD-ERROR] {e}")
            pass

    def get_typ_data(self, widgets):
        return {
            'norm': 1 if widgets['norm'].isChecked() else 0,
            'pano': 1 if widgets['pano'].isChecked() else 0,
            'si':   1 if widgets['si'].isChecked() else 0,
            'gal':  1 if widgets['gal'].isChecked() else 0,
            'hal':  1 if widgets['hal'].isChecked() else 0,

            # Projekt-KST/SK
            'kst_projekt': widgets['kst_projekt'].text(),
            'sk_projekt':  widgets['sk_projekt'].text(),

            # Normal-KST/SK
            'kst_reinigung': widgets['kst_reinigung'].text(),
            'kst_tv':        widgets['kst_tv'].text(),
            'kst_gal':       widgets['kst_gal'].text(),
            'sk_normal':     widgets['sk_normal'].text(),

            # NEU: dynamische Felder
            'laenge_tv':  widgets['laenge_tv'].text(),
            'anzahl_si':  widgets['anzahl_si'].text(),
            'anzahl_gal': widgets['anzahl_gal'].text(),
            'anzahl_hal': widgets['anzahl_hal'].text(),
        }

    def on_sachbearbeiter_changed(self):
        name = self.f_bearbeiter.currentText()
        if not name: return
        sachbearbeiter = self.einstellungen.get_values("Sachbearbeiter")
        for sb in sachbearbeiter:
            if isinstance(sb, dict) and f"{sb.get('vorname', '')} {sb.get('nachname', '')}".strip() == name.strip():
                self.f_telefon.setText(sb.get('telefon', ''))
                self.f_email.setText(sb.get('email', ''))
                break

    def on_firma_timer(self):
        """Timer-Trigger: Startet den Debounce-Timer."""
        self.f_firma_timer.start()

    def on_firma_changed(self):
        """Füllt Firma-Telefon und -Mail automatisch bei Auswahl einer Firma"""
        firma_name = self.f_firma.currentText()
        if not firma_name: return
        
        firmen = self.einstellungen.get_values("Firmen")
        for firma in firmen:
            if isinstance(firma, dict):
                if firma.get('name', '').strip() == firma_name.strip():
                    self.f_firma_tel.setText(firma.get('telefon', ''))
                    self.f_firma_mail.setText(firma.get('email', ''))
                    break

    def delayed_firma_fill(self):
        """Wird verzögert aufgerufen, um beim langsamen Tippen nicht zu zappeln."""
        self.on_firma_changed()

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Alle Dateien (*)")
        if file: self.f_datei.setText(file)

    def open_file(self):
        """Öffnet die hinterlegte Datei mit dem Standardprogramm (z.B. PDF-Reader)"""
        path = self.f_datei.text().strip()
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.information(self, "Info", "Keine gültige Datei hinterlegt oder Datei wurde verschoben/gelöscht.")

    def accept(self):
        """Wird aufgerufen, wenn der Benutzer auf 'Speichern' klickt. Kopiert die Datei."""
        current_file = self.f_datei.text().strip()

        if current_file and os.path.exists(current_file):
            # Basis-Pfad aus Einstellungen holen, ggf. Fallback auf Plugin-Verzeichnis
            basis = self.einstellungen.get_single_value("Plan_Basis_Pfad")
            if not basis:
                basis = os.path.dirname(__file__)

            # Jahres- und Projekt-Unterordner
            akt_jahr = str(datetime.datetime.now().year)
            projekt = self.f_projekt.text().strip() or "Untersuchungsauftrag"
            safe_proj = projekt.replace(" ", "_").replace("/", "-").replace("\\", "-")

            plaene_dir = os.path.join(basis, "Pläne", akt_jahr, safe_proj)

            # Prüfen, ob die Datei nicht ohnehin schon im Zielordner liegt
            if not os.path.normpath(current_file).startswith(os.path.normpath(plaene_dir)):
                try:
                    os.makedirs(plaene_dir, exist_ok=True)
                    filename = os.path.basename(current_file)
                    dest_path = os.path.join(plaene_dir, filename)

                    # Falls eine Datei mit demselben Namen schon existiert, Zeitstempel anhängen
                    if os.path.exists(dest_path) and os.path.normpath(current_file) != os.path.normpath(dest_path):
                        name, ext = os.path.splitext(filename)
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest_path = os.path.join(plaene_dir, f"{name}_{timestamp}{ext}")

                    # Datei kopieren und das Textfeld aktualisieren (damit get_data() den neuen Pfad greift)
                    shutil.copy2(current_file, dest_path)
                    self.f_datei.setText(dest_path)
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "Kopierfehler",
                        f"Die Datei konnte nicht in den Pläne-Ordner kopiert werden:\n{e}"
                    )
                    # Wir brechen den Speichervorgang nicht ab, aber die Datei bleibt am alten Ort

        # Originale Accept-Methode aufrufen, die den Dialog schließt und get_data() triggert
        super().accept()


    def load_ib_data(self, json_str):
        if not json_str: return
        try:
            d = json.loads(json_str)
            self.f_ib_name.setText(d.get('name', ''))
            self.f_ib_staat.setText(d.get('staat', ''))
            self.f_ib_plz.setText(d.get('plz', ''))
            self.f_ib_ort.setText(d.get('ort', ''))
            self.f_ib_str.setText(d.get('str', ''))
            self.f_ib_hnr.setText(d.get('hnr', ''))
            self.f_ib_vname.setText(d.get('vname', ''))
            self.f_ib_nname.setText(d.get('nname', ''))
            self.f_ib_mobil.setText(d.get('mobil', ''))
            self.f_ib_mail.setText(d.get('mail', ''))
        except: pass

    def get_data(self):
        ib_daten = {}
        if self.f_ib.isChecked():
            ib_daten = {
                'name': self.f_ib_name.text(), 'staat': self.f_ib_staat.text(),
                'plz': self.f_ib_plz.text(), 'ort': self.f_ib_ort.text(),
                'str': self.f_ib_str.text(), 'hnr': self.f_ib_hnr.text(),
                'vname': self.f_ib_vname.text(), 'nname': self.f_ib_nname.text(),
                'mobil': self.f_ib_mobil.text(), 'mail': self.f_ib_mail.text()
            }

        def _num(le):
            txt = le.text().strip()
            return float(txt.replace(',', '.')) if txt else 0.0

        return {
            'projektname': self.f_projekt.text().strip(),
            'strasse': self.f_strasse.currentText(),
            'abschnitt': self.f_abschnitt.text(),
            'sachbearbeiter': self.f_bearbeiter.currentText(),
            'telefon': self.f_telefon.text(),
            'email': self.f_email.text(),
            'beauftragt_am': self.f_beauftragt.date().toString("yyyy-MM-dd"),
            'ib_beteiligung': 1 if self.f_ib.isChecked() else 0,
            'typ_rw': 1 if self.f_typ_rw.isChecked() else 0,
            'typ_sw': 1 if self.f_typ_sw.isChecked() else 0,
            'typ_mw': 1 if self.f_typ_mw.isChecked() else 0,
            'datei': self.f_datei.text(),
            'zieldatum': self.f_zieldatum.date().toString("yyyy-MM-dd"),
            'grund': self.f_grund.currentText(),
            'bemerkung': self.f_bemerkung.toPlainText(),
            'ib_daten': json.dumps(ib_daten),
            'details_rw': json.dumps(self.get_typ_data(self.w_rw)) if self.f_typ_rw.isChecked() else "{}",
            'details_sw': json.dumps(self.get_typ_data(self.w_sw)) if self.f_typ_sw.isChecked() else "{}",
            'details_mw': json.dumps(self.get_typ_data(self.w_mw)) if self.f_typ_mw.isChecked() else "{}",
            'firma': self.f_firma.currentText(),
            'firma_tel': self.f_firma_tel.text(),
            'firma_mail': self.f_firma_mail.text(),
            'status': self.f_status.currentText(),
            'abschlussdatum': self.f_abschlussdatum.date().toString("yyyy-MM-dd") if self.f_status.currentText() == "Abgeschlossen" else None,
            # Projekt-Istkosten
            'ist_kosten_rw': _num(self.f_ist_rw),
            'ist_kosten_sw': _num(self.f_ist_sw),
            'ist_kosten_mw': _num(self.f_ist_mw),
            'modus': self.f_modus.currentText(),
            # NEU: Normal-Kosten je System/Art
            'k_rw_reinigung': _num(self.k_rw_reinigung),
            'k_rw_tv':        _num(self.k_rw_tv),
            'k_rw_gal':       _num(self.k_rw_gal),
            'k_sw_reinigung': _num(self.k_sw_reinigung),
            'k_sw_tv':        _num(self.k_sw_tv),
            'k_sw_gal':       _num(self.k_sw_gal),
            'k_mw_reinigung': _num(self.k_mw_reinigung),
            'k_mw_tv':        _num(self.k_mw_tv),
            'k_mw_gal':       _num(self.k_mw_gal),
        }



    def get_plan_ordner(self):
        """Gibt den Pfad zum Plan-Ordner des aktuellen Jahres zurück."""
        import os
        from datetime import datetime
        
        base_path = os.path.join(os.path.dirname(__file__), 'Pläne')
        jahr = datetime.now().year
        
        ordner_path = os.path.join(base_path, str(jahr))
        os.makedirs(ordner_path, exist_ok=True)
        return ordner_path

class AuftraegeManager:
    def __init__(self, dialog, einstellungen_manager):
        self.dialog = dialog
        self.einstellungen = einstellungen_manager
        self.ensure_table_exists()

    def ensure_table_exists(self):
        if not self.dialog.cur:
            return
        try:
            # 1. HAUPTTABELLE FÜR AUFTRÄGE
            if self.dialog.is_spatialite:
                self.dialog.cur.execute("""
                    CREATE TABLE IF NOT EXISTS untersuchungsauftraege (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        projektname TEXT NOT NULL,
                        strasse TEXT,
                        abschnitt TEXT,
                        sachbearbeiter TEXT,
                        telefon TEXT,
                        email TEXT,
                        beauftragt_am TEXT,
                        ib_beteiligung INTEGER,
                        typ_rw INTEGER,
                        typ_sw INTEGER,
                        typ_mw INTEGER,
                        datei TEXT,
                        zieldatum TEXT,
                        grund TEXT,
                        bemerkung TEXT,
                        ib_daten TEXT,
                        details_rw TEXT,
                        details_sw TEXT,
                        details_mw TEXT,
                        firma TEXT,
                        firma_tel TEXT,
                        firma_mail TEXT,
                        status TEXT DEFAULT 'In Bearbeitung',
                        abschlussdatum TEXT,
                        modus TEXT DEFAULT 'Projekt',
                        ist_kosten_rw REAL DEFAULT 0.0,
                        ist_kosten_sw REAL DEFAULT 0.0,
                        ist_kosten_mw REAL DEFAULT 0.0,
                        k_rw_reinigung REAL DEFAULT 0.0,
                        k_rw_tv REAL DEFAULT 0.0,
                        k_rw_gal REAL DEFAULT 0.0,
                        k_sw_reinigung REAL DEFAULT 0.0,
                        k_sw_tv REAL DEFAULT 0.0,
                        k_sw_gal REAL DEFAULT 0.0,
                        k_mw_reinigung REAL DEFAULT 0.0,
                        k_mw_tv REAL DEFAULT 0.0,
                        k_mw_gal REAL DEFAULT 0.0
                    )
                """)

                self.dialog.cur.execute("PRAGMA table_info(untersuchungsauftraege)")
                existing_cols = {row[1] for row in self.dialog.cur.fetchall()}

                new_cols = {
                    "ib_daten": "TEXT",
                    "details_rw": "TEXT",
                    "details_sw": "TEXT",
                    "details_mw": "TEXT",
                    "firma": "TEXT",
                    "firma_tel": "TEXT",
                    "firma_mail": "TEXT",
                    "status": "TEXT DEFAULT 'In Bearbeitung'",
                    "abschlussdatum": "TEXT",
                    "modus": "TEXT DEFAULT 'Projekt'",
                    "ist_kosten_rw": "REAL DEFAULT 0.0",
                    "ist_kosten_sw": "REAL DEFAULT 0.0",
                    "ist_kosten_mw": "REAL DEFAULT 0.0",
                    "k_rw_reinigung": "REAL DEFAULT 0.0",
                    "k_rw_tv": "REAL DEFAULT 0.0",
                    "k_rw_gal": "REAL DEFAULT 0.0",
                    "k_sw_reinigung": "REAL DEFAULT 0.0",
                    "k_sw_tv": "REAL DEFAULT 0.0",
                    "k_sw_gal": "REAL DEFAULT 0.0",
                    "k_mw_reinigung": "REAL DEFAULT 0.0",
                    "k_mw_tv": "REAL DEFAULT 0.0",
                    "k_mw_gal": "REAL DEFAULT 0.0",
                }

                for col, col_type in new_cols.items():
                    if col not in existing_cols:
                        self.dialog.cur.execute(
                            f"ALTER TABLE untersuchungsauftraege ADD COLUMN {col} {col_type}"
                        )

            else:
                self.dialog.cur.execute("""
                    CREATE TABLE IF NOT EXISTS public.untersuchungsauftraege (
                        id SERIAL PRIMARY KEY,
                        projektname VARCHAR(255) NOT NULL,
                        strasse VARCHAR(255),
                        abschnitt VARCHAR(255),
                        sachbearbeiter VARCHAR(255),
                        telefon VARCHAR(100),
                        email VARCHAR(255),
                        beauftragt_am DATE,
                        ib_beteiligung SMALLINT,
                        typ_rw SMALLINT,
                        typ_sw SMALLINT,
                        typ_mw SMALLINT,
                        datei TEXT,
                        zieldatum DATE,
                        grund VARCHAR(255),
                        bemerkung TEXT,
                        ib_daten TEXT,
                        details_rw TEXT,
                        details_sw TEXT,
                        details_mw TEXT,
                        firma TEXT,
                        firma_tel TEXT,
                        firma_mail TEXT,
                        status VARCHAR(50) DEFAULT 'In Bearbeitung',
                        abschlussdatum DATE,
                        modus VARCHAR(50) DEFAULT 'Projekt',
                        ist_kosten_rw NUMERIC(10,2) DEFAULT 0.0,
                        ist_kosten_sw NUMERIC(10,2) DEFAULT 0.0,
                        ist_kosten_mw NUMERIC(10,2) DEFAULT 0.0,
                        k_rw_reinigung NUMERIC(10,2) DEFAULT 0.0,
                        k_rw_tv NUMERIC(10,2) DEFAULT 0.0,
                        k_rw_gal NUMERIC(10,2) DEFAULT 0.0,
                        k_sw_reinigung NUMERIC(10,2) DEFAULT 0.0,
                        k_sw_tv NUMERIC(10,2) DEFAULT 0.0,
                        k_sw_gal NUMERIC(10,2) DEFAULT 0.0,
                        k_mw_reinigung NUMERIC(10,2) DEFAULT 0.0,
                        k_mw_tv NUMERIC(10,2) DEFAULT 0.0,
                        k_mw_gal NUMERIC(10,2) DEFAULT 0.0
                    )
                """)

                new_cols = {
                    "ib_daten": "TEXT",
                    "details_rw": "TEXT",
                    "details_sw": "TEXT",
                    "details_mw": "TEXT",
                    "firma": "TEXT",
                    "firma_tel": "TEXT",
                    "firma_mail": "TEXT",
                    "status": "VARCHAR(50) DEFAULT 'In Bearbeitung'",
                    "abschlussdatum": "DATE",
                    "modus": "VARCHAR(50) DEFAULT 'Projekt'",
                    "ist_kosten_rw": "NUMERIC(10,2) DEFAULT 0.0",
                    "ist_kosten_sw": "NUMERIC(10,2) DEFAULT 0.0",
                    "ist_kosten_mw": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_rw_reinigung": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_rw_tv": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_rw_gal": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_sw_reinigung": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_sw_tv": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_sw_gal": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_mw_reinigung": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_mw_tv": "NUMERIC(10,2) DEFAULT 0.0",
                    "k_mw_gal": "NUMERIC(10,2) DEFAULT 0.0",
                }

                for col, col_type in new_cols.items():
                    self.dialog.cur.execute(
                        f"ALTER TABLE public.untersuchungsauftraege "
                        f"ADD COLUMN IF NOT EXISTS {col} {col_type}"
                    )

            # 2. TABELLE HAUSHALTSMITTEL
            if self.dialog.is_spatialite:
                self.dialog.cur.execute("""
                    CREATE TABLE IF NOT EXISTS untersuchungs_haushaltsmittel (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        jahr INTEGER NOT NULL,
                        kostenstelle TEXT NOT NULL,
                        sachkonto TEXT NOT NULL,
                        budget_gesamt REAL DEFAULT 0.0
                    )
                """)
            else:
                self.dialog.cur.execute("""
                    CREATE TABLE IF NOT EXISTS public.untersuchungs_haushaltsmittel (
                        id SERIAL PRIMARY KEY,
                        jahr INTEGER NOT NULL,
                        kostenstelle VARCHAR(100) NOT NULL,
                        sachkonto VARCHAR(100) NOT NULL,
                        budget_gesamt NUMERIC(15,2) DEFAULT 0.0,
                        UNIQUE (jahr, kostenstelle, sachkonto)
                    )
                """)

            self.dialog.conn.commit()

        except Exception as e:
            self.dialog.conn.rollback()
            print(f"Fehler bei DB-Tabellen Anlage: {e}")

    def init_pdf_template_editors(self):
        if not hasattr(self.dialog, "pdf_info_editor") or not hasattr(self.dialog, "pdf_beauf_editor"):
            return

        default_info_html = (
            "<p>Untersuchungsauftrag</p>"
            "<p><b>Projekt:</b> {projektname}</p>"
            "<p><b>Straße:</b> {strasse} {abschnitt}</p>"
            "<p><b>Sachbearbeiter:</b> {sachbearbeiter}</p>"
            "<p><b>Beauftragt am:</b> {beauftragt_am}</p>"
            "<p><b>Zieldatum:</b> {zieldatum}</p>"
            "<p><b>Beauftragte Firma:</b> {firma}</p>"
            "<p><b>Bemerkung:</b><br>{bemerkung}</p>"
            "<p><b>Auftragsumfang:</b></p>"
            "{tabelle_haltungen}"
        )
        html_info = self.einstellungen.get_single_value("PDF_Info_HTML") or default_info_html
        self.dialog.pdf_info_editor.set_html(html_info)

        default_beauf_html = (
            "<p>Beauftragung Kanaluntersuchung</p>"
            "<p><b>Projekt:</b> {projektname}</p>"
            "<p><b>Ort/Straße:</b> {strasse}</p>"
            "<p><b>Fertigstellung bis:</b> {zieldatum}</p>"
            "<p><b>Beauftragte Firma:</b> {firma}</p>"
            "<p><b>Bemerkung:</b><br>{bemerkung}</p>"
            "<p><b>Auftragsumfang:</b></p>"
            "{tabelle_haltungen}"
        )
        html_beauf = self.einstellungen.get_single_value("PDF_Beauf_HTML") or default_beauf_html
        self.dialog.pdf_beauf_editor.set_html(html_beauf)

        placeholders = [
            "{id}",
            "{projektname}",
            "{strasse}",
            "{abschnitt}",
            "{sachbearbeiter}",
            "{telefon}",
            "{email}",
            "{beauftragt_am}",
            "{ib_beteiligung}",
            "{typ_rw}",
            "{typ_sw}",
            "{typ_mw}",
            "{datei}",
            "{zieldatum}",
            "{grund}",
            "{bemerkung}",
            "{ib_daten}",
            "{details_rw}",
            "{details_sw}",
            "{details_mw}",
            "{firma}",
            "{firma_tel}",
            "{firma_mail}",
            "{status}",
            "{abschlussdatum}",
            "{modus}",
            "{ist_kosten_rw}",
            "{ist_kosten_sw}",
            "{ist_kosten_mw}",
            "{k_rw_reinigung}",
            "{k_rw_tv}",
            "{k_rw_gal}",
            "{k_sw_reinigung}",
            "{k_sw_tv}",
            "{k_sw_gal}",
            "{k_mw_reinigung}",
            "{k_mw_tv}",
            "{k_mw_gal}",
            "{tabelle_haltungen}",
        ]
        self.dialog.pdf_info_editor.set_placeholders(placeholders)
        self.dialog.pdf_beauf_editor.set_placeholders(placeholders)


    # def create_project_pdf(self, data, template_key="PDF_Info_HTML", output_dir=None):
    #     """Erzeugt eine Projekt-PDF basierend auf Qt-HTML-Template mit voller WYSIWYG-Unterstützung."""
    #     print("[PDF] create_project_pdf (Qt) aufgerufen mit data:", data, "template_key:", template_key)

    #     # Ausgabeordner
    #     if output_dir is None:
    #         output_dir = os.path.expanduser("~/Documents/Untersuchungsaufträge")
    #     os.makedirs(output_dir, exist_ok=True)

    #     # HTML-Template aus Einstellungen holen
    #     html_template = self.einstellungen.get_single_value(template_key)
    #     if not html_template:
    #         # Fallback auf Default aus tab_auftraege
    #         if template_key == "PDF_Beauf_HTML":
    #             html_template = (
    #                 "<p>Beauftragung Kanaluntersuchung</p>"
    #                 "<p><b>Projekt:</b> {projektname}</p>"
    #                 "<p><b>Ort/Straße:</b> {strasse}</p>"
    #                 "<p><b>Fertigstellung bis:</b> {zieldatum}</p>"
    #                 "<p><b>Beauftragte Firma:</b> {firma}</p>"
    #                 "<p><b>Bemerkung:</b><br>{bemerkung}</p>"
    #                 "<p><b>Auftragsumfang:</b></p>"
    #                 "{tabelle_haltungen}"
    #             )
    #         elif template_key == "PDF_Info_HTML":
    #             html_template = (
    #                 "<p>Untersuchungsauftrag</p>"
    #                 "<p><b>Projekt:</b> {projektname}</p>"
    #                 "<p><b>Straße:</b> {strasse} {abschnitt}</p>"
    #                 "<p><b>Sachbearbeiter:</b> {sachbearbeiter}</p>"
    #                 "<p><b>Beauftragt am:</b> {beauftragt_am}</p>"
    #                 "<p><b>Zieldatum:</b> {zieldatum}</p>"
    #                 "<p><b>Beauftragte Firma:</b> {firma}</p>"
    #                 "<p><b>Bemerkung:</b><br>{bemerkung}</p>"
    #                 "<p><b>Auftragsumfang:</b></p>"
    #                 "{tabelle_haltungen}"
    #             )
    #         else:
    #             print("[PDF] Kein HTML-Template gefunden, breche ab.")
    #             return None

    #     # Hilfsfunktion: nur unsere Platzhalter ersetzen, nicht die CSS-Klammern
    #     def fill_placeholders(template, data_dict):
    #         result = template
    #         for key, value in data_dict.items():
    #             placeholder = "{" + key + "}"
    #             result = result.replace(placeholder, "" if value is None else str(value))
    #         return result

    #     # Platzhalter-Daten vorbereiten
    #     safe_data = {k: ("" if v is None else str(v)) for k, v in data.items()}

    #     try:
    #         print("[PDF-DEBUG] Template VORHER:", html_template[:200])
    #         print("[PDF-DEBUG] safe_data:", safe_data)
    #         html_text = fill_placeholders(html_template, safe_data)
    #         print("[PDF-DEBUG] Template NACHHER:", html_text[:200])
    #     except Exception as e:
    #         print("[PDF-TEMPLATE-ERROR]", e)
    #         html_text = html_template  # Notfall: ungefüllt

    #     proj = safe_data.get('projektname') or "Untersuchungsauftrag"
    #     safe_proj = str(proj).replace(' ', '_').replace('/', '-').replace('\\', '-')
    #     filename = f"Auftrag_{safe_proj}.pdf"
    #     pdf_path = os.path.join(output_dir, filename)
    #     print("[PDF] Zieldatei:", pdf_path)

    #     # QTextDocument mit dem HTML füllen
    #     doc = QTextDocument()
    #     doc.setHtml(html_text)

    #     # Seite auf A4 setzen (in Punkt)
    #     mm_to_pt = 72.0 / 25.4
    #     page_width = 210 * mm_to_pt
    #     page_height = 297 * mm_to_pt
    #     doc.setPageSize(QSizeF(page_width, page_height))

    #     printer = QPrinter(QPrinter.HighResolution)

    #     printer.setOutputFormat(QPrinter.PdfFormat)
    #     printer.setPaperSize(QPrinter.A4)
    #     printer.setFullPage(False)
    #     printer.setOutputFileName(pdf_path)
    #     printer.setPageMargins(20.0, 20.0, 20.0, 20.0, QPrinter.Millimeter)

    #     try:
    #         doc.print_(printer)
    #         print("[PDF] Erfolgreich erstellt (Qt):", pdf_path)
    #         return pdf_path
    #     except Exception as e:
    #         print("[PDF-ERROR]", e)
    #         return None

    def create_new_project(self):
        dlg = AuftragDialog(self.dialog, self.einstellungen)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            self.save_to_db(data)
            # Nach dem Speichern fragen:
            reply = QMessageBox.question(
                self.dialog,
                "Info-Mail senden?",
                "Möchten Sie eine interne Info-Mail zum neuen Auftrag versenden?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.send_info_mail(data)

    def edit_project(self, row_data):
        dlg = AuftragDialog(self.dialog, self.einstellungen, row_data)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            self.save_to_db(data, row_data[0])
            reply = QMessageBox.question(
                self.dialog,
                "Info-Mail senden?",
                "Möchten Sie eine interne Info-Mail zum geänderten Auftrag versenden?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.send_info_mail(data)

    def save_to_db(self, data, record_id=None):
        if not data['projektname']:
            QMessageBox.warning(self.dialog, "Fehler", "Projektname ist Pflichtfeld!")
            return

        params = (
            data['projektname'],
            data['strasse'],
            data['abschnitt'],
            data['sachbearbeiter'],
            data['telefon'],
            data['email'],
            data['beauftragt_am'],
            data['ib_beteiligung'],
            data['typ_rw'],
            data['typ_sw'],
            data['typ_mw'],
            data['datei'],
            data['zieldatum'],
            data['grund'],
            data['bemerkung'],
            data['ib_daten'],
            data['details_rw'],
            data['details_sw'],
            data['details_mw'],
            data['firma'],
            data['firma_tel'],
            data['firma_mail'],
            data['status'],
            data['abschlussdatum'],
            data['modus'],
            data['ist_kosten_rw'],
            data['ist_kosten_sw'],
            data['ist_kosten_mw'],
            data['k_rw_reinigung'],
            data['k_rw_tv'],
            data['k_rw_gal'],
            data['k_sw_reinigung'],
            data['k_sw_tv'],
            data['k_sw_gal'],
            data['k_mw_reinigung'],
            data['k_mw_tv'],
            data['k_mw_gal'],
        )

        try:
            if record_id is None:
                if self.dialog.is_spatialite:
                    self.dialog.cur.execute("""
                        INSERT INTO untersuchungsauftraege (
                            projektname,
                            strasse,
                            abschnitt,
                            sachbearbeiter,
                            telefon,
                            email,
                            beauftragt_am,
                            ib_beteiligung,
                            typ_rw,
                            typ_sw,
                            typ_mw,
                            datei,
                            zieldatum,
                            grund,
                            bemerkung,
                            ib_daten,
                            details_rw,
                            details_sw,
                            details_mw,
                            firma,
                            firma_tel,
                            firma_mail,
                            status,
                            abschlussdatum,
                            modus,
                            ist_kosten_rw,
                            ist_kosten_sw,
                            ist_kosten_mw,
                            k_rw_reinigung,
                            k_rw_tv,
                            k_rw_gal,
                            k_sw_reinigung,
                            k_sw_tv,
                            k_sw_gal,
                            k_mw_reinigung,
                            k_mw_tv,
                            k_mw_gal
                        ) VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?
                        )
                    """, params)
                else:
                    self.dialog.cur.execute("""
                        INSERT INTO public.untersuchungsauftraege (
                            projektname,
                            strasse,
                            abschnitt,
                            sachbearbeiter,
                            telefon,
                            email,
                            beauftragt_am,
                            ib_beteiligung,
                            typ_rw,
                            typ_sw,
                            typ_mw,
                            datei,
                            zieldatum,
                            grund,
                            bemerkung,
                            ib_daten,
                            details_rw,
                            details_sw,
                            details_mw,
                            firma,
                            firma_tel,
                            firma_mail,
                            status,
                            abschlussdatum,
                            modus,
                            ist_kosten_rw,
                            ist_kosten_sw,
                            ist_kosten_mw,
                            k_rw_reinigung,
                            k_rw_tv,
                            k_rw_gal,
                            k_sw_reinigung,
                            k_sw_tv,
                            k_sw_gal,
                            k_mw_reinigung,
                            k_mw_tv,
                            k_mw_gal
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s
                        )
                    """, params)

            else:
                if self.dialog.is_spatialite:
                    self.dialog.cur.execute("""
                        UPDATE untersuchungsauftraege SET
                            projektname=?,
                            strasse=?,
                            abschnitt=?,
                            sachbearbeiter=?,
                            telefon=?,
                            email=?,
                            beauftragt_am=?,
                            ib_beteiligung=?,
                            typ_rw=?,
                            typ_sw=?,
                            typ_mw=?,
                            datei=?,
                            zieldatum=?,
                            grund=?,
                            bemerkung=?,
                            ib_daten=?,
                            details_rw=?,
                            details_sw=?,
                            details_mw=?,
                            firma=?,
                            firma_tel=?,
                            firma_mail=?,
                            status=?,
                            abschlussdatum=?,
                            modus=?,
                            ist_kosten_rw=?,
                            ist_kosten_sw=?,
                            ist_kosten_mw=?,
                            k_rw_reinigung=?,
                            k_rw_tv=?,
                            k_rw_gal=?,
                            k_sw_reinigung=?,
                            k_sw_tv=?,
                            k_sw_gal=?,
                            k_mw_reinigung=?,
                            k_mw_tv=?,
                            k_mw_gal=?
                        WHERE id=?
                    """, params + (record_id,))
                else:
                    self.dialog.cur.execute("""
                        UPDATE public.untersuchungsauftraege SET
                            projektname=%s,
                            strasse=%s,
                            abschnitt=%s,
                            sachbearbeiter=%s,
                            telefon=%s,
                            email=%s,
                            beauftragt_am=%s,
                            ib_beteiligung=%s,
                            typ_rw=%s,
                            typ_sw=%s,
                            typ_mw=%s,
                            datei=%s,
                            zieldatum=%s,
                            grund=%s,
                            bemerkung=%s,
                            ib_daten=%s,
                            details_rw=%s,
                            details_sw=%s,
                            details_mw=%s,
                            firma=%s,
                            firma_tel=%s,
                            firma_mail=%s,
                            status=%s,
                            abschlussdatum=%s,
                            modus=%s,
                            ist_kosten_rw=%s,
                            ist_kosten_sw=%s,
                            ist_kosten_mw=%s,
                            k_rw_reinigung=%s,
                            k_rw_tv=%s,
                            k_rw_gal=%s,
                            k_sw_reinigung=%s,
                            k_sw_tv=%s,
                            k_sw_gal=%s,
                            k_mw_reinigung=%s,
                            k_mw_tv=%s,
                            k_mw_gal=%s
                        WHERE id=%s
                    """, params + (record_id,))

            self.dialog.conn.commit()
            self.refresh_projects_table()

        except Exception as e:
            self.dialog.conn.rollback()
            QMessageBox.critical(self.dialog, "DB Fehler", f"Fehler beim Speichern:\n{e}")

    def delete_project(self, record_id, name):
        reply = QMessageBox.question(self.dialog, "Löschen", f"'{name}' löschen?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if self.dialog.is_spatialite:
                    self.dialog.cur.execute("DELETE FROM untersuchungsauftraege WHERE id=?", (record_id,))
                else:
                    self.dialog.cur.execute("DELETE FROM public.untersuchungsauftraege WHERE id=%s", (record_id,))
                self.dialog.conn.commit()
                self.refresh_projects_table()
            except Exception as e:
                self.dialog.conn.rollback()
                QMessageBox.critical(self.dialog, "DB Fehler", f"Fehler beim Löschen:\n{e}")

    def refresh_projects_table(self):
        if not self.dialog.cur: return
        try:
            if self.dialog.is_spatialite:
                self.dialog.cur.execute("SELECT * FROM untersuchungsauftraege ORDER BY beauftragt_am DESC")
            else:
                self.dialog.cur.execute("SELECT * FROM public.untersuchungsauftraege ORDER BY beauftragt_am DESC")
            
            rows = self.dialog.cur.fetchall()
            self.dialog.auftraege_table.setRowCount(len(rows))
            
            from qgis.PyQt.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem
            
            for row_idx, row_data in enumerate(rows):
                # Basis-Daten
                self.dialog.auftraege_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[1] or ""))) # Projekt
                self.dialog.auftraege_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[7] or ""))) # Datum
                self.dialog.auftraege_table.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2] or ""))) # Strasse
                self.dialog.auftraege_table.setItem(row_idx, 3, QTableWidgetItem(str(row_data[4] or ""))) # Bearbeiter
                
                # NEU: Status (Index 23 statt 20)
                status = str(row_data[23]) if len(row_data) > 23 and row_data[23] else "In Bearbeitung"
                self.dialog.auftraege_table.setItem(row_idx, 4, QTableWidgetItem(status))
                
                # Summe der Ist-Kosten + Normal-Kosten berechnen
                gesamt_kosten = 0.0
                try:
                    # Projekt-Istkosten
                    if len(row_data) > IDX_IST_RW and row_data[IDX_IST_RW] is not None:
                        gesamt_kosten += float(row_data[IDX_IST_RW] or 0.0)
                    if len(row_data) > IDX_IST_SW and row_data[IDX_IST_SW] is not None:
                        gesamt_kosten += float(row_data[IDX_IST_SW] or 0.0)
                    if len(row_data) > IDX_IST_MW and row_data[IDX_IST_MW] is not None:
                        gesamt_kosten += float(row_data[IDX_IST_MW] or 0.0)

                    # Normal-Kosten RW
                    if len(row_data) > IDX_K_RW_REIN and row_data[IDX_K_RW_REIN] is not None:
                        gesamt_kosten += float(row_data[IDX_K_RW_REIN] or 0.0)
                    if len(row_data) > IDX_K_RW_TV and row_data[IDX_K_RW_TV] is not None:
                        gesamt_kosten += float(row_data[IDX_K_RW_TV] or 0.0)
                    if len(row_data) > IDX_K_RW_GAL and row_data[IDX_K_RW_GAL] is not None:
                        gesamt_kosten += float(row_data[IDX_K_RW_GAL] or 0.0)

                    # Normal-Kosten SW
                    if len(row_data) > IDX_K_SW_REIN and row_data[IDX_K_SW_REIN] is not None:
                        gesamt_kosten += float(row_data[IDX_K_SW_REIN] or 0.0)
                    if len(row_data) > IDX_K_SW_TV and row_data[IDX_K_SW_TV] is not None:
                        gesamt_kosten += float(row_data[IDX_K_SW_TV] or 0.0)
                    if len(row_data) > IDX_K_SW_GAL and row_data[IDX_K_SW_GAL] is not None:
                        gesamt_kosten += float(row_data[IDX_K_SW_GAL] or 0.0)

                    # Normal-Kosten MW
                    if len(row_data) > IDX_K_MW_REIN and row_data[IDX_K_MW_REIN] is not None:
                        gesamt_kosten += float(row_data[IDX_K_MW_REIN] or 0.0)
                    if len(row_data) > IDX_K_MW_TV and row_data[IDX_K_MW_TV] is not None:
                        gesamt_kosten += float(row_data[IDX_K_MW_TV] or 0.0)
                    if len(row_data) > IDX_K_MW_GAL and row_data[IDX_K_MW_GAL] is not None:
                        gesamt_kosten += float(row_data[IDX_K_MW_GAL] or 0.0)
                except (ValueError, TypeError):
                    pass
                # falls irgendwo kein numerischer Inhalt steht

                self.dialog.auftraege_table.setItem(
                    row_idx, 5, QTableWidgetItem(f"{gesamt_kosten:.2f}")
)                
                # Aktionen-Buttons
                btn_widget = QWidget()
                l = QHBoxLayout(btn_widget)
                l.setContentsMargins(2,2,2,2)
                
                btn_mail = QPushButton("✉️ Mail")
                btn_edit = QPushButton("✏️ Bearbeiten")
                btn_del = QPushButton("❌ Löschen")
                
                # Schmaler machen
                btn_mail.setFixedWidth(50)
                
                btn_mail.clicked.connect(lambda chk, d=row_data: self.send_beauftragung_mail(d))
                btn_edit.clicked.connect(lambda chk, d=row_data: self.edit_project(d))
                btn_del.clicked.connect(lambda chk, id=row_data[0], n=row_data[1]: self.delete_project(id, n))
                
                l.addWidget(btn_mail)
                l.addWidget(btn_edit)
                l.addWidget(btn_del)
                self.dialog.auftraege_table.setCellWidget(row_idx, 6, btn_widget)
                
        except Exception as e:
            self.dialog.conn.rollback()
            print("Ladefehler Aufträge:", e)


    def create_project_pdf(self, data, template_key="PDF_Info_HTML", output_dir=None):
        """Erzeugt eine Projekt-PDF basierend auf Qt-HTML-Template mit voller WYSIWYG-Unterstützung."""
        print("[PDF] create_project_pdf (Qt) aufgerufen mit data:", data, "template_key:", template_key)

        # Ausgabeordner
        if output_dir is None:
            output_dir = os.path.expanduser("~/Documents/Untersuchungsaufträge")
        os.makedirs(output_dir, exist_ok=True)

        # HTML-Template aus Einstellungen holen
        html_template = self.einstellungen.get_single_value(template_key)
        if not html_template:
            # Fallback auf Default aus tab_auftraege
            if template_key == "PDF_Beauf_HTML":
                html_template = (
                    "<p>Beauftragung Kanaluntersuchung</p>"
                    "<p><b>Projekt:</b> {projektname}</p>"
                    "<p><b>Ort/Straße:</b> {strasse}</p>"
                    "<p><b>Fertigstellung bis:</b> {zieldatum}</p>"
                    "<p><b>Beauftragte Firma:</b> {firma}</p>"
                    "<p><b>Bemerkung:</b><br>{bemerkung}</p>"
                    "<p><b>Auftragsumfang:</b></p>"
                    "{tabelle_haltungen}"
                )
            elif template_key == "PDF_Info_HTML":
                html_template = (
                    "<p>Untersuchungsauftrag</p>"
                    "<p><b>Projekt:</b> {projektname}</p>"
                    "<p><b>Straße:</b> {strasse} {abschnitt}</p>"
                    "<p><b>Sachbearbeiter:</b> {sachbearbeiter}</p>"
                    "<p><b>Beauftragt am:</b> {beauftragt_am}</p>"
                    "<p><b>Zieldatum:</b> {zieldatum}</p>"
                    "<p><b>Beauftragte Firma:</b> {firma}</p>"
                    "<p><b>Bemerkung:</b><br>{bemerkung}</p>"
                    "<p><b>Auftragsumfang:</b></p>"
                    "{tabelle_haltungen}"
                )
            else:
                print("[PDF] Kein HTML-Template gefunden, breche ab.")
                return None

        # Hilfsfunktion: nur unsere Platzhalter ersetzen, nicht die CSS-Klammern
        def fill_placeholders(template, data_dict):
            result = template
            for key, value in data_dict.items():
                placeholder = "{" + key + "}"
                result = result.replace(placeholder, "" if value is None else str(value))
            return result

        # Platzhalter-Daten vorbereiten (fehlende Keys -> leer)
        safe_data = {k: ("" if v is None else str(v)) for k, v in data.items()}

        try:
            print("[PDF-DEBUG] Template VORHER:", html_template[:200])
            print("[PDF-DEBUG] safe_data:", safe_data)
            html_text = fill_placeholders(html_template, safe_data)
            print("[PDF-DEBUG] Template NACHHER:", html_text[:200])
        except Exception as e:
            print("[PDF-TEMPLATE-ERROR]", e)
            html_text = html_template  # Notfall: ungefüllt

        proj = safe_data.get('projektname') or "Untersuchungsauftrag"
        safe_proj = str(proj).replace(' ', '_').replace('/', '-').replace('\\', '-')
        filename = f"Auftrag_{safe_proj}.pdf"
        pdf_path = os.path.join(output_dir, filename)
        print("[PDF] Zieldatei:", pdf_path)

        # QTextDocument mit dem HTML füllen
        doc = QTextDocument()
        doc.setHtml(html_text)

        # Seite auf A4 setzen (in Punkt)
        mm_to_pt = 72.0 / 25.4
        page_width = 210 * mm_to_pt
        page_height = 297 * mm_to_pt
        doc.setPageSize(QSizeF(page_width, page_height))

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setFullPage(False)
        printer.setOutputFileName(pdf_path)
        printer.setPageMargins(20.0, 20.0, 20.0, 20.0, QPrinter.Millimeter)

        try:
            doc.print_(printer)
            print("[PDF] Erfolgreich erstellt (Qt):", pdf_path)
            return pdf_path
        except Exception as e:
            print("[PDF-ERROR]", e)
            return None


    def send_info_mail(self, data):
        """Öffnet einen E-Mail-Entwurf für die interne Info an alle im Verteiler."""
        from urllib.parse import quote
        from qgis.PyQt.QtWidgets import QMessageBox
        from qgis.PyQt.QtGui import QDesktopServices
        from qgis.PyQt.QtCore import QUrl

        print("[MAIL-INFO] send_info_mail aufgerufen")

        # Sicherstellen, dass tabelle_haltungen im data-Dict vorhanden ist
        if "tabelle_haltungen" not in data:
            try:
                details_rw = data.get("details_rw", "{}")
                details_sw = data.get("details_sw", "{}")
                details_mw = data.get("details_mw", "{}")
                data["tabelle_haltungen"] = self.generate_haltungen_summary_from_details(
                    details_rw, details_sw, details_mw
                )
            except Exception as e:
                print("[TABELLE-SUMMARY-ERROR]", e)
                data["tabelle_haltungen"] = "Fehler beim Laden der Haltungsdaten"

        pdf_path = self.create_project_pdf(data, template_key="PDF_Info_HTML")
        print("[MAIL-INFO] pdf_path:", pdf_path)

        verteileradressen = self.einstellungen.get_values("Verteiler")
        if verteileradressen:
            empfaenger = ",".join(str(mail).strip() for mail in verteileradressen if str(mail).strip())
        else:
            empfaenger = data.get("email") or "info@dein-betrieb.de"
            QMessageBox.information(
                self.dialog,
                "Hinweis",
                "Der E-Mail-Verteiler in den Einstellungen ist leer. Mail an den Sachbearbeiter."
            )

        betreff = f"Neuer Untersuchungsauftrag {data.get('projektname')} {data.get('strasse')}"
        text = (
            "Hallo,\n\n"
            "es wurde ein neuer Untersuchungsauftrag im System erfasst.\n\n"
            f"Projekt: {data.get('projektname')}\n"
            f"Straße: {data.get('strasse')} {data.get('abschnitt')}\n"
            f"Sachbearbeiter: {data.get('sachbearbeiter')}\n"
            f"Zieldatum: {data.get('zieldatum')}\n"
            f"Beauftragte Firma: {data.get('firma')}\n"
            f"Bemerkung: {data.get('bemerkung')}\n\n"
            f"{data.get('tabelle_haltungen')}\n\n"
        )

        if pdf_path:
            text += (
                f"Hinweis: Die Projektunterlage als PDF liegt unter {pdf_path} "
                "– vor dem Versenden als Anhang hinzufügen.\n\n"
            )

        text += "Viele Grüße\nRené Müllers QGIS-Plugin"

        mailto_url = f"mailto:{empfaenger}?subject={quote(betreff)}&body={quote(text)}"
        QDesktopServices.openUrl(QUrl(mailto_url))


    def send_beauftragung_mail(self, row_data):
        """Öffnet einen E-Mail-Entwurf an die beauftragte Firma nach Bestätigung."""
        from urllib.parse import quote
        from qgis.PyQt.QtWidgets import QMessageBox
        from qgis.PyQt.QtGui import QDesktopServices
        from qgis.PyQt.QtCore import QUrl

        firma_mail = row_data[22] if len(row_data) > 22 and row_data[22] else ""
        firma_name = row_data[20] if len(row_data) > 20 and row_data[20] else "Sehr geehrte Damen und Herren"
        projekt = row_data[1]
        strasse = row_data[2]
        zieldatum = row_data[13] if row_data[13] else "schnellstmöglich"
        datei = row_data[12] if row_data[12] else "Keine Datei hinterlegt."

        if not firma_mail:
            QMessageBox.warning(
                self.dialog, "Fehlende E-Mail",
                f"Für die Firma '{firma_name}' ist keine E-Mail-Adresse hinterlegt!\nBitte in den Auftragseigenschaften ergänzen."
            )
            return

        reply = QMessageBox.question(
            self.dialog,
            "E-Mail an Firma senden",
            f"Möchten Sie jetzt eine Beauftragungs-E-Mail an folgende Adresse vorbereiten?\n\n"
            f"Firma: {firma_name}\n"
            f"E-Mail: {firma_mail}",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            return

        # Daten für PDF zusammenstellen
        data = {
            'projektname': projekt,
            'strasse': strasse,
            'abschnitt': row_data[3] if len(row_data) > 3 else "",
            'sachbearbeiter': row_data[4] if len(row_data) > 4 else "",
            'beauftragt_am': str(row_data[7]) if len(row_data) > 7 and row_data[7] else "",
            'zieldatum': str(zieldatum),
            'firma': firma_name,
            'firma_tel': row_data[21] if len(row_data) > 21 else "",
            'firma_mail': firma_mail,
            'bemerkung': row_data[15] if len(row_data) > 15 else "",
            'tabelle_haltungen': self.generate_haltungen_summary_text(row_data),  # wichtig
        }


        print("[MAIL-BEAUF] send_beauftragung_mail aufgerufen, row_data:", row_data)
        ...
        pdf_path = self.create_project_pdf(data, template_key="PDF_Beauf_HTML")
        print("[MAIL-BEAUF] pdf_path:", pdf_path)

        betreff = f"Beauftragung Kanaluntersuchung: {projekt} ({strasse})"

        text = f"Hallo {firma_name},\n\nhiermit beauftragen wir Sie mit der Kanaluntersuchung für folgendes Projekt:\n\n"
        text += f"Projekt: {projekt}\n"
        text += f"Ort/Straße: {strasse}\n"
        text += f"Fertigstellung bis: {zieldatum}\n\n"

        text += "\nAuftragsumfang:\n"
        text += self.generate_haltungen_summary_text(row_data)  # <-- Text statt HTML
        text += "\n\n"

        if datei:
            text += f"Die Pläne und Unterlagen finden Sie im Anhang oder in unserer Cloud.\n(Hinweis für Absender: Bitte Datei anhängen: {datei})\n\n"

        if pdf_path:
            text += f"Hinweis: Die automatisch erzeugte Projekt-PDF liegt unter:\n{pdf_path}\nBitte als Anhang hinzufügen.\n\n"

        text += "Bitte bestätigen Sie kurz den Eingang dieses Auftrags.\n\nMit freundlichen Grüßen\nAuftraggeber"

        mailto_url = f"mailto:{firma_mail}?subject={quote(betreff)}&body={quote(text)}"
        QDesktopServices.openUrl(QUrl(mailto_url))


    def generate_haltungen_summary_text(self, row_data):
        """Generiert PLAIN TEXT Zusammenfassung für Mail-Body (kein HTML)."""
        try:
            details_rw_raw = row_data[17] if len(row_data) > 17 and row_data[17] else "{}"
            details_sw_raw = row_data[18] if len(row_data) > 18 and row_data[18] else "{}"
            details_mw_raw = row_data[19] if len(row_data) > 19 and row_data[19] else "{}"

            def parse_details(raw):
                try:
                    d = json.loads(raw)
                    return {
                        "laenge_tv": float(d.get("laenge_tv") or 0),
                        "anzahl_si": int(d.get("anzahl_si") or 0),
                        "anzahl_gal": int(d.get("anzahl_gal") or 0),
                        "anzahl_hal": int(d.get("anzahl_hal") or 0),
                    }
                except Exception:
                    return {"laenge_tv": 0.0, "anzahl_si": 0, "anzahl_gal": 0, "anzahl_hal": 0}

            rw = parse_details(details_rw_raw)
            sw = parse_details(details_sw_raw)
            mw = parse_details(details_mw_raw)

            if all(v == 0 for v in rw.values()) and \
            all(v == 0 for v in sw.values()) and \
            all(v == 0 for v in mw.values()):
                return "Keine Haltungsdaten vorhanden"

            lines = []
            if not all(v == 0 for v in rw.values()):
                lines.append(f"RW: {rw['laenge_tv']:.2f} m TV, {rw['anzahl_si']} Schächte, {rw['anzahl_gal']} GAL, {rw['anzahl_hal']} HAL")
            if not all(v == 0 for v in sw.values()):
                lines.append(f"SW: {sw['laenge_tv']:.2f} m TV, {sw['anzahl_si']} Schächte, {sw['anzahl_gal']} GAL, {sw['anzahl_hal']} HAL")
            if not all(v == 0 for v in mw.values()):
                lines.append(f"MW: {mw['laenge_tv']:.2f} m TV, {mw['anzahl_si']} Schächte, {mw['anzahl_gal']} GAL, {mw['anzahl_hal']} HAL")

            return "\n".join(lines)

        except Exception as e:
            print(f"[TABELLE-SUMMARY-ERROR] {e}")
            return "Fehler beim Laden der Haltungsdaten"

    def generate_haltungen_summary_from_details(self, details_rw_raw, details_sw_raw, details_mw_raw):
        """Generiert eine textuelle Zusammenfassung aus den JSON-Details (RW/SW/MW)."""

        def parse_details(raw):
            try:
                d = json.loads(raw) if raw else {}
                return {
                    "laenge_tv": float(d.get("laenge_tv") or 0),
                    "anzahl_si": int(d.get("anzahl_si") or 0),
                    "anzahl_gal": int(d.get("anzahl_gal") or 0),
                    "anzahl_hal": int(d.get("anzahl_hal") or 0),
                }
            except Exception:
                return {"laenge_tv": 0.0, "anzahl_si": 0, "anzahl_gal": 0, "anzahl_hal": 0}

        rw = parse_details(details_rw_raw)
        sw = parse_details(details_sw_raw)
        mw = parse_details(details_mw_raw)

        if all(v == 0 for v in rw.values()) and \
        all(v == 0 for v in sw.values()) and \
        all(v == 0 for v in mw.values()):
            return "Keine Haltungsdaten vorhanden"

        lines = []
        if not all(v == 0 for v in rw.values()):
            lines.append(
                f"RW: {rw['laenge_tv']:.2f} m TV, {rw['anzahl_si']} Schächte, "
                f"{rw['anzahl_gal']} GAL, {rw['anzahl_hal']} HAL"
            )
        if not all(v == 0 for v in sw.values()):
            lines.append(
                f"SW: {sw['laenge_tv']:.2f} m TV, {sw['anzahl_si']} Schächte, "
                f"{sw['anzahl_gal']} GAL, {sw['anzahl_hal']} HAL"
            )
        if not all(v == 0 for v in mw.values()):
            lines.append(
                f"MW: {mw['laenge_tv']:.2f} m TV, {mw['anzahl_si']} Schächte, "
                f"{mw['anzahl_gal']} GAL, {mw['anzahl_hal']} HAL"
            )

        return "\n".join(lines)




