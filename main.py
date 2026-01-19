import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import keyboard
import time
import platform
import subprocess

system = platform.system()

"""
Issues after testing:

- My face is not my hand, nor is it a thumb_down or a pointing_up
- WSL was being a pain (normal), but trying to make cross-platform so I can install anywhere and utilize!
    can also just add the 5 lines if I ever want to use this anywhere else.
    Specificially I want to use it on my raspberry pi which I hope to addon to my car
    as a media player, OBD reader, etc. Of course, it could utilize hotspot networks for internet
    access and upload information or live stream stuff, idk man, anything.

    Just need to make sure it has a small power supply for turning off the car.

    We can likely signal that the car is off by receiving no response or a certain response from OBD,
    And then we can engage in a shutdown as to not corrupt the raspberry pis memory.
    This shutdown will be powered by the battery.

    The PI does not come with a BAT port, but the kit that I bought for a 4.5 inch
    screen and oled screen and camera, DOES!

    So this will all be possible. Hopefully the pi doesn't take too much energy to run.

"""

try:
    import pulsectl
except ImportError:
    print("Failed to import pulsectl.")

try:
    from pycaw.pycaw import AudioUtilities
except ImportError:
    print("Failed to import pycaw.")

def set_volume(volume_level):
    if system == 'Darwin':
        subprocess.run()

    elif system == 'Linux':
        print("awesome")

    elif system == 'Windows':
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        volume.SetMasterVolumeLevelScalar(volume_level, None)

def get_volume():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume
    return volume.GetMasterVolumeLevelScalar()

# Track last execution time for each gesture
last_gesture_time = {}
COOLDOWN_SECONDS = 2.0  # Wait 1 second between same gesture calls

def handle_gesture(gesture_name):
    current_time = time.time()
    
    current_vol = get_volume()

    # Place outside of timing because 2.0 seconds is too slow for volume up/down
    match gesture_name:
        case "Thumb_Up":
            set_volume(min(1.0, current_vol + 0.1))
            print("Volume up")
        case "Thumb_Down":
            set_volume(max(0.0, current_vol - 0.1))
            print("Volume down")

    # Check if gesture is on cooldown
    if gesture_name in last_gesture_time:
        if current_time - last_gesture_time[gesture_name] < COOLDOWN_SECONDS:
            return  # Skip if called too recently
    
    # Update last execution time
    last_gesture_time[gesture_name] = current_time
    
    """
    case "Open_Palm":
        # Not working
        print("wow")
    """

    match gesture_name:
        case "Closed_Fist":
            keyboard.press_and_release('play/pause media')
            print("Play/Pause")
        case "Victory":
            keyboard.press_and_release('previous track')
            print("Previous track")
        case "Pointing_Up":
            keyboard.press_and_release('next track')
            print("Next track")
        case "ILoveYou":
            set_volume(1.0)
            print("MAX Volume")
        case _:
            pass

def main():
    # Download gesture_recognizer.task from:
    # https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task
    
    base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    cap = cv2.VideoCapture(0)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Convert to MediaPipe image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Recognize gestures
        recognition_result = recognizer.recognize_for_video(mp_image, frame_count)
        
        # Handle detected gestures
        if recognition_result.gestures:
            gesture = recognition_result.gestures[0][0]
            gesture_name = gesture.category_name
            confidence = gesture.score
            
            if confidence > 0.7:  # Only act on confident detections
                handle_gesture(gesture_name)
                cv2.putText(frame, f'{gesture_name} ({confidence:.2f})', 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show current volume
        current_vol = get_volume()
        cv2.putText(frame, f'Volume: {int(current_vol * 100)}%', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow('Gesture Media Control', frame)
        cv2.waitKey(1)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()