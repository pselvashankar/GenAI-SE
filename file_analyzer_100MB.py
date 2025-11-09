import os
import sys
import time
from datetime import datetime, timedelta

# --- SIZE CONSTANTS ---
# Define the minimum file size for inclusion in the report: 100 MB in bytes
MIN_SIZE_BYTES = 100 * 1024 * 1024

# --- TIME CONSTANTS ---
# Define the age threshold: files older than this (in days) are considered "unused"
DAYS_IN_3_MONTHS = 90 
OLD_FILE_THRESHOLD_SECONDS = time.time() - (DAYS_IN_3_MONTHS * 24 * 60 * 60)

def human_readable_size(size_bytes):
    """
    Converts a file size in bytes to a human-readable format (B, KB, MB, GB).
    """
    if size_bytes is None:
        return "N/A"
    
    # Define units and their corresponding powers of 1024
    if size_bytes == 0:
        return "0 B"
    
    size = float(size_bytes)
    # The list of unit suffixes
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    
    # Calculate the appropriate unit index
    i = 0
    while size >= 1024.0 and i < len(units) - 1:
        size /= 1024.0
        i += 1
        
    return f"{size:.2f} {units[i]}"

def format_timestamp_to_date(timestamp):
    """
    Converts a Unix timestamp (seconds since epoch) to a readable date string (YYYY-MM-DD).
    """
    if timestamp is None:
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def get_files_by_size(start_dir):
    """
    Traverses a directory and its subdirectories to list all files 
    that meet BOTH the size (> 100MB) and age (> 90 days) criteria.
    """
    file_data = []
    
    # Check if the starting directory is valid
    if not os.path.isdir(start_dir):
        print(f"Error: Directory not found at path: {start_dir}", file=sys.stderr)
        return []

    print(f"\n--- Scanning directory: {start_dir} for large (> {human_readable_size(MIN_SIZE_BYTES)}) and old (> {DAYS_IN_3_MONTHS} days) files ---")

    # Use os.walk to traverse the directory tree
    for folder_path, _, file_names in os.walk(start_dir):
        for file_name in file_names:
            full_path = os.path.join(folder_path, file_name)
            
            try:
                # 1. Get size and modification time
                size_bytes = os.path.getsize(full_path)
                # We use mtime (last modification time) as a reliable proxy for "last used"
                last_modified_time = os.path.getmtime(full_path)
                
                # 2. Apply BOTH filters
                is_large = size_bytes > MIN_SIZE_BYTES
                is_old = last_modified_time < OLD_FILE_THRESHOLD_SECONDS
                
                if is_large and is_old:
                    file_data.append({
                        'name': file_name,
                        'path': full_path,
                        'size_bytes': size_bytes,
                        'last_modified_time': last_modified_time
                    })
            except OSError as e:
                # Catch potential permissions issues or files that vanish during scan
                print(f"Warning: Could not access file {full_path}. Reason: {e}", file=sys.stderr)

    # Sort the list: 'key' is the file size, 'reverse=True' means largest first (descending)
    file_data.sort(key=lambda x: x['size_bytes'], reverse=True)
    
    return file_data

def display_results(file_list):
    """
    Prints the sorted list of files in a clean, tabular format, including the last modified date.
    """
    if not file_list:
        print(f"No files found or accessible that are larger than {human_readable_size(MIN_SIZE_BYTES)} AND older than {DAYS_IN_3_MONTHS} days in the specified directory.")
        return

    print("\n--- Files Filtered by Size and Age (Largest to Smallest) ---")
    
    # Define header format - UPDATED TO INCLUDE DATE
    HEADER_FORMAT = "{:<12} | {:<10} | {:<30} | {}"
    # Adjusting the width to accommodate the new column
    LINE_WIDTH = 120 
    print("-" * LINE_WIDTH)
    print(HEADER_FORMAT.format("LAST USED", "SIZE", "FILE NAME", "PATH DETAILS"))
    print("-" * LINE_WIDTH)
    
    # Print data rows
    for file in file_list:
        readable_size = human_readable_size(file['size_bytes'])
        readable_date = format_timestamp_to_date(file['last_modified_time'])
        
        # Truncate path for cleaner display
        display_path = file['path']
        if len(display_path) > 50:
             # Show the end of the path for better context
             display_path = "..." + display_path[-47:] 
             
        print(HEADER_FORMAT.format(
            readable_date,
            readable_size,
            file['name'][:30], # Truncate file name if too long
            display_path
        ))
    
    print("-" * LINE_WIDTH)
    print(f"Note: 'LAST USED' date refers to the file's last modification time (mtime).")

if __name__ == "__main__":
    # Get the starting directory from the user
    print("Welcome to the File Size and Age Analyzer.")
    # On many systems, using '.' will scan the current directory. 
    # For a full system scan, a path like 'C:\\' (Windows) or '/' (Linux/macOS) is needed.
    start_directory = input("Enter the starting directory path (e.g., /home/user/Documents or C:\\Users\\User\\Desktop): ")
    
    # Run the process
    sorted_files = get_files_by_size(start_directory)
    
    # Display the final output
    display_results(sorted_files)