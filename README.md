# Gesture Controlled Media for Windows

Note: Only works on Windows as of January 17, 2026.

## Goal
```
build something with a camera
```

...and so I did!

## Result
"Gesture Media Control" is a Python script that enables control of your computers media via easy to remember hand gestures.

The hand gestures enable you to volume up/down, skip, go back, pause, max volume.

## Requirements
- Python 3.x
- opencv-python
- mediapipe
- pycaw
- gesture_recognizer.task ([Download Here](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task)).

### Gesture Recognizer dot Task
This is a pre-trained model that recognizes hand gestures from the camera frames captured by OpenCV. Download it and place it next to main.py.

## Actions
### 1. ***Closed_Fist***: Play/Pause Audio

![Closed_Fist](images_readme/Closed_Fist.JPG)

### 2. ***ILoveYou***: Max Volume

![ILoveYou](images_readme/ILoveYou.JPG)

### 3. ***Pointing_Up***: Next Song

![Pointing_Up](images_readme/Pointing_Up.JPG)

### 4. ***Victory***: Replay/Previous Song

![Victory](images_readme/Victory.JPG)

### 5. ***Thumb Up***: Volume Up

![Thumb_Up](images_readme/Thumb_Up.JPG)

### 6. ***Thumb Down***: Volume Down

![Thumb_Down](images_readme/Thumb_Down.JPG)