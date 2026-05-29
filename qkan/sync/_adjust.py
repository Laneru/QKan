from typing import Optional
from qgis.core import Qgis
from qgis.PyQt.QtWidgets import QProgressBar
from datetime import datetime as dtim
import os
from pathlib import Path
import tempfile

from qkan import QKan, enums
from qkan.database.dbfunc import DBConnection

from qkan.utils import get_logger, QkanDbError

logger = get_logger("QKan.sync._adjust")

progress_bar: Optional[QProgressBar] = None


class AdjustTask:
    def __init__(
        self,
    ):
        pass

    def run(self) -> bool:

        iface = QKan.instance.iface

        # Create progress bar
        progress_bar = QProgressBar(iface.messageBar())
        progress_bar.setRange(0, 100)

        status_message = iface.messageBar().createMessage(
            "", "Synchronisation durchführen..."
        )
        status_message.layout().addWidget(progress_bar)
        iface.messageBar().pushWidget(status_message, Qgis.MessageLevel.Info, 5)

        progress_bar.setValue(20)

        with DBConnection(dbname=QKan.config.database.qkan) as db_qkan:

            # SQL-Statements für dieses Modul laden
            # db_qkan.loadmodule('sync')


            if not db_qkan.sql(
                sql='ATTACH DATABASE ? AS ext;',
                stmt_category='synchronisation_dbs',
                parameters=(QKan.config.sync.ext,),
            ):
                logger.error_data(f'Datenbank {QKan.config.sync.ext=} konnte nicht angebunden werden')
                raise QkanDbError


            # Ergänzen der SQL-Abfragen für sync
            if QKan.sqls.get('sync_create_haltungen') is None:
                logger.debug('_adjust: sqls erneut geladen...')
                if QKan.config.database.type == enums.QKanDBChoice.SPATIALITE:
                    from ._create_yml import _create_yml_spatialite
                    _create_yml_spatialite(db_qkan)
                elif QKan.config.database.type == enums.QKanDBChoice.POSTGIS:
                    from ._create_yml import _create_yml_postgis
                    _create_yml_postgis(db_qkan)


            # Synchronisation aller gewählten Tabellen
            # Medien müssen in allen nachfolgenden Fällen berücksichtigt werden:
            check_medien = any(
                [
                    QKan.config.sync.check_schaechte_insp,
                    QKan.config.sync.check_haltungen_insp,
                    QKan.config.sync.check_haleitungen_insp
                ]
            )

            userchoices = [
                ['schaechte', QKan.config.sync.check_schaechte],
                ['haltungen', QKan.config.sync.check_haltungen],
                ['anschlussschaechte', QKan.config.sync.check_haschaechte],
                ['anschlussleitungen', QKan.config.sync.check_haleitungen],
                ['flaechen', QKan.config.sync.check_flaechen],
                ['einleit', QKan.config.sync.check_einleitdirekt],          # gleicher Schalter check_einleitdirekt
                ['aussengebiete', QKan.config.sync.check_einleitdirekt],    # gleicher Schalter check_einleitdirekt
                ['tezg', QKan.config.sync.check_tezg],
                ['linkfl', QKan.config.sync.check_linkfl],
                ['linksw', QKan.config.sync.check_linksw],                  # gleicher Schalter check_linksw
                ['linkageb', QKan.config.sync.check_linksw],                # gleicher Schalter check_linksw
                ['schaechte_untersucht', QKan.config.sync.check_schaechte_insp],
                ['untersuchdat_schacht', QKan.config.sync.check_schaechte_insp],
                ['haltungen_untersucht', QKan.config.sync.check_haltungen_insp],
                ['untersuchdat_haltung', QKan.config.sync.check_haltungen_insp],
                ['anschlussleitungen_untersucht', QKan.config.sync.check_haleitungen_insp],
                ['untersuchdat_anschlussleitung', QKan.config.sync.check_haleitungen_insp],
                ['notizen', QKan.config.sync.check_notizen],
                ['symbole', QKan.config.sync.check_symbole],
                ['pruefsql', QKan.config.sync.check_plausi],
                ['videos', check_medien],                                   # gleicher Schalter check_medien, s.o.
                ['fotos', check_medien],                                    # gleicher Schalter check_medien, s.o.
                ['refdata', QKan.config.sync.ckeck_refdata],
            ]

            try:
                protfile = open(QKan.config.sync.protfile, 'w')
            except:
                fpath = Path(tempfile.gettempdir())
                fnam = fpath / Path(QKan.config.sync.protfile).name
                protfile = open(fnam, 'w')
                logger.warning(f'Protokolldatei {QKan.config.sync.protfile=} konnte nicht geschrieben werden\n'
                               f'Stattdessen wird eine Protokolldatei {fnam} geschrieben')

            dat = dtim.now().strftime('%A, %d/%m/%y %H:%M:%S')
            protfile.write(f'Protokoll der Synchronisation am {dat}')
            for table, userchoice in userchoices:
                tableexist = db_qkan.sqls.get(f'sync_create_{table}')
                if userchoice and tableexist:
                    # Protokoll schreiben
                    sqlnam = f'sync_{table}_prot'
                    db_qkan.sqlyml(
                        sqlnam,
                        'adjust'
                    )
                    protfile.write(f'\nSynchronisation Tabelle {table}:')
                    for ds in db_qkan.fetchall():
                        line = ', '.join([f'{el}' for el in ds])
                        protfile.write(line + '\n')

                    sqlnames = [
                        f'sync_{table}_add',
                        f'sync_{table}_mod',
                        f'sync_reset_{table}',
                    ]
                    if QKan.config.sync.check_allow_deletions:
                        sqlnames.insert(2, f'sync_{table}_del')

                    # sqllis = ', '.join(sqlnames)
                    # logger.debug(f'Abgleich: {sqllis=}')

                    for sqlnam in sqlnames:
                        if not db_qkan.sqlyml(
                            sqlnam=sqlnam,
                            stmt_category='adjust',
                        ):
                            logger.error_code(f"Fehler in Abgleich: {sqlnam}")

            db_qkan.commit()
        del db_qkan

        progress_bar.setValue(100)
        status_message.setText("Synchronisation der ausgewählten Daten abgeschlossen.")
        status_message.setLevel(Qgis.MessageLevel.Success)

        return True
