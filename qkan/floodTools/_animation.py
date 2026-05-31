import os.path
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

from qgis.PyQt.QtWidgets import QProgressBar
from qgis.core import (
    Qgis,
    QgsProject,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
    QgsInterval,
    QgsTemporalUtils,
    QgsRasterLayer,
    QgsLayerTreeLayer,
)
from qgis.gui import QgsMapCanvas

from qkan import QKan, enums
from .flood_db import FloodDB
from ..utils import get_logger, QkanError

logger = get_logger("QKan.floodTools._animation")


class FloodanimationTask:
    def __init__(self):
        # all parameters are passed via QKan.config
        self.epsg = QKan.config.epsg
        self.import_dir = QKan.config.flood.import_dir
        self.projectfile = QKan.config.project.file
        self.db_name = QKan.config.flood.database
        self.velo_choice = QKan.config.flood.velo
        self.wlevel_choice = QKan.config.flood.wlevel
        self.veloMax_choice = QKan.config.flood.veloMax
        self.wlevelMax_choice = QKan.config.flood.wlevelMax
        self.gdblayer_choice = QKan.config.flood.gdblayer
        self.faktor_v = float(QKan.config.flood.faktor_v)
        self.min_v = float(QKan.config.flood.min_v)
        self.min_w = float(QKan.config.flood.min_w)
        self.mikeversion = QKan.config.flood.mikeversion

    def run(self) -> bool:

        iface = QKan.instance.iface

        if self.mikeversion == enums.MikeVersion.v1:
            self.tabnam_velo = 'result2d__velocity'
            self.tabnam_wlevel = 'result2d__topo_decimated'
        elif self.mikeversion == enums.MikeVersion.v2:
            self.tabnam_velo = "velocity"
            self.tabnam_wlevel = "topo_decimated"
        else:
            logger.error_code(f'Keine gültige Mike-Version: {QKan.config.flood.mikeversion}')
            raise QkanError
        logger.debug(f'Mike-Version: {QKan.config.flood.mikeversion}')

        # Create progress bar
        self.progress_bar = QProgressBar(iface.messageBar())
        self.progress_bar.setRange(0, 100)

        status_message = iface.messageBar().createMessage(
            "", "Flood-Animation wird erstellt. Bitte warten..."
        )
        status_message.layout().addWidget(self.progress_bar)
        iface.messageBar().pushWidget(status_message, Qgis.MessageLevel.Info, 10)

        datenbank_qkan_template = os.path.join(QKan.template_dir, "qkan.sqlite")
        shutil.copyfile(datenbank_qkan_template, self.db_name)

        # Read simulation parameters
        xml_file = os.path.join(self.import_dir, '..', 'report_info.xml')
        xml = ET.ElementTree()
        xml.parse(xml_file)
        starttime = datetime.strptime(xml.findtext("ReportStart"), '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        interval = float(xml.findtext("ReportInterval")) / 86400.

        if self.velo_choice:
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
            o_save_options.layerName = self.tabnam_velo
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

        if self.wlevel_choice:
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
            o_save_options.layerName = self.tabnam_wlevel
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

        with FloodDB(self.db_name) as db:
            timakt = datetime.now()

            if self.wlevel_choice:
                # Erstellung Tabelle wlevel
                sql = "PRAGMA table_list('wlevel')"
                data = db.select(sql, 'Tabelleninfos')
                logger.debug(f'{data=}\n')
                if not data:
                    logger.debug(f'not data\n')
                    sqls = [
                        """CREATE TABLE IF NOT EXISTS wlevel (
                           pk INTEGER PRIMARY KEY,
                           h REAL,
                           tanf TEXT,
                           tend TEXT)""",
                        f"SELECT AddGeometryColumn('wlevel','geom', {self.epsg},'POLYGON',2)",
                        "SELECT CreateSpatialIndex('wlevel','geom')",
                        'DELETE FROM wlevel',
                    ]

                    if not db.sqlmany(sqls, 'Erstellung Tabelle "wlevel"'):
                        return False

            if self.wlevelMax_choice:
                # Erstellung Tabelle wlevelMax
                sqls = [
                    """CREATE TABLE IF NOT EXISTS wlevelmax (
                       pk INTEGER PRIMARY KEY,
                       hmax REAL)""",
                    f"SELECT AddGeometryColumn('wlevelmax','geom', {self.epsg},'POLYGON',2)",
                    "SELECT CreateSpatialIndex('wlevelmax','geom')",
                    "DELETE FROM wlevelmax",
                ]

                if not db.sqlmany(sqls, 'Erstellung Tabelle "wlevelmax"'):
                    return False

            if self.velo_choice:
                # Erstellung Tabelle velo
                sql = "PRAGMA table_list('velo')"
                data = db.select(sql, 'Tabelleninfos')
                logger.debug(f'{data=}\n')
                if not data:
                    logger.debug(f'not data\n')
                    sqls = [
                        """CREATE TABLE IF NOT EXISTS velo (
                           pk INTEGER PRIMARY KEY,
                           v REAL,
                           tanf TEXT,
                           tend TEXT)""",
                        f"SELECT AddGeometryColumn('velo','geom', {self.epsg},'LINESTRING',2)",
                        "SELECT CreateSpatialIndex('velo','geom')",
                        'DELETE FROM velo',
                    ]

                    if not db.sqlmany(sqls, 'Erstellung Tabelle "velo"'):
                        return False

            if self.veloMax_choice:
                # Erstellung Tabelle velomax
                sqls = [
                    """CREATE TABLE IF NOT EXISTS velomax (
                       pk INTEGER PRIMARY KEY,
                       vmax REAL)""",
                    f"SELECT AddGeometryColumn('velomax','geom', {self.epsg},'LINESTRING',2)",
                    "SELECT CreateSpatialIndex('velomax','geom')",
                    'DELETE FROM velomax',
                ]

                if not db.sqlmany(sqls, 'Erstellung Tabelle "velomax"'):
                    return False

            db.commit()

            # Berechnung der Anzahl Zeitschritte
            if self.velo_choice:
                sql = f"PRAGMA table_info('{self.tabnam_velo}')"
                data = db.select(sql, 'Tabelleninfo velocity')
            elif self.wlevel_choice:
                sql = f"PRAGMA table_info('{self.tabnam_wlevel}')"
                data = db.select(sql, 'Tabelleninfo water level')
            # else:
                # logger.warning("In der Ergebnisauswahl wurde keine Auswahl getroffen. Abbruch!")
                # return True

            if self.velo_choice or self.wlevel_choice:
                db.logger.debug(f'{data=}\n')
                nstep = int((len(data) - 6) / 2)
                db.logger.debug(f'Anzahl Zeitschritte: {nstep=}\n')

                for tstep in range(nstep):
                    if (datetime.now() - timakt).seconds > 10:
                        timakt = datetime.now()
                        db.logger.info(f'Zeitschritt {tstep}')

                    if self.wlevel_choice:
                        # Flächen mit maßgeblichem Wasserstand übertragen
                        sql = f'''
                            INSERT INTO wlevel (h, tanf, tend, geom)
                            SELECT
                                wl_{tstep} AS h,
                                datetime(julianday('{starttime}') + {tstep} * {interval}) AS tanf,
                                datetime(julianday('{starttime}') + {tstep + 1} * {interval}) AS tend,
                                CastToXY(CastToPolygon(GEOMETRY)) AS geom
                            FROM {self.tabnam_wlevel}
                            WHERE wl_{tstep} >= {self.min_w}
                            '''
                        if not db.sql(sql, 'Erzeugen der wlevel-Flächen'):
                            return False

                    if self.velo_choice:
                        # Geschwindikeitspfeile für maßgebliche Geschwindigkeiten erzeugen
                        sql = f'''
                            INSERT INTO velo (v, tanf, tend, geom)
                            SELECT
                                v_{tstep} AS v,
                                datetime(julianday('{starttime}') + {tstep} * {interval}) AS tanf,
                                datetime(julianday('{starttime}') + {tstep + 1} * {interval}) AS tend,
                                Makeline(
                                    Makepoint(x(GEOMETRY), 
                                              y(GEOMETRY), {self.epsg}), 
                                    MakePoint(x(GEOMETRY)+v_{tstep}*cos(v_dir_{tstep}/57.2958)*{self.faktor_v}, 
                                              y(GEOMETRY)+v_{tstep}*sin(v_dir_{tstep}/57.2958)*{self.faktor_v},
                                              {self.epsg})
                                ) as geom
                            FROM {self.tabnam_velo}
                            WHERE v_{tstep} >= {self.min_v}
                            '''
                        if not db.sql(sql, 'Erzeugen der velo-Pfeile'):
                            db.logger.error_data('Fehler beim Erzeugen der velo-Pfeile')
                            return False

                db.commit()

            if self.wlevelMax_choice:
                # Flächen mit maßgeblichem Wasserstand übertragen
                sql = f'''
                    INSERT INTO wlevelmax (hmax, geom)
                    SELECT
                        WLevelMax AS hmax,
                        CastToXY(CastToPolygon(GEOMETRY)) AS geom
                    FROM {self.tabnam_wlevel}
                    '''
                if not db.sql(sql, 'Erzeugen der wlevelMax-Flächen'):
                    db.logger.error_data('Fehler beim Erzeugen der wlevelMax-Flächen')
                    return False

            if self.veloMax_choice:
                sql = f'''
                    INSERT INTO velomax (vmax, geom)
                    SELECT
                        V_Max AS vmax, 
                        Makeline(
                            Makepoint(x(GEOMETRY), 
                                      y(GEOMETRY), {self.epsg}), 
                            MakePoint(x(GEOMETRY)+V_Max*cos(V_Max_Dir/57.2958)*{self.faktor_v}, 
                                      y(GEOMETRY)+V_Max*sin(V_Max_Dir/57.2958)*{self.faktor_v},
                                      {self.epsg})
                        ) as geom
                    FROM {self.tabnam_velo}'''
                if not db.sql(sql, 'Erzeugen der wlevelMax-Flächen'):
                    db.logger.error_data('Fehler beim Erzeugen der wlevelMax-Flächen')
                    return False

        if self.wlevel_choice:
            vlayer = QgsVectorLayer(
                self.db_name + '|layername=wlevel',
                "wlevel",
                "ogr"
            )
            QgsProject.instance().addMapLayer(vlayer)
            qmlfile = os.path.join(QKan.template_dir, 'qml', "waterlevel.qml")
            try:
                vlayer.loadNamedStyle(qmlfile)
            except:
                db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                iface.messageBar().pushMessage("Programmfehler",
                                               f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
                                               level=Qgis.MessageLevel.Critical)
                return False

        if self.velo_choice:
            vlayer = QgsVectorLayer(
                self.db_name + '|layername=velo',
                "velo",
                "ogr"
            )
            QgsProject.instance().addMapLayer(vlayer)
            qmlfile = os.path.join(QKan.template_dir, 'qml', "velocity.qml")
            try:
                vlayer.loadNamedStyle(qmlfile)
            except:
                db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                iface.messageBar().pushMessage("Programmfehler",
                                               f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
                                               level=Qgis.MessageLevel.Critical)
                return False

        if self.wlevelMax_choice:
            vlayer = QgsVectorLayer(
                self.db_name + '|layername=wlevelMax',
                "wlevelmax",
                "ogr"
            )
            QgsProject.instance().addMapLayer(vlayer)
            qmlfile = os.path.join(QKan.template_dir, 'qml', "waterlevel_max.qml")
            try:
                vlayer.loadNamedStyle(qmlfile)
            except:
                db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                iface.messageBar().pushMessage("Programmfehler",
                                               f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
                                               level=Qgis.MessageLevel.Critical)
                return False

        if self.velo_choice:
            vlayer = QgsVectorLayer(
                self.db_name + '|layername=veloMax',
                "velomax",
                "ogr"
            )
            QgsProject.instance().addMapLayer(vlayer)
            qmlfile = os.path.join(QKan.template_dir, 'qml', "velocity_max.qml")
            try:
                vlayer.loadNamedStyle(qmlfile)
            except:
                db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                iface.messageBar().pushMessage("Programmfehler",
                                               f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
                                               level=Qgis.MessageLevel.Critical)
                return False

        # canvas = iface.mapCanvas()
        # # canvas = QgsMapCanvas()
        #
        # # set frame duration
        # timeController = canvas.temporalController()
        # intervall = QgsInterval()
        # intervall.setMinutes(interval * 1440)
        # timeController.setFrameDuration(intervall)
        #
        # # set frame rate
        # timeController.setFramesPerSecond(0.5)
        #
        # # set time range
        # timerange = QgsTemporalUtils.calculateTemporalRangeForProject(QgsProject.instance())
        # if timerange.isInfinite():
        #     db.logger.error_data(f'Die Ergebnisdaten enthalten keine Zeitschritte')
        #     iface.messageBar().pushMessage("Datenfehler", "Eine Ergebnistabelle enthält keine Zeitschritte. "
        #                                                   "Möglicherweise wurden bei der Ergebnisausgabe nicht "
        #                                                   "alle Zeitschrittausgaben aktiviert.",
        #                                    level=Qgis.MessageLevel.Warning)
        #     return False
        #
        # timeController.setTemporalExtents(timerange)

        # set navigation mode to 'animated'
        # timeController.setNavigationMode(1)

        urlWithParams = f"crs=EPSG:{self.epsg}&format=image/png&layers=web&" \
                        f"styles&url=https://sgx.geodatenzentrum.de/wms_topplus_open"
        rlayer = QgsRasterLayer(urlWithParams, 'TopPlusOpen', 'wms')
        if rlayer.isValid():
            # db.logger.error_data("Layer failed to load!")
            # return False
            QgsProject.instance().addMapLayer(rlayer, False)
            QgsProject.instance().layerTreeRoot().insertChildNode(2, QgsLayerTreeLayer(rlayer))

        iface.messageBar().pushMessage("Hinweis", 'Bitte Bedienfeld "Zeitsteuerung aktivieren"', level=Qgis.MessageLevel.Info)

        return True
