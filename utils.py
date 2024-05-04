import os
#import subprocess
import requests
import face_recognition
#from test import test
import shutil


def comparer_visages(known_person, unknown_person):
    # temporaire folder
    temp_folder = "temp"

    #img_unknown = unknown_person.split("\\")[-1]

    # Charger les images à partir des chemins donnés
    kn_person = face_recognition.load_image_file(known_person)
    #print(kn_person)
    unk_person = face_recognition.load_image_file(unknown_person)

    # Obtenir les encodages des visages pour chaque image
    known_face_encoding = face_recognition.face_encodings(kn_person)
    unknown_face_encoding = face_recognition.face_encodings(unk_person)

    if len(unknown_face_encoding) == 0 or len(known_face_encoding) == 0:
        print('no_persons_found')
        #delete_temp(temp_folder)
        return False
    else:
        unknown_face_encoding = unknown_face_encoding[0]
        #print(unknown_face_encoding)
        known_face_encoding = known_face_encoding[0]

    # Comparer les encodages pour voir s'ils représentent la même personne
    result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)[0]
    #print(result)

    # Déterminer le résultat
    if result:
        print("Les deux images représentent la même personne.")
        # Supprimer le dossier "temp" après la comparaison
        delete_temp(temp_folder)
        return True
    else:
        print("Les deux images représentent des personnes différentes.")
        # Supprimer le dossier "temp" après la comparaison
        delete_temp(temp_folder)
        return False



def telecharger_image_dans_temp(url_image, dossier_relatif="temp/unknownPerson"):
    # Créer le chemin absolu du dossier relatif
    chemin_dossier = os.path.join(os.getcwd(), dossier_relatif)

    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)

    # Récupérer le nom du fichier à partir de l'URL
    nom_fichier = url_image.split("/")[-1]

    # Chemin complet pour l'enregistrement du fichier
    chemin_fichier = os.path.join(chemin_dossier, nom_fichier)

    # Télécharger l'image
    print('téléchargement...')
    response = requests.get(url_image)

    if response.status_code == 200:
        # Enregistrer l'image dans le dossier
        with open(chemin_fichier, 'wb') as f:
            f.write(response.content)
        print(f"Image téléchargée avec succès : {chemin_fichier}")
        # Retourner le chemin relatif
        chemin_relatif = os.path.relpath(chemin_fichier)
        return chemin_relatif
    else:
        print(f"Erreur lors du téléchargement de l'image. Statut : {response.status_code}")
        return None


def delete_temp(temp_folder):
    if os.path.exists(temp_folder):
        try:
            shutil.rmtree(temp_folder)
            print(f"\nLe dossier '{temp_folder}' a été supprimé avec succès.")
        except Exception as e:
            print(f"\nErreur lors de la suppression du dossier '{temp_folder}': {e}")
    else:
        print(f"Le dossier '{temp_folder}' n'existe pas.")
