# Self Changing Wallpaper
This project downloads an image throught Reddit API and sets it as a wallpaper.

# Setup
1. download and unzip or clone the repository
2. make sure you have Python 3.6 or newer installed *(if you don't, download it on [official python website](https://www.python.org/downloads/))*
3. install python modules from requirements.txt *(command: pip install -r requirements.txt)*
4. create .env file in same directory and configure it similarly to this:
	```
	subreddit = "wallpaper"
	wallpaper_path = "C:/Users/User/wallpapers/"
	```
	*dont forget to create the folder*

5. use task scheduler (or some alternative) and setup when you want to change your wallpaper
6. make sure to clean your folder with wallpapers sometimes, because there will be a lot of images
7. done *(if you encountered a problem just create an issue)*
