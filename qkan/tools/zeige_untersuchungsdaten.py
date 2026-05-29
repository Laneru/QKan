from qgis.core import QgsProject
from qkan import QKan, enums
from qkan.utils import get_logger
from datetime import datetime as dtim
from pathlib import Path

logger = get_logger("QKan.tools.zeige_schaeden")

class ShowSelected():
    """Gemeinsame Funktion(en) für die nachfolgenden Klassen"""

    # Der Zeitstempel wird als Workaraound benötigt, um bei den Aktionen die Auswahl "Alle Objekte"
    # zu identifizieren.
    # lastcalltime = None

    def show_selected(
            self,
            layername: str = None,
            untersuchbezeich: str = None,
            untersuchattribut: str = None,
            einzel: bool = True,
    ):
        """Ändert den Layerfilter der Untersuchungsdaten

        :param layername:           Bezeichnung des untersuchten Objektes
        :type layername:            str

        :param untersuchbezeich:    Bezeichnung des untersuchten Objektes
        :type untersuchbezeich:     str

        :param untersuchattribut:   Attributname des untersuchten Objektes
        :type untersuchattribut:    str
        """

        # if ShowSelected.lastcalltime is None:
        #     ShowSelected.lastcalltime = dtim.now()
        # else:
        #     actcalltime = dtim.now()
        #     td = actcalltime - ShowSelected.lastcalltime
        #     # Wenn bei aktivierten Aktionen im Kontextmenü der Objektauswahl "Alle Objekte" angeklickt
        #     # wird, wird die Aktion direkt hintereinander für alle Objekte ausgelöst. Für diesen Fall
        #     # wird die Selektion auf untersuchtag deaktiviert. Auf ein Unterdrücken der nachfolgenden
        #     # Aktionen wird hier verzichtet, um den Code nicht noch komplizierter zu machen.
        #     if td.total_seconds() < 0.05:
        #         logger.debug(f"ShowSelected: Abbruch wegen Mehrfachaufruf")
        #         return
        #     ShowSelected.lastcalltime = actcalltime

        self.iface = QKan.instance.iface

        project = QgsProject.instance()
        if project.mapLayersByName(layername):
            layer = project.mapLayersByName(layername)[0]
        else:
            logger.debug(f"Kein Layer {layername} gefunden. Rules können nicht bearbeitet werden")
            return False
        ren = layer.renderer()
        if ren.type() != 'RuleRenderer':
            # logger.warning(f"Fehler: Der Layer '{layername}' enthält keine regelbasierenden Symbole"
            #                "\nAktualisieren Sie das Projekt oder bearbeiten den Layer entsprechend.")
            # return False
            style_file = str(Path(QKan.template_dir) / 'qml' / f'{layername}.qml')
            if style_file:
                layer.loadNamedStyle(style_file)
                layer.triggerRepaint()
                ren = layer.renderer()
                if ren.type() != 'RuleRenderer':
                    logger.error_code(f'Layerstil mit Rule {style_file=} konnte nicht geladen werden')
                    return
        try:
            root_rule = ren.rootRule()
        except BaseException as e:
            logger.error(f"Fehler: Der Layer '{layername}' enthält keine regelbasierenden Symbole")
            raise Exception(f"{self.__class__.__name__}")

        for child in root_rule.children():
            rule = root_rule.takeChild(child)
            label = rule.label()
            if 'Zustandsklasse' in label:
                pos = label.find('Zustandsklasse') + 15
                i = label[pos]
                if einzel:
                    expr = f"min(coalesce(ZD, ZB, ZS), coalesce(ZB, ZS, ZD), coalesce(ZS, ZD, ZB)) = {i}"
                else:
                    expr = (f"min(coalesce(max_ZD, max_ZB, max_ZS), "
                            f"coalesce(max_ZB, max_ZS, max_ZD), "
                            f"coalesce(max_ZS, max_ZD, max_ZB)) = {i}")
                # Filter auf Haltung, ID oder Untersuchungsdatum ergänzen:
                if untersuchbezeich is not None:
                    expr += f" AND {untersuchattribut} = '{untersuchbezeich}'"
                if self.untersuchtag is not None:
                    expr += f" AND untersuchtag = '{self.untersuchtag}'"
                elif self.id is not None:  # nur alternativ zu Untersuchungsdatum!
                    expr += f" AND id = {self.id}"
            else:
                expr = "ELSE"
            rule.setFilterExpression(expr)
            root_rule.appendChild(rule)
        layer.triggerRepaint()
        self.iface.layerTreeView().refreshLayerSymbology(layer.id())


