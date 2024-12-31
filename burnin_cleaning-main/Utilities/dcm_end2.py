import os

def füge_endung_hinzu(ordnerpfad, endung=".dcm"):
    # Gehe durch alle Dateien im angegebenen Ordner
    for root, dirs, files in os.walk(ordnerpfad):
        for dateiname in files:
            # Baue den vollständigen Pfad zur Datei
            aktueller_pfad = os.path.join(root, dateiname)

            # Überprüfe, ob es sich um eine Datei handelt
            if os.path.isfile(aktueller_pfad):
                # Überprüfe, ob die Datei bereits die Endung .dcm hat
                if not dateiname.endswith(endung):
                    # Baue den neuen Dateipfad mit der gewünschten Endung
                    neuer_pfad = f"{os.path.splitext(aktueller_pfad)[0]}{endung}"

                    # Benenne die Datei um
                    print ("%s --> %s" % (aktueller_pfad, neuer_pfad))
                    os.rename(aktueller_pfad, neuer_pfad)

def main():
    # Gib den Pfad des Ordners an, in dem du die Dateien ändern möchtest
    ordnerpfad = "//data02//Napkon//6825962"
    # "X:\\BDMS\\Napkon\\6825961"
    # Rufe die Funktion auf, um die Endung hinzuzufügen
    füge_endung_hinzu(ordnerpfad)

if __name__ == "__main__":
    main()
