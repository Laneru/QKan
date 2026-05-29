from qkan import enums

# noinspection PyUnresolvedReferences
from qgis.testing import unittest
from zipfile import ZipFile

from .base_test import BASE_WORK, BASE_DATA, QgisTest
from qkan import QKan

from qkan.sync._compare import CompareTask

# Fuer einen Test mit PyCharm Workingdir auf C:\Users\...\default\python\plugins einstellen (d. h. "\test" löschen)
class TestCompare(QgisTest):
    """Test des Moduls Plausi"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # Extract files
        with ZipFile(BASE_DATA / "test_sync.zip") as z:
            z.extractall(BASE_WORK)

    def test_compare(self) -> None:

        QKan.config.database.qkan = str(BASE_WORK / "nette.sqlite")
        QKan.config.project.file = str(BASE_WORK / "plan.qgs")
        QKan.config.sync.ext = str(BASE_WORK / "v220" / "nette_220.sqlite")
        QKan.config.epsg = 25832

        QKan.config.database.type = enums.QKanDBChoice.SPATIALITE

        QKan.config.sync.check_schaechte_insp = False
        QKan.config.sync.check_haltungen_insp = False
        QKan.config.sync.check_haleitungen_insp = False

        QKan.config.sync.check_schaechte = True
        QKan.config.sync.check_haltungen = True
        QKan.config.sync.check_haschaechte = True
        QKan.config.sync.check_haleitungen = True
        QKan.config.sync.check_flaechen = True
        QKan.config.sync.check_einleitdirekt = True
        QKan.config.sync.check_einleitdirekt = True
        QKan.config.sync.check_tezg = True
        QKan.config.sync.check_linkfl = True
        QKan.config.sync.check_linksw = True
        QKan.config.sync.check_linksw = True
        QKan.config.sync.check_schaechte_insp = True
        QKan.config.sync.check_schaechte_insp = True
        QKan.config.sync.check_haltungen_insp = True
        QKan.config.sync.check_haltungen_insp = True
        QKan.config.sync.check_haleitungen_insp = True
        QKan.config.sync.check_haleitungen_insp = True
        QKan.config.sync.check_notizen = True
        QKan.config.sync.check_symbole = True
        QKan.config.sync.check_plausi = True
        QKan.config.sync.ckeck_refdata = True

        QKan.config.sync.check_showAttrTables = False

        task = CompareTask()
        task.run()
        del task

        # self.assertTrue(False, "Fehlernachricht")

if __name__ == "__main__":
    unittest.main()
