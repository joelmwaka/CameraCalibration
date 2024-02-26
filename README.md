# Camera Calibrator



### Installation

Clone this repository to your local computer.
```console
git clone https://github.com/joelmwaka/CameraCalibration.git
```

Install requirements from the provided `.txt` files.
```console
cd CameraCalibration
pip install -r requirements.txt
```


### Execution

To execute the calibrator, ensure you have calibration images captured from the camera you intend to calibrate.
Each calibration image must have a checkerboard in it.

**Note:** You can create your own checkerboard using 
[this resource](https://markhedleyjones.com/projects/calibration-checkerboard-collection).

Execute the tool as follows:
```console
python3 calibrator.py --path_to_images <PATH_TO_CALIBRATION_IMAGES> --path_to_results <PATH_TO_FOLDER_TO_SAVE_RESULTS> --pattern_shape <RxC> --square_size <SQUARE_SIZE>
```

### Output

The calibration results will be saved in a JSON file named `calibration_results.json`. This file will be saved in the
folder you provided with the argument `--path_to_results`.

The JSON file contains the following results from the calibration:

- Root Mean Square Error (RMSE), `rmse`: a metric used to evaluate the accuracy of the calibration process.
- Intrinsic Camera Matrix, `camera_matrix`: the camera calibration with information about the focal length, principal point, and skew.
- Distortion Coefficients, `distortion_coefficients`: parameters for correction of camera lens distortion.

**Note:** Explanation of the intrinsic camera calibration and the distortion coefficients can be found on the 
[OpenCV camera calibration page](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).
