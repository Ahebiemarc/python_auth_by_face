from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import comparer_visages, telecharger_image_dans_temp, delete_temp

app = FastAPI()

# Configuration CORS - autoriser toutes les origines (à utiliser avec précaution)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)


#modèle pour les donnée de la requete
class ImageURLs(BaseModel):
    unknown_image_url: str
    known_image_url: str


@app.post("/compare-faces")
def compare_faces(data: ImageURLs):
    # Créer un dossier temporaire pour télécharger les images
    temp_folder = "temp"
    known_image_path = telecharger_image_dans_temp(data.known_image_url, "temp/knownPerson")
    unknown_image_path = telecharger_image_dans_temp(data.unknown_image_url, "temp/unknownPerson")

    if not known_image_path or not unknown_image_path:
        raise HTTPException(status_code=400, detail="Impossible de télécharger les images")

    try:
        # Comparer les visages
        print("\ncomparaison...")
        result = comparer_visages(known_image_path, unknown_image_path)

        # Retourner la réponse booléenne
        return {"is_same_person": result}
    finally:
        # Supprimer le dossier temporaire
        delete_temp(temp_folder)

"""if __name__ == '__main__':
    # Exemple d'utilisation
    unknown_person_dir_temp = 'temp/unknownPerson'
    known_person_dir_temp = 'temp/knownPerson'
    url_image_known = 'http://localhost:5000/uploads/elector/1714752962269.jpeg'  # Remplacez par l'URL de votre image
    url_image_unknown = 'http://localhost:5000/uploads/elector/1714753948756.jpeg'  # Remplacez par l'URL de votre image

    known_p= telecharger_image_dans_temp(url_image_known, known_person_dir_temp)
    unknown_p =telecharger_image_dans_temp(url_image_unknown, unknown_person_dir_temp)

    #known_p = "temp/knownPerson/1714752962269.jpeg"
    #unknown_p = "temp/unknownPerson/1714753948756.jpeg"
    print(known_p, unknown_p)
    print("\ncomparaison...")

    r = comparer_visages(known_p, unknown_p)

    print(f"\n return : {r}")"""

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
