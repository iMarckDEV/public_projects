# iMarckDEV Blog Repository

Welcome to the iMarckDEV Blog Repository! This repository contains the source code for the [iMarckDEV blog site](https://www.imarck.dev), a platform dedicated to exploring cloud technologies, sharing tutorials, and providing valuable resources for developers.

## Blink Detection Script

Well in this case i'll go to create a image in ECR, to deploy  a lambda, this lambda will use the image in ECR and this image using ubuntu and Docker will proces a face video located in S3 bucket, in the file comands_input_example.txt there's a json to test the lambda.

This script is written in Python and uses several libraries to detect and count the number of blinks in a camera or a face video. The following libraries are required:

- `cv2`: OpenCV library for image and video processing.
- `dlib`: Dlib library for facial landmark detection.
- `time`: Python's built-in library for time-related functions.
- `scipy.spatial.distance`: Scipy library for calculating distances between points.
- `numpy`: NumPy library for numerical computations.

Make sure you have these libraries installed before running the script.

## Dcokerfile

1. uses the OS ubuntu:22.04 

2. This image includes anothers libs because in local i used it, but you can detele them or use it for another proyect.

```batch
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install pillow
RUN pip install dlib
RUN pip install scipy
```

3. In the docuemntation of AWS lambda there use the entrypoint like this:
```batch
ENTRYPOINT [ "/usr/bin/python3", "-m", "awslambdaric" ]
```

## The Lambda

1. the files name is:
```batch
app_vid
```
2. The triggers
the lambda can use a s3 event that's why use 
```python
event["Records"] #....
```
Or can use a json directly in the test like:
```json
{
  "bucket": "data-inputs-opencv-tmps",
  "obj_key": "blink.mpeg"
}

```

3. The video used to test got this specs:

MPEG video (video/mpeg)
15seg
39,5 MB (39.545.706 bytes)
it's HD
and only contais a face with the blink eyes.


![Face Image](image_face.jpg)
Image example of the output like a pic.

## Contributing

Thank you for your interest in contributing to the iMarckDEV Blog Repository. If you have any improvements or bug fixes, please feel free to submit a pull request. We appreciate your contributions!

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this code for personal or commercial purposes.

For more information, visit the [iMarckDEV blog site](https://www.imarck.dev) and explore other resources and tutorials. Happy coding!'''
