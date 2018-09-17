import face_recognition
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.
# i.e. python .\recognise.py knownPeople/

pathToKnownPeopleImages = sys.argv[1] # known persons
outputFolderPath = sys.argv[2] # path where the processed image will be saved
inputImagePath = sys.argv[3] # input image with persons on it

print("Command line argument is " + inputImagePath)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

for filename in os.listdir(pathToKnownPeopleImages):
    image = face_recognition.load_image_file(pathToKnownPeopleImages + filename)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    file_name = os.path.splitext(filename)[0]
    known_face_names.append(file_name)


# Load an image with an unknown face
unknown_image = face_recognition.load_image_file(inputImagePath)

# Find all the faces and face encodings in the unknown image
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

# Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
# See http://pillow.readthedocs.io/ for more about PIL/Pillow
pil_image = Image.fromarray(unknown_image)
# Create a Pillow ImageDraw Draw instance to draw with
draw = ImageDraw.Draw(pil_image)

# Loop through each face found in the unknown image
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown"
    font_type = ImageFont.truetype("arial.ttf", 40)
    # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    text_width, text_height = draw.textsize(name, font=font_type)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255), font=font_type)


# Remove the drawing library from memory as per the Pillow docs
del draw

# Display the resulting image
# pil_image.show()

# You can also save a copy of the new image to disk if you want by uncommenting this line
base=os.path.basename(inputImagePath)
print(base)
pil_image.save(outputFolderPath + base)
# os.path.splitext(imageFileName)[0]
