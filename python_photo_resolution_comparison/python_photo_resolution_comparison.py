# -*- coding: utf-8 -*-

import os
from PIL import Image
import json
import math
from os.path import join

# A lot of times the photo will be cropped such that it no longer conforms to a 4:3 or 16:9 standard. That's one way.
# DVD producers can also choose to show even wider ratios such as 1.85:1 and 2.39:1[1] within the 16:9 DVD frame by hard matting or adding black bars within the image itself.


class PythonPhotoResolutionComparison():

    def __init__(self, file_path):
        self._file_path = file_path
        self._json_data = dict()
        self._image = None
        self._pil_tags = dict()
        self._json_data['file_path'] = file_path

    @property
    def json(self):
        return json.dumps(self._json_data)

    def _recursive_gcd(self, a, b):
        if b == 0:
            return a
        return self._recursive_gcd(b, a % b)

    def _get_aspect_ratio(self, width, height):
        gcd = self._recursive_gcd(width, height)
        return '{0}:{1}'.format(int(width/gcd), int(height/gcd))

    def _get_megapixel(self, width, height):
        pixels = width * height
        exact = pixels
        one_million = 1000000

        if pixels > one_million:
            round_up = math.ceil(pixels / one_million) * one_million
            formatted = round_up / 1000000
            normalised = formatted
        else:
            formatted = math.ceil(one_million / pixels)
            normalised = 1.0

        return exact, formatted, normalised

    def execute(self):
        self._image = Image.open(self._file_path)
        width, height = self._image.size
        aspect_ratio = self._get_aspect_ratio(width, height)
        exactpixels, megapixel, normalised = self._get_megapixel(width, height)

        self._json_data['normalised_mega_pixels'] = normalised
        self._json_data['exact_pixels'] = exactpixels
        self._json_data['megapixel'] = megapixel
        self._json_data['aspect_ratio'] = aspect_ratio
        self._json_data['width'] = width
        self._json_data['height'] = height


        # self._json_data['is_hdv_aspect_ratio'] = height
        # self._json_data['is_square_ratio'] = height
        # self._json_data['is_tv_or_classic_pc_ratio'] = height
        # self._json_data['is_hd_video_or_us_tv'] = height



if __name__ == "__main__":

    # extractor = PythonPhotoResolutionComparison('../Resources/IMG_0829.JPG')
    # extractor.execute()
    # print(extractor.json)
    # exit()

    # directory = r'C:\code\python-photo-resolution-comparison\Resources\test_images'
    directory = r'C:\code\python-photo-resolution-comparison\Resources\more_tests'
    for filename in os.listdir(directory):
        if filename.endswith('jpg'):
            file_path = join(directory, filename)
            extractor = PythonPhotoResolutionComparison(file_path)
            extractor.execute()
            print(extractor.json)



