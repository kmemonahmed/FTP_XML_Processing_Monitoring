import os
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ftplib
import time
import shutil

# FTP server details
FTP_SERVER = 'localhost'
FTP_USER = 'nybsys'
FTP_PASS = '12345'

# Directory paths
TEMP_FOLDER = 'Temp'
LOCAL_FOLDER = 'Local'
TRASH_FOLDER = 'Trash'

# Ensure directories exist
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(LOCAL_FOLDER, exist_ok=True)
os.makedirs(TRASH_FOLDER, exist_ok=True)

# List to keep track of processed files
processed_files = []

# Function to download files from FTP server
def download_files():
    while True:
        print("Checking for new files on FTP server and downloading...")
        try:
            with ftplib.FTP(FTP_SERVER) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                files = ftp.nlst()
                print(f"Files on FTP server: {files}")

                for file_name in files:
                    if file_name not in processed_files:
                        local_temp_path = os.path.join(TEMP_FOLDER, file_name)
                        local_final_path = os.path.join(LOCAL_FOLDER, file_name)

                        with open(local_temp_path, 'wb') as local_file:
                            print(f"Downloading {file_name}...")
                            ftp.retrbinary(f'RETR {file_name}', local_file.write)

                        print(f"Moving {file_name} to local folder...")
                        shutil.move(local_temp_path, local_final_path)

                        processed_files.append(file_name)
                        print(f"Downloaded {file_name} to {local_final_path}")
                    else:
                        pass # Skip already processed files

                print("FTP download process complete. Waiting for the next check...")
                time.sleep(1)
        except ftplib.all_errors as e:
            print(f"FTP error: {e}")
            time.sleep(1)

# Function to process XML file
def process_file(file_path):
    try:
        print(f"Processing file: {file_path}")
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespace from the root element
        ns = root.tag.split('}', 1)[0][1:]

        data_dict = {}

        # Extract measType elements and create a dictionary for quick lookup
        meas_types = {}
        for measType in root.findall(f'.//{{{ns}}}measType'):
            p = measType.get('p')
            name = measType.text.strip() if measType.text else ""
            meas_types[p] = name

        # Extract measValue elements and map values to measTypes
        for measValue in root.findall(f'.//{{{ns}}}measValue'):
            for r in measValue.findall(f'.//{{{ns}}}r'):
                p = r.get('p')
                value = r.text.strip() if r.text else ""
                if p in meas_types:
                    data_dict[meas_types[p]] = value
                else:
                    print(f"Warning: No matching measType for p={p}")

        # Move processed file to trash folder
        trash_path = os.path.join(TRASH_FOLDER, os.path.basename(file_path))
        shutil.move(file_path, trash_path)
        print(f"Moved {file_path} to {trash_path}")

        return data_dict

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}

# File event handler
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            process_result = process_file(event.src_path)
            print(f"Processed data: {process_result}")

# Start watching the local folder for new files
def monitor_local_folder():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, LOCAL_FOLDER, recursive=False)
    observer.start()
    print(f"Started monitoring {LOCAL_FOLDER} for new files.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start the download and monitoring processes
if __name__ == "__main__":
    from threading import Thread

    download_thread = Thread(target=download_files)
    download_thread.start()

    monitor_local_folder()
