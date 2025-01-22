import csv
import os
import threading
import requests

# Directory to save downloaded images
download_dir = 'basket'

# Create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Read URLs from CSV file
urls = []
csv_path = '/home/multi-sy-23/Downloads/merge_csv/Netball-Basket-Detection-20-01-2025-12-13-52.csv'

with open(csv_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        urls.append(row['Source Url'])

print(f"Total URLs to download: {len(urls)}")

# Function to download a file
def download_file(url, download_dir):
    try:
        # Send GET request
        response = requests.get(url, timeout=10, stream=True)
        if response.status_code == 200:
            # Extract filename from URL
            filename = os.path.basename(url)
            filepath = os.path.join(download_dir, filename)
            
            # Save the file
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Thread-based download manager
def download_files_in_threads(urls, download_dir, max_threads=10):
    # Internal function to handle thread creation and synchronization
    def worker(urls):
        for url in urls:
            download_file(url, download_dir)

    # Split URLs into chunks for each thread
    chunk_size = len(urls) // max_threads + 1
    threads = []

    for i in range(0, len(urls), chunk_size):
        chunk = urls[i:i + chunk_size]
        thread = threading.Thread(target=worker, args=(chunk,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Download using threads
download_files_in_threads(urls, download_dir, max_threads=10)

print("All downloads completed.")

