import importlib
import json
import os
from pathlib import Path
from typing import Callable, List, Optional, cast, Dict

import qgis
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator, QTimer
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QMenuBar, QWidget
from qgis.core import QgsProject, QgsSettings, QgsMapLayerType, QgsDataSourceUri
from qgis.gui import QgisInterface
from qgis.utils import pluginDirectory

from .config import Config
from .utils import setup_logging

from qkan import enums

# Toggle in DEV to log to console
LOG_TO_CONSOLE = False

# list of all available plugins
PLUGIN_LIST = [
    "createunbeffl.application.CreateUnbefFl",
    "he8porter.application.He8Porter",
    "dynaporter.DynaPorter",
    "muporter.application.MuPorter",
    "swmmporter.application.SWMMPorter",
    "swmm_erg.application.SWMMErg",
    "strakatporter.application.StrakatPorter",
    "linkflaechen.application.LinkFl",
    "surfaceTools.application.SurfaceTools",
    "isyporter.application.IsyPorter",
    "m150porter.application.M150Porter",
    "m145porter.application.M145Porter",
    "datacheck.application.Plausi",
    "zustandsklassen.application.Zustandsklassen",
    "sanierungsbedarfszahl.application.Sanierungsbedarfszahl",
    "subkans.application.Substanzklasse",
    "laengsschnitt.application.Laengsschnitt",
    "floodTools.application.FloodTools",
    "tools.application.QKanTools",
    "selection.application.Selection",
    "neigung.application.Neigung",
    "uploadPostgis.application.UploadPostgis",
    "sync.application.Synchronisation",
    "info.application.Infos",
    "createelements.application.CreateElements",
    "netzuebersicht.application.NetzuebersichtPlugin",
    "datenbankviewer.application.DatenbankviewerPlugin",
    "untersuchungsverwaltung.application.UntersuchungsverwaltungApplication",
]

TABLES_GEOM = [
    "notizen",
    "haltungen",
    "haltungen_untersucht",
    "untersuchdat_haltung",
    "anschlussleitungen",
    "anschlussleitungen_untersucht",
    "anschlussschaechte",
    "untersuchdat_anschlussleitung",
    "schaechte",
    "untersuchdat_schacht",
    "einzugsgebiete",
    "teilgebiete",
    "flaechen",
    "linkfl",
    "linksw",
    "tezg",
    "einleit",
    "aussengebiete",
    "symbole",
]

TABLES_GEOP = [
    "schaechte",
    "schaechte_untersucht",
]

TABLES_GBUF = [
    "linkfl",
    "linksw",
]

TABLES_GLINK = [
    "linkfl",
    "linksw",
    "linkageb",
]

TABLES_GEOMETRY = [
    "flaechen_he8",
]

TABLES_ATTR = [
    "simulationsstatus",
    "material",
    "auslasstypen",
    "abflussparameter",
    "flaechentypen",
    "bodenklassen",
    "abflusstypen",
    "knotentypen",
    "schachttypen",
    "eigentum",
    "symbolkatalog",
    "dynahal",
    "gruppen",
    "profile",
    "entwaesserungsarten",
    "haltungstypen",
    "untersuchrichtung",
    "wetter",
    "bewertungsart",
    "pumpentypen",
    "pruefsql",
    "pruefliste",
    "reflist_zustand",
    "info",
    "refdata",
    "fotos",
    "videos",
]

GEO_TYPES = [
    None,
    "POINT",
    "LINESTRING",
    "POLYGON",
    "MULTIPOINT",
    "MULTILINESTRING",
    "MULTIPOLYGON",
]


# noinspection PyPep8Naming
def classFactory(iface: QgisInterface) -> "QKan":  # pylint: disable=invalid-name
    qkan = QKan(iface)
    return qkan


class _ExternalQKanPlugin:
    """
    Used as an internal type for external extensions to QKan
    """

    name = __name__
    instance: "_ExternalQKanPlugin"
    plugins: List

    # noinspection PyPep8Naming
    def initGui(self) -> None:
        pass

    def unload(self) -> None:
        pass


