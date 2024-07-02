import argparse
import datetime
import numpy as np
import os
import pandas as pd
import requests
import sys
from typing import Any, Optional, Tuple
from sentinelhub import (SHConfig, DataCollection, SentinelHubCatalog, SentinelHubRequest, BBox, bbox_to_dimensions, CRS, MimeType, Geometry)
from creds import *


    
# Import credentials
def get_access_token(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",data=data)
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Access token creation failed. Reponse from the server was: {r.json()}")
    return r.json()["access_token"]
    

def download_Isat(start_date, end_date, north, south, east, west, data_collection,level, directory_save):
	"""
	This function downloads Sentinel-2 images from the Copernicus Data Space Ecosystem for the specified geographical area and time range, saving them in the specified directory.

	Args:
	start_date: Start date of the time range for downloading images in 'YYYY-MM-DD' format.
	end_date: End date of the time range for downloading images in 'YYYY-MM-DD' format.
	north: Northern coordinate of the area of interest (latitude).
	south: Southern coordinate of the area of interest (latitude).
	east: Eastern coordinate of the area of interest (longitude).
	west: Western coordinate of the area of interest (longitude).
	data_collection: Name of the data collection, e.g., "SENTINEL-2".
	level: 'L1C' or 'L2A'
	directory_save: Directory where the downloaded images will be saved.

	Example:
	download_Isat("2023-04-01", "2023-05-01", -34.81, -34.82, -57.8900, -57.8961, "SENTINEL-2", "L1C","/directory_example_S2_timeSeries/")
	"""
	print(f"Save directory: {directory_save}")
	print(f"Start date: {start_date}")
	print(f"End date: {end_date}")
	print(f"Data collection: {data_collection}")
	print(f"Level: {level}")
	print(f"North: {north}, South: {south}, East: {east}, West: {west}")
	try:

		# Construct the area of interest (AOI)
		aoi = f"POLYGON(({west} {north}, {east} {north}, {east} {south}, {west} {south}, {west} {north}))"

		# Request to obtain data from the catalog
		url = (
		   f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
		   f"$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') "
		   f"and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z"
		)
		response = requests.get(url)
		response.raise_for_status()
		json_data = response.json()

		# Create a DataFrame with the obtained data
		df = pd.DataFrame.from_dict(json_data["value"])

		# Download the products
		for index, row in df.iterrows():
			if level in row['Name']:
				print("Downloading",row['Name'])
				access_token = get_access_token(username, password)
				product_url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({row['Id']})/$value"
				headers = {"Authorization": f"Bearer {access_token}"}

				with requests.get(product_url, headers=headers, stream=True) as r:
					r.raise_for_status()
					file_path = f"{directory_save}{row['Name']}.zip"
					with open(file_path, 'wb') as file:
						for chunk in r.iter_content(chunk_size=8192):
							if chunk:
								file.write(chunk)
		print("Download completed.")
	except Exception as e:
		print(f"Error: {e}")

	return

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to download Sentinel-2 data.')
	parser.add_argument('--directory_save', type=str, required=True, help='Directory where the data will be saved.')
	parser.add_argument('--start_date', type=str, required=True, help='Start date (YYYY-MM-DD).')
	parser.add_argument('--end_date', type=str, required=True, help='End date (YYYY-MM-DD).')
	parser.add_argument('--data_collection', type=str, required=True, help='Data collection.')
	parser.add_argument('--north', type=float, required=True, help='North coordinate.')
	parser.add_argument('--south', type=float, required=True, help='South coordinate.')
	parser.add_argument('--east', type=float, required=True, help='East coordinate.')
	parser.add_argument('--west', type=float, required=True, help='West coordinate.')
	parser.add_argument('--level', type=str, required=True, help='Level products.')
	args = parser.parse_args()
	download_Isat(args.start_date, args.end_date, args.north, args.south, args.east, args.west, args.data_collection, args.level,args.directory_save)