class ShowHaltungsschaeden(ShowSelected):
    """Zeigt Zustandsdaten an Haltungen selektiv an"""

    lastcalltime = None

    def __init__(self, haltnam: str = None, schoben: str = None, schunten: str = None, untersuchtag: str = None, id: int = None):

        self.haltnam = haltnam
        self.schoben = schoben
        self.schunten = schunten
        self.untersuchtag = untersuchtag
        self.id = id
        self.showschaedencolumns = QKan.config.zustand.showschaedencolumns      # evtl. ergänzen: Eingabe unter Optionen

        # Wenn bei aktivierten Aktionen im Kontextmenü der Objektauswahl "Alle Objekte" angeklickt
        # wird, wird die Aktion direkt hintereinander für alle Objekte ausgelöst. Für diesen Fall
        # wird die Prozedur ab dem 2. Aufruf abgebrochen
        if ShowHaltungsschaeden.lastcalltime is None:
            ShowHaltungsschaeden.lastcalltime = dtim.now()
        else:
            actcalltime = dtim.now()
            td = actcalltime - ShowHaltungsschaeden.lastcalltime
            if td.total_seconds() < 0.05:
                logger.debug(f"ShowHaltungsschaeden: Abbruch wegen Mehrfachaufruf")
                return
            ShowHaltungsschaeden.lastcalltime = actcalltime

        untersuchbezeich = self.haltnam

        untersuchattribut = 'untersuchhal'
        layername = enums.LAYERBEZ.EINZELSCHAEDEN_HALTUNGEN.value
        self.show_selected(layername, untersuchbezeich, untersuchattribut, True)

        untersuchattribut = 'haltnam'
        layername = enums.LAYERBEZ.ZUSTAND_HALTUNGEN.value
        self.show_selected(layername, untersuchbezeich, untersuchattribut, False)


class ShowSchachtschaeden(ShowSelected):
    """Zeigt Zustandsdaten an Schächten selektiv an"""

    lastcalltime = None

    def __init__(self, schnam: str = None, untersuchtag: str = None, id: int = None):

        self.schnam = schnam
        self.untersuchtag = untersuchtag
        self.id = id

        # Siehe Erläuterung oben
        if ShowSchachtschaeden.lastcalltime is None:
            ShowSchachtschaeden.lastcalltime = dtim.now()
        else:
            actcalltime = dtim.now()
            td = actcalltime - ShowSchachtschaeden.lastcalltime
            if td.total_seconds() < 0.05:
                logger.debug(f"ShowSchachtschaeden: Abbruch wegen Mehrfachaufruf")
                return
            ShowSchachtschaeden.lastcalltime = actcalltime

        untersuchbezeich = self.schnam

        untersuchattribut = 'untersuchsch'
        layername = enums.LAYERBEZ.EINZELSCHAEDEN_SCHAECHTE.value
        self.show_selected(layername, untersuchbezeich, untersuchattribut, True)

        untersuchattribut = 'schnam'
        layername = enums.LAYERBEZ.ZUSTAND_SCHAECHTE.value
        self.show_selected(layername, untersuchbezeich, untersuchattribut, False)


class ShowHausanschlussschaeden(ShowSelected):
    """Zeigt Zustandsdaten an Hausanschlussleitungen selektiv an"""

    lastcalltime = None

    def __init__(self, untersuchleit: str = None, untersuchtag: str = None, id: int = None):

        self.untersuchleit = untersuchleit
        self.untersuchtag = untersuchtag
        self.id = id

        # Siehe Erläuterung oben
        if ShowHausanschlussschaeden.lastcalltime is None:
            ShowHausanschlussschaeden.lastcalltime = dtim.now()
        else:
            actcalltime = dtim.now()
            td = actcalltime - ShowHausanschlussschaeden.lastcalltime
            if td.total_seconds() < 0.05:
                logger.debug(f"ShowHausanschlussschaeden: Abbruch wegen Mehrfachaufruf")
                return
            ShowHausanschlussschaeden.lastcalltime = actcalltime

        untersuchbezeich = self.untersuchleit

        untersuchattribut = 'untersuchleit'
        layername = enums.LAYERBEZ.EINZELSCHAEDEN_HA_LEITUNGEN.value
        self.show_selected(layername, untersuchbezeich, untersuchattribut, True)

        untersuchattribut = 'leitnam'
        layername = enums.LAYERBEZ.ZUSTAND_HA_LEITUNGEN.value
        self.show_selected(layername, untersuchbezeich, untersuchattribut, False)
