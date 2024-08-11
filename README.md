# iGEM Timelapse with Raspberry Pi 4 Model B and Camera Module 3

## Overview

This project is designed to capture a timelapse using a Raspberry Pi 4 Model B and the Camera Module 3.The system runs
on Raspberry Pi OS Lite (64-bit) and leverages the terminal multiplexer zellij for efficient terminal management.

## Network Access

The Raspberry Pi hosts its own WLAN network, allowing you to connect and SSH into the device from anywhere, even without
an external internet connection. This ensures that you can manage and monitor the timelapse setup remotely, no matter
where you are.

## Setup and Configuration

### Finding Optimal Camera Parameters

To determine the best settings for the lens position, exposure time, and ISO, use the `find_parameters.py` script. This
script allows you to interactively test and adjust these parameters until you find the optimal values for your
environment and desired output.

### Creating a Timelapse

Once you've identified the ideal camera settings using `find_parameters.py`, you should configure these settings in
the `create_timelapse.py` script by updating the respective global variables.
Additionally, the script includes global variables to control the time between each photo and the hours during which no
pictures should be taken.

## Running the Timelapse

Once the parameters are set in `create_timelapse.py`, simply run the script to start capturing images at the defined
intervals. The images will be saved with timestamps in the specified directory, and the script will automatically handle
the no-capture periods based on your configuration.
