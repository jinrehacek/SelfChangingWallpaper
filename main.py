import ctypes
import requests
import datetime
from os import environ
from os.path import normpath
from dotenv import load_dotenv

# Loading .env file which can store variables outside of the script
load_dotenv()

# Selection of subreddit that we want to use
if environ.get("subreddit"):
    SUBREDDIT = environ.get("subreddit")
else:
    SUBREDDIT = "wallpaper"

# Path where to save the images
PATH = normpath(environ.get("wallpaper_path"))

# Template for name of the file
NAME_TEMPLATE = f"{'%Y'}-{'%m'}-{'%d'}"
NAME_TEMPLATE_WITH_HOURS = NAME_TEMPLATE + f"({'%H'})"

# Setup for workin with datetime module
time = datetime.datetime.now()

# Url for Reddit API request
url = f"https://www.reddit.com/r/{SUBREDDIT}/top/.json?&t=day&limit=1"

# Request to reddit API with special header to acess it
response = requests.get(
    url, headers={'User-agent': 'SelfChangingWallpaper 0.1'})

# Getting url of the image and then requesting it
img_url = response.json()["data"]["children"][0]["data"]["url"]
image = requests.get(img_url)

# Deciding between .png and .jpg extension
if ".png" in img_url:
    extension = ".png"
elif ".jpg" in img_url or "¨.jpeg" in img_url:
    extension = ".jpg"
else:
    print("Image is not .png or .jpeg:\n", img_url)
    raise Exception


assert (response.status_code ==
        200), "Error occurred when connecting to Reddit.com"

try:
    # Saving the image file
    filename = normpath(
        PATH + "/" + time.strftime(NAME_TEMPLATE) + extension)
    file = open(filename, mode="bx")
    file.write(image.content)
except FileExistsError:
    # Runs if there's already file with name of same date
    # Setting different filename by adding hour time information
    # filename = os.ath.normpath(PATH + "/" + time.strftime(NAME_TEMPLATE) + time.strftime(f"({'%H'})") + extension)
    filename = normpath(
        PATH + "/" + time.strftime(NAME_TEMPLATE_WITH_HOURS) + extension)
    # Saving the image file
    file = open(filename, mode="xb")
    file.write(image.content)


# Setting image as wallpaper
ctypes.windll.user32.SystemParametersInfoW(20, 0, filename, 0)
