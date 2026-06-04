import os
import shutil
from typing import Callable, Optional

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QWidget,
    QRadioButton
)
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
)

from qgis.gui import QgsProjectionSelectionWidget

from qkan import QKan, enums
from ..utils import get_logger, QkanError

logger = get_logger("QKan.floodTools.application_dialog")


class _Dialog(QDialog):
    def __init__(
        self,
        default_dir: str,
        tr: Callable,
        parent: Optional[QWidget] = None,
    ):
        # noinspection PyArgumentList
        super().__init__(parent)
        self.setupUi(self)
        self.default_dir = default_dir
        self.tr = tr


ANIMATION_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "res", "animation_dialog_base.ui")
)


class AnimationDialog(_Dialog, ANIMATION_CLASS):  # type: ignore
    tf_database: QLineEdit
    tf_import: QLineEdit
    tf_project: QLineEdit

    pb_database: QPushButton
    pb_import: QPushButton
    pb_project: QPushButton

    pw_epsg: QgsProjectionSelectionWidget

    pb_import_gdb: QPushButton

    cb_velo: QCheckBox
    cb_wlevel: QCheckBox
    cb_selected: QCheckBox
    cb_syncSelections: QCheckBox

    tf_faktor_v: QLineEdit
    tf_min_w: QLineEdit
    tg_min_v: QLineEdit
    tf_selected: QLineEdit

    rb_v1 : QRadioButton
    rb_v2 : QRadioButton

    def __init__(
        self,
        iface,
        default_dir: str,
        tr: Callable,
        parent: Optional[QWidget] = None,
    ):
        # noinspection PyCallByClass,PyArgumentList
        super().__init__(default_dir, tr, parent)

        self.iface = iface
        # Attach events
        self.pb_import.clicked.connect(self.select_import)
        self.pb_project.clicked.connect(self.select_project)
        self.pb_database.clicked.connect(self.select_database)
        self.pb_import_gdb.clicked.connect(self.import_gdb)
        self.button_box.helpRequested.connect(self.click_help)

        # Init fields
        self.tf_database.setText(QKan.config.flood.database)
        self.tf_import.setText(QKan.config.flood.import_dir)
        # noinspection PyCallByClass,PyArgumentList
        self.pw_epsg.setCrs(QgsCoordinateReferenceSystem.fromEpsgId(QKan.config.epsg))
        self.tf_project.setText(QKan.config.project.file)

        self.cb_velo.setChecked(QKan.config.flood.velo)
        self.cb_wlevel.setChecked(QKan.config.flood.wlevel)
        self.cb_gdb_remove.setChecked(QKan.config.flood.gdblayer)
        self.cb_syncSelections.setChecked(QKan.config.flood.syncSelections)

        self.tf_faktor_v.setText(str(QKan.config.flood.faktor_v))
        self.tf_min_v.setText(str(QKan.config.flood.min_v))
        self.tf_min_w.setText(str(QKan.config.flood.min_w))

        if QKan.config.flood.mikeversion == enums.MikeVersion.v1:
            self.rb_v1.setChecked(True)
        elif QKan.config.flood.mikeversion == enums.MikeVersion.v2:
            self.rb_v2.setChecked(True)
        else:
            logger.error_code(f'Keine gültige Mike-Version: {QKan.config.flood.mikeversion}')
            raise QkanError

        self.layervelo = None           # dient zur Verwaltung des selected-Signals
        self.layerwlevel = None         # dient zur Verwaltung des selected-Signals

    def select_import(self) -> None:
        # noinspection PyArgumentList,PyCallByClass
        dirname = QFileDialog.getExistingDirectory (
            self,
            self.tr("Zu importierendes Geodatabase-Verzeichnis"),
            self.default_dir,
        )
        if dirname:
            self.tf_import.setText(dirname)
            self.default_dir = os.path.dirname(dirname)

    def select_project(self) -> None:
        # noinspection PyArgumentList,PyCallByClass
        filename, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Zu erstellende Projektdatei"),
            self.default_dir,
            "*.qgs",
        )
        if filename:
            self.tf_project.setText(filename)
            self.default_dir = os.path.dirname(filename)

    def select_database(self) -> None:
        # noinspection PyArgumentList,PyCallByClass
        filename, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Zu erstellende SQLite-Datei"),
            self.default_dir,
            "*.sqlite",
        )
        if filename:
            self.tf_database.setText(filename)
            self.default_dir = os.path.dirname(filename)

    def import_gdb(self) -> None:
        """Import der beiden Ergebnisdateien aus der Geodatabase"""
        if self.rb_v1.isChecked():
            self.tabnam_velo = 'result2d__velocity'
            self.tabnam_wlevel = 'result2d__topo_decimated'
        elif self.rb_v2.isChecked():
            self.tabnam_velo = "velocity"
            self.tabnam_wlevel = "topo_decimated"
        else:
            logger.error_code(f'Keine gültige Mike-Version: {QKan.config.flood.mikeversion}')
            raise QkanError
        logger.debug(f'Mike-Version: {QKan.config.flood.mikeversion}')

        self.db_name =  QKan.config.flood.database = self.tf_database.text()
        self.gdblayer_choice = self.cb_gdb_remove.isChecked()
        self.import_dir = QKan.config.flood.import_dir = self.tf_import.text()
        self.epsg = QKan.config.epsg
        QKan.config.project.file = self.tf_project.text()

        datenbank_qkan_template = os.path.join(QKan.template_dir, "qkan.sqlite")
        shutil.copyfile(datenbank_qkan_template, self.db_name)

        # Make sure that path includes 'Result2D.gdb'
        if 'Result2D.gdb' not in self.import_dir:
            result_dir = os.path.join(self.import_dir, 'Result2D.gdb|layername=Velocity')
        else:
            result_dir = self.import_dir.replace('Result2D.gdb', 'Result2D.gdb|layername=Velocity')
        logger.debug(f'floodTools._animation.run.velo: {result_dir=}')

        vlayer = QgsVectorLayer(
            result_dir,
            self.tabnam_velo,
            "ogr"
        )
        vlayer.setCrs(QgsCoordinateReferenceSystem.fromEpsgId(self.epsg))
        QgsProject.instance().addMapLayer(vlayer)

        o_save_options = QgsVectorFileWriter.SaveVectorOptions()
        o_save_options.layerName = 'velocities'
        o_save_options.driverName = 'SQLite'
        o_save_options.fileEncoding = 'utf-8'
        o_save_options.onlySelectedFeatures = False
        # o_save_options.layerOptions = ['SPATIALITE=YES']
        o_save_options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        erg = QgsVectorFileWriter.writeAsVectorFormatV3(
            layer=vlayer,
            fileName=self.db_name,
            transformContext=QgsCoordinateTransformContext(),
            options=o_save_options
        )

        if not self.gdblayer_choice:
            QgsProject.instance().removeMapLayer(vlayer.id())

        # Make sure that path includes 'Result2D.gdb'
        if 'Result2D.gdb' not in self.import_dir:
            result_dir = os.path.join(self.import_dir, 'Result2D.gdb|layername=Topo_Decimated')
        else:
            result_dir = self.import_dir.replace('Result2D.gdb', 'Result2D.gdb|layername=Topo_Decimated')
        logger.debug(f'floodTools._animation.run.wlevel: {result_dir=}')

        vlayer = QgsVectorLayer(
            result_dir,
            self.tabnam_wlevel,
            "ogr"
        )
        vlayer.setCrs(QgsCoordinateReferenceSystem.fromEpsgId(self.epsg))
        QgsProject.instance().addMapLayer(vlayer)

        o_save_options = QgsVectorFileWriter.SaveVectorOptions()
        o_save_options.layerName = 'waterlevels'
        o_save_options.driverName = 'SQLite'
        o_save_options.fileEncoding = 'utf-8'
        o_save_options.onlySelectedFeatures = False
        # o_save_options.layerOptions = ['SPATIALITE=YES']
        o_save_options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        erg = QgsVectorFileWriter.writeAsVectorFormatV3(
            layer=vlayer,
            fileName=self.db_name,
            transformContext=QgsCoordinateTransformContext(),
            options=o_save_options
        )

        if not self.gdblayer_choice:
            QgsProject.instance().removeMapLayer(vlayer.id())

        vlayer = QgsVectorLayer(
            self.db_name + '|layername=waterlevels',
            "waterlevels",
            "ogr"
        )
        QgsProject.instance().addMapLayer(vlayer)
        qmlfile = os.path.join(QKan.template_dir, 'qml', "waterlevels.qml")
        try:
            vlayer.loadNamedStyle(qmlfile)
        except:
            logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
            QkanError()

        vlayer.selectionChanged.connect(self.selChanged)
        self.layerwlevel = vlayer

        vlayer = QgsVectorLayer(
            self.db_name + f'|layername=velocities',
            "velocities",
            "ogr"
        )

        QgsProject.instance().addMapLayer(vlayer)
        qmlfile = os.path.join(QKan.template_dir, 'qml', "velocities.qml")
        try:
            vlayer.loadNamedStyle(qmlfile)
        except:
            logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
            QkanError()

        vlayer.selectionChanged.connect(self.selChanged)
        self.layervelo = vlayer

    def selChanged(self, selected, deselected, clearAndSelect) -> None:
        """Anzahl selektierter Objekte in Maske aktualisieren"""
        anzahl = self.layervelo.selectedFeatureCount() + self.layerwlevel.selectedFeatureCount()
        self.tf_selected.setText(str(anzahl))
        self.cb_selected.setChecked(anzahl > 0)

    def click_help(self) -> None:
        help_file = "https://qkan.eu/QKan_Ueberflutung.html"
        os.startfile(help_file)
