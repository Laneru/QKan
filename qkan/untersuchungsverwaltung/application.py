# qkan/untersuchungsverwaltung/application.py

import os

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import plugins


class UntersuchungsverwaltungApplication:
    def __init__(self, iface):
        self.iface = iface
        self.dlg = None
        self.action = None

        self.plugin_dir = os.path.dirname(__file__)
        self.icon_path = os.path.join(self.plugin_dir, "Kostenermittlung.png")

        print("[Untersuchungsverwaltung] __init__")
        print(f"[Untersuchungsverwaltung] plugin_dir = {self.plugin_dir}")
        print(f"[Untersuchungsverwaltung] icon_path = {self.icon_path}")

    def _get_qkan_instance(self):
        qkan_plugin = plugins.get("qkan")
        print(f"[Untersuchungsverwaltung] qkan plugin instance = {qkan_plugin}")
        return qkan_plugin

    def initGui(self):
        print("[Untersuchungsverwaltung] initGui() gestartet")
        try:
            qkan_instance = self._get_qkan_instance()
            if qkan_instance is None:
                raise RuntimeError("QKan-Hauptinstanz konnte nicht gefunden werden.")

            icon_path = self.icon_path if os.path.exists(self.icon_path) else ""
            print(f"[Untersuchungsverwaltung] verwende icon_path = {icon_path}")

            self.action = qkan_instance.add_action(
                icon_path=icon_path,
                text="Untersuchungsverwaltung",
                toolbar="QKan-Allgemein",
                callback=self.run,
                parent=self.iface.mainWindow(),
            )
            print(f"[Untersuchungsverwaltung] QAction registriert: {self.action}")

        except Exception as e:
            print(f"[Untersuchungsverwaltung] initGui ERROR: {e}")
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Untersuchungsverwaltung",
                f"Fehler beim Registrieren des Tools:\n{e}",
            )

    def unload(self):
        print("[Untersuchungsverwaltung] unload()")
        if self.dlg is not None:
            try:
                self.dlg.close()
            except Exception as e:
                print(f"[Untersuchungsverwaltung] dlg close warning: {e}")
            self.dlg = None
        self.action = None

    def run(self):
        print("[Untersuchungsverwaltung] run()")
        try:
            if self.dlg is not None:
                try:
                    print("[Untersuchungsverwaltung] vorhandenen Dialog nach vorne holen")
                    self.dlg.show()
                    self.dlg.raise_()
                    self.dlg.activateWindow()
                    return
                except Exception as e:
                    print(f"[Untersuchungsverwaltung] reuse warning: {e}")
                    self.dlg = None

            print("[Untersuchungsverwaltung] erzeuge Dialog neu")
            from .Kostenermittlung_Tool import KostenermittlungTool
            self.dlg = KostenermittlungTool(parent=self)

            self.dlg.show()
            self.dlg.raise_()
            self.dlg.activateWindow()
            print("[Untersuchungsverwaltung] Dialog angezeigt")

        except Exception as e:
            print(f"[Untersuchungsverwaltung] run ERROR: {e}")
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Untersuchungsverwaltung",
                f"Fehler beim Starten der Untersuchungsverwaltung:\n{e}",
            )