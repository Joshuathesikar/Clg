import pandas as pd
import os
from datetime import datetime

LOG_FILE = r"C:\Users\LENOVO\Desktop\database\violation_log.csv"

def log_violation(plate_number, violation_type):
    # Create new entry
    new_entry = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "LicensePlate": plate_number,
        "Violation": violation_type
    }])

    # Check if file exists
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry

    # Save to CSV
    df.to_csv(LOG_FILE, index=False)
