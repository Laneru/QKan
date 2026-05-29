from qkan.database.dbfunc import DBConnection
from qkan.utils import get_logger, QkanDbError
VERSION = "3.4.9"  # must be higher than previous one and correspond with qkan_database.py: __dbVersion__

logger = get_logger("QKan.database.migrations.0041")

def run(dbcon: DBConnection) -> bool:
    # Ergänzung einiger Felder in Videos

    if 'untersuchrichtung' not in dbcon.attrlist('videos'):
        try:
            dbcon.alter_table(
                tabnam='videos',
                # Untersuchungsrichtung nach name und untersuchtag einfügen ...
                attributes_new=[
                    "name TEXT",
                    "untersuchtag TEXT",
                    "untersuchrichtung TEXT",
                ],
            )
        except:
            logger.error_code('Fehlgeschlagen: migration_0041, untersuchrichtung ergänzen')

    if 'untersuchrichtung' not in dbcon.attrlist('untersuchdat_haltungen'):
        try:
            dbcon.alter_table(
                tabnam='videos',
                # Untersuchungsrichtung nach name und untersuchtag einfügen ...
                attributes_new=[
                    "untersuchhal TEXT",
                    "schoben TEXT                                   /* join schaechte.schnam  */ ",
                    "schunten TEXT                                  /* join schaechte.schnam */ ",
                    "id INTEGER                                     /* absolute Nummer der Inspektion */ ",
                    "untersuchtag TEXT",
                    "untersuchrichtung TEXT",
                ],
            )
        except:
            logger.error_code('Fehlgeschlagen: migration_0041, untersuchrichtung ergänzen')

    return True
