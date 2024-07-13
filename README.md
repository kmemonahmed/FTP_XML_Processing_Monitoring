# FTP Download and XML Processing Script

## Overview
This script downloads files from an FTP server, processes XML files, and monitors a local directory for new files. It utilizes threading to handle FTP downloads and directory monitoring concurrently.

## Prerequisites
- Python 3.x
- `ftplib`, `watchdog`, and `xml.etree.ElementTree` libraries (these are standard Python libraries, but `watchdog` needs to be installed via pip)
- Docker for running the FTP server

## Setting Up the FTP Server Using Docker
To set up the FTP server, you can use the `fauria/vsftpd` Docker image. Here are the steps:

1. Run the FTP server:
    ```sh
    docker-compose up -d
    ```

## Uploading Files to the FTP Server Using `curl`
To upload files to the FTP server, you can use the `curl` command. Here are the steps:

1. Make sure you have `curl` installed. If not, install it using your package manager (e.g., `apt`, `yum`, `brew`).

2. Upload a file to the FTP server:
    ```sh
    curl -T <your_file_path> ftp://localhost:21 --user nybsys:12345
    ```

   Replace `<your_file_path>` with the path to the file you want to upload.

## Running the Script
To run the script, follow these steps:

1. Make sure you have Python installed.

2. Install the required Python package `watchdog`:
    ```sh
    pip install watchdog
    ```

3. Run the script:
    ```sh
    python file_processor.py
    ```

## Summary
This README provides instructions on setting up an FTP server using Docker, uploading files using `curl`, and running the Python script to download, process, and monitor XML files.
