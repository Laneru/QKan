import os

from qgis.core import QgsProject, QgsEditorWidgetSetup

from qkan.database.dbfunc import DBConnection
from qkan.utils import get_logger, QkanDbError
from qgis.utils import pluginDirectory
from qkan import QKan, enums
from qkan.tools.qkan_utils import loadLayer, get_database_QKan
VERSION = "3.4.8"  # must be higher than previous one and correspond with qkan_database.py: __dbVersion__

logger = get_logger("QKan.database.migrations.0040")

def run(dbcon: DBConnection) -> bool:
    # Ergänzung einiger Felder in anschlussleitungen

    project = QgsProject.instance()

    qkan_db=QKan.config.database.qkan           # wurde im Formular zum Datenbankupdate festgelegt

    pname = QKan.config.project.file            # wurde im Formular zum Datenbankupdate festgelegt
    logger.debug(f'{pname=}')

    dbcon.alter_table(
        tabnam=         'schaechte',
        attributes_new= [],
        attributes_del= None,
        geo_attrchange='geom',
        geo_newtype=    'MULTILINESTRING',
        geo_modfun=     'CastToMultiLineString(LinesFromRings(geom)) AS geom',
    )

    sql_file = os.path.join(pluginDirectory("qkan"), 'database/migrations', '0040_sqlite.sql')
    try:
        dbcon.executefile(sql_file)
    except BaseException as err:
        logger.error_code(f"Fehler {err} in {__name__}.0040, {sql_file =}")
        return False

    # Tabelle wurde bereits mit sql_file erstellt
    epsg = QKan.config.epsg
    sql = f"SELECT AddGeometryColumn('anschlussschaechte', 'geom', {epsg}, 'POINT', 2);"
    if not dbcon.sql(sql, f"migration 0040, Version {VERSION}: Geoobjekt für anschlussschaechte"):
        raise QkanDbError

    sql = f"SELECT CreateSpatialIndex('anschlussschaechte', 'geom');"
    if not dbcon.sql(sql, f"migration 0040, Version {VERSION}: Geoindex für anschlussschaechte"):
        raise QkanDbError

    if 'urstation' not in dbcon.attrlist('anschlussleitungen'):
        try:
            dbcon.sql(
                'ALTER TABLE anschlussleitungen ADD COLUMN urstation REAL;',
                'migration_0040, urstation ergänzen'
            )
        except:
            logger.error_code('Fehlgeschlagen: migration_0040, urstation ergänzen')

    if 'ursprung' not in dbcon.attrlist('anschlussleitungen'):
        try:
            dbcon.sql(
                'ALTER TABLE anschlussleitungen ADD COLUMN ursprung TEXT;',
                'migration_0040, ursprung ergänzen'
            )
        except:
            logger.error_code('Fehlgeschlagen: migration_0040, ursprung ergänzen')

    if 'lageanschluss' not in dbcon.attrlist('anschlussleitungen'):
        try:
            dbcon.sql(
                'ALTER TABLE anschlussleitungen ADD COLUMN lageanschluss INTEGER;',
                'migration_0040, lageanschluss ergänzen'
            )
        except:
            logger.error_code('Fehlgeschlagen: migration_0040, lageanschluss ergänzen')

    if 'eigentum' not in dbcon.attrlist('anschlussleitungen'):
        try:
            dbcon.sql(
                'ALTER TABLE anschlussleitungen ADD COLUMN eigentum TEXT;',
                'migration_0040, eigentum ergänzen'
            )
        except:
            logger.error_code('Fehlgeschlagen: migration_0040, eigentum ergänzen')

    # Übertragen der M150-Daten der einzelnen Referenztabellen in die neue Tabelle refdata
    # 1. für Schächte und Haltungen
    reftabs = [
        # tabellenname,          attributname, attributname in Tabellen schaechte & haltungen, begrenzung der attribute
        ['entwaesserungsarten', 'bezeichnung',   'entwart', 3],
        ['material',            'bezeichnung',  'material', 2],
        ['simulationsstatus',   'bezeichnung', 'simstatus', 3]
    ]
    modules = [
        ['m150', 'm150porter'],
        ['isybau', 'isyporter'],
        ['he_nr', 'he8porter']
    ]
    for tabnam, attrnam, attrdat, nk in reftabs:
        for mattr, module in modules[:nk]:
            sql = f"""
                WITH refsall AS (
                    SELECT {attrdat}
                    FROM haltungen
                    UNION
                    SELECT {attrdat}
                    FROM schaechte
                ),
                ru AS (
                    SELECT {attrdat} AS bezqkan
                    FROM refsall
                    GROUP BY {attrdat}
                )
                INSERT INTO refdata (bezext, bezqkan, kuerzel, subject, modul, kommentar)
                SELECT 
                    NULL AS bezext, 
                    rt.{attrnam} AS bezqkan,
                    rt.{mattr} AS kuerzel,
                    'export_{tabnam}' AS subject,
                    '{module}' AS modul,
                    'Migration 0040: Übertragung aus alter Referenztabelle {tabnam}' AS kommentar
                FROM {tabnam} AS rt
                JOIN ru ON ru.bezqkan = rt.{attrnam}
                GROUP BY rt.{attrnam}"""
            dbcon.sql(sql, f'migration_0040: Übertragung aus alter Referenztabelle {tabnam}')

    # 2. nur für Haltungen
    reftabs = [
        # tabellenname,          attributname in Tabellen schaechte & haltungen, begrenzung der attribute
        ['profile',             'profilnam', 'profilnam', 3],
    ]
    modules = [
        ['m150', 'm150porter'],
        ['isybau', 'isyporter'],
        ['he_nr', 'he8porter']
    ]
    for tabnam, attrnam, attrdat, nk in reftabs:
        for mattr, module in modules[:nk]:
            sql = f"""
                WITH refsall AS (
                    SELECT {attrdat}
                    FROM haltungen
                ),
                ru AS (
                    SELECT {attrdat} AS bezqkan
                    FROM refsall
                    GROUP BY {attrdat}
                )
                INSERT INTO refdata (bezext, bezqkan, kuerzel, subject, modul, kommentar)
                SELECT 
                    NULL AS bezext, 
                    rt.{attrnam} AS bezqkan,
                    rt.{mattr} AS kuerzel,
                    'export_{tabnam}' AS subject,
                    '{module}' AS modul,
                    'Migration 0040: Übertragung aus alter Referenztabelle {tabnam}' AS kommentar
                FROM {tabnam} AS rt
                JOIN ru ON ru.bezqkan = rt.{attrnam}
                GROUP BY rt.{attrnam}"""
            dbcon.sql(sql, f'migration_0040: Übertragung aus alter Referenztabelle {tabnam}')

    dbcon.commit()

    if 4 == False:
        project.read()

        # Neuer Layer HA-Schächte
        grouppath = [
            enums.LAYERBEZ.QKAN_GROUP.value,
            enums.LAYERBEZ.SCHAECHTE_GROUP.value,
        ]
        loadLayer(
            layerbez=enums.LAYERBEZ.HA_SCHAECHTE.value,
            table="schaechte",
            geom_column='geop',
            qmlfile="HA-Schächte.qml",
            filter='',
            uifile="qkan_anschlussschaechte.ui",
            group=grouppath,
            gpos=4,
        )

        layers = project.mapLayersByName(enums.LAYERBEZ.HA_SCHAECHTE.value)         # können mehrere sein, auch wenn's nicht gewollt ist ...
        for layer in layers:
            qmlfile = os.path.join(pluginDirectory("qkan"), 'templates/qml', "HA-Schächte.qml")
            try:
                layer.loadNamedStyle(qmlfile)
            except:
                logger.error_code(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                return False

        # Layer Geometrien ändern
        layers = project.mapLayersByName(enums.LAYERBEZ.GEOMETRIEN.value)         # können mehrere sein, auch wenn's nicht gewollt ist ...
        for layer in layers:
            qmlfile = os.path.join(pluginDirectory("qkan"), 'database/migrations', "0040_Geometrien.qml")
            try:
                layer.loadNamedStyle(qmlfile)
            except:
                logger.error_code(f'Die Styledatei {qmlfile} konnte nicht gelesen werden!')
                return False

        logger.debug(f'{qkan_db=}')
        if not loadLayer(
            layerbez=enums.LAYERBEZ.MATERIAL.value,
            table='material',
            geom_column=None,
            qmlfile='Material.qml',
            filter='',
            uifile='qkan_material.ui',
            group='Referenztabellen',
            gpos=6,
            qkan_db=qkan_db,
        ):
            logger.error(
                f"Fehler beim Einfügen des Layers Material"
            )
            return False
        else:
            logger.debug(f'Layer Material geladen')

        # Attribut haltungen.rwanschluss in Attributtabelle umbenennen
        layers = project.mapLayersByName(enums.LAYERBEZ.HALTUNGEN.value)
        for layer in layers:
            fields = layer.fields()
            for i, field in enumerate(fields):
                if field.name() == 'rwanschluss':
                    layer.setFieldAlias(i, 'hat RW-Anschlüsse')

        # Layer Abflusstypen umbennen in Abflussmodelle (enums.LAYERBEZ.ABFLUSSTYPEN)
        abmodlayers = project.mapLayersByName('Abflusstypen')           # alte Bezeichnung!
        for abmodlayer in abmodlayers:
            abmodlayer.setName(enums.LAYERBEZ.ABFLUSSTYPEN.value)

        # Wertebezeichnungen für das Feld "abflusstyp" in Layer "Anbindungen Flächen" korrigieren
        reflayers = project.mapLayersByName(enums.LAYERBEZ.ABFLUSSTYPEN.value)
        if (anz := len(reflayers)) != 1:
            logger.warning_user(f'Es gibt {anz} Layer "{enums.LAYERBEZ.ABFLUSSTYPEN.value}". '
                              f'Es darf aber nur einen geben!\n'
                              f'Es wird empfohlen, mit dem Menü "QKan-Projekt übertragen" das Projekt zu aktualisieren')
        else:
            reflayer = reflayers[0]
            layers = project.mapLayersByName(enums.LAYERBEZ.ANBINDUNG_FLAECHEN.value)
            for layer in layers:
                # Alle aufgelisteten Attribute
                idx = layer.fields().indexFromName('abflusstyp')
                ews = layer.editorWidgetSetup(idx)
                ewsconf = ews.config()
                # del ewsconf['LayerSource']
                ewsconf['Layer'] = reflayer.id()
                ewsconf['LayerName'] = reflayer.name()
                ewsconf['Key'] = 'abflusstyp'
                ewsconf['Value'] = 'abflusstyp'
                ewsnew = QgsEditorWidgetSetup('ValueRelation', ewsconf)
                layer.setEditorWidgetSetup(idx, ewsnew)

                logger.debug(f'Layer {layer.name()} geändert')

                # Kontrolle
                ews = layer.editorWidgetSetup(idx)
                ewsconf = ews.config()
                logger.debug(f'{ewsconf=}')

        # Wertebeziehungen, die bisher auf Schächte verweisen, auf Knotentypen ändern
        reflayers = project.mapLayersByName(enums.LAYERBEZ.KNOTENTYP.value)
        if len(reflayers) != 1:
            logger.warning_user('Entweder fehlt der Layer "Knotentypen oder es gibt mehr als einen Layer mit '
                                'diesem Namen')
        else:
            reflayer = reflayers[0]                 # Layer, auf den die Werteliste referenziert
            layerlist = [
                (enums.LAYERBEZ.ANBINDUNG_FLAECHEN, 'schnam'),
                (enums.LAYERBEZ.ANBINDUNG_DIREKTEINLEITUNGEN, 'schnam'),
                (enums.LAYERBEZ.EINZELFLAECHEN, 'schnam'),
                (enums.LAYERBEZ.HA_LEITUNGEN, 'schoben', 'schunten'),
                (enums.LAYERBEZ.AUSSENGEBIETE, 'schnam'),
                (enums.LAYERBEZ.DROSSELN, 'schoben', 'schunten'),
                (enums.LAYERBEZ.DIREKTEINLEITUNGEN, 'schnam'),
                (enums.LAYERBEZ.GRUND_SEITENAUSLASS, 'schoben', 'schunten'),
                (enums.LAYERBEZ.HALTUNGEN, 'schoben', 'schunten'),
                (enums.LAYERBEZ.H_REGLER, 'schoben', 'schunten'),
                (enums.LAYERBEZ.ANBINDUNG_AUSSENGEBIETE, 'schnam'),
                (enums.LAYERBEZ.PUMPEN, 'schoben', 'schunten'),
                (enums.LAYERBEZ.Q_REGLER, 'schoben', 'schunten'),
                (enums.LAYERBEZ.SCHIEBER, 'schoben', 'schunten'),
                (enums.LAYERBEZ.WEHRE, 'schoben', 'schunten'),
            ]
            # Alle Layernamen aus layerlist
            for (layername, *attrs) in layerlist:
                layers = project.mapLayersByName(layername.value)
                # Jedes Auftreten dieses Layernamens
                for layer in layers:
                    # Alle aufgelisteten Attribute
                    for attr in attrs:
                        idx = layer.fields().indexFromName(attr)
                        ews = layer.editorWidgetSetup(idx)
                        ewsconf = ews.config()
                        ewsconf['Layer'] = reflayer.id()
                        ewsconf['LayerName'] = reflayer.name()
                        ewsnew = QgsEditorWidgetSetup('ValueRelation', ewsconf)
                        layer.setEditorWidgetSetup(idx, ewsnew)

                        logger.debug(f'Layer {layer.name()} geändert')

        project.write(pname)
        project.clear()
        project.setDirty(False)

    return True
