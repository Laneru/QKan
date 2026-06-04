Ueberflutung
============

.. index:: Überflutungsanimation 
   
Überflutungsanimation
---------------------

Eine Videoanleitung zum Import von 2-D-Simulationsergebnissen aus einer gekoppelten Kanalnetz- und 
Oberflächenabflusssimulation mit HYSTEM-EXTRAN-2D ist |video_flood2d| (Passwort: *qkan*) zu finden.

.. |video_flood2d| raw:: html

   <a href="https://fh-aachen.sciebo.de/s/jDibeyZZZDpMjD7" target="_blank">hier</a>

Mit der Funktion |Tool_ueberflutung| :guilabel:`Überflutungsanimation` können die Ergebnisse von Überflutungsberechnungen aus externen Simulationen 
(z. B. mit FOG) direkt in QGIS visualisiert werden.
Das Tool dient dazu, zeitlich ablaufende Überflutungsszenarien anschaulich als Animation darzustellen – etwa zur Beurteilung von Fließwegen und Wassertiefen im Gelände.

.. image:: ./QKan_Bilder/Formulare/ueberflutung.png
.. |Tool_ueberflutung| image:: ./QKan_Bilder/Tool_ueberflutung.png
                             :width: 1.25 em
							 

Vor der Nutzung dieses Tools müssen die hydraulischen Simulationen mit dem Programm HYSTEM-EXTRAN-2D durchgeführt werden. Das Programm erzeugt dabei eine Ergebnis-Datenbank im Geodatabase-Format (z. B. Result2D.gdb), die die zeitabhängigen Simulationsergebnisse der Überflutung enthält.

Diese Datenbank bildet die Grundlage für die spätere Visualisierung in QGIS und wird im ersten Schritt ausgewählt.
Anschließend muss eine Datenbank angegeben werden, in der die aufbereiteten Daten für die Visualisierung gespeichert werden sollen.
Zunächst müssen die Berechnungsergebnisse mit der 
Schaltfläche :guilabel:`Ergebnisdateien aus Result2D.gdb importieren` importiert werden. 

Bei großen Einzugsgebieten mit mehr als 10.000 Elementen ist es empfehlenswert, die Animation nur für 
ausgewählte Teilbereiche erstellen zu lassen. Hierzu müssen in einem der beiden Layer "**velocities**" 
oder "**waterlevels**" die darzustellenden Elemente ausgewählt werden. 

Zusätzlich kann ausgwewählt werden, welche Daten dargestellt werden sollen und welche Skalierfaktoren dafür genutzt werden sollen.

Für die animierte Darstellung muss nach der Datenaufbereitung die QGIS-Zeitsteuerung aktiviert und 
der Zeitschritt eingestellt werden. 
