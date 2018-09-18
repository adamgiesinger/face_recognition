### Dependencies

  python 3.7
  
  dlib:  
  https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf

  python face_recognition lib:  
  https://github.com/ageitgey/face_recognition

  opencv:  
  https://medium.com/@nuwanprabhath/installing-opencv-in-macos-high-sierra-for-python-3-89c79f0a246a  
  (`brew install opencv` is probably sufficient)


### Requirements

load images in directory with labels  
 * important: one person per image  

constantly load images from web cam  
 * in intervals of 10s for example  

for every new image from web cam:  
 * try to identify all persons that were defined in A  
 * blurr unknown person  
 * temporary store images in both versions: with blurr and without  
 * display blurred version on screen  
 * update csv file


exported csv:
```
  filename, personA, personB, personC, ... , personN
  1.jpg   ,       1,       0,       0, ... ,       0       ### person a was recognized in image with name 1.jpg
  2.jpg   ,       1,       1,       0, ... ,       0       ### persons a and b were recognized in image with name 2.jpg
  3.jpg   ,       1,       0,       1, ... ,       0       ### persons a and c were recognized in image with name 3.jpg
```

### further considerations:

live demo at party:
 * demonstrate blurr feature

people will register in the afternoon
 * take photo + name file respectively

in the eventing we will take/collect photos
 * just store them - no worries

in post processing:
 * use images of registered people and the photos taken during the party

in presentation:
 * assure we do not show anybody who has not registered

 
 
### cli scripts

#### recognize_single_image.py

This script recognizes people on a given image, draws border around the faces and puts a name underneath it. If it cannot recognize it will write "Unknown".

For example:
`python .\recognize_single_image.py knownPeopleFolderPath\ outputFolderPath\ inputImagePath`

 - `knownPeopleFolderPath` is a path to a folder with known people images. These should be images with a single person on it. The name of the image file will be used as a name of the person.
 - `outputFolderPath` is a path to a folder where processed image will be saved.
 - `inputImagePath` is the path to the image in which we want to recognize people.

#### live_face_recognition.py
This script recognizes people on the live video stream. It uses folder with known people images and if it cannot recognize someone it will blur persons face.

For example:
`python .\live_face_recognition.py knownPeopleFolderPath\ 1`

 - `knownPeopleFolderPath` is a path to a folder with known people images. These should be images with a single person on it. The name of the image file will be used as a name of the person.
 - `1` is an index of the camera device. 0 represents integrated web camera.
 
#### io_helpers.py
This script contains two helper methods for reading image files from a certain folder and creating the data which is needed in the face recognition scripts. This is currently used only in `batch_recognize.py` script.

 - `scan_known_people(known_people_folder)` function has one parameter, path to a known people images and it returns two arrays, `known_face_names` which represents the string array with the names of the people on the images and `known_face_encodings` which represents image encodings objects which are being used by dlib face recognition algorithms.
 
 For example:
 `known_face_names, known_face_encodings = scan_known_people(pathToKnownPeopleImages)`

 - `image_files_in_folder(folder)` function has one parameter, path to a folder whch contains images. What this function does is that it returns an string array where each element represents folder name and the name of an image from that folder concatenated.

#### batch_recognize_single_threaded.py
This script recognizes people from images in a batch and then exports the results in to a csv file. It uses `Export.py` export function for that. It uses folder with known people images and recognize people on the images in the `inputImagesFolderPath` folder. In the end it exports the results into .csv file. It does everything in a single thread.

For example:
`python .\batch_recognize.py knownPeopleFolderPath\ inputImagesFolderPath\`

 - `knownPeopleFolderPath` is a path to a folder with known people images. These should be images with a single person on it. The name of the image file will be used as a name of the person.
 - `inputImagesFolderPath` is a path to a folder with images in which we want to recognize people.

#### batch_recognize_multi_threaded.py
This script recognizes people from images in a batch and then exports the results in to a csv file. It uses `Export.py` export function for that. It uses folder with known people images and recognize people on the images in the `inputImagesFolderPath` folder. In the end it exports the results into .csv file. It uses as much cpu cores as user defines it, if it's not explicitly defined it will use all available cpu cores.

For example:
`python .\batch_recognize_multi_threaded.py knownPeopleFolderPath\ inputImagesFolderPath\`
or
`python .\batch_recognize_multi_threaded.py knownPeopleFolderPath\ inputImagesFolderPath\ 4`
if we want it to use 4 cpu cores for processing

 - `knownPeopleFolderPath` is a path to a folder with known people images. These should be images with a single person on it. The name of the image file will be used as a name of the person.
 - `inputImagesFolderPath` is a path to a folder with images in which we want to recognize people.
 - `4` is number of cpu cores which will be utilized during image recognition process