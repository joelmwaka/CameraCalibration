import os
import cv2
import json
import argparse
import numpy as np


class CameraCalibrator:

    def __init__(self, path_images, path_results, pattern_shape, square_size):

        self.path_images = path_images
        self.path_results = path_results

        self.cb_pn_shape = pattern_shape
        self.cb_sq_size = square_size  # in mm

        self.all_calibration_images = os.listdir(self.path_images)
        self.valid_calibration_images = []

        self.h, self.w = None, None

        self.conv_size = (11, 11)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        self.image_points = []
        self.object_points = []

    def check_image(self, image):

        output_image = np.copy(image)

        img_gray = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(img_gray, self.cb_pn_shape)

        if ret:
            output_image = cv2.drawChessboardCorners(output_image, self.cb_pn_shape, corners, ret)
            h, w, _ = output_image.shape
            if self.h is None and self.w is None:
                self.h, self.w = h, w
            else:
                if h != self.h or w != self.w:
                    raise IOError("Provided calibration images have varying heights and widths!")
            return ret, output_image
        else:
            return ret, output_image

    def get_object_points(self):

        object_points = np.zeros((self.cb_pn_shape[0] * self.cb_pn_shape[1], 3), np.float32)
        object_points[:, :2] = np.mgrid[0:self.cb_pn_shape[0], 0:self.cb_pn_shape[1]].T.reshape(-1, 2)
        object_points = self.cb_sq_size * object_points

        return object_points

    def eventloop(self):

        count_valid = 0
        count_all = 0

        for fname in self.all_calibration_images:
            if fname.lower().endswith(".png") or fname.lower().endswith(".jpg"):
                fpath = os.path.join(self.path_images, fname)
                image = cv2.imread(fpath)
                ret, cb_image = self.check_image(image)

                if ret:
                    count_valid += 1
                    self.valid_calibration_images.append(fname)
                else:
                    print(f"Info: Checkerboard not found in image {fpath}!")

                count_all += 1

        print(f"Info: {count_valid}/{count_all} valid calibration image(s).")
        obj_points = self.get_object_points()

        for fname in self.valid_calibration_images:
            fpath = os.path.join(self.path_images, fname)
            image = cv2.imread(fpath)

            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(image_gray, self.cb_pn_shape)

            if ret:
                corners = cv2.cornerSubPix(image_gray, corners, self.conv_size, (-1, -1), self.criteria)

                self.image_points.append(corners)
                self.object_points.append(obj_points)

        ret, mtx, dist, _, _ = cv2.calibrateCamera(self.object_points, self.image_points, (self.w, self.h), None, None)
        print(f"Info: Calibration done!\n\tResultant RMSE: {ret}.")

        camera_calibration_results = {
            "rmse": ret,
            "camera_matrix": mtx.tolist(),
            "distortion_coefficients": dist.tolist()
        }

        json_filename = os.path.join(self.path_results, "calibration_results.json")
        with open(json_filename, "w") as file:
            json.dump(camera_calibration_results, file)

        print(f"\tInfo: Calibration results are saved in '{json_filename}'")


def main(arguments):

    path_images = arguments.path_to_images
    path_results = arguments.path_to_results
    str_ps = arguments.pattern_shape.split("x")
    pattern_shape = (int(str_ps[0]), int(str_ps[1]))
    square_size = arguments.square_size

    calibrator = CameraCalibrator(path_images=path_images, path_results=path_results,
                                  pattern_shape=pattern_shape, square_size=square_size)
    calibrator.eventloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intrinsic camera calibration.")

    parser.add_argument("-p", "--path_to_images", type=str, help="Path to folder containing images files. "
                                                                 "Images must be PNG or JPG format.")
    parser.add_argument("-r", "--path_to_results", type=str, help="Path to folder in which to save the calibration "
                                                                  "results. Results are saved in a JSON file.")
    parser.add_argument("-c", "--pattern_shape", type=str, help="Checkerboard shape 'rxc' e.g. '5x7'. Rows and "
                                                                "columns in the checkerboard.")
    parser.add_argument("-s", "--square_size", type=float, help="Checkerboard square size in millimeters.")

    args = parser.parse_args()

    main(arguments=args)