class QKan:
    instance: "QKan"
    config: Config
    template_dir: str
    forms: list[str]

    dbVersion = "3.4.8"  # Version der QKan-Datenbank
    qgsVersion = "3.4.8"  # Version des Projektes und der Projektdatei. Kann höher als die der QKan-Datenbank sein
    build = "0002"

    # SQL-Statements werden abhängig vom Datenbanktyp und Modul geladen.
    sqls: dict = {}                     # SQL-Statements for all loaded modules
    dbtype: enums.QKanDBChoice = None   # Datenbanktyp des Projekts, wird durch get_database_QKan() aktualisiert
    dbsource: str = None                # Datenbankverbindung des Projekts, wird durch get_database_QKan() aktualisiert

    def __init__(self, iface: qgis.gui.QgisInterface):
        QKan.instance = self

        # QGIS
        self.iface = iface
        self.actions: List[QAction] = []

        # Projektsignale
        try:
            QgsProject.instance().readProject.connect(self.init_project_connection)
        except Exception:
            pass

        try:
            self.iface.projectRead.connect(self.init_project_connection)
        except Exception:
            pass

        # Verzögerter Versuch, falls Projekt bereits offen
        QTimer.singleShot(1000, self.init_project_connection)

        # Beim Plugin-Start einmal versuchen, falls Projekt schon offen ist
        self.init_project_connection()

        # Init logging
        self.logger, self.log_path = setup_logging(LOG_TO_CONSOLE, iface)

        # Init config
        try:
            QKan.config = Config.load()
        except (json.JSONDecodeError, OSError):
            self.logger.error("Failed to read config file.", exc_info=True)
            QKan.config = Config()
            QKan.config.save()

        # Set default template directory
        QKan.template_dir = os.path.join(pluginDirectory("qkan"), "templates")

        # Set list of QKan-Forms
        forms_dir = os.path.join(pluginDirectory("qkan"), "forms")
        QKan.forms = [
            el for el in os.listdir(forms_dir) if os.path.splitext(el)[1] == ".ui"
        ]
        # self.logger.debug(f"forms_dir: {forms_dir}")
        # self.logger.debug(f"Formularliste: \n{QKan.forms}")

        # QKan-Tabellen

        # Tabellen mit Geometrieobjekten
        QKan.tablesgeom = TABLES_GEOM
        QKan.tablesgeop = TABLES_GEOP
        QKan.tablesgbuf = TABLES_GBUF
        QKan.tablesglink = TABLES_GLINK
        QKan.tablesgeometry = TABLES_GEOMETRY

        # Referenztabellen
        QKan.tablesattr = TABLES_ATTR
        # Alle in QKan vorkommenden Geometriedatentypen:
        QKan.geotypes = GEO_TYPES

        # Plugins
        self.instances: List[_ExternalQKanPlugin] = []

        # Translations
        self.translator = QTranslator()
        locale = (QSettings().value("locale/userLocale") or "en")[0:2]
        for _file in (Path(__file__).parent / "i18n").iterdir():
            if _file.name.endswith("_{}.qm".format(locale)):
                self.translator.load(str(_file))
        # noinspection PyArgumentList
        QCoreApplication.installTranslator(self.translator)

        self.plugins: List = []

        for plugin_name in PLUGIN_LIST:
            try:
                module_name, class_name = plugin_name.rsplit(".", 1)
                klass = getattr(importlib.import_module(f"qkan.{module_name}"), class_name)
                if klass is None:
                    self.logger.error_code("Failed to find class %s inside %s", class_name, module_name)
                    continue

                self.plugins.append(klass(iface))
            except ImportError:
                self.logger.error_code("Failed to load plugin %s", plugin_name, exc_info=True)
                continue

        actions = cast(QMenuBar, self.iface.mainWindow().menuBar()).actions()

        self.menu: Optional[QMenu] = None
        for menu in actions:
            if menu.text() == "QKan":
                self.menu = menu.menu()
                self.menu_action = menu
                break

        # mnuSub1 = self.menu.addMenu('Sub-menu')

        #self.toolbar = self.iface.addToolBar("QKan")
        #self.toolbar.setObjectName("QKan")

        self.toolbar = self.iface.addToolBar("QKan-Allgemein")
        self.toolbar.setObjectName("QKan-Allgemein")

        self.toolbar_2 = self.iface.addToolBar("QKan-Datenaustausch")
        self.toolbar_2.setObjectName("QKan-Datenaustausch")

        self.toolbar_3 = self.iface.addToolBar("QKan-Flächenbearbeitung")
        self.toolbar_3.setObjectName("QKan-Flächenbearbeitung")

        self.toolbar_4 = self.iface.addToolBar("QKan-Befahrungsdaten")
        self.toolbar_4.setObjectName("QKan-Befahrungsdaten")
        
        self.toolbar_5 = self.iface.addToolBar("QKan-Elementerzeugung")
        self.toolbar_5.setObjectName("QKan-Elementerzeugung")


        # Add QKan SVG path
        qkanSvgPath = os.path.join(pluginDirectory("qkan"), "templates/svg")
        svgPaths = QgsSettings().value('svg/searchPathsForSVG')
        if svgPaths:                        # Ist bei automatisierten Text Null...
            if qkanSvgPath not in svgPaths:
                svgPaths.append(qkanSvgPath)
                QgsSettings().setValue('svg/searchPathsForSVG', svgPaths)

        # Set Identify Forms Option
        QgsSettings().setValue('Map/identifyAutoFeatureForm', 'true')
        QgsSettings().setValue('Map/identifyMode', 'LayerSelection')

        # plugin 'grassprovider' ist needed for surfaceTool.SurfaceTask.run_voronoi
        if not qgis.utils.isPluginLoaded('grassprovider'):
            QgsSettings().setValue('PythonPlugins/grassprovider', True)
            qgis.utils.startPlugin('grassprovider')

    # noinspection PyPep8Naming
    def initGui(self) -> None:
        # Create and insert QKan menu after the 3rd menu
        if self.menu is None:
            self.menu = QMenu("QKan", self.iface.mainWindow().menuBar())

            actions = self.iface.mainWindow().menuBar().actions()
            prepend = actions[3] if len(actions) > 3 else None

            self.menu_action = (
                self.iface.mainWindow().menuBar().insertMenu(prepend, self.menu)
            )

        # Calls initGui on all known QKan plugins
        for plugin in self.plugins:
            plugin.initGui()

        self.sort_actions()

    def sort_actions(self) -> None:
        # Finally sort all actions
        self.actions.sort(key=lambda x: cast(str, cast(QAction, x).text().lower()))
        alis: Dict[str, int] = {}
        e = 0
        for x in self.actions:
            alis[x.text()] = e
            e += 1

        def safe_add_action(menu: QMenu, key: str) -> None:
            if key not in alis:
                return
            if alis[key] >= len(self.actions):
                return

            menu.addAction(self.actions[alis[key]])

        if self.menu:
            self.menu.clear()
            allgemein = self.menu.addMenu("Allgemein")
            # verwaltung = self.menu.addMenu("Verwaltung")
            daten = self.menu.addMenu("Daten")
            sync = self.menu.addMenu("Synchronisation")
            hyex = self.menu.addMenu("Hystem-Extran")
            xml = self.menu.addMenu("XML")
            dyna = self.menu.addMenu("DYNA")
            mike = self.menu.addMenu("Mike+")
            swmm = self.menu.addMenu("SWMM")
            strakat = self.menu.addMenu("STRAKAT")
            flaechen = self.menu.addMenu("Flächenverarbeitung")
            zustand = self.menu.addMenu("Zustandsbewertung")
            substanz = self.menu.addMenu("Substanzbewertung")
            flood2D = self.menu.addMenu("Überflutung")
            info = self.menu.addMenu("Info")

            safe_add_action(allgemein, "Optionen")
            safe_add_action(allgemein, "QKan-Projekt aktualisieren")
            safe_add_action(allgemein, "QKan-Projektdatei übertragen")
            safe_add_action(allgemein, "QKan-Datenbank aktualisieren")
            safe_add_action(allgemein, "Neue QKan-Datenbank erstellen")
            safe_add_action(allgemein, "Dateipfade suchen")

            safe_add_action(daten, "Plausibilitätsprüfungen")
            safe_add_action(daten, "Tabellendaten aus Clipboard einfügen")
            safe_add_action(daten, "Tabellendaten aus Clipboard: Zuordnung anzeigen")
            safe_add_action(daten, "Längsschnitt")
            safe_add_action(daten, "Auswahl erweitern / Netzverfolgung")
            safe_add_action(daten, "Netzübersicht")  # neuer Eintrag
            safe_add_action(daten, "Datenbankviewer")
            safe_add_action(daten, "Untersuchungsverwaltung")

            safe_add_action(flaechen, "Erzeuge unbefestigte Flächen...")
            safe_add_action(flaechen, "Erzeuge Voronoiflächen zu Haltungen")
            safe_add_action(flaechen, "Entferne Überlappungen")
            safe_add_action(flaechen, "Zuordnung zu Teilgebiet")
            safe_add_action(flaechen, "Teilgebietszuordnungen als Gruppen verwalten")
            safe_add_action(flaechen, "Erzeuge Verknüpfungslinien von Flächen zu Haltungen")
            safe_add_action(flaechen, "Erzeuge Verknüpfungslinien von Einzeleinleitungen zu Haltungen")
            safe_add_action(flaechen, "Verknüpfungen bereinigen")
            safe_add_action(flaechen, "Oberflächenabflussparameter eintragen")
            safe_add_action(flaechen, "Neigungsklassen ermitteln")

            safe_add_action(hyex, "Import aus Hystem-Extran 8")
            safe_add_action(hyex, "Export nach Hystem-Extran 8")
            safe_add_action(hyex, "Ergebnisse aus Hystem-Extran 8")

            safe_add_action(mike, "Import aus Mike+")

            safe_add_action(dyna, "Import aus DYNA-Datei (*.EIN)")
            safe_add_action(dyna, "Export in DYNA-Datei...")

            safe_add_action(xml, "Import aus DWA-150-XML")
            safe_add_action(xml, "Export nach DWA-150-XML")
            safe_add_action(xml, "Import aus ISYBAU-XML")
            safe_add_action(xml, "Export nach ISYBAU-XML")
            safe_add_action(xml, "Import aus DWA-145-XML")

            safe_add_action(swmm, "Import aus SWMM-Datei (*.INP)")
            safe_add_action(swmm, "Export in SWMM-Datei (*.INP)")
            safe_add_action(swmm, "Import von SWMM-Ergebnissen (*.RPT)")

            safe_add_action(strakat, "Import aus STRAKAT")
            # safe_add_action(laengs, "Längsschnitt-Tool für HE8")
            # safe_add_action(laengs, "Ganglinien-Tool für HE8")

            safe_add_action(zustand, "Zustandsklassen ermitteln")
            safe_add_action(zustand, "Sanierungsbedarfszahl ermitteln")
            safe_add_action(substanz, "Substanzklassen ermitteln")

            safe_add_action(sync, "Vergleich mit einem anderen QKan-Projekt")
            safe_add_action(sync, "Synchronisation mit einem anderen QKan-Projekt")
            safe_add_action(sync, "Upload nach PostGIS WebSuite")

            safe_add_action(flood2D, "Überflutungsanimation")

            safe_add_action(info, "Über QKan")
            safe_add_action(info, "Infos zum QKan Projekt")

    def unload(self) -> None:
        from qgis.utils import unloadPlugin

        # Shutdown logger
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Unload all other instances
        for instance in self.instances:
            print("Unloading ", instance.name)
            if not unloadPlugin(instance.name):
                print("Failed to unload plugin!")

        if self.menu:
            # Remove entries from own menu
            for action in self.menu.actions():
                self.menu.removeAction(action)

        # Remove entries from Plugin menu and toolbar
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

        # Remove the toolbar
        if self.toolbar is not None:
            del self.toolbar

        if self.toolbar_2 is not None:
            del self.toolbar_2

        if self.toolbar_3 is not None:
            del self.toolbar_3

        if self.toolbar_4 is not None:
            del self.toolbar_4

        # Remove menu
        self.iface.mainWindow().menuBar().removeAction(self.menu_action)

        # Unload translator
        # noinspection PyArgumentList
        QCoreApplication.removeTranslator(self.translator)

        # Call unload on all loaded plugins
        for plugin in self.plugins:
            plugin.unload()

    def register(self, instance: "_ExternalQKanPlugin") -> None:
        self.instances.append(instance)

        self.plugins += instance.plugins

    def unregister(self, instance: "_ExternalQKanPlugin") -> None:
        self.instances.remove(instance)

        for plugin in instance.plugins:
            self.plugins.remove(plugin)

    def add_action(
        self,
        icon_path: str,
        text: str,
        toolbar: str,
        callback: Callable,
        enabled_flag: bool = True,
        checkable: bool = False,
        add_to_menu: bool = True,
        add_to_toolbar: bool = True,
        status_tip: str = None,
        whats_this: str = None,
        parent: QWidget = None,
    ) -> QAction:
        """Add a toolbar icon to the toolbar/menu.

        :param icon_path:       Path to the icon for this action. Can be a resource
                                path (e.g. ':/plugins/foo/bar.png') or a normal
                                file system path.
        :param text:            Text that should be shown in menu items for this action.
        :param toolbar:         Toolbar menu item
        :param callback:        Function to be called when the action is triggered.
        :param enabled_flag:    A flag indicating if the action should be enabled
                                by default. Defaults to True.
        :param checkable:       Flag indicating whether Icon has/shows checked status
        :param add_to_menu:     Flag indicating whether the action should also
                                be added to the menu. Defaults to True.
        :param add_to_toolbar:  Flag indicating whether the action should also
                                be added to the toolbar. Defaults to True.
        :param status_tip:      Optional text to show in a popup when mouse pointer
                                hovers over the action.
        :param whats_this:      Optional text to show in the status bar when the
                                mouse pointer hovers over the action.
        :param parent:          Parent widget for the new action. Defaults None.
        :returns:               The action that was created. Note that the action is also
                                added to self.actions.
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if checkable:
            action.setCheckable(checkable)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            if toolbar == 'QKan-Allgemein':
                self.toolbar.addAction(action)

            elif toolbar == 'QKan-Datenaustausch':
                self.toolbar_2.addAction(action)

            elif toolbar == 'QKan-Flächenbearbeitung':
                self.toolbar_3.addAction(action)

            elif toolbar == 'QKan-Befahrungsdaten':
                self.toolbar_4.addAction(action)
                
            elif toolbar == 'QKan-Elementerzeugung':
                self.toolbar_5.addAction(action)

        if add_to_menu and self.menu:
            self.menu.addAction(action)

        self.actions.append(action)

        return action

    # --- Neue Methoden: Projekt-DB-Autoerkennung ---------------------

    def init_project_connection(self, *args):
        """
        Ermittelt die aktive QKan-Datenbank aus bereits im Projekt
        vorhandenen QKan-Layern und setzt dbsource / dbtype.
        Wird beim Plugin-Start und nach dem Laden eines Projekts aufgerufen.
        """
        print("[QKan] init_project_connection()")

        candidate_tables = {
            "haltungen",
            "schaechte",
            "anschlussleitungen",
            "entwaesserungsrinnen",
            "sonderbauwerke_view",
            "Sinkkästen",
            "Sinkkaesten",
        }

        project = QgsProject.instance()
        layers = list(project.mapLayers().values())

        for layer in layers:
            try:
                if layer.type() != QgsMapLayerType.VectorLayer:
                    continue

                provider = layer.providerType()
                if provider != "spatialite":
                    continue

                source = layer.source()
                uri = QgsDataSourceUri(source)
                db_path = uri.database()

                table_name = None
                try:
                    table_name = uri.table()
                except Exception:
                    pass

                if not db_path:
                    continue

                clean_table = (table_name or "").replace('"', "")

                # Wenn Tabellennamen bekannt sind, nur QKan-Schichten verwenden
                if clean_table and clean_table not in candidate_tables:
                    continue

                # Aktive DB im QKan-Status setzen
                QKan.dbsource = source
                QKan.dbtype = enums.QKanDBChoice.SPATIALITE if hasattr(
                    enums.QKanDBChoice, "SPATIALITE"
                ) else "spatialite"

                print(f"[QKan] Aktive QKan-DB erkannt: {db_path}")
                print(f"[QKan] dbsource = {QKan.dbsource}")
                print(f"[QKan] dbtype = {QKan.dbtype}")
                return True

            except Exception as e:
                print(f"[QKan] Layer-Auswertung fehlgeschlagen: {e}")

        print("[QKan] Keine aktive QKan-Datenbank aus Projektlayern erkannt")
        QKan.dbsource = None
        QKan.dbtype = None
        return False

    def has_active_database(self) -> bool:
        """
        True, wenn QKan aktuell eine aktive DB-Verbindung kennt.
        """
        return bool(QKan.dbsource)

    def get_active_dbsource(self) -> str:
        """
        Liefert die aktuelle dbsource (Datenquellen-String) oder None.
        """
        return QKan.dbsource