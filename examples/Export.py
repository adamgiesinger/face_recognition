import csv
import time


def write_csv(rows, target_file):
    with open(target_file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def get_export_file_name():
    ts = time.strftime("%Y%m%d-%H%M%S")
    return 'export_' + ts + '.csv'


def export(people_names, people_image_assignment, target_file='export.csv'):
    exportable = []

    for image in people_image_assignment:

        row = {
            'photo': image
        }

        # expect no person to be found in image
        for name in people_names:
            row[name] = 0

        # override values of person which have been recognized
        persons_recognized = people_image_assignment[image]
        for name in persons_recognized:
            row[name] = 1

        exportable.append(row)

    write_csv(exportable, target_file)


def test():

    persons = ['one', 'two', 'three', 'four']

    recognitions = {
        'a.jpg': ['one', 'two'],
        'b.jpg': [],
        'c.jpg': ['three'],
        'd.jpg': ['one', 'two', 'three']
    }

    export(persons, recognitions, get_export_file_name())


test()

