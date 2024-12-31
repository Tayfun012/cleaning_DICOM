## Name
cleaning_DICOM_tags

## Description
Dieser Code ist ein Python-Skript, das DICOM-Dateien aus einem Eingangsordner liest, der über eine GUI ausgewählt wird. Es durchsucht die Header-Elemente der DICOM-Dateien, die in einer angegebenen Konfigurationsdatei enthalten sind, und ersetzt sie mit dem String '*removed*', wenn es gefunden wird. Anschließend wird das modifizierte Datensatz-Objekt in eine neue DICOM-Datei gespeichert und in einen Ausgangsordner gespeichert, der sich auf derselben Ebene wie der Eingangsordner befindet und die gleiche Ordnerstruktur wie der Eingangsordner hat. Der Name des Ausgangsordners ist derselbe wie der Eingangsordner, nur mit einem Suffix "out" drangehängt. Bereits vorhandene Daten  im Ausgangsordner werden nicht überschrieben.
 
Der vorliegende Code dient der Strukturierung und Anonymisierung von Seriennummern in DICOM-Dateien. Konkret ersetzt der Code die Seriennummern im DICOM-Tag "Device Serial Number" (0x0018,0x1000) durch neue IDs.

Zur Umsetzung dieses Vorgangs wird zuerst eine CSV-Datei eingelesen, die im Projekt "https://git.bihealth.org/icm-dhcz/num/replace_serialnumber" erstellt wurde. Diese CSV-Datei enthält sämtliche Seriennummern des Datensatzes sowie den zugehörigen neuen IDs.

Der Code sucht nun in den DICOM-Dateien nach dem Tag (0x0018,0x1000) und ersetzt den entsprechenden Inhalt durch die zugehörige ID, sofern eine Übereinstimmung vorliegt.

Zu Beginn des Programms wird die Matching_CSV-Datei eingelesen und ein Matching-Dictionary initialisiert. Bei der Verarbeitung einer neuen DICOM-Datei wird der DICOM-Tag gescannt, um die passende Seriennummer zu identifizieren und gegebenenfalls durch die entsprechende ID zu ersetzen.


## Usage

1. git clone -b branchname remote-repo-url

2. Erstelle eine config.json und platziere sie im Ordner "config". Ein Template (config_template_path.json) befindet sich im Ordner, an dem du dich orientieren kannst.

3. Erstelle eine config.ini (siehe Template unten) und gebe den Pfad zu der config.ini in der config.json unter dem Parameter config_file an

4. Gebe den Pfad zu der erstellten CSV-Datei aus dem Projekt "https://git.bihealth.org/icm-dhcz/num/replace_serialnumber" in der config.json unter dem Parameter device_serial_table an.

4. Aufruf wie folgt:
- python3 .../cleaning_dicom_tags/main.py

## config.ini
Konfigurationsdatei enthält folgende Tags:

Die Variablen "remove_tags_string" und "remove_tags_bytes" enthalten DICOM-Tags, deren Inhalt mit dem Wert *removed* ersetzt werden, wenn sie in der DICOM-Datei gefunden werden. Die Variablen "remove_tags_string_selection" und "remove_tags_bytes_selection" enthalten DICOM-Tags. Wenn in den Tags die Zeichenketten in den Variable "selection_string" und "selection_byte" enthalten sind, werden diese Zeichenketten mit *removed* ersetzt.

## Support
Tayfun Kilic: tayfun.kilic@charite.de 

## Roadmap

## Contributing

## Authors and acknowledgment
Tayfun Kilic: tayfun.kilic@charite.de 

## License

## Project status
erfolgreich ausführbar

## Improvements
[2023-02-07] Daten werden im Ausgangsordner nicht überschrieben.