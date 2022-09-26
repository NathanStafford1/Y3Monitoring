import face_recognition
import numpy as np
from PIL import Image, ImageDraw

# Load in the sample picture
known_image = face_recognition.load_image_file("enda.png")
enda_encoding = face_recognition.face_encodings(known_image)[0]

# Load in the image with the unknown faces
unknown_image = face_recognition.load_image_file("dkit_erasmus.png")

# Find all faces and their encodings in the unknown image
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

# Convert the image to PIL format to allow is to draw on it
pil_image = Image.fromarray(unknown_image)

# Create a pillow image draw instance
draw = ImageDraw.Draw(pil_image)

# Loop through each face in the unknown image and see if the face if a match for Enda
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces([enda_encoding], face_encoding)
# Use the face that is closest
    face_distances = face_recognition.face_distance([enda_encoding], face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        draw.rectangle(((left-20, top-20), (right+20, bottom+20)), outline=(0, 255, 0), width=5)
del draw
pil_image.show()
