# untersuchungsverwaltung/pdf_template_editor.py
import os
import shutil
from qgis.PyQt import QtWidgets, QtGui, QtCore


class PdfTemplateEditor(QtWidgets.QWidget):
    """
    Eigenständiger Rich-Text-Editor für PDF-Vorlagen:
    - Toolbar mit Schriftart, Größe, Fett/Kursiv/Unterstrichen, Farbe, Ausrichtung
    - Platzhalter-Auswahl für DB-Felder
    - Medien-Einfügen (Bilder/Videos als HTML-Verweise)
    - HTML-Quelltext-Ansicht umschaltbar
    """

    def __init__(self, parent=None, base_dir=None):
        super().__init__(parent)

        # Platzhalter-Liste (wird von außen befüllt)
        self.placeholders = []  # Liste von Strings wie "{projektname}"

        # Basis-Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- Toolbar erstellen ---
        self.toolbar = QtWidgets.QHBoxLayout()

        # 0. Platzhalter-Auswahl
        self.combo_placeholder = QtWidgets.QComboBox()
        self.combo_placeholder.setToolTip("Platzhalter auswählen")
        self.combo_placeholder.setEditable(False)
        self.combo_placeholder.setFixedWidth(180)

        self.btn_insert_placeholder = self.create_toolbar_btn(
            "Platzhalter einfügen",
            self.insert_selected_placeholder,
            checkable=False,
            tooltip="Ausgewählten Platzhalter einfügen"
        )

        # 1. Schriftart
        self.combo_font = QtWidgets.QFontComboBox()
        self.combo_font.setToolTip("Schriftart")
        self.combo_font.setFontFilters(QtWidgets.QFontComboBox.ScalableFonts)
        self.combo_font.currentTextChanged.connect(self.set_font_family)
        self.combo_font.setFixedWidth(140)

        # 2. Schriftgröße
        self.combo_size = QtWidgets.QComboBox()
        self.combo_size.setToolTip("Größe")
        self.combo_size.setEditable(True)
        self.combo_size.addItems(
            [str(s) for s in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]]
        )
        self.combo_size.setCurrentText("10")
        self.combo_size.currentTextChanged.connect(self.set_font_size)
        self.combo_size.setFixedWidth(60)

        # 3. Stil-Buttons
        self.btn_bold = self.create_toolbar_btn(
            "B", self.toggle_bold, checkable=True, tooltip="Fett (Strg+B)"
        )
        self.btn_bold.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))

        self.btn_italic = self.create_toolbar_btn(
            "I", self.toggle_italic, checkable=True, tooltip="Kursiv (Strg+I)"
        )
        self.btn_italic.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.StyleItalic))

        self.btn_underline = self.create_toolbar_btn(
            "U", self.toggle_underline, checkable=True, tooltip="Unterstrichen (Strg+U)"
        )
        font_u = QtGui.QFont("Arial", 10)
        font_u.setUnderline(True)
        self.btn_underline.setFont(font_u)

        # 4. Ausrichtung
        self.btn_align_left = self.create_toolbar_btn(
            "⇤", lambda: self.set_alignment(QtCore.Qt.AlignLeft),
            checkable=True, tooltip="Linksbündig"
        )
        self.btn_align_center = self.create_toolbar_btn(
            "↔", lambda: self.set_alignment(QtCore.Qt.AlignCenter),
            checkable=True, tooltip="Zentriert"
        )
        self.btn_align_right = self.create_toolbar_btn(
            "⇥", lambda: self.set_alignment(QtCore.Qt.AlignRight),
            checkable=True, tooltip="Rechtsbündig"
        )

        # 5. Textfarbe
        self.btn_color = self.create_toolbar_btn(
            "", self.choose_text_color, tooltip="Textfarbe ändern"
        )
        self.update_color_icon(QtGui.QColor("black"))

        # 6. Medien
        self.btn_media = self.create_toolbar_btn(
            "🖼 Medien", self.insert_media, tooltip="Bild oder Video einfügen"
        )

        # 7. HTML-Ansicht
        self.btn_html = self.create_toolbar_btn(
            "HTML", self.toggle_source_view, checkable=True, tooltip="Quelltext anzeigen"
        )

        # Toolbar zusammenbauen
        widgets = [
            self.combo_placeholder, self.btn_insert_placeholder,
            self.combo_font, self.combo_size,
            self.btn_bold, self.btn_italic, self.btn_underline, self.btn_color,
            self.btn_align_left, self.btn_align_center, self.btn_align_right,
            self.btn_media
        ]
        for w in widgets:
            self.toolbar.addWidget(w)

        self.toolbar.addStretch()
        self.toolbar.addWidget(self.btn_html)
        layout.addLayout(self.toolbar)

        # --- Editor-Bereich ---
        self.stack = QtWidgets.QStackedWidget()

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setStyleSheet(
            "QTextEdit { font-family: 'MS Shell Dlg 2'; font-size: 10pt; }"
        )

        self.source_edit = QtWidgets.QPlainTextEdit()
        font_mono = QtGui.QFont("Courier New")
        font_mono.setStyleHint(QtGui.QFont.Monospace)
        self.source_edit.setFont(font_mono)

        self.stack.addWidget(self.text_edit)
        self.stack.addWidget(self.source_edit)
        layout.addWidget(self.stack)

        # Signale für Format-Buttons aktualisieren
        self.text_edit.currentCharFormatChanged.connect(self.update_format_buttons)
        self.text_edit.cursorPositionChanged.connect(self.update_format_buttons)

        # Base-URL für relative Medienpfade
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        if not base_dir.endswith(os.sep):
            base_dir += os.sep
        self.base_dir = base_dir
        base_url = QtCore.QUrl.fromLocalFile(base_dir)
        self.text_edit.document().setBaseUrl(base_url)

    # --- Platzhalter-API ---

    def set_placeholders(self, placeholders):
        """
        Erwartet eine Liste von Strings, z.B. ["{projektname}", "{strasse}", ...]
        """
        self.placeholders = list(placeholders) if placeholders else []
        self.combo_placeholder.blockSignals(True)
        self.combo_placeholder.clear()
        if self.placeholders:
            self.combo_placeholder.addItems(self.placeholders)
        self.combo_placeholder.blockSignals(False)

    def insert_selected_placeholder(self):
        text = self.combo_placeholder.currentText()
        if not text:
            return
        self.text_edit.setFocus()
        self.text_edit.insertPlainText(text)

    # --- Helper für Toolbar-Buttons ---

    def create_toolbar_btn(self, text, slot, checkable=False, tooltip=""):
        btn = QtWidgets.QPushButton(text)
        if checkable:
            btn.setCheckable(True)
        btn.setFixedWidth(30 if len(text) < 3 else 120 if "Platzhalter" in text else 80)
        btn.setToolTip(tooltip)
        btn.clicked.connect(slot)
        return btn

    # --- Formatierungsmethoden ---

    def set_font_family(self, font_name):
        if not font_name:
            return
        self.text_edit.setFocus()
        cursor = self.text_edit.textCursor()

        fmt = QtGui.QTextCharFormat()
        try:
            fmt.setFontFamilies([font_name])
        except AttributeError:
            fmt.setFontFamily(font_name)

        if cursor.hasSelection():
            cursor.mergeCharFormat(fmt)
        else:
            new_fmt = cursor.charFormat()
            try:
                new_fmt.setFontFamilies([font_name])
            except AttributeError:
                new_fmt.setFontFamily(font_name)
            self.text_edit.setCurrentCharFormat(new_fmt)

    def set_font_size(self, size_str):
        self.text_edit.setFocus()
        try:
            val = float(size_str)
            if val > 0:
                fmt = QtGui.QTextCharFormat()
                fmt.setFontPointSize(val)
                self.text_edit.mergeCurrentCharFormat(fmt)
        except ValueError:
            pass

    def toggle_bold(self):
        self.text_edit.setFocus()
        weight = QtGui.QFont.Bold if self.btn_bold.isChecked() else QtGui.QFont.Normal
        self.text_edit.setFontWeight(weight)

    def toggle_italic(self):
        self.text_edit.setFocus()
        self.text_edit.setFontItalic(self.btn_italic.isChecked())

    def toggle_underline(self):
        self.text_edit.setFocus()
        self.text_edit.setFontUnderline(self.btn_underline.isChecked())

    def set_alignment(self, alignment):
        self.text_edit.setFocus()
        self.text_edit.setAlignment(alignment)
        self.update_format_buttons()

    def choose_text_color(self):
        cursor = self.text_edit.textCursor()
        current_color = cursor.charFormat().foreground().color()
        if not current_color.isValid():
            current_color = QtGui.QColor("black")

        col = QtWidgets.QColorDialog.getColor(current_color, self, "Textfarbe wählen")
        if col.isValid():
            self.text_edit.setFocus()
            fmt = QtGui.QTextCharFormat()
            fmt.setForeground(col)
            self.text_edit.mergeCurrentCharFormat(fmt)
            self.update_color_icon(col)

    def update_color_icon(self, color):
        if not color.isValid():
            color = QtGui.QColor("black")

        pixmap = QtGui.QPixmap(26, 26)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        font = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor("black"))
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "A")

        painter.fillRect(4, 21, 18, 4, color)
        painter.end()

        self.btn_color.setIcon(QtGui.QIcon(pixmap))

    # --- UI-Update-Logik ---

    def update_format_buttons(self, fmt=None):
        if self.stack.currentIndex() == 1:
            return
        if not isinstance(fmt, QtGui.QTextCharFormat):
            fmt = self.text_edit.currentCharFormat()

        self.block_signals_all(True)

        self.btn_bold.setChecked(fmt.font().bold())
        self.btn_italic.setChecked(fmt.fontItalic())
        self.btn_underline.setChecked(fmt.fontUnderline())
        self.combo_font.setCurrentFont(fmt.font())

        size = fmt.fontPointSize()
        if size <= 0:
            size = fmt.font().pointSize()
        if size <= 0:
            size = 10
        self.combo_size.setCurrentText(str(int(size)))

        col = fmt.foreground().color()
        self.update_color_icon(col)

        cursor = self.text_edit.textCursor()
        align = cursor.blockFormat().alignment()
        self.btn_align_left.setChecked(
            bool(align & QtCore.Qt.AlignLeft or align & QtCore.Qt.AlignLeading)
        )
        self.btn_align_center.setChecked(bool(align & QtCore.Qt.AlignCenter))
        self.btn_align_right.setChecked(bool(align & QtCore.Qt.AlignRight))

        self.block_signals_all(False)

    def block_signals_all(self, block):
        for w in [
            self.btn_bold, self.btn_italic, self.btn_underline,
            self.combo_font, self.combo_size,
            self.btn_align_left, self.btn_align_center, self.btn_align_right
        ]:
            w.blockSignals(block)

    # --- Medien einfügen ---

    def insert_media(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Bild oder Video auswählen",
            "",
            "Medien (*.png *.jpg *.jpeg *.gif *.mp4 *.webm);;"
            "Bilder (*.png *.jpg *.jpeg *.gif);;"
            "Videos (*.mp4 *.webm)"
        )
        if not file_path:
            return

        base_dir = self.base_dir
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        is_video = ext in ['.mp4', '.webm', '.mkv']
        subfolder = 'videos' if is_video else 'images'

        target_dir = os.path.join(base_dir, subfolder)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_path = os.path.join(target_dir, filename)

        if os.path.abspath(file_path) != os.path.abspath(target_path):
            try:
                shutil.copy2(file_path, target_path)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Fehler", f"Konnte Datei nicht kopieren: {e}")
                return

        props = self.ask_media_properties(filename, is_video)
        if not props:
            return

        rel_path = f"{subfolder}/{filename}"

        style = ""
        if props['align'] == 'center':
            style = "display: block; margin-left: auto; margin-right: auto;"
        elif props['align'] == 'left':
            style = "float: left; margin-right: 15px; margin-bottom: 10px;"
        elif props['align'] == 'right':
            style = "float: right; margin-left: 15px; margin-bottom: 10px;"

        if props['width']:
            style += f" width: {props['width']}px;"

        if is_video:
            html = f"""
            <div class="video-container" style="text-align: {props['align']}; margin: 10px 0;">
                <p><b>Video:</b> {filename}</p>
                <a href="{rel_path}">
                    ▶ Video abspielen ({filename})
                </a>
            </div>
            """
        else:
            html = f'<img src="{rel_path}" alt="{props["alt"]}" style="{style}">'
            if props['caption']:
                html = f"""
                <div class="img-wrapper" style="text-align: {props['align']};">
                    {html}
                    <div class="caption" style="font-size: 0.9em; color: #666;">{props['caption']}</div>
                </div>
                """

        self.text_edit.insertHtml(html)

    def ask_media_properties(self, filename, is_video):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Medien Eigenschaften")
        layout = QtWidgets.QFormLayout(dlg)

        spin_width = QtWidgets.QSpinBox()
        spin_width.setRange(50, 2000)
        spin_width.setValue(600 if is_video else 400)
        spin_width.setSuffix(" px")
        layout.addRow("Breite:", spin_width)

        combo_align = QtWidgets.QComboBox()
        combo_align.addItems(["Links", "Zentriert", "Rechts"])
        combo_align.setCurrentIndex(1)
        layout.addRow("Ausrichtung:", combo_align)

        edit_alt = QtWidgets.QLineEdit()
        edit_alt.setText(filename)
        layout.addRow("Beschreibung (Alt):", edit_alt)

        edit_caption = QtWidgets.QLineEdit()
        layout.addRow("Unterschrift:", edit_caption)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        layout.addRow(btns)

        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            align_map = {0: 'left', 1: 'center', 2: 'right'}
            return {
                'width': spin_width.value(),
                'align': align_map[combo_align.currentIndex()],
                'alt': edit_alt.text(),
                'caption': edit_caption.text()
            }
        return None

    # --- HTML-Ansicht umschalten ---

    def toggle_source_view(self, show_source):
        if show_source:
            self.source_edit.setPlainText(self.text_edit.toHtml())
            self.stack.setCurrentIndex(1)
            self.enable_controls(False)
        else:
            self.text_edit.setHtml(self.source_edit.toPlainText())
            self.stack.setCurrentIndex(0)
            self.enable_controls(True)

    def enable_controls(self, enable):
        for i in range(self.toolbar.count() - 1):  # letztes Element ist HTML-Button
            item = self.toolbar.itemAt(i)
            if not item:
                continue
            w = item.widget()
            if w:
                w.setEnabled(enable)

    # --- API für außen ---

    def get_html(self):
        if self.stack.currentIndex() == 1:
            return self.source_edit.toPlainText()
        return self.text_edit.toHtml()

    def set_html(self, html):
        self.text_edit.setHtml(html)
        self.source_edit.setPlainText(html)
        self.update_format_buttons()
