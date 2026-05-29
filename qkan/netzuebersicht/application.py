# qkan/netzuebersicht/application.py
import os

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import plugins

from .netzuebersicht_db_dialog import Netzuebersicht_DB


class NetzuebersichtPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dlg = None
        self.action = None

        self.plugin_dir = os.path.dirname(__file__)
        self.icon_path = os.path.join(self.plugin_dir, "Netzübersicht.png")

        print("[Netzuebersicht] __init__")
        print(f"[Netzuebersicht] plugin_dir = {self.plugin_dir}")
        print(f"[Netzuebersicht] icon_path = {self.icon_path}")

    def _get_qkan_instance(self):
        qkan_plugin = plugins.get("qkan")
        print(f"[Netzuebersicht] qkan plugin instance = {qkan_plugin}")
        return qkan_plugin

    def initGui(self):
        print("[Netzuebersicht] initGui() gestartet")
        try:
            qkan_instance = self._get_qkan_instance()
            if qkan_instance is None:
                raise RuntimeError("QKan-Hauptinstanz konnte nicht gefunden werden.")

            icon_path = self.icon_path if os.path.exists(self.icon_path) else ""
            print(f"[Netzuebersicht] verwende icon_path = {icon_path}")

            self.action = qkan_instance.add_action(
                icon_path=icon_path,
                text="Netzübersicht",
                toolbar="QKan-Allgemein",
                callback=self.run,
                parent=self.iface.mainWindow(),
            )
            print(f"[Netzuebersicht] QAction registriert: {self.action}")

        except Exception as e:
            print(f"[Netzuebersicht] initGui ERROR: {e}")
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Netzübersicht",
                f"Fehler beim Registrieren des Tools:\n{e}",
            )

    def unload(self):
        print("[Netzuebersicht] unload()")
        if self.dlg is not None:
            try:
                from .db_backend import get_backend
                backend = get_backend()
                backend.cleanup(self.dlg)
            except Exception as e:
                print(f"[Netzuebersicht] backend cleanup warning: {e}")
            try:
                self.dlg.close()
            except Exception as e:
                print(f"[Netzuebersicht] dlg close warning: {e}")
            self.dlg = None
        self.action = None

    def run(self):
        print("[Netzuebersicht] run()")
        try:
            # alten Dialog inkl. Verbindungen entsorgen
            if self.dlg is not None:
                try:
                    print("[Netzuebersicht] schließe alten Dialog")
                    self.dlg.close()
                except Exception as e:
                    print(f"[Netzuebersicht] close warning: {e}")
                self.dlg = None

            print("[Netzuebersicht] erzeuge Dialog neu")
            self.dlg = Netzuebersicht_DB(parent=self.iface.mainWindow())

            self.dlg.show()
            self.dlg.raise_()
            self.dlg.activateWindow()
            print("[Netzuebersicht] Dialog angezeigt")
        except Exception as e:
            print(f"[Netzuebersicht] run ERROR: {e}")
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Netzübersicht",
                f"Fehler beim Starten der Netzübersicht:\n{e}",
            )