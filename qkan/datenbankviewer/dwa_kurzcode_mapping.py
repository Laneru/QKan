# -*- coding: utf-8 -*-
"""
DWA-Kürzel Mapping für ISYBAU-Inspektionsdaten
Quelle: BFR Abwasser, Stand Januar 2025

Struktur: DWA_DATA[Gruppe][Kürzel][(Charakt1, Charakt2)] = Langtext
"""

DWA_DATA = {
    "Haltungen": {
        # BAA - Verformung (Tab. A-2-26)
        "BAA": {
            ("", ""): "Verformung",
            ("A", ""): "vertikal - die Höhe des Rohres hat sich verringert",
            ("B", ""): "horizontal - die Rohrweite hat sich verringert",
        },

        # BAB - Rissbildung (Tab. A-2-27)
        "BAB": {
            ("", ""): "Rissbildung",
            ("A", "A"): "Oberflächenriss (Haarriss); in Längsrichtung",
            ("A", "B"): "Oberflächenriss (Haarriss); am Rohrumfang",
            ("A", "C"): "Oberflächenriss (Haarriss); komplexe Rissbildung",
            ("A", "D"): "Oberflächenriss (Haarriss); gewundene oder spiralförmige Rissbildung",
            ("A", "E"): "Oberflächenriss (Haarriss); von einem Punkt ausgehende Ausbreitung",
            ("B", "A"): "Riss - Risslinien erkennbar, Segmente am Platz; in Längsrichtung",
            ("B", "B"): "Riss - Risslinien erkennbar, Segmente am Platz; am Rohrumfang",
            ("B", "C"): "Riss - Risslinien erkennbar, Segmente am Platz; komplexe Rissbildung",
            ("B", "D"): "Riss - Risslinien erkennbar, Segmente am Platz; gewundene oder spiralförmige Rissbildung",
            ("B", "E"): "Riss - Risslinien erkennbar, Segmente am Platz; von einem Punkt ausgehende Ausbreitung",
            ("C", "A"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; in Längsrichtung",
            ("C", "B"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; am Rohrumfang",
            ("C", "C"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; komplexe Rissbildung",
            ("C", "D"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; gewundene oder spiralförmige Rissbildung",
            ("C", "E"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; von einem Punkt ausgehende Ausbreitung",
        },

        # BAC - Rohrbruch/Einsturz (Tab. A-2-28)
        "BAC": {
            ("", ""): "Rohrbruch/Einsturz",
            ("A", ""): "Bruch - Segmente sichtbar verschoben, aber nicht fehlend",
            ("B", ""): "Fehlen von Teilen - Segmente der Rohrwand fehlen",
            ("C", ""): "Einsturz - Konstruktionsgefüge vollständig zerstört",
        },

        # BAD - Defektes Mauerwerk (Tab. A-2-29)
        "BAD": {
            ("", ""): "Defektes Mauerwerk",
            ("A", "A"): "verschoben - Mauersteine/Ziegel aus ursprünglicher Lage verschoben; weitere Mauerwerksschicht sichtbar",
            ("A", "B"): "verschoben - Mauersteine/Ziegel aus ursprünglicher Lage verschoben; es ist nichts zu sehen",
            ("B", "A"): "fehlend - Mauersteine/Ziegel fehlen; weitere Mauerwerksschicht sichtbar",
            ("B", "B"): "fehlend - Mauersteine/Ziegel fehlen; es ist nichts zu sehen",
            ("C", "A"): "Sohle abgesackt; weitere Mauerwerksschicht sichtbar",
            ("C", "B"): "Sohle abgesackt; es ist nichts zu sehen",
            ("D", "A"): "Einsturz - Konstruktionsgefüge vollständig zerstört; weitere Mauerwerksschicht sichtbar",
            ("D", "B"): "Einsturz - Konstruktionsgefüge vollständig zerstört; es ist nichts zu sehen",
        },

        # BAE - Fehlender Mörtel (Tab. A-2-30)
        "BAE": {
            ("", ""): "Fehlender Mörtel",
        },

        # BAF - Oberflächenschaden (Tab. A-2-31)
        "BAF": {
            ("", ""): "Oberflächenschaden",
            ("A", "A"): "erhöhte Rauheit; mechanisch",
            ("A", "B"): "erhöhte Rauheit; chemisch - allgemein",
            ("A", "C"): "erhöhte Rauheit; chemisch - Beschädigung im oberen Teil des Rohres",
            ("A", "D"): "erhöhte Rauheit; chemisch - Beschädigung im unteren Teil des Rohres",
            ("A", "E"): "erhöhte Rauheit; Ursache nicht eindeutig feststellbar",
            ("A", "Z"): "erhöhte Rauheit; andere Ursache",
            ("B", "A"): "Abplatzung; mechanisch",
            ("B", "E"): "Abplatzung; Ursache nicht eindeutig feststellbar",
            ("B", "Z"): "Abplatzung; andere Ursache",
            ("C", "A"): "Zuschlagstoffe sichtbar; mechanisch",
            ("C", "B"): "Zuschlagstoffe sichtbar; chemisch - allgemein",
            ("C", "C"): "Zuschlagstoffe sichtbar; chemisch - Beschädigung im oberen Teil des Rohres",
            ("C", "D"): "Zuschlagstoffe sichtbar; chemisch - Beschädigung im unteren Teil des Rohres",
            ("C", "E"): "Zuschlagstoffe sichtbar; Ursache nicht eindeutig feststellbar",
            ("C", "Z"): "Zuschlagstoffe sichtbar; andere Ursache",
            ("D", "A"): "Zuschlagstoffe einragend; mechanisch",
            ("D", "B"): "Zuschlagstoffe einragend; chemisch - allgemein",
            ("D", "C"): "Zuschlagstoffe einragend; chemisch - Beschädigung im oberen Teil des Rohres",
            ("D", "D"): "Zuschlagstoffe einragend; chemisch - Beschädigung im unteren Teil des Rohres",
            ("D", "E"): "Zuschlagstoffe einragend; Ursache nicht eindeutig feststellbar",
            ("D", "Z"): "Zuschlagstoffe einragend; andere Ursache",
            ("E", "A"): "Zuschlagstoffe fehlen; mechanisch",
            ("E", "B"): "Zuschlagstoffe fehlen; chemisch - allgemein",
            ("E", "C"): "Zuschlagstoffe fehlen; chemisch - Beschädigung im oberen Teil des Rohres",
            ("E", "D"): "Zuschlagstoffe fehlen; chemisch - Beschädigung im unteren Teil des Rohres",
            ("E", "E"): "Zuschlagstoffe fehlen; Ursache nicht eindeutig feststellbar",
            ("E", "Z"): "Zuschlagstoffe fehlen; andere Ursache",
            ("F", "A"): "Bewehrung sichtbar; mechanisch",
            ("F", "B"): "Bewehrung sichtbar; chemisch - allgemein",
            ("F", "C"): "Bewehrung sichtbar; chemisch - Beschädigung im oberen Teil des Rohres",
            ("F", "D"): "Bewehrung sichtbar; chemisch - Beschädigung im unteren Teil des Rohres",
            ("F", "E"): "Bewehrung sichtbar; Ursache nicht eindeutig feststellbar",
            ("F", "Z"): "Bewehrung sichtbar; andere Ursache",
            ("G", "A"): "Bewehrung einragend; mechanisch",
            ("G", "B"): "Bewehrung einragend; chemisch - allgemein",
            ("G", "C"): "Bewehrung einragend; chemisch - Beschädigung im oberen Teil des Rohres",
            ("G", "D"): "Bewehrung einragend; chemisch - Beschädigung im unteren Teil des Rohres",
            ("G", "E"): "Bewehrung einragend; Ursache nicht eindeutig feststellbar",
            ("G", "Z"): "Bewehrung einragend; andere Ursache",
            ("H", "B"): "Bewehrung korrodiert; chemisch - allgemein",
            ("H", "C"): "Bewehrung korrodiert; chemisch - Beschädigung im oberen Teil des Rohres",
            ("H", "D"): "Bewehrung korrodiert; chemisch - Beschädigung im unteren Teil des Rohres",
            ("H", "E"): "Bewehrung korrodiert; Ursache nicht eindeutig feststellbar",
            ("I", "A"): "fehlende Wand; mechanisch",
            ("I", "B"): "fehlende Wand; chemisch - allgemein",
            ("I", "C"): "fehlende Wand; chemisch - Beschädigung im oberen Teil des Rohres",
            ("I", "D"): "fehlende Wand; chemisch - Beschädigung im unteren Teil des Rohres",
            ("I", "E"): "fehlende Wand; Ursache nicht eindeutig feststellbar",
            ("J", "B"): "Korrosionserscheinungen an der Oberfläche; chemisch - allgemein",
            ("J", "C"): "Korrosionserscheinungen an der Oberfläche; chemisch - Beschädigung im oberen Teil des Rohres",
            ("J", "D"): "Korrosionserscheinungen an der Oberfläche; chemisch - Beschädigung im unteren Teil des Rohres",
            ("J", "E"): "Korrosionserscheinungen an der Oberfläche; Ursache nicht eindeutig feststellbar",
            ("J", "Z"): "Korrosionserscheinungen an der Oberfläche; andere Ursache",
            ("K", "A"): "Blasen (Beulen); mechanisch",
            ("K", "B"): "Blasen (Beulen); chemisch - allgemein",
            ("K", "C"): "Blasen (Beulen); chemisch - Beschädigung im oberen Teil des Rohres",
            ("K", "D"): "Blasen (Beulen); chemisch - Beschädigung im unteren Teil des Rohres",
            ("K", "E"): "Blasen (Beulen); Ursache nicht eindeutig feststellbar",
            ("Z", "A"): "andere Oberflächenschäden; mechanisch",
            ("Z", "B"): "andere Oberflächenschäden; chemisch - allgemein",
            ("Z", "C"): "andere Oberflächenschäden; chemisch - Beschädigung im oberen Teil des Rohres",
            ("Z", "D"): "andere Oberflächenschäden; chemisch - Beschädigung im unteren Teil des Rohres",
            ("Z", "E"): "andere Oberflächenschäden; Ursache nicht eindeutig feststellbar",
            ("Z", "Z"): "andere Oberflächenschäden; andere Ursache",
        },

        # BAG - Einragender Anschluss (Tab. A-2-32)
        "BAG": {
            ("", ""): "Einragender Anschluss",
        },

        # BAH - Schadhafter Anschluss (Tab. A-2-33)
        "BAH": {
            ("", ""): "Schadhafter Anschluss",
            ("A", ""): "Lage des Anschlusses um das Rohr ist falsch",
            ("B", ""): "Spalt zwischen dem Ende des Anschlusses und der Rohrleitung",
            ("C", ""): "am Umfang des Anschlusses ist teilweise ein Spalt",
            ("D", ""): "Anschluss beschädigt",
            ("E", ""): "Anschluss verstopft",
            ("Z", ""): "andere",
        },

        # BAI - Einragendes Dichtungsmaterial (Tab. A-2-34)
        "BAI": {
            ("", ""): "Einragendes Dichtungsmaterial",
            ("A", "A"): "Dichtring; sichtbar verschoben, jedoch nicht in die Rohrleitung hineinragend",
            ("A", "B"): "Dichtring; einragend, aber nicht gebrochen - tiefster Punkt oberhalb horizontaler Mittellinie",
            ("A", "C"): "Dichtring; einragend, aber nicht gebrochen - tiefster Punkt unterhalb horizontaler Mittellinie",
            ("A", "D"): "Dichtring; einragend und gebrochen",
            ("Z", ""): "andere Dichtungsart",
        },

        # BAJ - Verschobene Verbindung (Tab. A-2-35)
        "BAJ": {
            ("", ""): "Verschobene Verbindung",
            ("A", ""): "in Längsrichtung - die Rohre sind parallel zur Rohrleitungsachse verschoben",
            ("B", ""): "radial - die Rohre sind rechtwinklig zur Rohrleitungsachse verschoben",
            ("C", ""): "im Winkel - die Rohrachsen sind nicht parallel zur Rohrleitungsachse",
        },

        # BAK - Feststellung der Innenauskleidung (Tab. A-2-36)
        "BAK": {
            ("", ""): "Feststellung der Innenauskleidung",
            ("A", ""): "Innenauskleidung abgelöst",
            ("B", ""): "Innenauskleidung verfärbt",
            ("C", ""): "Endstelle der Auskleidung schadhaft",
            ("D", "A"): "Falten in der Auskleidung; in Längsrichtung",
            ("D", "B"): "Falten in der Auskleidung; radial am Umfang",
            ("D", "C"): "Falten in der Auskleidung; komplex",
            ("D", "D"): "Falten in der Auskleidung; spiralförmig",
            ("E", ""): "Blasen oder Beulen in der Auskleidung nach innen",
            ("F", ""): "Beulen außen",
            ("G", ""): "Ablösen der Innenhaut/Beschichtung",
            ("H", ""): "Ablösen der Abdeckung der Verbindungsnaht",
            ("I", ""): "Riss oder Spalt (einschließlich schadhafter Schweißnaht)",
            ("J", ""): "Loch in der Auskleidung",
            ("K", ""): "Auskleidungsverbindung defekt",
            ("L", ""): "Auskleidungswerkstoff erscheint weich",
            ("M", ""): "Harz fehlt im Laminat",
            ("N", ""): "Ende der Auskleidung ist nicht abgedichtet",
            ("Z", ""): "Anderer Auskleidungsschaden",
        },

        # BAL - Schadhafte Reparatur (Tab. A-2-38)
        "BAL": {
            ("", ""): "Schadhafte Reparatur",
            ("A", "A"): "Wand fehlt teilweise; in Längsrichtung",
            ("A", "B"): "Wand fehlt teilweise; radial am Umfang",
            ("A", "C"): "Wand fehlt teilweise; komplex",
            ("A", "D"): "Wand fehlt teilweise; spiralförmig",
            ("B", "A"): "Reparatur zur Abdichtung eines Lochs ist schadhaft; in Längsrichtung",
            ("B", "B"): "Reparatur zur Abdichtung eines Lochs ist schadhaft; radial am Umfang",
            ("B", "C"): "Reparatur zur Abdichtung eines Lochs ist schadhaft; komplex",
            ("B", "D"): "Reparatur zur Abdichtung eines Lochs ist schadhaft; spiralförmig",
            ("C", "C"): "Ablösen des Reparaturwerkstoffs vom Basisrohr; komplex",
            ("D", "A"): "Fehlender Reparaturwerkstoff an der Kontaktfläche; in Längsrichtung",
            ("D", "B"): "Fehlender Reparaturwerkstoff an der Kontaktfläche; radial am Umfang",
            ("D", "C"): "Fehlender Reparaturwerkstoff an der Kontaktfläche; komplex",
            ("D", "D"): "Fehlender Reparaturwerkstoff an der Kontaktfläche; spiralförmig",
            ("E", ""): "Überschüssiger Reparaturwerkstoff, der ein Hindernis darstellt",
            ("F", "A"): "Loch im Reparaturwerkstoff; in Längsrichtung",
            ("F", "B"): "Loch im Reparaturwerkstoff; radial am Umfang",
            ("F", "C"): "Loch im Reparaturwerkstoff; komplex",
            ("F", "D"): "Loch im Reparaturwerkstoff; spiralförmig",
            ("G", ""): "Riss im Reparaturwerkstoff",
            ("Z", ""): "Andere",
        },

        # BAM - Schadhafte Schweißnaht (Tab. A-2-40)
        "BAM": {
            ("", ""): "Schadhafte Schweißnaht",
            ("A", ""): "in Längsrichtung - Schaden parallel zur Rohrachse",
            ("B", ""): "am Umfang - Schaden am Umfang",
            ("C", ""): "spiralförmiger Verlauf",
        },

        # BAN - Poröses Rohr (Tab. A-2-41)
        "BAN": {
            ("", ""): "Poröses Rohr",
        },

        # BAO - Boden sichtbar (Tab. A-2-42)
        "BAO": {
            ("", ""): "Boden sichtbar",
        },

        # BAP - Hohlraum sichtbar (Tab. A-2-43)
        "BAP": {
            ("", ""): "Hohlraum sichtbar",
        },

        # BBA - Wurzeln (Tab. A-2-44)
        "BBA": {
            ("", ""): "Wurzeln",
            ("A", ""): "Pfahlwurzeln",
            ("B", ""): "einzelne feine Wurzeln",
            ("C", ""): "komplexes Wurzelwerk",
        },

        # BBB - Anhaftende Stoffe (Tab. A-2-45)
        "BBB": {
            ("", ""): "Anhaftende Stoffe",
            ("A", ""): "Inkrustation",
            ("B", ""): "Fett",
            ("C", ""): "Fäulnis",
            ("Z", ""): "andere",
        },

        # BBC - Ablagerungen (Tab. A-2-46)
        "BBC": {
            ("", ""): "Ablagerungen",
            ("A", ""): "feines Material (z. B. Sand, Schluff)",
            ("B", ""): "grobes Material (z. B. Kies, Schutt)",
            ("C", ""): "hartes oder verdichtetes Material (z. B. Beton)",
            ("Z", ""): "andere",
        },

        # BBD - Eindringen von Bodenmaterial (Tab. A-2-47)
        "BBD": {
            ("", ""): "Eindringen von Bodenmaterial",
            ("A", ""): "Sand",
            ("B", ""): "Torf",
            ("C", ""): "Feinmaterial (z. B. Ton/Schluff)",
            ("D", ""): "Grobmaterial",
            ("Z", ""): "andere",
        },

        # BBE - Andere Hindernisse (Tab. A-2-48)
        "BBE": {
            ("", ""): "Andere Hindernisse",
            ("A", ""): "Ziegel oder Mauerwerk liegen in der Rohrsohle",
            ("B", ""): "Bruchstücke einer Abwasserleitung liegen in der Rohrsohle",
            ("C", ""): "anderer Gegenstand liegt in der Rohrsohle",
            ("D", ""): "Gegenstand ragt durch die Wand ein",
            ("E", ""): "Gegenstand in Rohrverbindung eingekeilt",
            ("F", ""): "Gegenstand dringt durch einen Anschluss/Abzweig ein",
            ("G", ""): "fremde Leitungen oder Kabel durchqueren die Rohrleitung",
            ("H", ""): "Gegenstand/Objekt in den Rohrkörper eingebaut",
            ("Z", ""): "andere",
        },

        # BBF - Infiltration (Tab. A-2-49)
        "BBF": {
            ("", ""): "Infiltration",
            ("A", ""): "Schwitzen - langsames Eindringen von Wasser - keine sichtbaren Tropfen",
            ("B", ""): "Tropfen - Eintropfen - kein kontinuierliches Fließen",
            ("C", ""): "Fließen - kontinuierliches Fließen",
            ("D", ""): "Spritzen - Eindringen unter Druck",
        },

        # BBG - Exfiltration (Tab. A-2-50)
        "BBG": {
            ("", ""): "Exfiltration",
        },

        # BBH - Ungeziefer (Tab. A-2-51)
        "BBH": {
            ("", ""): "Ungeziefer",
            ("A", "A"): "Ratte; in der Rohrleitung",
            ("A", "B"): "Ratte; in einem Anschluss",
            ("A", "C"): "Ratte; in einer offenen Rohrverbindung",
            ("A", "Z"): "Ratte; andere",
            ("B", "A"): "Küchenschabe/Kakerlake; in der Rohrleitung",
            ("B", "B"): "Küchenschabe/Kakerlake; in einem Anschluss",
            ("B", "C"): "Küchenschabe/Kakerlake; in einer offenen Rohrverbindung",
            ("B", "Z"): "Küchenschabe/Kakerlake; andere",
            ("Z", "A"): "andere; in der Rohrleitung",
            ("Z", "B"): "andere; in einem Anschluss",
            ("Z", "C"): "andere; in einer offenen Rohrverbindung",
            ("Z", "Z"): "andere; andere",
        },

        # BCA - Anschluss (Tab. A-2-10)
        "BCA": {
            ("", ""): "Anschluss",
            ("A", "A"): "Abzweig; Anschluss offen",
            ("A", "B"): "Abzweig; Anschluss geschlossen",
            ("B", "A"): "Sattelanschluss - gebohrt; Anschluss offen",
            ("B", "B"): "Sattelanschluss - gebohrt; Anschluss geschlossen",
            ("C", "A"): "Sattelanschluss - gemeißelt; Anschluss offen",
            ("C", "B"): "Sattelanschluss - gemeißelt; Anschluss geschlossen",
            ("D", "A"): "einfacher Anschluss - gebohrt; Anschluss offen",
            ("D", "B"): "einfacher Anschluss - gebohrt; Anschluss geschlossen",
            ("E", "A"): "einfacher Anschluss - gemeißelt; Anschluss offen",
            ("E", "B"): "einfacher Anschluss - gemeißelt; Anschluss geschlossen",
            ("F", "A"): "anderer Anschluss; Anschluss offen",
            ("F", "B"): "anderer Anschluss; Anschluss geschlossen",
            ("G", "A"): "unbekannter Anschluss; Anschluss offen",
            ("G", "B"): "unbekannter Anschluss; Anschluss geschlossen",
            ("Z", "A"): "andere; Anschluss offen",
            ("Z", "B"): "andere; Anschluss geschlossen",
        },

        # BCB - Punktuelle Reparatur (Tab. A-2-11)
        "BCB": {
            ("", ""): "Punktuelle Reparatur",
            ("A", ""): "Reparatur mit Injektionstechnik",
            ("B", ""): "Reparatur mit Roboter",
            ("C", ""): "Reparatur mit partieller Auskleidungs-/Manchettentechnik",
            ("D", ""): "Zulaufeinbindung",
            ("E", ""): "Reparatur Rohrwand manuell",
            ("F", ""): "Reparatur Rohrverbindung manuell",
            ("G", ""): "Ringspalt-/-raumdichtung (der Auskleidung) zum Anschluss an Schacht/Inspektionsöffnung",
            ("H", ""): "Zulauföffnung ohne Einbindung (Auskleidung)",
            ("I", ""): "Rohr ausgetauscht",
            ("Z", ""): "sonstige Technik",
        },

        # BCC - Krümmung der Leitung (Tab. A-2-12)
        "BCC": {
            ("", ""): "Krümmung der Leitung",
            ("A", "A"): "nach links; nach oben",
            ("A", "B"): "nach links; nach unten",
            ("B", "A"): "nach rechts; nach oben",
            ("B", "B"): "nach rechts; nach unten",
        },

        # BCD - Anfangsknoten (Tab. A-2-13)
        "BCD": {
            ("XP", ""): "Rohranfang",
        },

        # BCE - Endknoten (Tab. A-2-14)
        "BCE": {
            ("XP", ""): "Rohrende",
        },

        # BDA - Allgemeines Foto (Tab. A-2-15)
        "BDA": {
            ("", ""): "Allgemeines Foto",
        },

        # BDB - Allgemeine Anmerkung (Tab. A-2-16, A-2-17)
        "BDB": {
            ("", ""): "Allgemeine Anmerkung",
            ("AA", ""): "Verbindung zweier Rohre ohne Formstück, eingesteckt, gerade",
            ("AB", ""): "Verbindung zweier Rohre ohne Formstück, übergestülpt, gerade",
            ("AC", ""): "Verbindung zweier Rohre ohne Formstück, eingesteckt, abgewinkelt",
            ("AD", ""): "Verbindung zweier Rohre ohne Formstück, übergestülpt, abgewinkelt",
            ("AE", ""): "Verbindung zweier Rohre ohne Formstück, stumpf aneinandergestoßen",
            ("BA", ""): "Verschluss eines Rohrs durch Abmauerung",
            ("BB", ""): "Verschluss eines Rohrs durch Mörtel",
            ("BC", ""): "Verschluss eines Rohrs durch Deckel (Muffenstopfen)",
        },

        # BDC - Inspektion endet vor dem Endknoten (Tab. A-2-18)
        "BDC": {
            ("", ""): "Inspektion endet vor dem Endknoten",
            ("Y", "A"): "Abbruch der Inspektion; Inspektionsziel erreicht",
            ("Y", "B"): "Abbruch der Inspektion; Auftraggeber verzichtet auf weitere Inspektion",
            ("Y", "C"): "Abbruch der Inspektion; Gegenseite erreicht",
            ("Y", "D"): "Abbruch der Inspektion; Gegenseite nicht erreicht",
            ("Y", "E"): "Abbruch der Inspektion; Unklar, ob Gegenseite erreicht",
            ("Y", "Z"): "Abbruch der Inspektion; andere",
        },

        # BDD - Wasserspiegel (Tab. A-2-19)
        "BDD": {
            ("", ""): "Wasserspiegel",
            ("A", ""): "klar (Sohle sichtbar)",
            ("B", ""): "Anwendung des Kodes nicht fortgeführt",
            ("C", ""): "trüb",
            ("D", ""): "gefärbt",
            ("E", ""): "trüb und gefärbt",
        },

        # BDE - Zufluss aus einem Anschluss (Tab. A-2-52)
        "BDE": {
            ("", ""): "Zufluss aus einem Anschluss",
            ("A", "A"): "klar; falsch angeschlossen, Schmutzwasser in Regenwasserleitung",
            ("A", "B"): "klar; falsch angeschlossen, Regenwasser in Schmutzwasserleitung",
            ("A", "C"): "klar; kein Fehlanschluss erkennbar",
            ("B", "A"): "Anwendung nicht fortgeführt; falsch angeschlossen, Schmutzwasser in Regenwasserleitung",
            ("B", "B"): "Anwendung nicht fortgeführt; falsch angeschlossen, Regenwasser in Schmutzwasserleitung",
            ("B", "C"): "Anwendung nicht fortgeführt; kein Fehlanschluss erkennbar",
            ("C", "A"): "trüb; falsch angeschlossen, Schmutzwasser in Regenwasserleitung",
            ("C", "B"): "trüb; falsch angeschlossen, Regenwasser in Schmutzwasserleitung",
            ("C", "C"): "trüb; kein Fehlanschluss erkennbar",
            ("D", "A"): "gefärbt; falsch angeschlossen, Schmutzwasser in Regenwasserleitung",
            ("D", "B"): "gefärbt; falsch angeschlossen, Regenwasser in Schmutzwasserleitung",
            ("D", "C"): "gefärbt; kein Fehlanschluss erkennbar",
            ("E", "A"): "trüb und gefärbt; falsch angeschlossen, Schmutzwasser in Regenwasserleitung",
            ("E", "B"): "trüb und gefärbt; falsch angeschlossen, Regenwasser in Schmutzwasserleitung",
            ("E", "C"): "trüb und gefärbt; kein Fehlanschluss erkennbar",
        },

        # BDF - Atmosphäre in der Leitung (Tab. A-2-20)
        "BDF": {
            ("", ""): "Atmosphäre in der Leitung",
            ("A", ""): "Sauerstoffmangel",
            ("B", ""): "Schwefelwasserstoff",
            ("C", ""): "Methan",
            ("Z", ""): "andere",
        },

        # BDG - Keine Sicht (Tab. A-2-21)
        "BDG": {
            ("", ""): "Keine Sicht",
            ("A", ""): "Kamera unter Wasser",
            ("B", ""): "Verschlammung",
            ("C", ""): "Dämpfe",
            ("Z", ""): "andere",
        },
    },

    "Schächte": {
        # CAA/DAA - Verformung (Tab. A-2-65)
        "DAA": {
            ("", ""): "Verformung",
            ("A", ""): "Allgemein - betrifft einen großen Teil der Wand",
            ("B", ""): "Punktuell - betrifft einen relativ kleinen Teil der Wand",
        },

        # CAB/DAB - Rissbildung (Tab. A-2-66)
        "DAB": {
            ("", ""): "Rissbildung",
            ("A", "A"): "Oberflächenriss (Haarriss); vertikal",
            ("A", "B"): "Oberflächenriss (Haarriss); horizontal",
            ("A", "C"): "Oberflächenriss (Haarriss); komplex",
            ("A", "D"): "Oberflächenriss (Haarriss); geneigt",
            ("A", "E"): "Oberflächenriss (Haarriss); von einem Punkt ausgehende Ausbreitung",
            ("B", "A"): "Riss - Risslinien erkennbar, Segmente am Platz; vertikal",
            ("B", "B"): "Riss - Risslinien erkennbar, Segmente am Platz; horizontal",
            ("B", "C"): "Riss - Risslinien erkennbar, Segmente am Platz; komplex",
            ("B", "D"): "Riss - Risslinien erkennbar, Segmente am Platz; geneigt",
            ("B", "E"): "Riss - Risslinien erkennbar, Segmente am Platz; von einem Punkt ausgehende Ausbreitung",
            ("C", "A"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; vertikal",
            ("C", "B"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; horizontal",
            ("C", "C"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; komplex",
            ("C", "D"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; geneigt",
            ("C", "E"): "Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; von einem Punkt ausgehende Ausbreitung",
        },

        # CAC/DAC - Bruch/Einsturz (Tab. A-2-67)
        "DAC": {
            ("", ""): "Bruch/Einsturz",
            ("A", ""): "Bruch - Wandsegmente sichtbar verschoben, aber nicht fehlend",
            ("B", ""): "Fehlen von Teilen - Wandsegmente fehlen",
            ("C", ""): "Einsturz - Konstruktionsgefüge vollständig zerstört",
        },

        # CAD/DAD - Defektes Mauerwerk (Tab. A-2-68)
        "DAD": {
            ("", ""): "Defektes Mauerwerk",
            ("A", "A"): "verschoben - Mauersteine/Ziegel aus ursprünglicher Lage verschoben; weitere Mauerwerksschicht sichtbar",
            ("A", "B"): "verschoben - Mauersteine/Ziegel aus ursprünglicher Lage verschoben; es ist nichts zu sehen",
            ("B", "A"): "fehlend - Mauersteine/Ziegel fehlen; weitere Mauerwerksschicht sichtbar",
            ("B", "B"): "fehlend - Mauersteine/Ziegel fehlen; es ist nichts zu sehen",
            ("C", "A"): "Einsturz - Konstruktionsgefüge vollständig zerstört; weitere Mauerwerksschicht sichtbar",
            ("C", "B"): "Einsturz - Konstruktionsgefüge vollständig zerstört; es ist nichts zu sehen",
        },

        # CAE/DAE - Fehlender Mörtel (Tab. A-2-69)
        "DAE": {
            ("", ""): "Fehlender Mörtel",
        },

        # CAF/DAF - Oberflächenschaden (Tab. A-2-70)
        "DAF": {
            ("", ""): "Oberflächenschaden",
            ("A", "A"): "erhöhte Rauheit; mechanisch",
            ("A", "B"): "erhöhte Rauheit; chemisch - allgemein",
            ("A", "C"): "erhöhte Rauheit; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("A", "D"): "erhöhte Rauheit; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("A", "E"): "erhöhte Rauheit; Schadensursache nicht feststellbar",
            ("A", "Z"): "erhöhte Rauheit; andere Ursache",
            ("B", "A"): "Abplatzung; mechanisch",
            ("B", "E"): "Abplatzung; Schadensursache nicht feststellbar",
            ("B", "Z"): "Abplatzung; andere Ursache",
            ("C", "A"): "Zuschlagstoffe sichtbar; mechanisch",
            ("C", "B"): "Zuschlagstoffe sichtbar; chemisch - allgemein",
            ("C", "C"): "Zuschlagstoffe sichtbar; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("C", "D"): "Zuschlagstoffe sichtbar; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("C", "E"): "Zuschlagstoffe sichtbar; Schadensursache nicht feststellbar",
            ("C", "Z"): "Zuschlagstoffe sichtbar; andere Ursache",
            ("D", "A"): "Zuschlagstoffe einragend; mechanisch",
            ("D", "B"): "Zuschlagstoffe einragend; chemisch - allgemein",
            ("D", "C"): "Zuschlagstoffe einragend; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("D", "D"): "Zuschlagstoffe einragend; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("D", "E"): "Zuschlagstoffe einragend; Schadensursache nicht feststellbar",
            ("D", "Z"): "Zuschlagstoffe einragend; andere Ursache",
            ("E", "A"): "Zuschlagstoffe fehlen; mechanisch",
            ("E", "B"): "Zuschlagstoffe fehlen; chemisch - allgemein",
            ("E", "C"): "Zuschlagstoffe fehlen; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("E", "D"): "Zuschlagstoffe fehlen; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("E", "E"): "Zuschlagstoffe fehlen; Schadensursache nicht feststellbar",
            ("E", "Z"): "Zuschlagstoffe fehlen; andere Ursache",
            ("F", "A"): "Bewehrung sichtbar; mechanisch",
            ("F", "B"): "Bewehrung sichtbar; chemisch - allgemein",
            ("F", "C"): "Bewehrung sichtbar; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("F", "D"): "Bewehrung sichtbar; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("F", "E"): "Bewehrung sichtbar; Schadensursache nicht feststellbar",
            ("F", "Z"): "Bewehrung sichtbar; andere Ursache",
            ("G", "A"): "Bewehrung einragend; mechanisch",
            ("G", "B"): "Bewehrung einragend; chemisch - allgemein",
            ("G", "C"): "Bewehrung einragend; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("G", "D"): "Bewehrung einragend; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("G", "E"): "Bewehrung einragend; Schadensursache nicht feststellbar",
            ("G", "Z"): "Bewehrung einragend; andere Ursache",
            ("H", "B"): "Bewehrung korrodiert; chemisch - allgemein",
            ("H", "C"): "Bewehrung korrodiert; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("H", "D"): "Bewehrung korrodiert; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("H", "E"): "Bewehrung korrodiert; Schadensursache nicht feststellbar",
            ("I", "A"): "fehlende Wand; mechanisch",
            ("I", "B"): "fehlende Wand; chemisch - allgemein",
            ("I", "C"): "fehlende Wand; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("I", "D"): "fehlende Wand; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("I", "E"): "fehlende Wand; Schadensursache nicht feststellbar",
            ("J", "B"): "Korrosionserscheinungen an der Oberfläche; chemisch - allgemein",
            ("J", "C"): "Korrosionserscheinungen an der Oberfläche; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("J", "D"): "Korrosionserscheinungen an der Oberfläche; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("J", "E"): "Korrosionserscheinungen an der Oberfläche; Schadensursache nicht feststellbar",
            ("J", "Z"): "Korrosionserscheinungen an der Oberfläche; andere Ursache",
            ("K", "A"): "Blasenbildung (Beulen); mechanisch",
            ("K", "B"): "Blasenbildung (Beulen); chemisch - allgemein",
            ("K", "C"): "Blasenbildung (Beulen); chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("K", "D"): "Blasenbildung (Beulen); chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("K", "E"): "Blasenbildung (Beulen); Schadensursache nicht feststellbar",
            ("Z", "A"): "anderer Oberflächenschaden; mechanisch",
            ("Z", "B"): "anderer Oberflächenschaden; chemisch - allgemein",
            ("Z", "C"): "anderer Oberflächenschaden; chemisch - Beschädigung im oberen Teil des Gerinnes oder weiter oben",
            ("Z", "D"): "anderer Oberflächenschaden; chemisch - Beschädigung im unteren Teil des Gerinnes",
            ("Z", "E"): "anderer Oberflächenschaden; Schadensursache nicht feststellbar",
            ("Z", "Z"): "anderer Oberflächenschaden; andere Ursache",
        },

        # CAG/DAG - Einragender Anschluss (Tab. A-2-71)
        "DAG": {
            ("", ""): "Einragender Anschluss",
        },

        # CAH/DAH - Schadhafter Anschluss (Tab. A-2-72)
        "DAH": {
            ("", ""): "Schadhafter Anschluss",
            ("A", ""): "Lage des Anschlusses ist falsch",
            ("B", ""): "Spalt zwischen dem Ende des Anschlusses und der Schachtwand",
            ("C", ""): "am Umfang des Anschlusses ist teilweise ein Spalt",
            ("D", ""): "Anschluss beschädigt",
            ("E", ""): "Anschluss verstopft",
            ("Z", ""): "andere",
        },
        # DAI - Einragendes Dichtungsmaterial (Tab. A-2-73)
        "DAI": {
            ("", ""): "Einragendes Dichtungsmaterial",
            ("A", "A"): "Dichtring; sichtbar verschoben, jedoch nicht in den Schacht hineinragend",
            ("A", "B"): "Dichtring; einragend, aber nicht gebrochen",
            ("A", "C"): "Dichtring; gebrochen",
            ("A", "Z"): "Dichtring; andere",
            ("Z", ""): "andere einragende Dichtungsmaterialien",
        },

        # DAJ - Verschobene Verbindung (Tab. A-2-74)
        "DAJ": {
            ("", ""): "Verschobene Verbindung",
            ("A", ""): "vertikal – die Elemente sind vertikal verschoben",
            ("B", ""): "horizontal – die Elemente sind horizontal verschoben",
            ("C", ""): "im Winkel – die Achsen der Elemente sind nicht parallel",
        },

        # DAK - Feststellung der Innenauskleidung (Tab. A-2-75)
        "DAK": {
            ("", ""): "Feststellung der Innenauskleidung",
            ("A", ""): "Innenauskleidung abgelöst",
            ("B", ""): "Innenauskleidung verfärbt",
            ("C", ""): "Endstelle der Auskleidung schadhaft",
            ("D", "A"): "Falten in der Innenauskleidung; vertikal",
            ("D", "B"): "Falten in der Innenauskleidung; horizontal",
            ("D", "C"): "Falten in der Innenauskleidung; komplex",
            ("D", "D"): "Falten in der Innenauskleidung; spiralförmig",
            ("E", ""): "Blasen oder Beulen in der Auskleidung nach innen",
            ("F", ""): "Beulen außen",
            ("G", ""): "Ablösen der Innenhaut/Beschichtung",
            ("H", ""): "Ablösen der Abdeckung der Verbindungsnaht",
            ("I", ""): "Riss oder Spalt (einschließlich schadhafter Schweißnaht)",
            ("J", ""): "Loch in der Auskleidung",
            ("K", ""): "Auskleidungsverbindung defekt",
            ("L", ""): "Auskleidungswerkstoff erscheint weich",
            ("M", ""): "Harz fehlt im Laminat",
            ("N", ""): "Ende der Auskleidung ist nicht abgedichtet",
            ("Z", ""): "anderer Auskleidungsschaden",
        },
        # DAL - Schadhafte Reparatur (Tab. A-2-77)
        "DAL": {
            ("", ""): "Schadhafte Reparatur",
            ("A", ""): "Wand fehlt teilweise",
            ("B", ""): "Reparatur zur Abdichtung eines Lochs ist schadhaft",
            ("C", ""): "Ablösen des Reparaturwerkstoffs vom Basisrohr",
            ("D", ""): "Fehlender Reparaturwerkstoff an der Kontaktfläche",
            ("E", ""): "Überschüssiger Reparaturwerkstoff, der ein Hindernis darstellt",
            ("F", ""): "Loch im Reparaturwerkstoff",
            ("G", ""): "Riss im Reparaturwerkstoff",
            ("Z", ""): "andere schadhafte Reparatur",
        },
        # DAM - Schadhafte Schweißnaht (Tab. A-2-79)
        "DAM": {
            ("A", ""): "Schadhafte Schweißnaht vertikal",
            ("B", ""): "Schadhafte Schweißnaht horizontal",
            ("C", ""): "Schadhafte Schweißnaht geneigt",
        },

        # CAN/DAN - Poröse Wand (Tab. A-2-80)
        "DAN": {
            ("", ""): "Poröse Wand",
        },

        # CAO/DAO - Boden sichtbar (Tab. A-2-81)
        "DAO": {
            ("", ""): "Boden sichtbar",
        },

        # CAP/DAP - Hohlraum sichtbar (Tab. A-2-82)
        "DAP": {
            ("", ""): "Hohlraum sichtbar",
        },

        # CAQ/DAQ - Schadhafte Steighilfen (Tab. A-2-83)
        "DAQ": {
            ("", ""): "Schadhafte Steighilfen",
            ("A", ""): "lockeres Steigeisen",
            ("B", ""): "fehlendes Steigeisen",
            ("C", ""): "korrodiertes Steigeisen",
            ("D", ""): "verbogenes Steigeisen",
            ("E", ""): "Kunststoffverkleidung des Steigeisens gebrochen",
            ("F", ""): "Handlauf der Steigleiter korrodiert",
            ("G", ""): "lockere Absturzsicherung der Leiter",
            ("H", ""): "fehlende Absturzsicherung der Leiter",
            ("I", ""): "korrodierte Absturzsicherung der Leiter",
            ("J", ""): "korrodierte Leitersprossen",
            ("K", ""): "schadhafter Steigkasten",
            ("Z", ""): "andere",
        },

        # CAR/DAR - Schäden an Abdeckung und Rahmen (Tab. A-2-84)
        "DAR": {
            ("", ""): "Schäden an Abdeckung und Rahmen",
            ("A", ""): "Abdeckung gebrochen",
            ("B", ""): "Abdeckung wackelt",
            ("C", ""): "Abdeckung nicht vorhanden",
            ("D", ""): "Rahmen gebrochen",
            ("E", ""): "Rahmen locker",
            ("F", ""): "Rahmen fehlt",
            ("G", ""): "Abdeckung unterhalb der Geländeoberfläche",
            ("H", ""): "Abdeckung oberhalb der Geländeoberfläche",
            ("Z", ""): "andere",
        },

        # CBA/DBA - Wurzeln (Tab. A-2-85)
        "DBA": {
            ("", ""): "Wurzeln",
            ("A", ""): "Pfahlwurzeln",
            ("B", ""): "einzelne feine Wurzeln",
            ("C", ""): "komplexes Wurzelwerk",
        },

        # CBB/DBB - Anhaftende Stoffe (Tab. A-2-86)
        "DBB": {
            ("", ""): "Anhaftende Stoffe",
            ("A", ""): "Inkrustation",
            ("B", ""): "Fett",
            ("C", ""): "Fäulnis",
            ("Z", ""): "andere",
        },

        # CBC/DBC - Ablagerungen (Tab. A-2-87)
        "DBC": {
            ("", ""): "Ablagerungen",
            ("A", ""): "feines Material (z. B. Sand, Schluff)",
            ("B", ""): "grobes Material (z. B. Kies, Schutt)",
        },
        # DBD - Eindringen von Bodenmaterial (Tab. A-2-88)
        "DBD": {
            ("", ""): "Eindringen von Bodenmaterial",
        },
        # DBE - Andere Hindernisse (Tab. A-2-89)
        "DBE": {
            ("A", ""): "Ziegel oder Mauerwerk",
            ("B", ""): "Rohrteile der Abwasserleitung oder des Abwasserkanals",
            ("C", ""): "anderer Gegenstand",
            ("D", ""): "Gegenstand ragt durch die Wand ein",
            ("E", ""): "Gegenstand in Verbindung eingekeilt",
            ("F", ""): "Gegenstand dringt durch einen Anschluss/Abzweig ein",
            ("G", ""): "fremde Leitungen oder Kabel durchqueren das Bauwerk",
            ("H", ""): "Gegenstand/Objekt in das Bauwerk eingebaut",
            ("Z", ""): "andere - wenn dies verwendet wird, müssen weitere Angaben als Anmerkungen aufgezeichnet werden",
        },
        # DBF - Infiltration (Tab. A-2-90)
        "DBF": {
            ("", ""): "Infiltration",
            ("A", "A"): "Schwitzen – langsames Eindringen von Wasser – keine sichtbaren Tropfen; durch die Wand des Schachtes oder der Inspektionsöffnung",
            ("A", "B"): "Schwitzen – langsames Eindringen von Wasser – keine sichtbaren Tropfen; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss im Sohlbereich",
            ("A", "C"): "Schwitzen – langsames Eindringen von Wasser – keine sichtbaren Tropfen; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss oberhalb des Auftritts",

            ("B", "A"): "Tropfen – Eintropfen – kein kontinuierliches Fließen; durch die Wand des Schachtes oder der Inspektionsöffnung",
            ("B", "B"): "Tropfen – Eintropfen – kein kontinuierliches Fließen; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss im Sohlbereich",
            ("B", "C"): "Tropfen – Eintropfen – kein kontinuierliches Fließen; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss oberhalb des Auftritts",

            ("C", "A"): "Fließen – kontinuierliches Fließen; durch die Wand des Schachtes oder der Inspektionsöffnung",
            ("C", "B"): "Fließen – kontinuierliches Fließen; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss im Sohlbereich",
            ("C", "C"): "Fließen – kontinuierliches Fließen; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss oberhalb des Auftritts",

            ("D", "A"): "Spritzen – Eindringen unter Druck; durch die Wand des Schachtes oder der Inspektionsöffnung",
            ("D", "B"): "Spritzen – Eindringen unter Druck; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss im Sohlbereich",
            ("D", "C"): "Spritzen – Eindringen unter Druck; durch einen Spalt der Wand des Schachtes oder der Inspektionsöffnung und einem Anschluss oberhalb des Auftritts",
        },

        # DBG - Exfiltration (Tab. A-2-91)
        "DBG": {
            ("", ""): "Exfiltration",
        },
        # DBH - Ungeziefer (Tab. A-2-92)
        "DBH": {
            ("", ""): "Ungeziefer",

            ("A", "A"): "Ratte; im Schacht oder in der Inspektionsöffnung",
            ("A", "B"): "Ratte; in einem Anschluss",
            ("A", "C"): "Ratte; in einer offenen Verbindung",
            ("A", "Z"): "Ratte; andere Lage",

            ("B", "A"): "Küchenschabe/Kakerlake; im Schacht oder in der Inspektionsöffnung",
            ("B", "B"): "Küchenschabe/Kakerlake; in einem Anschluss",
            ("B", "C"): "Küchenschabe/Kakerlake; in einer offenen Verbindung",
            ("B", "Z"): "Küchenschabe/Kakerlake; andere Lage",

            ("Z", "A"): "andere Ungeziefer; im Schacht oder in der Inspektionsöffnung",
            ("Z", "B"): "andere Ungeziefer; in einem Anschluss",
            ("Z", "C"): "andere Ungeziefer; in einer offenen Verbindung",
            ("Z", "Z"): "andere Ungeziefer; andere Lage",
        },
        # DCA - Anschluss (Tab. A-2-53)
        "DCA": {
            ("", ""): "Anschluss",
            ("A", "A"): "Anschluss im Auftritt; Gerinne im Auftritt",
            ("A", "B"): "Anschluss im Auftritt; Anschluss leitet über den Auftritt ab",
            ("A", "C"): "Anschluss im Auftritt; Absturz mit Schussgerinne",
            ("A", "D"): "Anschluss im Auftritt; Rohr unter dem Auftritt",
            ("A", "Z"): "Anschluss im Auftritt; andere",
            ("B", ""): "freier Zulauf ins Gerinne",
            ("C", ""): "außenliegender Untersturz",
            ("D", ""): "innenliegender Untersturz",
            ("E", ""): "Absturz mit Schussgerinne",
            ("F", ""): "Belüftungsrohr",
            ("Z", ""): "anderer Anschluss",
        },

        # DCB - Punktuelle Reparatur (Tab. A-2-54)
        "DCB": {
            ("", ""): "Punktuelle Reparatur",
            ("Z", ""): "andere",
        },

        # DCG - Anschlussleitung (Tab. A-2-55)
        "DCG": {
            ("", ""): "Anschlussleitung",
            ("A", "A"): "kreisförmig; Anschluss entwässert in den Schacht",
            ("A", "B"): "kreisförmig; Anschluss entwässert aus dem Schacht",
            ("A", "C"): "kreisförmig; Anschluss verschlossen",
            ("B", "A"): "rechteckig; Anschluss entwässert in den Schacht",
            ("B", "B"): "rechteckig; Anschluss entwässert aus dem Schacht",
            ("B", "C"): "rechteckig; Anschluss verschlossen",
            ("C", "A"): "eiförmig; Anschluss entwässert in den Schacht",
            ("C", "B"): "eiförmig; Anschluss entwässert aus dem Schacht",
            ("C", "C"): "eiförmig; Anschluss verschlossen",
            ("D", "A"): "U-förmig; Anschluss entwässert in den Schacht",
            ("D", "B"): "U-förmig; Anschluss entwässert aus dem Schacht",
            ("D", "C"): "U-förmig; Anschluss verschlossen",
            ("E", "A"): "bogenförmig; Anschluss entwässert in den Schacht",
            ("E", "B"): "bogenförmig; Anschluss entwässert aus dem Schacht",
            ("E", "C"): "bogenförmig; Anschluss verschlossen",
            ("F", "A"): "oval; Anschluss entwässert in den Schacht",
            ("F", "B"): "oval; Anschluss entwässert aus dem Schacht",
            ("F", "C"): "oval; Anschluss verschlossen",
            ("Z", "A"): "andere; Anschluss entwässert in den Schacht",
            ("Z", "B"): "andere; Anschluss entwässert aus dem Schacht",
            ("Z", "C"): "andere; Anschluss verschlossen",
        },
        # CCH/DCH - Auftritt (Tab. A-2-93)
        "DCH": {
            ("A", ""): "Auftritt schadhaft",
            ("B", ""): "Auftritt nicht schadhaft",
            ("C", ""): "kein Auftritt",
        },
        # DCI - Gerinne (Tab. A-2-94)
        "DCI": {
            ("", ""): "Gerinne",

            ("A", ""): "Gerinne schadhaft",
            ("A", "A"): "Gerinne schadhaft; Gerinne verengt (in Fließrichtung)",
            ("A", "B"): "Gerinne schadhaft; Gerinne erweitert (in Fließrichtung)",
            ("A", "C"): "Gerinne schadhaft; Gerinne besitzt Hochpunkt",
            ("A", "D"): "Gerinne schadhaft; Gerinne besitzt Niedrigpunkt",

            ("B", ""): "Gerinne nicht schadhaft",
            ("B", "A"): "Gerinne nicht schadhaft; Gerinne verengt (in Fließrichtung)",
            ("B", "B"): "Gerinne nicht schadhaft; Gerinne erweitert (in Fließrichtung)",
            ("B", "C"): "Gerinne nicht schadhaft; Gerinne besitzt Hochpunkt",
            ("B", "D"): "Gerinne nicht schadhaft; Gerinne besitzt Niedrigpunkt",

            ("C", ""): "kein Gerinne",
        },
        # DCJ - Sicherheitsketten/-balken (Tab. A-2-95)
        "DCJ": {
            ("", ""): "Sicherheitsketten/-balken",

            ("A", ""): "Sicherheitskette vorhanden ohne Schäden",
            ("B", ""): "Sicherheitskette fehlend (unter der Annahme, dass eine Kette vorhanden war)",
            ("C", ""): "Sicherheitskette schadhaft",
            ("D", ""): "Sicherheitskette mit Ablagerungen belegt",

            ("E", ""): "Sicherheitsbalken vorhanden ohne Schäden",
            ("F", ""): "Sicherheitsbalken fehlend (unter der Annahme, dass ein Balken vorhanden war)",
            ("G", ""): "Sicherheitsbalken schadhaft",
            ("H", ""): "Sicherheitsbalken mit Ablagerungen belegt",
        },
        # DCK - Abflussregulierung (Tab. A-2-56)
        "DCK": {
            ("", ""): "Abflussregulierung",
            ("A", "A"): "Wehr; Durchflussregulierung",
            ("A", "B"): "Wehr; Abschlagsregulierung",
            ("B", "A"): "Heber; Durchflussregulierung",
            ("B", "B"): "Heber; Abschlagsregulierung",
            ("C", "A"): "Öffnungsklappe; Durchflussregulierung",
            ("C", "B"): "Öffnungsklappe; Abschlagsregulierung",
            ("D", "A"): "Wirbeldrossel; Durchflussregulierung",
            ("D", "B"): "Wirbeldrossel; Abschlagsregulierung",
            ("E", "A"): "Absperrschieber; Durchflussregulierung",
            ("E", "B"): "Absperrschieber; Abschlagsregulierung",
            ("F", "A"): "abflussabhängiger Absperrschieber; Durchflussregulierung",
            ("F", "B"): "abflussabhängiger Absperrschieber; Abschlagsregulierung",
            ("G", "A"): "Messgerinne; Durchflussregulierung",
            ("G", "B"): "Messgerinne; Abschlagsregulierung",
            ("H", "A"): "Rückschlagklappe; Durchflussregulierung",
            ("H", "B"): "Rückschlagklappe; Abschlagsregulierung",
            ("I", "A"): "Rechen/Sieb; Durchflussregulierung",
            ("I", "B"): "Rechen/Sieb; Abschlagsregulierung",
            ("Z", "A"): "andere; Durchflussregulierung",
            ("Z", "B"): "andere; Abschlagsregulierung",
        },
        # DCL - Rohrdurchführung durch Schacht bzw. Inspektionsöffnung (Tab. A-2-96)
        "DCL": {
            ("", ""): "Rohrdurchführung durch Schacht bzw. Inspektionsöffnung",

            ("A", "A"): "keine Öffnungsmöglichkeit an der Rohrdurchführung vorhanden; schadhaft",
            ("A", "B"): "keine Öffnungsmöglichkeit an der Rohrdurchführung vorhanden; nicht schadhaft",

            ("B", "A"): "Öffnungsmöglichkeit vorhanden – Abdeckung am Platz; schadhaft",
            ("B", "B"): "Öffnungsmöglichkeit vorhanden – Abdeckung am Platz; nicht schadhaft",

            ("C", "A"): "Öffnungsmöglichkeit vorhanden – Abdeckung fehlt; schadhaft",
            ("C", "B"): "Öffnungsmöglichkeit vorhanden – Abdeckung fehlt; nicht schadhaft",
        },
        # DCM - Schmutzfänger unter der Abdeckung (Tab. A-2-97)
        "DCM": {
            ("", ""): "Schmutzfänger unter der Abdeckung",
            ("A", ""): "Schmutzfänger vorhanden ohne Schäden",
            ("B", ""): "Schmutzfänger fehlend (unter der Maßgabe, dass ein Schmutzfänger vorhanden war)",
            ("C", ""): "Schmutzfänger schadhaft",
        },

        # DCN - Schlammfang in der Sohle (Tab. A-2-98)
        "DCN": {
            ("", ""): "Schlammfang in der Sohle",
            ("A", ""): "Schlammfang nicht schadhaft",
            ("B", ""): "Schlammfang schadhaft",
        },
        # DCO - Querschnitt (Tab. A-2-57)
        "DCO": {
            ("", ""): "Querschnitt",
            ("A", ""): "kreisförmig",
            ("B", ""): "rechteckig",
            ("Z", ""): "andere",
        },

        # DDA - Allgemeines Foto (Tab. A-2-58)
        "DDA": {
            ("", ""): "Allgemeines Foto",
        },

        # DDB - Allgemeine Anmerkung (Tab. A-2-59)
        "DDB": {
            ("", ""): "Allgemeine Anmerkung",
        },

        # DDC - Inspektion nicht vollständig durchgeführt (Tab. A-2-60)
        "DDC": {
            ("", ""): "Inspektion nicht vollständig durchgeführt",
            ("Y", "A"): "Abbruch der Inspektion; Inspektionsziel erreicht",
            ("Y", "B"): "Abbruch der Inspektion; Auftraggeber verzichtet auf weitere Inspektion",
            ("Y", "Z"): "Abbruch der Inspektion; andere",
        },

        # DDD - Wasserspiegel (Tab. A-2-61)
        "DDD": {
            ("", ""): "Wasserspiegel",
        },
        # DDE - Zufluss aus einem Anschluss (Tab. A-2-99)
        "DDE": {
            ("", ""): "Zufluss aus einem Anschluss",

            # Charakterisierung 1: Beschaffenheit des Abwassers
            ("A", ""): "klares Abwasser (Sohle sichtbar)",
            ("B", ""): "Anwendung des Kodes nicht fortgeführt",
            ("C", ""): "trüb",
            ("D", ""): "gefärbt",
            ("E", ""): "trüb und gefärbt",

            # Kombinationen mit Charakterisierung 2: Fehlschluss / kein Fehlschluss
            ("A", "A"): "klares Abwasser; falsch angeschlossen, da Schmutzwasser in Regenwasserleitung/-kanal abfließt",
            ("A", "B"): "klares Abwasser; falsch angeschlossen, da Regenwasser in Schmutzwasserleitung/-kanal abfließt",
            ("A", "C"): "klares Abwasser; kein Fehlschluss erkennbar",

            ("C", "A"): "trüb; falsch angeschlossen, da Schmutzwasser in Regenwasserleitung/-kanal abfließt",
            ("C", "B"): "trüb; falsch angeschlossen, da Regenwasser in Schmutzwasserleitung/-kanal abfließt",
            ("C", "C"): "trüb; kein Fehlschluss erkennbar",

            ("D", "A"): "gefärbt; falsch angeschlossen, da Schmutzwasser in Regenwasserleitung/-kanal abfließt",
            ("D", "B"): "gefärbt; falsch angeschlossen, da Regenwasser in Schmutzwasserleitung/-kanal abfließt",
            ("D", "C"): "gefärbt; kein Fehlschluss erkennbar",

            ("E", "A"): "trüb und gefärbt; falsch angeschlossen, da Schmutzwasser in Regenwasserleitung/-kanal abfließt",
            ("E", "B"): "trüb und gefärbt; falsch angeschlossen, da Regenwasser in Schmutzwasserleitung/-kanal abfließt",
            ("E", "C"): "trüb und gefärbt; kein Fehlschluss erkennbar",
        },
        # DDF - Atmosphäre im Schacht (Tab. A-2-62)
        "DDF": {
            ("", ""): "Atmosphäre im Schacht oder der Inspektionsöffnung",
            ("A", ""): "Sauerstoffmangel",
            ("B", ""): "Schwefelwasserstoff",
            ("C", ""): "Methan",
            ("Z", ""): "andere",
        },

        # DDG - Keine Sicht (Tab. A-2-63)
        "DDG": {
            ("", ""): "Keine Sicht",
            ("A", ""): "Kamera unter Wasser",
            ("B", ""): "Verschlammung",
            ("C", ""): "Dämpfe",
            ("Z", ""): "andere",
        },
    },
}


def get_beschreibung(gruppe, kuerzel, charakt1="", charakt2=""):
    """
    Lookup-Funktion zum Abrufen der Beschreibung für eine Kürzel-Kombination.

    Args:
        gruppe: "Haltungen" oder "Schächte"
        kuerzel: DWA-Kürzel (z.B. "BAA", "BAB")
        charakt1: Charakterisierung 1 (Standard: "")
        charakt2: Charakterisierung 2 (Standard: "")

    Returns:
        Beschreibungstext oder None wenn Kombination nicht gefunden

    Beispiel:
        >>> get_beschreibung("Haltungen", "BAA", "A", "")
        'vertikal - die Höhe des Rohres hat sich verringert'

        >>> get_beschreibung("Haltungen", "BAB", "C", "A")
        'Klaffender Riss - offener Spalt erkennbar, Segmente am Platz; in Längsrichtung'
    """
    try:
        return DWA_DATA[gruppe][kuerzel][(charakt1, charakt2)]
    except KeyError:
        return None


def get_beschreibung_with_fallback(gruppe, kuerzel, charakt1="", charakt2=""):
    """
    Lookup-Funktion mit Fallback-Logik.

    Versucht folgende Kombinationen in Reihenfolge:
    1. (charakt1, charakt2) - exakte Kombination
    2. (charakt1, "") - nur Charakterisierung 1
    3. ("", "") - nur Kürzel

    Args:
        gruppe: "Haltungen" oder "Schächte"
        kuerzel: DWA-Kürzel
        charakt1: Charakterisierung 1
        charakt2: Charakterisierung 2

    Returns:
        Tuple (beschreibung, matched_key) oder (None, None)

    Beispiel:
        >>> get_beschreibung_with_fallback("Haltungen", "BAG", "", "")
        ('Einragender Anschluss', ('', ''))

        >>> get_beschreibung_with_fallback("Haltungen", "UNKNOWN", "", "")
        (None, None)
    """
    if gruppe not in DWA_DATA or kuerzel not in DWA_DATA[gruppe]:
        return None, None

    kuerzel_dict = DWA_DATA[gruppe][kuerzel]

    # Versuche exakte Kombination
    if (charakt1, charakt2) in kuerzel_dict:
        return kuerzel_dict[(charakt1, charakt2)], (charakt1, charakt2)

    # Fallback: nur Charakterisierung 1
    if (charakt1, "") in kuerzel_dict:
        return kuerzel_dict[(charakt1, "")], (charakt1, "")

    # Fallback: nur Kürzel
    if ("", "") in kuerzel_dict:
        return kuerzel_dict[("", "")], ("", "")

    return None, None
