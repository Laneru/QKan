# netzuebersicht/geometry_tools.py
from qgis.core import QgsVectorLayer, QgsProject, QgsGeometry
from qgis.PyQt import QtWidgets
from . import db_postgres
from .table_models import (
    setup_qt_sql_connection,
    load_data_into_tables,
    load_data_for_tab,
    filter_data,
    fill_column_combobox,
)

def get_id_column(table_name):
    """Hartcodierte ID-Spalten für alle bauwerke_* Tabellen."""
    id_map = {
        "bauwerke_pw": "pw_id",
        "bauwerke_rbf": "rbf_id", 
        "bauwerke_rkb": "rkb_id",
        "bauwerke_rrb": "rrb_id",
        "bauwerke_rue": "rue_id",
        "bauwerke_rueb": "rueb_id",
        "bauwerke_vs": "vs_id",
        "bauwerke_rv": "rv_id",
    }
    return id_map.get(table_name)

def frage_nach_geometrie(parent, entry_id, table_name):
    """Fragt nach Polygon- und optional Punkt-Geometrie nach Anlegen eines Sonderbauwerks."""
    reply = QtWidgets.QMessageBox.question(
        parent,
        "Geometrie anlegen",
        "Möchten Sie für dieses Sonderbauwerk eine Geometrie anlegen?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )
    if reply == QtWidgets.QMessageBox.Yes:
        add_polygon_to_sonderbauwerk(parent, entry_id, table_name)

def add_polygon_to_sonderbauwerk(parent, entry_id, table_name):
    """Fügt einem Sonderbauwerk eine Polygon-Geometrie hinzu."""
    crs = "EPSG:25832"
    temp_layer = QgsVectorLayer(f"MultiPolygon?crs={crs}", "Sonderbauwerk Polygon", "memory")
    QgsProject.instance().addMapLayer(temp_layer)
    temp_layer.startEditing()

    QtWidgets.QMessageBox.information(
        parent, "Polygon zeichnen",
        "Bitte zeichnen Sie ein Polygon im Layer 'Sonderbauwerk Polygon' und speichern Sie ab."
    )

    uebernehmen_btn = QtWidgets.QPushButton("Geometrie übernehmen")
    uebernehmen_btn.show()

    def uebernehme_polygon():
        features = list(temp_layer.getFeatures())
        if not features:
            QtWidgets.QMessageBox.warning(parent, "Fehler", "Kein Polygon gefunden.")
            return
        
        geom = features[0].geometry()
        if geom is None or geom.isEmpty():
            QtWidgets.QMessageBox.warning(parent, "Fehler", "Keine gültige Geometrie.")
            return
        
        if not geom.isGeosValid():
            geom = geom.makeValid()

        wkt = geom.asWkt()
        
        conn = db_postgres.load_postgres_connection(parent)
        if conn:
            try:
                id_col = get_id_column(table_name)
                if id_col:
                    cur = conn.cursor()
                    cur.execute(
                        f"UPDATE {table_name} SET geom = ST_GeomFromText(%s, 25832) WHERE {id_col} = (SELECT MAX({id_col}) FROM {table_name})",
                        (wkt,)
                    )
                    conn.commit()
                    QtWidgets.QMessageBox.information(parent, "Erfolg", "Polygon-Geometrie gespeichert.")
                    
                    # Nach Polygon → Punkt fragen
                    frage_nach_punkt(parent, entry_id, table_name)
                else:
                    QtWidgets.QMessageBox.warning(parent, "Fehler", f"ID-Spalte für {table_name} nicht gefunden.")
                    
            except Exception as e:
                QtWidgets.QMessageBox.critical(parent, "Fehler", f"Geometrie speichern fehlgeschlagen:\n{str(e)}")
            finally:
                conn.close()
        else:
            QtWidgets.QMessageBox.critical(parent, "Fehler", "Datenbankverbindung fehlgeschlagen.")
        
        # Cleanup
        QgsProject.instance().removeMapLayer(temp_layer.id())
        uebernehmen_btn.hide()

    uebernehmen_btn.clicked.connect(uebernehme_polygon)

def frage_nach_punkt(parent, entry_id, table_name):
    """Fragt nach optionaler Punkt-Geometrie."""
    reply = QtWidgets.QMessageBox.question(
        parent,
        "Punktgeometrie hinzufügen",
        "Möchten Sie diesem Sonderbauwerk auch eine Punktgeometrie (Position) hinzufügen?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )
    if reply == QtWidgets.QMessageBox.Yes:
        add_point_to_sonderbauwerk(parent, entry_id, table_name)

def add_point_to_sonderbauwerk(parent, entry_id, table_name):
    """Fügt einem Sonderbauwerk eine Punkt-Geometrie hinzu."""
    # Gleiche Logik wie bei Polygon, aber für geop
    crs = "EPSG:25832"
    temp_layer = QgsVectorLayer(f"Point?crs={crs}", "Sonderbauwerk Punkt", "memory")
    QgsProject.instance().addMapLayer(temp_layer)
    temp_layer.startEditing()

    QtWidgets.QMessageBox.information(
        parent, "Punkt zeichnen",
        "Bitte zeichnen Sie einen Punkt im Layer 'Sonderbauwerk Punkt' und speichern Sie ab."
    )

    uebernehmen_btn = QtWidgets.QPushButton("Position übernehmen")
    uebernehmen_btn.show()

    def uebernehme_punkt():
        features = list(temp_layer.getFeatures())
        if not features:
            QtWidgets.QMessageBox.warning(parent, "Fehler", "Kein Punkt gefunden.")
            return
        
        geom = features[0].geometry()
        if geom is None or geom.isEmpty():
            QtWidgets.QMessageBox.warning(parent, "Fehler", "Keine gültige Geometrie.")
            return

        wkt = geom.asWkt()
        
        conn = db_postgres.load_postgres_connection(parent)
        if conn:
            try:
                id_col = get_id_column(table_name)
                if id_col:
                    cur = conn.cursor()
                    cur.execute(
                        f"UPDATE {table_name} SET geop = ST_GeomFromText(%s, 25832) WHERE {id_col} = (SELECT MAX({id_col}) FROM {table_name})",
                        (wkt,)
                    )
                    conn.commit()
                    QtWidgets.QMessageBox.information(parent, "Erfolg", "Punkt-Position gespeichert.")
                else:
                    QtWidgets.QMessageBox.warning(parent, "Fehler", f"ID-Spalte für {table_name} nicht gefunden.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(parent, "Fehler", f"Punkt speichern fehlgeschlagen:\n{str(e)}")
            finally:
                conn.close()
        else:
            QtWidgets.QMessageBox.critical(parent, "Fehler", "Datenbankverbindung fehlgeschlagen.")
        
        # Cleanup
        QgsProject.instance().removeMapLayer(temp_layer.id())
        uebernehmen_btn.hide()

    uebernehmen_btn.clicked.connect(uebernehme_punkt)