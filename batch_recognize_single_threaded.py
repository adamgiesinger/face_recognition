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

known_people_folder = sys.argv[1]
image_to_check = sys.argv[2]
cpus = 1# int(sys.argv[3])
tolerance = 0.6
show_distance = False
people_image_assignment = defaultdict(list)

def add_to_dictionary(filename, name):
    image_file_name = os.path.basename(filename)
    if(image_file_name not in people_image_assignment):
        people_image_assignment[image_file_name] = list()
    people_image_assignment[image_file_name].append(name)
    print("adding to dictionary : {},{}".format(image_file_name, name))

def test_image(image_to_check, known_names, known_face_encodings, tolerance=0.6, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        if True in result:
            [add_to_dictionary(image_to_check, name) for is_match, name, distance in zip(result, known_names, distances) if is_match]
        else:
            add_to_dictionary(image_to_check, "unknown_person")

    # if not unknown_encodings:
        # print out fact that no faces were found in image
        # add_to_dictionary(image_to_check, "")

def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

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

    pool.starmap(test_image, function_parameters)

#@click.command()
#@click.argument('known_people_folder')
#@click.argument('image_to_check')
#@click.option('--cpus', default=1, help='number of CPU cores to use in parallel (can speed up processing lots of images). -1 means "use all in system"')
#@click.option('--tolerance', default=0.6, help='Tolerance for face comparisons. Default is 0.6. Lower this if you get multiple matches for the same person.')
#@click.option('--show-distance', default=False, type=bool, help='Output face distance. Useful for tweaking tolerance setting.')

def main():
    known_names, known_face_encodings = scan_known_people(known_people_folder)

    if os.path.isdir(image_to_check):
        if cpus == 1:
            [test_image(image_file, known_names, known_face_encodings, tolerance, show_distance) for image_file in image_files_in_folder(image_to_check)]
        else:
            process_images_in_process_pool(image_files_in_folder(image_to_check), known_names, known_face_encodings, cpus, tolerance, show_distance)
    else:
        test_image(image_to_check, known_names, known_face_encodings, tolerance, show_distance)

    print(people_image_assignment)
    known_names.append("unknown_person")
    export(known_names, people_image_assignment, get_export_file_name())

if __name__ == "__main__":
    main()
