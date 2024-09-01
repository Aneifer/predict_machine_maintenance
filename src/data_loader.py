import os
import requests
import zipfile

def download_data(url: str, save_path: str):
    # Resolve paths relative to the current script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_save_path = os.path.join(base_dir, save_path)

    # Ensure that the 'data' and 'raw' directories exist
    if not os.path.exists(full_save_path):
        os.makedirs(full_save_path)

    zip_path = os.path.join(full_save_path, 'dataset.zip')
    
    # Download the file
    response = requests.get(url)
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    print("Data downloaded successfully!")

    # Unpack the zip file into the specified directory
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(full_save_path)
    print(f"Data unpacked successfully in {os.path.abspath(full_save_path)}")

    # Find the unpacked file and rename it
    for filename in os.listdir(full_save_path):
        if filename.endswith(".csv"):
            original_file_path = os.path.join(full_save_path, filename)
            new_file_path = os.path.join(full_save_path, 'predictive_maintenance_raw_data.csv')
            os.rename(original_file_path, new_file_path)
            print(f"File renamed to {new_file_path}")
            break
    
    # Optionally, delete the zip file after extraction
    os.remove(zip_path)
    print("Zip file removed!")

if __name__ == "__main__":
    url = 'https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip'
    save_path = '../data/raw/'  # This is the directory where the data will be unpacked
    download_data(url, save_path)
