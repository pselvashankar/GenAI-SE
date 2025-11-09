import psutil
import time

try:
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used_gb = round(ram.used / (1024**3), 2)
        print(f"CPU Usage: {cpu_percent}% | RAM Usage: {ram_percent}% | RAM Used: {ram_used_gb} GB")
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    # press Ctrl+C to stop the monitoring