import os
import requests
import pandas as pd


def downloadImage(url, output_dir):
    """
    Takes in the url of an image and downloads it into the output directory
    :param url:
    :param output_dir:
    :return:
    """
    r = requests.get(url)
    print(r.headers)
    img_name = url.split("/")[-1]
    img_path = os.path.join(output_dir, img_name)
    with open(img_path, "wb") as f:
        f.write(r.content)


# Download nyt images
images = pd.read_csv("data/image_database.csv")
output_dir = "images/2010"
for url in images.url:
    downloadImage(url)
