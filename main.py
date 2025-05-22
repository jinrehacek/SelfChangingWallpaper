import ctypes
import requests
import datetime
import sys
from os import environ
from os.path import normpath, join
from dotenv import load_dotenv

def save_img(f_name, image_content):
    """Saves an image to a file.

    Args:
        f_name (str): The name of the file to save the image to.
                      This should include the path and extension.
        image_content (bytes): The content of the image to save.
    """
    try:
        with open(f_name, mode="wb") as file:
            file.write(image_content)
        print(f"Image saved successfully as {f_name}")
    except IOError as e:
        print(f"Error saving image to {f_name}: {e}")
        sys.exit(1)

def set_wallpaper_from_reddit():
    # Load environment variables from a .env file if it exists.
    # This allows configuration outside the script.
    load_dotenv()

    # Retrieve the subreddit name from environment variables, defaulting to "wallpaper".
    subreddit = environ.get("subreddit", "wallpaper")
    # Retrieve the path for saving wallpapers from environment variables.
    wallpaper_path = environ.get("wallpaper_path")

    # wallpaper_path is mandatory for the script to function.
    if not wallpaper_path:
        print("Error: wallpaper_path environment variable not set.")
        sys.exit(1) # Exit if the path is not provided.
    
    # Normalize the path to ensure it's in a consistent format (e.g., corrects slashes).
    wallpaper_path = normpath(wallpaper_path)

    # Define a filename template using strftime format codes.
    # Includes year, month, day, hour, minute, second, and microseconds for uniqueness.
    # Example: "20231027_153045123456"
    name_template = f"{'%Y%m%d_%H%M%S%f'}" 

    # Get the current date and time, used for generating filenames.
    current_time = datetime.datetime.now()

    # Construct the Reddit API URL.
    # Fetches the top 5 posts from the last day in JSON format.
    # Limit is 5 to reduce response size, though we only use the first post.
    url = f"https://www.reddit.com/r/{subreddit}/top/.json?&t=day&limit=5"

    # Make the GET request to the Reddit API.
    try:
        response = requests.get(
            url, 
            headers={'User-agent': 'SelfChangingWallpaper 0.1'}, # Reddit API requires a custom User-Agent.
            timeout=10 # Set a timeout for the request to prevent indefinite hanging.
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX or 5XX status codes).
    except requests.exceptions.RequestException as e:
        print(f"Error during Reddit API request to {url}: {e}")
        sys.exit(1)

    # Parse the JSON response to extract the image URL.
    # Assumes a specific structure in the JSON response from Reddit.
    # response.json()["data"]["children"][0]["data"]["url"]
    try:
        # Access the first post's URL from the JSON data.
        img_url = response.json()["data"]["children"][0]["data"]["url"]
    except (KeyError, IndexError, TypeError) as e: 
        # Handle cases where the expected JSON structure is not found or response is not JSON.
        print(f"Error: Could not parse image URL from Reddit API response. Response: {response.text}")
        sys.exit(1)

    # Download the image from the extracted URL.
    try:
        image_response = requests.get(img_url, timeout=10) # Timeout for image download.
        image_response.raise_for_status() # Check for errors during image download.
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {img_url}: {e}")
        sys.exit(1)

    # Determine the image file extension from its URL.
    # Converts URL to lowercase for case-insensitive matching.
    img_url_lower = img_url.lower()
    if ".png" in img_url_lower:
        extension = ".png"
    elif ".jpg" in img_url_lower or ".jpeg" in img_url_lower:
        extension = ".jpg"
    else:
        # If the extension is not recognized, print an error and exit.
        print(f"Image URL does not contain a recognized extension (.png, .jpg, .jpeg): {img_url}")
        sys.exit(1)
    
    # Generate the full filename for the image.
    # 1. Format the current time using the name_template to create a unique stem.
    filename_stem = current_time.strftime(name_template)
    # 2. Join the wallpaper_path, filename_stem, and determined extension.
    # normpath ensures the final path is correct for the OS.
    filename = normpath(join(wallpaper_path, filename_stem + extension))
    
    # Save the downloaded image content to the generated filename.
    # image_response.content contains the raw bytes of the image.
    save_img(filename, image_response.content)

    # Set the downloaded image as the desktop wallpaper (Windows specific).
    try:
        # SystemParametersInfoW is a Windows API function.
        # Arguments:
        #   20 (SPI_SETDESKWALLPAPER): Action to set the desktop wallpaper.
        #   0: Reserved parameter, must be zero.
        #   filename: Path to the wallpaper image file.
        #   3 (SPIF_UPDATEINIFILE | SPIF_SENDCHANGE): Update user profile and broadcast change.
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filename, 3)
        print(f"Wallpaper set to {filename}")
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # This block ensures set_wallpaper_from_reddit() is called only when the script is executed directly,
    # not when imported as a module.
    set_wallpaper_from_reddit()
