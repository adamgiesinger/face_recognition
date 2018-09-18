# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import os
import re
import face_recognition.api as face_recognition
import multiprocessing
import itertools
import sys
import PIL.Image
import numpy as np
from io_helpers import scan_known_people, image_files_in_folder
from Export import export, get_export_file_name
from collections import defaultdict
from multiprocessing import Manager

known_people_folder = sys.argv[1]
image_to_check = sys.argv[2]
cpus = -1 # the default value if nothing is provided as command argument
tolerance = 0.6
show_distance = False

def process_image(image_to_check, known_names, known_face_encodings, tolerance=0.6, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)
    result_list = list()

    # Scale down image if it's giant so things run a little faster
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        recognized_name = ""
        if True in result:
            for is_match, name, distance in zip(result, known_names, distances):
                if is_match:
                    recognized_name = name
        else:
            recognized_name = "unknown_person"

        result_list.append(recognized_name)

    return image_to_check, result_list

def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

    result_dictionary =  dict()
    # macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods():
        context = multiprocessing.get_context("forkserver")

    pool = context.Pool(processes=processes)

    function_parameters = zip(
        images_to_check,
        itertools.repeat(known_names),
        itertools.repeat(known_face_encodings),
        itertools.repeat(tolerance),
        itertools.repeat(show_distance)
    )

    for image_file_name, list in pool.starmap(process_image, function_parameters):
        result_dictionary[os.path.basename(image_file_name)] = list

    known_names.append("unknown_person")
    export(known_names, result_dictionary, get_export_file_name())

def main():
    if len(sys.argv) < 4:
          cpus = -1;
    known_names, known_face_encodings = scan_known_people(known_people_folder)

    if os.path.isdir(image_to_check):
        if cpus == 1:
            [process_image(image_file, known_names, known_face_encodings, tolerance, show_distance) for image_file in image_files_in_folder(image_to_check)]
        else:
            process_images_in_process_pool(image_files_in_folder(image_to_check), known_names, known_face_encodings, cpus, tolerance, show_distance)
    else:
        test_image(image_to_check, known_names, known_face_encodings, tolerance, show_distance)

if __name__ == "__main__":
    main()
