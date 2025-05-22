# Self Changing Wallpaper

This project downloads the top daily image from a specified subreddit using the Reddit API and sets it as your desktop wallpaper.

## Features

- Fetches the top image from a subreddit (defaults to "wallpaper").
- Saves images with a unique timestamp-based filename (e.g., `YYYYMMDD_HHMMSSffffff.ext`) to prevent collisions.
- Sets the downloaded image as the desktop wallpaper (Windows only).
- Improved error handling for network issues, API problems, and file operations.

## Setup

1.  **Prerequisites:**
    *   Python 3.6 or newer. You can download it from the [official Python website](https://www.python.org/downloads/).
    *   `pip` (Python package installer), which usually comes with Python.

2.  **Download/Clone:**
    *   Download and unzip the repository, or clone it using Git:
        ```bash
        git clone <repository_url>
        cd <repository_directory>
        ```

3.  **Install Dependencies:**
    *   Install the required Python modules using `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure Environment Variables:**
    *   Create a `.env` file in the same directory as the script (`main.py`).
    *   Add the following variables to the `.env` file:

        ```env
        wallpaper_path="C:/Users/YourUser/Pictures/Wallpapers/"
        # subreddit="aww" # Optional: defaults to "wallpaper" if not specified
        ```

    *   **`wallpaper_path` (Mandatory):**
        *   This is the full path to the directory where downloaded wallpapers will be saved.
        *   **You must create this folder if it doesn't exist.**
        *   Example for Windows: `C:/Users/YourUser/Pictures/Wallpapers/`
        *   Example for Linux/macOS: `/home/YourUser/Pictures/Wallpapers/`
    *   **`subreddit` (Optional):**
        *   The name of the subreddit you want to fetch images from.
        *   If not specified, it defaults to `wallpaper`.
        *   Do not include `/r/` in the name (e.g., use `pics`, not `/r/pics`).

5.  **Filename Convention:**
    *   Images are saved with a filename format like `YYYYMMDD_HHMMSSffffff.ext` (e.g., `20231027_153045123456.jpg`). The microsecond precision ensures that filenames are unique, preventing accidental overwrites if the script runs multiple times a day.

6.  **Schedule Execution (Optional):**
    *   Use Task Scheduler (Windows), cron (Linux/macOS), or a similar tool to run `main.py` automatically at your desired frequency (e.g., daily).

7.  **Folder Maintenance:**
    *   While unique filenames prevent overwriting, images will accumulate in your `wallpaper_path` directory. You may want to periodically clean out old images to save disk space.

8.  **Run:**
    *   You can run the script manually:
        ```bash
        python main.py
        ```

## Error Handling

The script includes error handling for common issues:

-   **Network Problems:** Catches errors during requests to the Reddit API or when downloading images (e.g., connection timeouts, DNS failures).
-   **API Errors:** Handles non-200 HTTP status codes from Reddit (e.g., subreddit not found, server errors) and issues with parsing the API response (e.g., unexpected JSON structure).
-   **Image Issues:** Checks for valid image extensions (.png, .jpg, .jpeg) in the URL. If an unrecognized or missing extension is found, the script will report an error.
-   **File System Errors:** Manages potential problems when saving the image file (e.g., invalid path, permissions issues).
-   **Wallpaper Setting Errors:** Catches errors that might occur when trying to set the wallpaper (Windows-specific).

In case of an error, the script will print an informative message to the console and attempt to exit gracefully.

## Dependencies and Limitations

-   **Reddit API:**
    *   This script relies on the public Reddit API to fetch image information. Changes to the API's structure, availability, or terms of service by Reddit could affect the script's functionality.
    *   While the script currently makes very few requests (one API call and one image download per run), Reddit does have rate limits. If you modify the script to make requests more frequently, you might encounter these limits.
-   **Platform:**
    *   The wallpaper setting functionality (`ctypes.windll.user32.SystemParametersInfoW`) is specific to **Windows**. It will not work on Linux or macOS without modification.
-   **Image Content:**
    *   The script fetches the top post of the day from the chosen subreddit. The content, type, and resolution of the image are determined by what is posted on Reddit.

## Contributing

If you encounter a problem or have a suggestion, please create an issue on the project's repository.

Use code with caution.
