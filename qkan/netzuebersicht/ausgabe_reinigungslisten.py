from qgis.core import (QgsProject, QgsVectorLayer, QgsFeature, QgsField, QgsFields, 
                       QgsGeometry, QgsWkbTypes, QgsProcessingFeedback, Qgis, QgsSpatialIndex, QgsFeatureRequest, QgsFields)
from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QComboBox, QPushButton, QMessageBox)
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant  # Für Feld-Typ

import processing  # Für Toolbox-Alternative+
from qgis.analysis import QgsNativeAlgorithms

class LinePolygonAggregateDialog(QDialog):
    """Dialog: Linien + Polygone auswählen → Neuer Layer mit aggregierten Attributen"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔗 Linien + Polygone aggregieren")
        self.resize(400, 150)
        
        layout = QVBoxLayout(self)
        
        # Linien-Layer Auswahl
        layout.addWidget(QLabel("Linien-Layer (z.B. Kanalhaltungen):"))
        self.line_combo = QComboBox()
        self.populate_layers(QgsWkbTypes.LineGeometry)
        layout.addWidget(self.line_combo)
        
        # Polygon-Layer Auswahl
        layout.addWidget(QLabel("Polygon-Layer (z.B. Rahmen):"))
        self.poly_combo = QComboBox()
        self.populate_layers(QgsWkbTypes.PolygonGeometry)
        layout.addWidget(self.poly_combo)
        
        # Polygon-Feld Auswahl (dynamisch)
        self.poly_field_combo = QComboBox()
        self.poly_field_combo.setEnabled(False)
        layout.addWidget(QLabel("Polygon-Feld zum Aggregieren:"))
        layout.addWidget(self.poly_field_combo)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("🚀 Neuen Layer erstellen")
        self.run_btn.clicked.connect(self.create_aggregated_layer)
        btn_layout.addWidget(self.run_btn)
        
        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        # Events
        self.poly_combo.currentTextChanged.connect(self.update_poly_fields)
    
    def populate_layers(self, wkb_type):
        """Füllt ComboBox mit passenden Layern"""
        layers = [l for l in QgsProject.instance().mapLayers().values() 
                if isinstance(l, QgsVectorLayer) and l.geometryType() == wkb_type]
        
        # FIX: str() statt len() – featureCount() ist schon int!
        names = [f"{l.name()} ({l.featureCount()} Features)" for l in layers]
        
        if wkb_type == QgsWkbTypes.LineGeometry:
            self.line_combo.addItems(names)
        else:
            self.poly_combo.addItems(names)

    
    def update_poly_fields(self):
        """Aktualisiert Polygon-Feld-Liste"""
        self.poly_field_combo.clear()
        poly_layer = self.get_selected_layer(self.poly_combo)
        if poly_layer:
            self.poly_field_combo.addItems([f.name() for f in poly_layer.fields()])
            self.poly_field_combo.setEnabled(True)
    
    def get_selected_layer(self, combo):
        """Holt Layer aus ComboBox-Text"""
        text = combo.currentText()
        if not text: return None
        name = text.split(" (")[0]
        return QgsProject.instance().mapLayersByName(name)[0]
    
    def create_aggregated_layer(self):
        """✅ PyQGIS pur: Spatial Index Join (Schnell & sicher!)"""
        line_layer = self.get_selected_layer(self.line_combo)
        poly_layer = self.get_selected_layer(self.poly_combo)
        poly_field = self.poly_field_combo.currentText()
        
        if not all([line_layer, poly_layer, poly_field]):
            QMessageBox.warning(self, "Fehler", "Alle Felder ausfüllen!")
            return

        # 1. Linien-Layer duplizieren (Memory Layer)
        # Wir erstellen einen neuen Memory-Layer mit denselben Feldern + polygon_info
        new_fields = QgsFields(line_layer.fields())
        new_fields.append(QgsField("polygon_info", QVariant.String))
        
        vl = QgsVectorLayer(f"LineString?crs={line_layer.crs().authid()}", 
                            f"{line_layer.name()}_mit_{poly_layer.name()}", "memory")
        dp = vl.dataProvider()
        dp.addAttributes(new_fields)
        vl.updateFields()
        
        # 2. Spatial Index für Polygone aufbauen (für Speed!)
        print("🔧 Baue Spatial Index...")
        poly_index = QgsSpatialIndex()
        poly_features = {}  # Cache für Attribute {id: wert}
        
        # Hole alle Polygon-Features & fülle Index
        # Wichtig: Wir holen nur Geometrie und das gewünschte Feld
        req = QgsFeatureRequest().setSubsetOfAttributes([poly_field], poly_layer.fields())
        for p_feat in poly_layer.getFeatures(req):
            poly_index.insertFeature(p_feat)
            poly_features[p_feat.id()] = str(p_feat[poly_field]) # Als String speichern!

        # 3. Linien iterieren und verschneiden
        print("🚀 Starte Join...")
        new_features = []
        
        # Iteriere über alle Linien
        line_req = QgsFeatureRequest() # Alle Attribute
        total = line_layer.featureCount()
        count = 0
        
        for l_feat in line_layer.getFeatures(line_req):
            l_geom = l_feat.geometry()
            
            # Kandidaten über Bounding Box (schnell)
            candidate_ids = poly_index.intersects(l_geom.boundingBox())
            
            found_values = set()
            for pid in candidate_ids:
                # Exakte Prüfung (intersects) - da wir Features nicht direkt haben, 
                # müssten wir Geometrie holen. Optimierung:
                # Für "intersects" reicht oft der Index wenn Polygone groß sind, aber sauberer:
                # Wir holen Geometrie aus dem Layer für exakten Test
                # (Um Performance zu sparen, testen wir hier NUR BB-Intersection + Index-Treffer. 
                # Für exaktes 'intersects' bräuchte man p_geom. Das ist teurer.
                # Wenn Index genau genug ist (Rahmen), reicht das oft.
                # Für 100% Exaktheit: Geometry cachen!)
                
                # Bessere Variante: Wir haben Geometrie nicht im Cache. 
                # Aber wir können intersect() prüfen, wenn wir p_feat holen.
                # Da das langsam sein kann, holen wir p_feat via ID.
                
                p_feat = poly_layer.getFeature(pid)
                if l_geom.intersects(p_feat.geometry()):
                    val = str(p_feat[poly_field])
                    if val: # Keine leeren Werte
                        found_values.add(val)
            
            # Aggregieren
            info_str = ", ".join(sorted(found_values))
            
            # Neues Feature bauen
            new_feat = QgsFeature(new_fields)
            new_feat.setGeometry(l_geom)
            
            # Attribute kopieren
            attrs = l_feat.attributes()
            attrs.append(info_str) # Neues Feld am Ende
            new_feat.setAttributes(attrs)
            
            new_features.append(new_feat)
            
            count += 1
            if count % 100 == 0:
                print(f"   {count}/{total} Linien verarbeitet...")

        # 4. Features hinzufügen
        dp.addFeatures(new_features)
        vl.updateExtents()
        
        QgsProject.instance().addMapLayer(vl)
        QMessageBox.information(self, "✅ Erfolg", 
                            f"Layer '{vl.name()}' erstellt!\n"
                            f"{len(new_features)} Linien prozessiert.\n"
                            f"Polygon-Infos in Feld 'polygon_info'.")
        self.accept()





    def _fallback_processing(self, line_layer, poly_layer, poly_field):
        """Processing Join mit Debug (korrekte native:joinbylocationsummary)"""
        try:
            params = {
                'INPUT': line_layer,
                'JOIN': poly_layer,
                'PREDICATE': [0],  # 0 = intersects
                'JOIN_FIELDS': [poly_field],  # Liste mit Feldnamen
                'SUMMARIES': [5],  # 5 = concatenate_unique
                'DISCARD_NONMATCHING': False,  # Alle Linien behalten
                'OUTPUT': 'TEMPORARY_OUTPUT'
            }
            
            print(f"🔧 Processing: JOIN_FIELDS=['{poly_field}'], SUMMARIES=[5]")
            print(f"   Linien: {line_layer.name()} ({line_layer.featureCount()})")
            print(f"   Polygone: {poly_layer.name()} ({poly_layer.featureCount()})")
            
            result = processing.run('native:joinbylocationsummary', params)
            
            if result and 'OUTPUT' in result:
                new_layer = result['OUTPUT']
                
                # Debug: Felder prüfen
                field_names = [f.name() for f in new_layer.fields()]
                print(f"📋 Joined Layer Felder ({len(field_names)}): {field_names}")
                
                # Debug: Erste Feature-Werte
                try:
                    feat = next(new_layer.getFeatures())
                    print(f"📊 Erste Feature-Werte: {feat.attributes()[:10]}")
                except StopIteration:
                    print("   ⚠️ Keine Features im Joined Layer!")
                
                QgsProject.instance().addMapLayer(new_layer)
                
                # Finde aggregiertes Feld (meist {poly_field}_concatenate_unique)
                agg_field = f"{poly_field}_concatenate_unique"
                if agg_field in field_names:
                    msg = f"Feld '{agg_field}' enthält aggregierte Werte."
                else:
                    msg = f"Felder: {', '.join(field_names[-5:])}"
                
                QMessageBox.information(self, "✅ Erfolg (Processing)", 
                                    f"Layer '{new_layer.name()}' erstellt!\n"
                                    f"{new_layer.featureCount()} Features.\n{msg}")
                self.accept()
            else:
                QMessageBox.critical(self, "Fehler", "Kein OUTPUT von Processing!")
                print(f"   Result: {result}")
                
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"❌ Processing Fehler:\n{error_msg}")
            QMessageBox.critical(self, "Fehler", 
                                f"Processing-Error:\n{str(e)}\n\nSiehe Console für Details.")







# Zum Plugin-Button hinzufügen:
def on_aggregate_button_clicked(self):
    """Button-Handler in deinem Haupt-Widget"""
    dialog = LinePolygonAggregateDialog(self)
    dialog.exec_()
