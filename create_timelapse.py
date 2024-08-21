import time
from datetime import datetime, timedelta

from libcamera import controls
from picamera2 import Picamera2

# Global variables for the interval, distance, exposure, ISO, and no-capture time range
INTERVAL_MINUTES = 15

DISTANCE_METERS = 0.5
PICTURE_COUNT = 9
PICTURE_STEP_METERS = 0.02

EXPOSURE_MICROSECONDS = 50000
ISO_VALUE = 200

NO_CAPTURE_START_HOUR = "21:00"
NO_CAPTURE_END_HOUR = "05:00"


def is_within_no_capture_time():
    now = datetime.now().time()
    start = datetime.strptime(NO_CAPTURE_START_HOUR, "%H:%M").time()
    end = datetime.strptime(NO_CAPTURE_END_HOUR, "%H:%M").time()

    if start < end:  # Non-overnight period
        return start <= now < end
    else:  # Overnight period
        return start <= now or now < end


def update_lens_position(picam2, distance):
    pos = 1.0 / distance
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": pos})
    print(f"Lens position set to: {pos} for distance: {distance} meters")


def update_exposure_time(picam2, exposure):
    picam2.set_controls({"ExposureTime": exposure})
    print(f"Exposure time set to: {exposure} microseconds")


def update_iso(picam2, iso):
    picam2.set_controls({"AnalogueGain": iso / 100.0})
    print(f"ISO set to: {iso}")


def take_picture(picam2, first_capture_time):
    if is_within_no_capture_time():
        print("Skipping picture: within no-capture time period.")
        return

    now = datetime.now()
    minutes = int((now - first_capture_time).total_seconds() / 60.0)
    base_filename = now.strftime(f"/home/igem/Pictures/{minutes:04d}_%Y-%m-%d_%H-%M")

    for i in range(PICTURE_COUNT):
        filename = f"{base_filename}_{i:02d}.jpg"
        update_lens_position(picam2, DISTANCES[i])
        picam2.capture_file(filename)
    print(f"{PICTURE_COUNT} pictures taken and saved as {base_filename}")


def get_next_capture_time(interval):
    now = datetime.now()
    # Calculate the next interval
    next_minute = (now.minute // interval + 1) * interval
    if next_minute >= 60:
        next_minute = 0
        next_hour = now.hour + 1
    else:
        next_hour = now.hour
    next_capture_time = now.replace(minute=next_minute, second=0, microsecond=0, hour=next_hour)
    return next_capture_time


# Initialize the camera
picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)
picam2.start()

# Set additional global variables
CENTER_DISTANCE = DISTANCE_METERS if PICTURE_COUNT % 2 == 1 else DISTANCE_METERS + 0.5 * PICTURE_STEP_METERS
DISTANCES = [CENTER_DISTANCE + PICTURE_STEP_METERS * i
             for i in range(-(PICTURE_COUNT // 2), PICTURE_COUNT - (PICTURE_COUNT // 2))]

# Update the camera settings based on the global variables
update_lens_position(picam2, CENTER_DISTANCE)
update_exposure_time(picam2, EXPOSURE_MICROSECONDS)
update_iso(picam2, ISO_VALUE)

# Calculate the first capture time
first_capture_time = get_next_capture_time(INTERVAL_MINUTES)
next_capture_time = first_capture_time

try:
    while True:
        now = datetime.now()
        if now >= next_capture_time:
            take_picture(picam2, first_capture_time)
            # Schedule the next capture based on the global interval
            next_capture_time += timedelta(minutes=INTERVAL_MINUTES)

        # Sleep until the next scheduled capture time
        time_to_sleep = (next_capture_time - datetime.now()).total_seconds()
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

finally:
    picam2.stop()
    picam2.close()
