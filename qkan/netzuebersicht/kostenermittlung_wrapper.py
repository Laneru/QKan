# netzuebersicht/kostenermittlung_wrapper.py
from qgis.utils import iface
from .gis_actions import select_feature

# Importiere die Klasse aus dem Modul
from ..untersuchungsverwaltung.Kostenermittlung_Tool import KostenermittlungTool


def kostenermittlung_wrapper(self):
    select_feature(self)

    # Instanz der Klasse erzeugen, parent übergeben
    kostenermittlung_tool = KostenermittlungTool(self)

    layer = iface.activeLayer()
    selected_features = [f for f in layer.selectedFeatures()]

    # kostenermittlung_tool.populateTableWidget(selected_features)
    kostenermittlung_tool.exec()
