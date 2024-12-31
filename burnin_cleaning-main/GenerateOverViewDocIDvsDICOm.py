import pydicom
import time
import pandas as pd
import os

def extract_dicom_metadata(directory, output_csv):
    # List to store results
    data = []
    
    # Traverse directory and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if it's a DICOM file (basic check: extension .dcm)
            if file.lower().endswith('.dcm'):
                try:
                    # Read DICOM file
                    ds = pydicom.dcmread(file_path,stop_before_pixels=True)
                    
                    # Extract desired metadata
                    StudyInstUID    = getattr(ds, 'StudyInstanceUID', 'N/A')
                    SOPInstUID      = getattr(ds, 'SOPInstanceUID', 'N/A')
                    SeriesInstID    = getattr(ds, 'SeriesInstanceUID', 'N/A')
                    InstNum         = getattr(ds, 'InstanceNumber', 'N/A')
                    DOCId           = os.path.basename(os.path.dirname(os.path.normpath(file_path)))
                    # Append data to list
                    data.append({
                        "Folder": root,
                        "File": file,
                        "DOCId": DOCId,
                        "Header_StudyInstanceUID": StudyInstUID,
                        "Header_SOPInstanceUID": SOPInstUID,
                        "Header_SeriesInstanceUID": SeriesInstID,
                        "Header_InstanceNumber"   : InstNum
                    })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    # Convert to DataFrame for easier manipulation and save as CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Metadata saved to {output_csv}")



start_time = time.perf_counter()
SoureFolder="../Example/US_Package/"
SoureFolder="/home/ipoethke/projects-ICM/BDMS/Napkon/6825962_out/"
LastFolder=os.path.basename(os.path.dirname(os.path.normpath(SoureFolder)))
extract_dicom_metadata(SoureFolder,"OverView_%s.json" % (LastFolder))



end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")


