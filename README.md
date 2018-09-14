Dependencies

  python 3.7
  
  dlib: 
  https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf

  python face_recognition lib:
  https://github.com/ageitgey/face_recognition

  opencv
  https://medium.com/@nuwanprabhath/installing-opencv-in-macos-high-sierra-for-python-3-89c79f0a246a
  (`brew install opencv` is probably sufficient)






Requirements

  A:
  load images in directory with labels
    -> important: one person per image

  constantly load images from web cam
    -> in intervals of 10s for example

  for every new image from web cam:
    -> try to identify all persons that were defined in A
    -> blurr unknown person
    -> temporary store images in both versions: with blurr and without
    -> display blurred version on screen
    -> update csv file


  csv:

  filename, personA, personB, personC, ... , personN
  1.jpg   ,       1,       0,       0, ... ,       0       ### person a was recognized in image with name 1.jpg
  2.jpg   ,       1,       1,       0, ... ,       0       ### persons a and b were recognized in image with name 2.jpg
  3.jpg   ,       1,       0,       1, ... ,       0       ### persons a and c were recognized in image with name 3.jpg


  further considerations:

    live demo at party:
      -> demonstrate blurr feature
    
    people will register in the afternoon
      -> take photo + name file respectively
    
    in the eventing we will take/collect photos
      -> just store them - no worries
    
    in post processing:
      -> use images of registered people and the photos taken during the party

    in presentation:
      -> assure we do not show anybody who has not registered
