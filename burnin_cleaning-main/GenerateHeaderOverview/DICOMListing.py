import os
import pydicom
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict
import pandas as pd

def read_dicom_header(file_path):
    """
    Liest den Header einer DICOM-Datei aus und gibt eine verschachtelte Struktur der Tags und Werte zurück.
    """
    print(f"processing {file_path}")
    try:
        ds = pydicom.dcmread(file_path,stop_before_pixels=True)
        header_info = {}

        def extract_tags(dataset, parent_key=""):
            for elem in dataset:
                key = f"{parent_key}.{elem.tag}" if parent_key else str(elem.tag)
                if elem.VR == "SQ":  # Sequence
                    header_info[key] = "Sequence"
                    for i, item in enumerate(elem.value):
                        extract_tags(item, f"{key}[{i}]")
                else:
                    if  type(elem.value) == list:
                        temp=[]
                        for value in elem.value:
                            temp.append(str(value))
                        header_info[key] = temp
                    else:
                        header_info[key] = str(elem.value)

        extract_tags(ds)
        return {file_path: header_info}
    except Exception as e:
        return {file_path: {"error": str(e)}}

def process_dicom_files(file_paths):
    """
    Verarbeitet eine Liste von DICOM-Dateien parallel und gibt eine kombinierte Struktur zurück.
    """
    combined_results = defaultdict(dict)

    with ProcessPoolExecutor() as executor:
        results = executor.map(read_dicom_header, file_paths)

    for result in results:
        combined_results.update(result)

    return combined_results

def find_dicom_files(root_dir):
    """
    Durchsucht ein Verzeichnis und alle Unterverzeichnisse nach DICOM-Dateien.
    """
    dicom_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            dicom_files.append(os.path.join(dirpath, file))
    return dicom_files

def ReducetoLastDICOMTag(all_headers):
    import re
    def extract_last_parentheses_part(input_string):
        # Use regex to match the content within the last set of parentheses
        match = re.search(r'\(([^()]*)\)(?!.*\()', input_string)
        if match:
            return match.group(1)
        return None
    Result={}
    for file, header in all_headers.items():
        for tag,value in header.items():
            tagRed=extract_last_parentheses_part(tag) 
            if tagRed not in Result:
                Result[tagRed]=[]
            if tagRed in Result:
                if value not in Result[tagRed]:
                    Result[tagRed].append(value)
    return Result


def reduce_sublists_to_new_list(lst):
    from functools import reduce
    # Use reduce to concatenate all sublists into a single list
    return reduce(lambda acc, sublist: acc + sublist, lst, [])

def translate_dicom_tag(tag_string):
    from pydicom.datadict import keyword_for_tag
    from pydicom.tag import Tag
    """
    Translates a DICOM tag in the form gggg,tttt to a human-readable keyword.

    Args: 
        tag_string (str): The DICOM tag as a string, e.g., "0010,0020".

    Returns:
        str: The human-readable keyword for the tag, or an error message if not found.
    """
    try:
        # Convert the string into a Tag object
        group, element = (int(tag_string[0:4], 16), int(tag_string[5:9], 16))
        tag = Tag(group, element)
        
        # Get the keyword for the tag
        keyword = keyword_for_tag(tag)
        
        if keyword:
            return keyword
        else:
            return f"None"
    except Exception as e:
        return f"Error"
    

if __name__ == "__main__":
    # Verzeichnis mit DICOM-Dateien angeben
    dicom_dir = "/data02/Napkon/6825962_out_CTP/"
    print("Get all filepathes - Start")
    # Alle DICOM-Dateien im Verzeichnis sammeln
    dicom_files = find_dicom_files(dicom_dir)
    print("Get all filepathes - End")
    # DICOM-Dateien parallel verarbeiten
    all_headers = process_dicom_files(dicom_files)
    Reduction=ReducetoLastDICOMTag(all_headers)
    for k,v in Reduction.items():
        Reduction[k]=[str(translate_dicom_tag(k)),""] +v

    # Ergebnisse ausgeben
    i=0
    for file, header in all_headers.items():
        i=i+1
        print("Datei %7i/%7i/: %s" % (i,len(all_headers.keys(),file) ))
        for tag, value in header.items():
            print(f"  {tag}: {value}")
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in Reduction.items()]))
    
    transposed_df = df.T

    output_file = "Reduction.xlsx"
    transposed_df.to_excel(output_file, index=True, header=False)