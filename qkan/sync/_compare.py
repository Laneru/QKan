from qgis.core import Qgis, QgsProject
from qgis.PyQt.QtWidgets import QProgressBar

from qkan.database.dbfunc import DBConnection
from qkan import QKan, enums

from qkan.utils import get_logger, QkanDbError
from qkan.tools.qkan_utils import loadLayer

logger = get_logger("QKan.sync._compare")


class CompareTask:
    def run(self, test: bool = False) -> bool:

        iface = QKan.instance.iface

        # Create progress bar
        progress_bar = QProgressBar(iface.messageBar())
        progress_bar.setRange(0, 100)

        status_message = iface.messageBar().createMessage(
            "", "Abgleich ausführen..."
        )
        status_message.layout().addWidget(progress_bar)
        iface.messageBar().pushWidget(status_message, Qgis.MessageLevel.Info, 5)

        progress_bar.setValue(20)

        with DBConnection(dbname=QKan.config.database.qkan) as db_qkan:

            # SQL-Statements für dieses Modul laden
            # db_qkan.loadmodule('sync')

            if not db_qkan.sql(
                sql='ATTACH DATABASE ? AS ext;',
                stmt_category='compare_dbs',
                parameters=(QKan.config.sync.ext,),
            ):
                logger.error_data(f'Datenbank {QKan.config.sync.ext=} konnte nicht angebunden werden')
                raise QkanDbError

            # Ergänzen der SQL-Abfragen für sync
            if QKan.config.database.type == enums.QKanDBChoice.SPATIALITE:
                from ._create_yml import _create_yml_spatialite
                _create_yml_spatialite(db_qkan)
            elif QKan.config.database.type == enums.QKanDBChoice.POSTGIS:
                from ._create_yml import _create_yml_postgis
                _create_yml_postgis(db_qkan)

            # anz = len(db_qkan.sqls)
            # logger.debug(f"Anzahl SQLs in 'sync': {anz}")

            # Vergleich aller gewählten Tabellen
            _check_medien = any(
                [
                    QKan.config.sync.check_schaechte_insp,
                    QKan.config.sync.check_haltungen_insp,
                    QKan.config.sync.check_haleitungen_insp,
                ]
            )

            # Auflistung für Synchronisationslayer:
            # - Tabellenname in der QKan-Datenbank
            # - Nutzerauswahl
            # - Liste von Layerbezeichnungen:
            #    · Synchronisationslayer
            #    · externer Layer
            #    · Originallayer (nur zur Übernahme des Layerstils)
            # - Gruppenname (wird an Pfad QKan > Synchronisation > angehängt)
            tables = [
                [
                    'schaechte',
                    QKan.config.sync.check_schaechte,
                    [
                        enums.LAYERBEZ.SYNC_SCHAECHTE_COMPARE.value,
                        enums.LAYERBEZ.SYNC_SCHAECHTE_EXT.value,
                        enums.LAYERBEZ.SCHAECHTE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_SCHAECHTE.value,
                ],
                [
                    'haltungen',
                    QKan.config.sync.check_haltungen,
                    [
                        enums.LAYERBEZ.SYNC_HALTUNGEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_HALTUNGEN_EXT.value,
                        enums.LAYERBEZ.HALTUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_HALTUNGEN.value,
                ],
                [
                    'anschlussschaechte',
                    QKan.config.sync.check_haschaechte,
                    [
                        enums.LAYERBEZ.SYNC_HA_SCHAECHTE_COMPARE.value,
                        enums.LAYERBEZ.SYNC_HA_SCHAECHTE_EXT.value,
                        enums.LAYERBEZ.HA_SCHAECHTE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_HA_SCHAECHTE.value,
                ],
                [
                    'anschlussleitungen',
                    QKan.config.sync.check_haleitungen,
                    [
                        enums.LAYERBEZ.SYNC_HA_LEITUNGEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_HA_LEITUNGEN_EXT.value,
                        enums.LAYERBEZ.HA_LEITUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_HA_LEITUNGEN.value,
                ],
                [
                    'flaechen',
                    QKan.config.sync.check_flaechen,
                    [
                        enums.LAYERBEZ.SYNC_FLAECHEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_FLAECHEN_EXT.value,
                        enums.LAYERBEZ.EINZELFLAECHEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_FLAECHEN.value,
                ],
                [
                    'einleit',
                    QKan.config.sync.check_einleitdirekt,               # gleicher Schalter check_einleitdirekt
                    [
                        enums.LAYERBEZ.SYNC_DIREKT_COMPARE.value,
                        enums.LAYERBEZ.SYNC_DIREKT_EXT.value,
                        enums.LAYERBEZ.DIREKTEINLEITUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_DIREKT.value,
                ],
                [
                    'aussengebiete',
                    QKan.config.sync.check_einleitdirekt,               # gleicher Schalter check_einleitdirekt
                    [
                        enums.LAYERBEZ.SYNC_AUSSEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_AUSSEN_EXT.value,
                        enums.LAYERBEZ.AUSSENGEBIETE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_AUSSEN.value,
                ],
                [
                    'tezg',
                    QKan.config.sync.check_tezg,
                    [
                        enums.LAYERBEZ.SYNC_TEZG_COMPARE.value,
                        enums.LAYERBEZ.SYNC_TEZG_EXT.value,
                        enums.LAYERBEZ.TEILGEBIETE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_TEZG.value,
                ],
                [
                    'linkfl',
                    QKan.config.sync.check_linkfl,
                    [
                        enums.LAYERBEZ.SYNC_ANBINDUNG_FLAECHEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_ANBINDUNG_FLAECHEN_EXT.value,
                        enums.LAYERBEZ.ANBINDUNG_FLAECHEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_FLAECHEN.value,
                ],
                [
                    'linksw',
                    QKan.config.sync.check_linksw,                      # gleicher Schalter check_linksw
                    [
                        enums.LAYERBEZ.SYNC_ANBINDUNG_DIREKT_COMPARE.value,
                        enums.LAYERBEZ.SYNC_ANBINDUNG_DIREKT_EXT.value,
                        enums.LAYERBEZ.ANBINDUNG_DIREKTEINLEITUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_DIREKT.value,
                ],
                [
                    'linkageb',
                    QKan.config.sync.check_linksw,                      # gleicher Schalter check_linksw
                    [
                        enums.LAYERBEZ.SYNC_ANBINDUNG_AUSSEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_ANBINDUNG_AUSSEN_EXT.value,
                        enums.LAYERBEZ.ANBINDUNG_AUSSENGEBIETE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_ANBINDUNG_AUSSEN.value,
                ],
                [
                    'schaechte_untersucht',
                    QKan.config.sync.check_schaechte_insp,
                    [
                        enums.LAYERBEZ.SYNC_ZUSTAND_SCHAECHTE_COMPARE.value,
                        enums.LAYERBEZ.SYNC_ZUSTAND_SCHAECHTE_EXT.value,
                        enums.LAYERBEZ.ZUSTAND_SCHAECHTE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_ZUSTAND_SCHAECHTE.value,
                ],
                [
                    'untersuchdat_schacht',
                    QKan.config.sync.check_schaechte_insp,
                    [
                        enums.LAYERBEZ.SYNC_SCHAEDEN_SCHAECHTE_COMPARE.value,
                        enums.LAYERBEZ.SYNC_SCHAEDEN_SCHAECHTE_EXT.value,
                        enums.LAYERBEZ.EINZELSCHAEDEN_SCHAECHTE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_SCHAEDEN_SCHAECHTE.value,
                ],
                [
                    'haltungen_untersucht',
                    QKan.config.sync.check_haltungen_insp,
                    [
                        enums.LAYERBEZ.SYNC_ZUSTAND_HALTUNGEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_ZUSTAND_HALTUNGEN_EXT.value,
                        enums.LAYERBEZ.ZUSTAND_HALTUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_ZUSTAND_HALTUNGEN.value,
                ],
                [
                    'untersuchdat_haltung',
                    QKan.config.sync.check_haltungen_insp,
                    [
                        enums.LAYERBEZ.SYNC_SCHAEDEN_HALTUNGEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_SCHAEDEN_HALTUNGEN_EXT.value,
                        enums.LAYERBEZ.EINZELSCHAEDEN_HALTUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_SCHAEDEN_HALTUNGEN.value,
                ],
                [
                    'anschlussleitungen_untersucht',
                    QKan.config.sync.check_haleitungen_insp,
                    [
                        enums.LAYERBEZ.SYNC_ZUSTAND_HA_LEITUNGEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_ZUSTAND_HA_LEITUNGEN_EXT.value,
                        enums.LAYERBEZ.ZUSTAND_HA_LEITUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_ZUSTAND_HA_LEITUNGEN.value,
                ],
                [
                    'untersuchdat_anschlussleitung',
                    QKan.config.sync.check_haleitungen_insp,
                    [
                        enums.LAYERBEZ.SYNC_SCHAEDEN_HA_LEITUNGEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_SCHAEDEN_HA_LEITUNGEN_EXT.value,
                        enums.LAYERBEZ.EINZELSCHAEDEN_HA_LEITUNGEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_SCHAEDEN_HA_LEITUNGEN.value,
                ],
                [
                    'notizen',
                    QKan.config.sync.check_notizen,
                    [
                        enums.LAYERBEZ.SYNC_NOTIZEN_COMPARE.value,
                        enums.LAYERBEZ.SYNC_NOTIZEN_EXT.value,
                        enums.LAYERBEZ.NOTIZEN.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_NOTIZEN.value,
                ],
                [
                    'symbole',
                    QKan.config.sync.check_symbole,
                    [
                        enums.LAYERBEZ.SYNC_SYMBOLE_COMPARE.value,
                        enums.LAYERBEZ.SYNC_SYMBOLE_EXT.value,
                        enums.LAYERBEZ.SYMBOLE.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_SYMBOLE.value,
                ],
                [
                    'pruefsql',
                    QKan.config.sync.check_plausi,
                    [
                        enums.LAYERBEZ.SYNC_PLAUSI_COMPARE.value,
                        enums.LAYERBEZ.SYNC_PLAUSI_EXT.value,
                        enums.LAYERBEZ.PLAUSISQL.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_PLAUSI.value,
                ],
                [
                    'videos',
                    _check_medien,                                       # gleicher Schalter _check_medien, s.o.
                    [
                        enums.LAYERBEZ.SYNC_VIDEOS_COMPARE.value,
                        enums.LAYERBEZ.SYNC_VIDEOS_EXT.value,
                        enums.LAYERBEZ.VIDEOS.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_VIDEOS.value,
                ],
                [
                    'fotos',
                    _check_medien,                                       # gleicher Schalter _check_medien, s.o.
                    [
                        enums.LAYERBEZ.SYNC_FOTOS_COMPARE.value,
                        enums.LAYERBEZ.SYNC_FOTOS_EXT.value,
                        enums.LAYERBEZ.FOTOS.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_FOTOS.value,
                ],
                [
                    'refdata',
                    QKan.config.sync.ckeck_refdata,
                    [
                        enums.LAYERBEZ.SYNC_REFDATA_COMPARE.value,
                        enums.LAYERBEZ.SYNC_REFDATA_EXT.value,
                        enums.LAYERBEZ.REFDATA.value,
                    ],
                    enums.LAYERBEZ.SYNC_GROUP_REFDATA.value,
                ],
            ]

            # anz = len(db_qkan.sqls)
            # logger.debug(f"Anzahl SQLs in 'sync': {anz}")

            # 1. Sync-Tabellen löschen
            for tabnam, userchoice, _, _ in tables:
                # tableexist = db_qkan.attrlist(tabnam)
                tableexist = db_qkan.sqls.get(f'sync_create_{tabnam}')

                if userchoice and tableexist:
                    sqlnam = f'sync_drop_{tabnam}'
                    if not db_qkan.sqlyml(
                            sqlnam,
                            stmt_category='comp_1',
                    ):
                        logger.error_code(f'SQL-Fehler: {sqlnam=}, {tabnam=}')
                    if tabnam not in enums.SyncTables.TABLES_ATTR.value:
                        sqlnam = f'sync_drop_{tabnam}_geom'
                        if not db_qkan.sqlyml(
                                sqlnam,
                                stmt_category='comp_2',
                        ):
                            logger.error_code(f'SQL-Fehler: {sqlnam=}, {tabnam=}')
            db_qkan.commit()

            for tabnam, userchoice, _, _ in tables:
                # tableexist = db_qkan.attrlist(tabnam)
                tableexist = db_qkan.sqls.get(f'sync_create_{tabnam}')

                if userchoice and tableexist:
            # 2. Sync-Tabellen (neu) erstellen und Vergleich ausführen
                    if tabnam in enums.SyncTables.TABLES_ATTR.value:
                        sqlnames = [
                            f'sync_create_{tabnam}',
                        ]
                    else:
                        sqlnames = [
                            f'sync_create_{tabnam}',
                            f'sync_create_{tabnam}_geom',
                        ]

                    for sqlnam in sqlnames:
                        if not db_qkan.sqlyml(
                            sqlnam,
                            stmt_category='comp_3',
                            parameters={
                                'epsg': QKan.config.epsg,
                            }
                        ):
                            logger.error_code(f'SQL-Fehler: {sqlnam=}, {tabnam=}')

            # 3. Vergleich ausführen
                    sqlnames = [
                        # f'sync_reset_{tabnam}',
                        f'sync_{tabnam}_ext',
                        f'sync_{tabnam}_local',
                        f'sync_{tabnam}_dif',
                    ]
                    if tabnam not in enums.SyncTables.TABLES_UNTERSUCH.value:
                        sqlnames += [
                            f'sync_{tabnam}_be_redundant',
                            f'sync_{tabnam}_ex_redundant',
                        ]
                    for sqlnam in sqlnames:
                        if not db_qkan.sqlyml(
                            sqlnam,
                            stmt_category='comp_4',
                            parameters={
                                'status_add': QKan.config.sync.check_add,
                                'status_mod': QKan.config.sync.check_mod,
                                'status_del': QKan.config.sync.check_del,
                            }
                        ):
                            logger.error_code(f'SQL-Fehler: {sqlnam=}, {tabnam=}')

            db_qkan.commit()

        if test:
            return True

        project = QgsProject.instance()
        for tabnam, userchoice, layers, group in tables:
            if userchoice:
                grouppath = [
                    enums.LAYERBEZ.QKAN_GROUP.value,
                    enums.LAYERBEZ.SYNC_GROUP_SYNCHRONISATION.value,
                    group,
                ]
                layer_sync, layer_ext, layer_loc = layers

                # Geo-Objekt
                if tabnam in enums.SyncTables.TABLES_GEOM.value:
                    gobj = 'geom'
                elif tabnam in enums.SyncTables.TABLES_GEOP.value:
                    gobj = 'geop'
                elif tabnam in enums.SyncTables.TABLES_GLINK.value:
                    gobj = 'glink'
                elif tabnam in enums.SyncTables.TABLES_ATTR.value:
                    gobj = None
                else:
                    logger.error_code(f'Fehler: {tabnam=} konnte in den Tabellenlisten nicht gefunden werden')
                    raise QkanDbError

                # Synchronisationstabelle
                loadLayer(
                    layerbez=   layer_sync,
                    table=      f'sync_{tabnam}',
                    geom_column=None if gobj is None else 'geom',
                    qmlfile=    f'{layer_sync}.qml',
                    filter=     '',
                    uifile=     f'sync_{tabnam}.ui',
                    group=      grouppath,
                    exclusive=  True,
                )

                loadLayer(
                    layerbez=   layer_ext,
                    table=      tabnam,
                    geom_column=gobj,
                    qmlfile=    f'{layer_loc}.qml',
                    filter=     '',
                    uifile=     f'qkan_{tabnam}.ui',
                    group=      grouppath,
                    gpos=       0,
                    qkan_db=    QKan.config.sync.ext,
                )

                loadLayer(
                    layerbez=   f'{layer_loc} Bestand',
                    table=      tabnam,
                    geom_column=gobj,
                    qmlfile=    f'{layer_loc}.qml',
                    filter=     '',
                    uifile=     f'qkan_{tabnam}.ui',
                    group=      grouppath,
                    gpos=       0,
                    qkan_db=    QKan.config.database.qkan,
                )

                # Synchronisationslayer sichtbar machen
                layer = project.mapLayersByName(layer_sync)[0]
                root = QgsProject.instance().layerTreeRoot()
                layer_node = root.findLayer(layer.id())
                layer_node.setItemVisibilityChecked(True)

        # Attributtabellen anzeigen
        if QKan.config.sync.check_showAttrTables:
            for _, userchoice, layers, _ in tables:
                if userchoice:
                    layercomp = layers[0]
                    layer = project.mapLayersByName(layercomp)[0]
                    nds = layer.featureCount()
                    if nds > 0:
                        iface.showAttributeTable(layer)

        progress_bar.setValue(100)
        status_message.setText("Vergleich der ausgewählten Tabellen abgeschlossen.")
        status_message.setLevel(Qgis.MessageLevel.Success)

        return True

