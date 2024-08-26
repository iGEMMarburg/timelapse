from libcamera import controls
from picamera2 import Picamera2, Preview

DEFAULT_DISTANCE_METERS = 0.5
DEFAULT_EXPOSURE_MICROSECONDS = 50000
DEFAULT_ISO_VALUE = 200

# Initialize the camera
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
capture_config = picam2.create_still_configuration()
picam2.configure(preview_config)
picam2.start_preview(Preview.QT)
picam2.start()

# Initialize the current settings
current_distance = None
current_exposure = None
current_iso = None


# Function to update the lens position based on the distance
def update_lens_position(distance):
    global current_distance
    current_distance = distance
    pos = 1.0 / distance
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": pos})
    print(f"Lens position set to: {pos} for distance: {distance} meters")


# Function to update the exposure time in microseconds
def update_exposure_time(exposure):
    global current_exposure
    current_exposure = exposure
    picam2.set_controls({"ExposureTime": exposure})
    print(f"Exposure time set to: {exposure} microseconds")


# Function to update the ISO value
def update_iso(iso):
    global current_iso
    current_iso = iso
    picam2.set_controls({"AnalogueGain": iso / 100.0})
    print(f"ISO set to: {iso}")


# Function to take a picture using the capture configuration
def take_picture(filename="capture.png"):
    picam2.switch_mode_and_capture_file(capture_config, filename)
    print(f"Picture taken and saved as {filename}")


update_lens_position(DEFAULT_DISTANCE_METERS)
update_exposure_time(DEFAULT_EXPOSURE_MICROSECONDS)
update_iso(DEFAULT_ISO_VALUE)

# Main loop to get user input
try:
    while True:
        user_input = input(
            "Enter 'd #distance', 'e #exposure' in microseconds, 'i #ISO', 't' to take a picture, 'p' to print current settings, or 'exit' to quit: ")

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "t":
            take_picture()
        elif user_input.lower() == "p":
            print(
                f"Current settings: Distance = {current_distance if current_distance is not None else 'Not set'} meters, Exposure = {current_exposure if current_exposure is not None else 'Not set'} microseconds, ISO = {current_iso if current_iso is not None else 'Not set'}")
        elif user_input.lower().startswith("d "):
            try:
                distance = float(user_input.split()[1])
                if distance <= 0:
                    print("Please enter a positive value for distance.")
                else:
                    update_lens_position(distance)
            except (ValueError, IndexError):
                print("Invalid input. Please enter a numerical value for distance in the format 'd #number'.")
        elif user_input.lower().startswith("e "):
            try:
                exposure = int(user_input.split()[1])
                if exposure <= 0:
                    print("Please enter a positive value for exposure time.")
                else:
                    update_exposure_time(exposure)
            except (ValueError, IndexError):
                print("Invalid input. Please enter a numerical value for exposure time in the format 'e #number'.")
        elif user_input.lower().startswith("i "):
            try:
                iso = int(user_input.split()[1])
                if iso <= 0:
                    print("Please enter a positive value for ISO.")
                else:
                    update_iso(iso)
            except (ValueError, IndexError):
                print("Invalid input. Please enter a numerical value for ISO in the format 'i #number'.")
        else:
            print("Invalid command. Please use 'd #distance', 'e #exposure', 'i #ISO', 't', 'p', or 'exit'.")
finally:
    picam2.stop_preview()
    picam2.close()
