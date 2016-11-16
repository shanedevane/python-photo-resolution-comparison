# -*- coding: utf-8 -*-

import os
import exifread
from PIL import Image, ImageStat, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS
import json
from fractions import Fraction
from os.path import join, getsize

# A lot of times the photo will be cropped such that it no longer conforms to a 4:3 or 16:9 standard. That's one way.


class PythonPhotoResolutionComparison():

    def __init__(self, file_path):
        self._file_path = file_path
        self._json_data = dict()
        self._image = None
        self._pil_tags = dict()

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

    def execute(self):
        self._image = Image.open(self._file_path)
        width, height = self._image.size
        image_aspect_ratio = self._get_aspect_ratio(width, height)

        # self._json_data['ratio'] = ratio
        self._json_data['image_aspect_ratio'] = image_aspect_ratio
        self._json_data['width'] = width
        self._json_data['height'] = height


        # self._get_exif_data()
        # self._get_gps_data()
        # self._store_gps_data()

if __name__ == "__main__":

    extractor = PythonPhotoResolutionComparison('../Resources/IMG_0829.JPG')
    extractor.execute()
    print(extractor.json)
    exit()

    directory = r'C:\code\python-photo-resolution-comparison\Resources\test_images'
    for filename in os.listdir(directory):
        if filename.endswith('jpg'):
            file_path = join(directory, filename)
            extractor = PythonPhotoResolutionComparison(file_path)
            extractor.execute()
            print(extractor.json)



