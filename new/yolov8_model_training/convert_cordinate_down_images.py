import os
import glob
import json
import cv2
import pandas as pd

txt_path = "labels/"
os.makedirs(txt_path, exist_ok=True)

img_path = "/home/multi-sy-23/volleyball_serve_model_training/serve/"
com_path = sorted(glob.glob(img_path + "*.jpg"))  

df = pd.read_csv("/home/multi-sy-23/volleyball_serve_model_training/Volleyball-Server-Detection-30-01-2025-15-06-48.csv")
df["image_name"] = df["Source Url"].apply(lambda x: x.split("/")[-1].split(".")[0])  # Extract image filename

# df.to_csv("jdjd.csv")

for img_file in com_path:
    file_name = os.path.basename(img_file).split(".")[0]  
    row = df[df["image_name"] == file_name]
    
    if row.empty:
        print(f"Skipping {file_name}, not found in CSV!")
        continue  

    data = json.loads(row["annotation"].values[0])  
    xywh = data["rect"][0][:-1]  
    x1, y1, w, h = xywh
    print(f"Processing: {file_name} | Coords: {xywh}")
    
    img = cv2.imread(img_file)
    if img is None:
        print(f"Error loading image: {img_file}")
        continue
    img_height, img_width, _ = img.shape 
    
    xcycwh = [x1+w/2, y1+h/2, w,h]
    xcycwh = [xcycwh[0]/img_width, xcycwh[1]/img_height, w/img_width, h/img_height]

    txt_filename = os.path.join(txt_path, f"{file_name}.txt")

    with open(txt_filename, "w") as txt:
        txt.write(f"0 {xcycwh[0]} {xcycwh[1]} {xcycwh[2]} {xcycwh[3]}\n")