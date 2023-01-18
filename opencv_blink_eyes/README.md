# iMarckDEV Blog Repository

Welcome to the iMarckDEV Blog Repository! This repository contains the source code for the [iMarckDEV blog site](https://www.imarck.dev), a platform dedicated to exploring cloud technologies, sharing tutorials, and providing valuable resources for developers.

## Blink Detection Script

This script is written in Python and uses several libraries to detect and count the number of blinks in a camera or a face video. The following libraries are required:

- `cv2`: OpenCV library for image and video processing.
- `dlib`: Dlib library for facial landmark detection.
- `time`: Python's built-in library for time-related functions.
- `scipy.spatial.distance`: Scipy library for calculating distances between points.
- `numpy`: NumPy library for numerical computations.

Make sure you have these libraries installed before running the script.

## Installation

1. Clone this repository to your local machine.

```batch
git clone <repository-url>
```


2. Install the required libraries using pip and the encodings of video.
```batch
pip install opencv-python dlib scipy numpy
apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
```

3. verufy than the shape_predictor_68_face_landmarks.dat where in the work dir


## Usage

1. Navigate to the project directory.
```batch
cd <dir repo>
```


2. Run the script using Python.
```batch
python blink_detection.py
```
    so, in this case the origin of the video could be a video file o the camera if in the line 36 of blink_detection.py 
    ```python
    vs = cv2.VideoCapture(0) ##change 0 by the path of the video too
    
    

3. The script will open the camera or load a face video and start detecting blinks. The blink count will be displayed on the console.

## How It Works

1. The script captures video frames from the camera or loads a face video.

2. It uses the Dlib library to detect facial landmarks on each frame.

3. The script calculates the eye aspect ratio (EAR) to determine if a blink occurs. The EAR is the ratio of the distances between the vertical eye landmarks and the distances between the horizontal eye landmarks.

4. If the EAR drops below a certain threshold, it indicates a blink.

5. The script keeps track of the blink count and displays it on the console.

![Face Image](image_face.jpg)
Image example of the output like a pic.

## Contributing

Thank you for your interest in contributing to the iMarckDEV Blog Repository. If you have any improvements or bug fixes, please feel free to submit a pull request. We appreciate your contributions!

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this code for personal or commercial purposes.

For more information, visit the [iMarckDEV blog site](https://www.imarck.dev) and explore other resources and tutorials. Happy coding!'''
