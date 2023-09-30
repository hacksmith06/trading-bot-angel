import pandas as pd
import requests
from tqdm import tqdm

# Fetch the JSON data from the URL
url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = requests.get(url, stream=True)

# Use tqdm to show progress while downloading
response.iter_content(chunk_size=8192)
total_size = int(response.headers.get('content-length', 0))
download_progress = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading JSON")
data = []
for chunk in response.iter_content(chunk_size=8192):
    download_progress.update(len(chunk))
    data.append(chunk)
download_progress.close()

data = b''.join(data).decode('utf-8')
data = eval(data)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(data)

# Filter the DataFrame to include only rows where 'exch_seg' is 'NSE'
nse_stocks = df[df['exch_seg'] == 'NSE']

# Extract the desired columns: 'name', 'symbol', and 'token'
result = nse_stocks[['name', 'symbol', 'token']]

# Save the result to a CSV file with tqdm progress
csv_filename = "nse_stocks.csv"
with tqdm(total=len(result), desc="Saving to CSV") as pbar:
    result.to_csv(csv_filename, index=False, mode='w', chunksize=100, header=True)
    pbar.update(len(result))
