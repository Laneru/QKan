import os.path
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from qgis.PyQt.QtWidgets import QProgressBar
from qgis.core import (
    Qgis,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsLayerTreeLayer,
)
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
        self.gdblayer_choice = QKan.config.flood.gdblayer
        self.faktor_v = float(QKan.config.flood.faktor_v)
        self.min_v = float(QKan.config.flood.min_v)
        self.min_w = float(QKan.config.flood.min_w)
        self.mikeversion = QKan.config.flood.mikeversion

    def run(self, selected=False) -> bool:

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

        # Check, ob Ergebnislayer geladen
        if not QgsProject.instance().mapLayersByName('velocities'):
            logger.warning_user(f"Layer 'velocities' fehlt:\nEs wurden noch keine Ergebnisdaten geladen (siehe Schaltfläche)")
            return False

        # Create progress bar
        self.progress_bar = QProgressBar(iface.messageBar())
        self.progress_bar.setRange(0, 100)

        status_message = iface.messageBar().createMessage(
            "", "Flood-Animation wird erstellt. Bitte warten..."
        )
        status_message.layout().addWidget(self.progress_bar)
        iface.messageBar().pushWidget(status_message, Qgis.MessageLevel.Info, 10)
        #
        # datenbank_qkan_template = os.path.join(QKan.template_dir, "qkan.sqlite")
        # shutil.copyfile(datenbank_qkan_template, self.db_name)

        # Read simulation parameters
        xml_file = os.path.join(self.import_dir, '..', 'report_info.xml')
        xml = ET.ElementTree()
        xml.parse(xml_file)
        starttime = datetime.strptime(xml.findtext("ReportStart"), '%m/%d/%Y %H:%M:%S')
        interval = timedelta(float(xml.findtext("ReportInterval"))/86400.)

        with FloodDB(self.db_name) as db:
            db.loadmodule('floodTools')
            if self.wlevel_choice:
                # Erstellung Tabelle wlevel
                sql = "floodtools_info_wlevel"
                data = db.selectyml(sqlnam=sql, kommentar='Tabelleninfos')
                if not data:
                    logger.debug(f'not data\n')

                sql = "floodtools_create_wlevel1"
                if not db.sqlyml(sqlnam=sql, stmt_category= 'Erstellung Tabelle "wlevel"'):
                    db.logger.error_data('Fehler beim Erstellung Tabelle "wlevel"')
                    return False

                sql = "floodtools_create_wlevel2"
                if not db.sqlyml(
                    sqlnam=sql,
                    stmt_category='Hinzufügen geometry in Tabelle "wlevel"',
                    parameters=(self.epsg,)
                ):
                    db.logger.error_data('Fehler beim Hinzufügen geometry in Tabelle "wlevel"')
                    return False

                # sql = "floodtools_create_wlevel3"
                # if not db.sqlyml(sqlnam=sql, stmt_category='Geoindex für Tabelle "wlevel"'):
                #     db.logger.error_data('Fehler beim Erstellung Geoindex für Tabelle "wlevel"')
                #     return False

                sql = "floodtools_delete_wlevel"
                if not db.sqlyml(sqlnam=sql, stmt_category='Zurücksetzen Tabelle "wlevel"'):
                    db.logger.error_data('Fehler beim Zurücksetzen der Tabelle "wlevel"')
                    return False

            # if self.wlevelMax_choice:
            #     # Erstellung Tabelle wlevelMax
            #     sql = "floodtools_create_wlevelmax1"
            #     if not db.sqlyml(sqlnam=sql, stmt_category='Erstellung Tabelle "wlevelMax"'):
            #         db.logger.error_data('Fehler beim Erstellung Tabelle "wlevelMax"')
            #         return False
            #
            #     sql = "floodtools_create_wlevelmax2"
            #     if not db.sqlyml(
            #         sqlnam=sql,
            #         stmt_category='Hinzufügen geometry in Tabelle "wlevelMax"',
            #         parameters=(self.epsg,)
            #     ):
            #         db.logger.error_data('Fehler beim Hinzufügen geometry in Tabelle "wlevelMax"')
            #         return False
            #
            #     # sql = "floodtools_create_wlevelmax3"
            #     # if not db.sqlyml(sqlnam=sql, stmt_category='Geoindex für Tabelle "wlevelMax"'):
            #     #     db.logger.error_data('Fehler beim Erstellung Geoindex für Tabelle "wlevelMax"')
            #     #     return False
            #
            #     sql = "floodtools_delete_wlevelmax"
            #     if not db.sqlyml(sqlnam=sql, stmt_category='Zurücksetzen Tabelle "wlevelMax"'):
            #         db.logger.error_data('Fehler beim Zurücksetzen der Tabelle "wlevelMax"')
            #         return False

            if self.velo_choice:
                # Erstellung Tabelle velo
                sql = "floodtools_info_velo"
                data = db.selectyml(sqlnam=sql, kommentar='Tabelleninfos')
                if not data:
                    logger.debug(f'not data\n')

                sql = "floodtools_create_velo1"
                if not db.sqlyml(sqlnam=sql, stmt_category= 'Erstellung Tabelle "velo"'):
                    db.logger.error_data('Fehler beim Erstellung Tabelle "velo"')
                    return False

                sql = "floodtools_create_velo2"
                if not db.sqlyml(
                    sqlnam=sql,
                    stmt_category='Hinzufügen geometry in Tabelle "velo"',
                    parameters=(self.epsg,)
                ):
                    db.logger.error_data('Fehler beim Hinzufügen geometry in Tabelle "velo"')
                    return False

                # sql = "floodtools_create_velo3"
                # if not db.sqlyml(sqlnam=sql, stmt_category='Geoindex für Tabelle "velo"'):
                #     db.logger.error_data('Fehler beim Erstellung Geoindex für Tabelle "velo"')
                #     return False

                sql = "floodtools_delete_velo"
                if not db.sqlyml(sqlnam=sql, stmt_category='Zurücksetzen Tabelle "velo"'):
                    db.logger.error_data('Fehler beim Zurücksetzen der Tabelle "velo"')
                    return False
            #
            # if self.veloMax_choice:
            #     # Erstellung Tabelle velomax
            #     sql = "floodtools_create_velomax1"
            #     if not db.sqlyml(sqlnam=sql, stmt_category='Erstellung Tabelle "veloMax"'):
            #         db.logger.error_data('Fehler beim Erstellung Tabelle "veloMax"')
            #         return False
            #
            #     sql = "floodtools_create_velomax2"
            #     if not db.sqlyml(
            #         sqlnam=sql,
            #         stmt_category='Hinzufügen geometry in Tabelle "veloMax"',
            #         parameters=(self.epsg,)
            #     ):
            #         db.logger.error_data('Fehler beim Hinzufügen geometry in Tabelle "veloMax"')
            #         return False
            #
            #     # sql = "floodtools_create_velomax3"
            #     # if not db.sqlyml(sqlnam=sql, stmt_category='Geoindex für Tabelle "veloMax"'):
            #     #     db.logger.error_data('Fehler beim Erstellung Geoindex für Tabelle "veloMax"')
            #     #     return False
            #
            #     sql = "floodtools_delete_velomax"
            #     if not db.sqlyml(sqlnam=sql, stmt_category='Zurücksetzen Tabelle "veloMax"'):
            #         db.logger.error_data('Fehler beim Zurücksetzen der Tabelle "veloMax"')
            #         return False

            db.commit()

            layervelo = QgsProject.instance().mapLayersByName('velocities')[0]
            layerwlevel = QgsProject.instance().mapLayersByName('waterlevels')[0]

            if selected:
                if QKan.config.flood.syncSelections:
                    # Auswahl zwischen den beiden Layern übertragen
                    layer1 = layervelo
                    layer2 = layerwlevel
                    for i in range(2):
                        for sel in layer1.selectedFeatures():
                            id = sel.id()
                            layer2.select(id)
                        layer1, layer2 = layer2, layer1  # das gleiche nochmal entgegengesetzt

            if self.wlevel_choice:
                # Flächen mit maßgeblichem Wasserstand übertragen
                if selected:
                    features = list(layerwlevel.selectedFeatures())
                    if not features:
                        logger.error_user("Es wurden keine Objekte gewählt!")
                        return False
                else:
                    features = list(layerwlevel.getFeatures())
                nstep = len(layerwlevel.fields()) - 9
                tlis = [datetime.strftime(starttime + interval*tstep, '%Y-%m-%d %H:%M:%S') for tstep in range(nstep + 1)]
                sql = 'floodtools_insert_wlevel'
                logger.debug("Start Einfügen wlevel")
                for ds in features:
                    vals = ds.attributes()[9:]
                    geomWkb = ds.geometry().asWkb()
                    logger.debug("Einfügen wlevel")
                    params = [(val, tanf, tend, geomWkb, self.epsg,) for val, tanf, tend in zip(vals, tlis[:-1], tlis[1:])]
                        # db.logger.debug(f'Zeitschritt {tstep}')
                    if not db.sqlyml(sql, stmt_category='Erzeugen der wlevel-Flächen', parameters=params, many=True):
                        db.logger.error_data('Fehler bei Erzeugen der wlevel-Flächen')
                        return False
                db.commit()

            if self.velo_choice:
                # Geschwindikeitspfeile für maßgebliche Geschwindigkeiten erzeugen
                if selected:
                    features = list(layervelo.selectedFeatures())
                    if not features:
                        logger.error_user("Es wurden keine Objekte gewählt!")
                        return False
                else:
                    features = list(layervelo.getFeatures())
                nstep = (len(layervelo.fields()) - 6) // 2
                tlis = [datetime.strftime(starttime + interval*tstep, '%Y-%m-%d %H:%M:%S') for tstep in range(nstep + 1)]
                sql = 'floodtools_insert_velo'
                logger.debug("Start Einfügen velo")
                for ds in features:
                    vals = ds.attributes()[6::2]
                    angles = ds.attributes()[7::2]
                    geomWkb = ds.geometry().asWkb()
                    logger.debug("Einfügen velo")
                    params = [(val, angle, tanf, tend, geomWkb, self.epsg,) for val, angle, tanf, tend in zip(vals, angles, tlis[:-1], tlis[1:])]
                        # db.logger.debug(f'Zeitschritt {tstep}')
                    if not db.sqlyml(sql, stmt_category='Erzeugen der velo-Punkte', parameters=params, many=True):
                        db.logger.error_data('Fehler bei Erzeugen der velo-Punkte')
                        return False
                db.commit()

            # if self.wlevelMax_choice:
            #     # Flächen mit maßgeblichem Wasserstand übertragen
            #     sql = f'''
            #         INSERT INTO wlevelmax (hmax, geom)
            #         SELECT
            #             WLevelMax AS hmax,
            #             CastToXY(CastToPolygon(GEOMETRY)) AS geom
            #         FROM {self.tabnam_wlevel}
            #         '''
            #     if not db.sql(sql, 'Erzeugen der wlevelMax-Flächen'):
            #         db.logger.error_data('Fehler beim Erzeugen der wlevelMax-Flächen')
            #         return False
            #
            # if self.veloMax_choice:
            #     sql = f'''
            #         INSERT INTO velomax (vmax, geom)
            #         SELECT
            #             V_Max AS vmax,
            #             Makeline(
            #                 Makepoint(x(GEOMETRY),
            #                           y(GEOMETRY), {self.epsg}),
            #                 MakePoint(x(GEOMETRY)+V_Max*cos(V_Max_Dir/57.2958)*{self.faktor_v},
            #                           y(GEOMETRY)+V_Max*sin(V_Max_Dir/57.2958)*{self.faktor_v},
            #                           {self.epsg})
            #             ) as geom
            #         FROM {self.tabnam_velo}'''
            #     if not db.sql(sql, 'Erzeugen der wlevelMax-Flächen'):
            #         db.logger.error_data('Fehler beim Erzeugen der wlevelMax-Flächen')
            #         return False
            #
        # Layer anlegen
        if self.wlevel_choice:
            vlayer = QgsVectorLayer(
                self.db_name + '|layername=wlevel',
                "wlevel",
                "ogr"
            )
            QgsProject.instance().addMapLayer(vlayer)
            qmlfile = os.path.join(QKan.template_dir, 'qml', "wlevel.qml")
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
            qmlfile = os.path.join(QKan.template_dir, 'qml', "velo.qml")
            try:
                vlayer.loadNamedStyle(qmlfile)
            except:
                db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                iface.messageBar().pushMessage("Programmfehler",
                                               f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
                                               level=Qgis.MessageLevel.Critical)
                return False

        # if self.wlevelMax_choice:
        #     vlayer = QgsVectorLayer(
        #         self.db_name + '|layername=wlevelMax',
        #         "wlevelmax",
        #         "ogr"
        #     )
        #     QgsProject.instance().addMapLayer(vlayer)
        #     qmlfile = os.path.join(QKan.template_dir, 'qml', "waterlevel_max.qml")
        #     try:
        #         vlayer.loadNamedStyle(qmlfile)
        #     except:
        #         db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
        #         iface.messageBar().pushMessage("Programmfehler",
        #                                        f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
        #                                        level=Qgis.MessageLevel.Critical)
        #         return False
        #
        # if self.veloMax_choice:
        #     vlayer = QgsVectorLayer(
        #         self.db_name + '|layername=veloMax',
        #         "velomax",
        #         "ogr"
        #     )
        #     QgsProject.instance().addMapLayer(vlayer)
        #     qmlfile = os.path.join(QKan.template_dir, 'qml', "velocity_max.qml")
        #     try:
        #         vlayer.loadNamedStyle(qmlfile)
        #     except:
        #         db.logger.error_data(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
        #         iface.messageBar().pushMessage("Programmfehler",
        #                                        f"Die Styledatei {qmlfile} konnte nicht gelesen werden!",
        #                                        level=Qgis.MessageLevel.Critical)
        #         return False

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
