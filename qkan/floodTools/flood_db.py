__author__ = "Jörg Höttges"

import os.path
import yaml

from qgis.utils import spatialite_connect, pluginDirectory

from qkan.utils import get_logger, QkanDbError, QkanUserError, QkanAbortError

from qkan import QKan, enums

from typing import Any, List, Optional, Union, cast, Dict, Tuple

logger = get_logger("QKan.floodTools.flood_db")

class FloodDB:
    """Zugriff auf eine SQLite Datenbank"""

    def __init__(self, dbname):
        """Initialiseren der Datenbankverbindung.
           Wenn die Datenbank nicht existiert, wird sie neu angelegt"""

        if os.path.exists(dbname):
            self.db = spatialite_connect(
                database=dbname, check_same_thread=False
            )
            self.conn = self.db.cursor()
        else:
            self.db = spatialite_connect(
                database=dbname, check_same_thread=False
            )
            self.conn = self.db.cursor()
            self.conn.execute("SELECT InitSpatialMetaData()")

        # Init logging
        self.logger = get_logger("QKan.floodTools.application_dialog")

        self.dbtype = None

        self.sqlnam = None
        self.sqls = {}
        self.dbtype = enums.QKanDBChoice.SPATIALITE

    def __del__(self):
        self.logger.debug('FloodDB.__del__')
        self.db.commit()                                # Transaktionen abschliessen
        self.db.close()                                 # Datenbankzugriff lösen

    def __enter__(self):
        """Allows use via context manager (e.g. with)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Allows use via context manager (e.g. with)"""
        self.logger.debug('FloodDB.__exit__')

    def sql(self, sql, kommentar='', parameters=None, many=False):
        # SQL-Anweisung in Datenbank ausführen
        if many:
            try:
                self.conn.executemany(sql, parameters)
                # self.logger.debug(f'FloodDB.sql: {sql=}, {parameters=}')
                return True
            except self.db.Error as errortext:
                self.logger.error(f'Fehler in Datenbankaufruf {kommentar}:\n{errortext}\n{sql=}\n,{many=}, {parameters=}')
                return False
        else:
            try:
                self.conn.execute(sql, parameters)
                # self.logger.debug(f'FloodDB.sql: {sql=}, {parameters=}')
                return True
            except self.db.Error as errortext:
                self.logger.error(f'Fehler in Datenbankaufruf {kommentar}:\n{errortext}\n{sql=}\n,{parameters=}')
                return False

    def sqllis(self, sqllis, kommentar=''):
        # SQL-Anweisung in Datenbank ausführen
        for sql in sqllis:
            try:
                self.conn.execute(sql)
                # self.logger.debug(f'FloodDB.sqlmany {kommentar}:\n{sql=}')
            except self.db.Error as errortext:
                self.logger.error(f'Fehler in Datenbankaufruf {kommentar}:\n{errortext}\n{sql=}')
                return False
        return True

    def sqlyml(
            self,
            sqlnam: str,
            stmt_category: str = "allgemein",
            parameters: Union[Tuple, List, dict[str, Any]] = (),
            many: bool = False,
            mute_logger: bool = False,
            ignore: bool = False,
            replacefun: Union[callable, None] = None
    ) -> bool:
        """Wrapper for sql(). Reads sql from dict and optionaly replaces
           parameters using the format function replacefun.

           dict must first be read from module specific yaml file "sqlite.yml" / "postgres.yml"
           using db_qkan.loadmodule()

        :sqlnam:                Name of the SQL-statement in dict 'sqls'
        :type sqlnam:           String

        :stmt_category:         Category name. Allows suppression of sql-statement in logfile for
                                2 seconds appending on mute_logger
        :type stmt_category:    String

        :parameters:            parameters used in sql statement
        :type parameters:       Tuple, List or Dict

        :many:                  executes sql for every element in parameters -> must be a sequence of lists
        :type many:             Boolean

        :mute_logger:           suppress logging message for the same stmt_category for 2 seconds
        :type mute_logger:      Boolean

        :ignore:                ignore error and continue
        :type ignore:           Boolean

        :replacefun:            function which replaces variables in sql expression
        :type replacefun:       function

        :returns: void"""

        if sqlnam != self.sqlnam:
            self.sqlnam = sqlnam
            try:
                self.sql_txt = self.sqls[sqlnam].replace('*/ ', '*/\n').strip()
            except:
                logger.error_code(
                    f'{self.__class__.__name__}: '
                    f'SQL {sqlnam} nicht gefunden\n'
                    f'{stmt_category=}'
                    f'Möglicherweise wurde im Modulcode vergessen db_qkan.loadmodule aufzurufen.\n'
                    f'geladene SQLs:\n{self.sqls}'
                )

        # Die nachfolgende Funktion muss auch bei gleichem Abfragetyp durchgeführt werden, siehe _plausi.py
        if replacefun is not None:
            self.sqltext = replacefun(self.sql_txt)
            if '{' in self.sqltext:
                logger.error_code(
                    f'{self.__class__.__name__}: '
                    f'Fehler in yaml-Datei: sql enthält Parameter, obwohl keine ersetzen-Funktion'
                    f'im Aufruf geliefert wird.')
        else:
            self.sqltext = self.sql_txt

        try:
            erg = self.sql(
                sql=self.sqltext,
                parameters=parameters,
                many=many
            )
        except:
            logger.error_code(
                f'{self.__class__.__name__}: \n'
                f'SQL-Name: {sqlnam}'
            )
            raise QkanDbError
        return erg

    def fetchone(self):
        """Einen Datensatz abfragen"""
        dataset = self.conn.fetchone()
        return dataset

    def fetchall(self):
        """Alle Datensätze abfragen"""
        dataset = self.conn.fetchall()
        return dataset

    def select(self, sqltext, kommentar=''):
        """Führt eine SQL-Abfrage aus und gibt alle Datensätze zurück"""
        if self.sql(sqltext, kommentar):
            dataset = self.fetchall()
            return dataset
        else:
            return None

    def selectyml(self, sqlnam, kommentar=''):
        """Führt eine SQL-Abfrage aus und gibt alle Datensätze zurück"""
        if self.sqlyml(sqlnam, kommentar):
            dataset = self.fetchall()
            return dataset
        else:
            return None

    def commit(self):
        logger.debug('commit ...')
        self.db.commit()

    def loadmodule(self, module) -> None:
        """Lädt Modul spezifische SQL-Statements. Kann beliebig oft aufgerufen werden, da
        geprüft wird, ob ein Modul schon geladen wurde"""

        self.module = module
        # Bei Wechsel des Datenbanktyps QKan.sqls zurücksetzen
        if QKan.dbtype != self.dbtype:
            QKan.sqls = {}
        # Queries zu diesem Modul laden, wenn noch nicht geschehen oder Modul geändert und Modul-Sqls
        # noch nicht gelesen
        if not QKan.dbtype or not QKan.sqls.get(module):
            QKan.dbtype = self.dbtype
            if QKan.dbtype is None:
                logger.warning_user("Es wurde noch kein Projekt geladen!")
                raise QkanUserError
            elif QKan.dbtype == enums.QKanDBChoice.SPATIALITE:
                sqlfilename = os.path.join(pluginDirectory("qkan"), module, 'sqlite.yml')
            elif QKan.dbtype == enums.QKanDBChoice.POSTGIS:
                sqlfilename = os.path.join(pluginDirectory("qkan"), module, 'postgres.yml')
            else:
                logger.error_code(f'{self.__class__.__name__}: Datenbanktyp {QKan.dbtype} nicht zulässig!')
                raise QkanDbError

            try:
                with open(sqlfilename) as fr:
                    sql_yml = yaml.safe_load(fr.read())
                    logger.debug(f"{module=}: {QKan.sqls.get(module)=}")
                    if QKan.sqls.get(module) is None:
                        QKan.sqls[module] = sql_yml
                    else:
                        QKan.sqls[module].update(sql_yml)
                logger.debug(f'{self.__class__.__name__}: SQL-Liste aus Datei {sqlfilename=} geladen')
            except UnicodeDecodeError as err:
                logger.error_code(f'{self.__class__.__name__}, Fehler {err}: '
                                  f'Yaml-Datei {sqlfilename} konnte nicht gelesen werden, '
                                  f'weil sie nicht UTF-8-codiert ist. Bitte umwandeln')
                raise QkanAbortError
            except BaseException as err:
                logger.error_code(f'{self.__class__.__name__}, Fehler {err}: '
                                  f'Yaml-Datei {sqlfilename} konnte nicht gelesen werden')
                raise QkanAbortError

        # set sqls for active module
        self.sqls.update(QKan.sqls[module])
