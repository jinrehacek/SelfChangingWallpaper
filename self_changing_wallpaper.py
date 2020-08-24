import ctypes
import os
import requests
import json
import datetime

#Selection of subreddit that we want to use
SUBREDDIT = "wallpaper"

#Template for name of the file
NAME_TEMPLATE = f"{'%d'}-{'%m'}-{'%Y'}"

#Setup for workin with datetime module
time = datetime.datetime.now()

#Url for Reddit API request
url = f"https://www.reddit.com/r/{SUBREDDIT}/top/.json?&t=day&limit=5"

#Request to reddit API with special header to acess it
response = requests.get(
    url, headers={'User-agent': 'SelfChangingWallpaper 0.1'})

#Getting url of the image and then requesting it
img_url = response.json()["data"]["children"][0]["data"]["url"]
image = requests.get(img_url)

#Deciding between .png and .jpg extension
if ".png" in img_url:
    extension = ".png"
elif ".jpg" in img_url or "¨.jpeg" in img_url:
    extension = ".jpg"


filename = time.strftime(NAME_TEMPLATE) + extension

if response.status_code == 200:
	try:
		#Saving the image file
		file = open(filename, mode="bx")
		file.write(image.content)
	except:
		#Runs if there's already file with name of same date
		#Setting different filename by adding hour time information
		filename = time.strftime(NAME_TEMPLATE) + time.strftime(f"({'%H'})") + extension
		#Saving the image file
		file = open(filename, mode="xb")
		file.write(image.content)


#Path to the image
img_path = os.path.normpath(
    "C:/Users/ASUS/SelfChangingWallpaper/" + filename)

#Setting image as wallpaper
ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 0)
