import pandas as pd
import csv
import urllib
import cv2
import os
import numpy as np
import json
import torch
from ultralytics import YOLO

# Check if CUDA (GPU support) is available
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using GPU for computation.")
else:
    device = torch.device("cpu")
    print("CUDA is not available. Using CPU for computation.")

# Load image URLs and tags from the CSV file
data = pd.read_csv("/home/multi-sy-23/Downloads/merge_csv/newdata.csv")
img_urls = data["Source Url"].tolist()
tags = data["Tags"].tolist()

# Define the folder path for reading images
create_fold = "/home/multi-sy-23/Downloads/merge_csv/ball/"

# Load YOLO models
model1 = YOLO('/home/multi-sy-23/Downloads/merge_csv/79rDGGnRPFYxcxx.pt')
model2 = YOLO("/home/multi-sy-23/Downloads/merge_csv/basket.pt")

# CSV file to save coordinates
new_csv = "new_coordinates.csv"

# Write header to CSV
with open(new_csv, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Type", "Original Id", "Tags", "Source Url", "annotation"])

# Process each downloaded image
for tag, url in zip(tags, img_urls):
    ty = "train"
    id_ = ""

    image_name = os.path.basename(urllib.parse.urlparse(url).path)
    image_path = os.path.join(create_fold, image_name)

    try:
        cap = cv2.imread(image_path)

        if cap is None:
            raise ValueError(f"Failed to read image from {image_path}")

        # Initialize annotation dictionary
        annotation = {"rect": [], "point": [], "line": [], "polygon": [], "circle": [], "rectAndKeypoints": []}

        # Predict using both models and merge results
        for model in [model1, model2]:
            results = model.predict(cap, max_det=1, imgsz=1024)
            results = results[0]
            result_box = results.obb.xywhr.cpu().numpy()
            labels = results.obb.cls.tolist()
            scores = np.array(results.obb.conf.tolist(), dtype="float").round(2)

            for rect, label, score in zip(result_box.tolist(), labels, scores):
                try:
                    x = rect[0]
                    y = rect[1]
                    w = rect[2]
                    h = rect[3]

                    xmin = x - (w / 2)
                    ymin = y - (h / 2)

                    if isinstance(label, (int, float)):
                        label = int(label)
                        if 0 <= label < len(model.names):
                            name = model.names[label]
                            annotation["rect"].append([xmin, ymin, w, h, name])
                        else:
                            print(f"Invalid class ID: {label}")
                    else:
                        print(f"Invalid label type: {type(label)}")
                except Exception as e:
                    print(f"Error processing bounding box: {e}")

        # Write to CSV
        with open(new_csv, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([ty, id_, tag, url, json.dumps(annotation)])

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")

