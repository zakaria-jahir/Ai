from tkinter import filedialog, simpledialog
import tkinter as tk
from PIL import Image, ImageDraw
import face_recognition
import numpy as np
import os

# Function to add images and names to the known faces
def add_face():
    file_path = filedialog.askopenfilename(title="Select Image")
    if file_path:
        image = face_recognition.load_image_file(file_path)
        encodage_visage = face_recognition.face_encodings(image)[0]

        encodage_visage_connu.append(encodage_visage)

        # Use simpledialog to get the name from the user
        nom = simpledialog.askstring("Input", "Enter the name for the face:")
        nom_visage_connu.append(nom)

# Function to search and identify names based on a given image
def search_face():
    file_path = filedialog.askopenfilename(title="Select Image")
    if file_path:
        image_inconnu = face_recognition.load_image_file(file_path)
        emp_visage_inconnu = face_recognition.face_locations(image_inconnu)
        encodage_visage_inconnu = face_recognition.face_encodings(image_inconnu, emp_visage_inconnu)

        image_pil = Image.fromarray(image_inconnu)
        draw = ImageDraw.Draw(image_pil)

        for i, ((haut, droite, bas, gauche), encodage_visage) in enumerate(zip(emp_visage_inconnu, encodage_visage_inconnu)):
            corresp = face_recognition.compare_faces(encodage_visage_connu, encodage_visage)

            nom = "Inconnu"

            if encodage_visage_connu:  # Check if the list is not empty
                distances_visages = face_recognition.face_distance(encodage_visage_connu, encodage_visage)
                meilleur_indice = np.argmin(distances_visages)
                if corresp[meilleur_indice]:
                    nom = nom_visage_connu[meilleur_indice]

            draw.rectangle(((gauche, haut), (droite, bas)), outline=(0, 0, 255))
            draw.text((gauche + 6, haut - 5), nom, fill=(255, 255, 255, 255))

        # Create a unique filename based on the original filename and the index
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        output_path = f"{file_name}_detected_{i}{file_extension}"

        image_pil.save(output_path)
        print(f"Detected faces saved to: {output_path}")

# Initializations
encodage_visage_connu = []
nom_visage_connu = []

# GUI setup
root = tk.Tk()
root.title("Face Recognition App")

# Add a title label
title_label = tk.Label(root, text="Recognition Image", font=("Helvetica", 16, "bold"), fg="black")
title_label.pack()

# Buttons to add faces and search for faces
add_button = tk.Button(root, text="Add Face", command=add_face,font=("Helvetica", 14), height=2, width=15)
add_button.pack(pady=10)

search_button = tk.Button(root, text="Search Face", command=search_face,font=("Helvetica", 14), height=2, width=15)
search_button.pack(pady=10)

root.mainloop()
