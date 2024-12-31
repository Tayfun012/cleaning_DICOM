import os

# Definiere den Eingangsordner, in dem die Unterordner durchsucht werden sollen
eingangsordner = "X:/BDMS/Herausgabe/Herausgabefall/032_TagsClean/ze_part_2_out"

# Gehe alle Ordner und Unterordner durch und bearbeite die Ordnernamen
for root, dirs, files in os.walk(eingangsordner):
    for dir in dirs:
        # Entferne die Zeichenkette "DropFiles_inThisSubfolder_" aus dem Ordnernamen
        neuer_ordnername = dir.replace("DropFiles_inThisSubfolder_", "")
        alter_ordnerpfad = os.path.join(root, dir)
        neuer_ordnerpfad = os.path.join(root, neuer_ordnername)
        os.rename(alter_ordnerpfad, neuer_ordnerpfad)
        print(f"Ordner {alter_ordnerpfad} umbenannt in {neuer_ordnerpfad}")
