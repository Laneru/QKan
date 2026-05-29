Erstellen und Bearbeiten von Kanalnetzen
========================================

Bei der Erstellung sowie der Bearbeitung von Kanalnetzen können die QGIS-Standardfunktionen 
verwendet werden. Dabei ist zu beachten, dass die Änderungen erst dann in die QKan-Datenbank 
geschrieben werden, wenn die Änderungen jedes Layers gespeichert wurden. 

Sowohl QGIS als auch QKan bietet ein paar sehr nützliche Funktionalitäten an, die hier erläutert 
werden sollen. 


Digitalisieren von Kanälen
^^^^^^^^^^^^^^^^^^^^^^^^^^

Beim Digitalisieren sollten zuerst die Schächte erfasst, benannt und gespeichert werden. So können die Trigger ausgenutzt werden,
die beim Speichern des Haltungslayers ausgelöst werden.
Werden anschließend die Haltungen digitalisiert und gespeichert, übernimmt ein Trigger automatisch die Namen der gefangenen Schächte
als Schacht oben und Schacht unten.

