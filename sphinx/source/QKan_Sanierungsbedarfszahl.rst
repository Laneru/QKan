Sanierungsbedarfszahl
=====================

Vor der Nutzung dieses Plugins muss zunächst eine Zustandsklassifizierung mit dem Plugin Zustandsklassen durchgeführt werden.
Zusätzlich müssen in QGIS weitere Angaben wie Baujahr, hydraulische Leistungsfähigkeit und Bodenart ergänzt werden.
Anschließend kann das Plugin über die Menüleiste unter „Erweiterungen“ gestartet werden.

.. image:: ./QKan_Bilder/Sanierungsklassen/sanierung1.png

Daraufhin öffnet sich das in der folgenden Abbildung gezeigte Eingabefenster.

.. image:: ./QKan_Bilder/Sanierungsklassen/sanierung2.png

In dem Eingabefenster sind folgende Eingaben möglich:
 - Projektionssystem
 - Datenbank
 - Erstellungsdatum der Daten
 - Auswahl ob Sanierungsbedarfszahl (DWA) bzw. die Systemzahl (ISYSBAU) der Haltungen ermittelt werden soll
 - Auswahl ob Sanierungsbedarfszahl (DWA) bzw. die Systemzahl (ISYSBAU) der Schächte ermittelt werden soll
 - Auswahl ob Sanierungsbedarfszahl (DWA) bzw. die Systemzahl (ISYSBAU) der Leitungen ermittelt werden soll
 - Atlas Layer für Pläne erstellen
 - Automatisierte Planerstellung
 - Ausgabe einer Excel-Datei

In dem Eingabefenster wird zuerst das Projektionssystem ausgewählt. Danach wird die Datenbank ausgewählt, die für die Berechnung der Sanierungsbedarfszahl beziehungsweise der 
Systemzahl verwendet werden soll. Daraufhin kann das Erstellungsdatum ausgewählt werden, falls verschiedene Datensätze in der Datenbank vorhanden sind. Als nächstes wird für 
die Schächte, Haltungen und Leitungen ausgewählt, ob die Sanierungsbedarfszahl oder die Systemzahl nach ISYBAU ermittelt werden soll.
Wenn die Ermittlung der Sanierungsbedarfszahl nach DWA-M 149 durchgeführt wurde, werden die in der folgenden Abbildung gezeigten Layer für die Haltungen und Schächte dem Projekt 
hinzugefügt.


.. image:: ./QKan_Bilder/Sanierungsklassen/sanierung3.png
                             :scale: 50%
							 

Bei der Ermittlung der Systemzahl nach ISYBAU werden die in der folgenden Abbildung gezeigten Layer für die Haltungen und Schächte dem Projekt hinzugefügt.

.. image:: ./QKan_Bilder/Sanierungsklassen/sanierung4.png
							 

Ferner bietet das Plugin im Schritt sieben die Möglichkeit automatisiert Pläne zu erzeugen. Dafür kann der geforderte Maßstab und die Plangröße in der Eingabe ausgewählt werden. 
Ebenso kann ein Speicherort für die zu erstellenden Pläne ausgewählt werden. Daraufhin werden mit den im Projekt hinterlegten Layouts automatisch Pläne vom gesamten Gebiet erstellt. 
Die Layouts sollten im Vorhinein noch um Firmenlayouts und Planbeschreibungen ergänzt werden.
Die Layouts können geändert werden, indem in der Menüleiste „Projekt" ausgewählt wird. Daraufhin öffnet sich das in der folgenden Abbildung zu sehende Menü. Wird dort „Layouts" 
ausgewählt, erscheint ein Menü mit den im Projekt hinterlegten Layouts. Wird eins dieser Layouts angeklickt, öffnet sich dieses in einem neuen Fenster und Änderungen können 
vorgenommen werden.

.. image:: ./QKan_Bilder/Sanierungsklassen/sanierung5.png


Im letzten Schritt gibt es die Möglichkeit Excel Tabellen auszugeben. Dafür muss zuerst angegeben werden, ob es sich bei den Daten in der Datenbank um DWA-M 149 oder ISYBAU Daten 
handelt. Bei der Excel Ausgabe kann ausgewählt werden, ob nur Schächte/Haltungen/Leitungen oder alles ausgegeben werden soll. Des Weiteren muss die Entscheidung getroffen werden, 
ob alle Daten in ein Excel Tabellenblatt geschrieben werden sollen oder ob für jeden Schacht/Haltung ein einzelnes Tabellenblatt erstellt werden soll. Zum Schluss kann noch der 
Speicherort für die Excel Tabellen gewählt werden.
Im Vorhinein muss dafür einmalig das Python Modul XIsxWriter installiert werden, dafür müssen die folgenden Schritte durchgeführt werden. Zuerst muss das Programm „OSGe04W shell" 
geöffnet werden. Danach müssen die Befehle „cd C:\" und „python -m Pip install XIsxWriter" dort eingegeben werden. Dadurch wird das Modul XIsxWriter installiert und mit dem Plugin 
Sanierungsbedarfszahl kann eine Excel Tabelle ausgegeben werden. 



