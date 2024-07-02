# Sentinel2Downloader

## Description

This repository provides tools to download Sentinel-2 (Level 1C and 2A) satellite images from the Copernicus Data Space Ecosystem using Python.

## Table of Contents

- [Setup](#setup)
- [Activate Copernicus Data Space Ecosystem](#activate-copernicus-data-space-ecosystem)
- [Usage](#usage)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/meleroafar/Sentinel2Downloader.git
   cd Sentinel2Downloader
   ```
2. **Install required packages:**
   ```sh
   pip install -r requirements.txt

## Activate Copernicus Data Space Ecosystem



First, you need to request access to the Copernicus Data Space Ecosystem through the API at https://dataspace.copernicus.eu/. If you have been a user of the Copernicus Open Access Hub, you can use your existing credentials. To download products from the Copernicus Data Space Ecosystem catalog via the API, every user must have an access token. Once registered, you can generate this token easily using a Python script. If you don't have an account yet, you can sign up at the registration portal.

Obtain the access token:
Once you have an account, you will need to obtain an access token. Here are the steps to do it:
## Usage
Once you have an account, you will need to obtain an access token. Here are the steps to do it:
Replace YOUR_USERNAME and YOUR_PASSWORD with your Copernicus Data Space Ecosystem login credentials in the creds.py file. This is equivalent to entering your username and password into the Copernicus Browser application. Ensure you keep them secure and do not share them with others.

Navigate to the cloned repository directory:

The next function downloads Sentinel-2 images from the Copernicus Data Space Ecosystem for the specified geographical area and time range, saving them in the specified directory. Adjust the parameters according that you need.

   ```sh
   python utils.py --directory_save "/directory_example_S2_timeSeries/" --start_date "2023-08-01" --end_date "2023-08-02" --data_collection "SENTINEL-2" --level "L1C" --north -34.81 --south -34.82 --east -57.8900 --west -57.8961
   ```
Parameters:

   - start_date: Start date of the time range for downloading images in 'YYYY-MM-DD' format.
   - end_date: End date of the time range for downloading images in 'YYYY-MM-DD' format.
   - north: Northern coordinate of the area of interest (latitude).
   - south: Southern coordinate of the area of interest (latitude).
   - east: Eastern coordinate of the area of interest (longitude).
   - west: Western coordinate of the area of interest (longitude).
   - data_collection: Name of the data collection, "SENTINEL-2".
   - level: 'L1C' or 'L2A' for Top-Of-Atmosphere (TOA) or Bottom-Of-Atmosphere (BOA) products, respectively
   - directory_save: Directory where the downloaded images will be saved.

