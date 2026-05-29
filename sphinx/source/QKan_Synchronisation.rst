Vergleich und Synchronisation von QKan-Datenbanken
==================================================

Es gibt in der Praxis mehrere Fälle, in denen ein Vergleich zwischen zwei QKan-Projekten sinnvoll ist: 

    - Ein Teilgebiet wurde zur Bearbeitung herausgegeben und die Änderungen sollen übernommen werden
    - Im Rahmen einer TV-Untersuchung wurde ein QKan-Projekt erstellt, dessen Daten in ein QKan-Bestandsprojekt 
      übernommen werden sollen.
    - Es existieren zwei Versionen eines QKan-Projektes, aus denen wieder eine Version erstellt werden soll
    - Mehrere Teilnetze sollen zusammengeführt werden.

Das grundsätzliche Vorgehen bei der Synchronisation von QKan-Projekten ist wie folgt: 

#. Das aktuell geladene Projekt wird mit einem ausgewählten *externen Projekt* mit der 
   Funktion |Tool_Bearbeitungsmodus| :guilabel:`Vergleich mit einem anderen QKan-Projekt` verglichen. Datei wird für 
   jede QKan-Tabelle eine Synchronisationstabelle erstellt, in der individuell festgelegt kann, welche 
   der möglichen Maßnahmen (ändern, hinzufügen, löschen) auch tatsächlich ausgeführt werden sollen. Dazu muss 
   in der ersten Spalte "ausführen" eine "1" stehen. Zum Ändern muss der Bearbeitungsmodus mit dem 
   Icon |Tool_Abgleich|:guilabel:`Bearbeitungsmodus` aktiviert werden. Bei der Bearbeitung des Feldes erscheint anstelle der Zahl 
   ein Kontrollfeld. Wie in der nachfolgenden Grafik beispielhaft zu sehen, sind aktive Änderungen farbig 
   hinterlegt (grün: hinzufügen, orange: ändern, rot: löschen), während deaktivierte Änderungen durchgestrichen 
   sind und nur die Textfarbe entsprechend ist. 
   
   Violett hinterlegte Datensätze zeigen dagegen Bezeichnungen an, die entweder in der externen oder der 
   Bestandsdatenbank mehrfach vorkommen. Diese werden bei der anschließenden Synchronisation nicht berücksichtigt. 


.. image:: ./QKan_Bilder/tabelle_sync.png

#. Die eigentliche Synchronisation erfolgt mit der Funktion |Tool_Sync| :guilabel:`Synchronisation mit einem anderen QKan-Projekt`. 
Falls dabei auch Datensätze gelöscht werden sollen, muss dies zur Sicherheit extra mit dem entsprechenden Kontrollfeld bestätigt werden. 

.. |Tool_Abgleich| image:: ./QKan_Bilder/Tool_Abgleich.png
                             :width: 1.25 em

.. |Tool_Sync| image:: ./QKan_Bilder/Tool_Sync.png
                             :width: 1.25 em

.. |Tool_Bearbeitungsmodus| image:: ./QKan_Bilder/Tool_bearbeitungsmodus.png
                             :width: 1.25 em

