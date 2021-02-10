# Ce fichier permet de charger les meta data sur les images puis les stocker sous format csv.

import scipy.io
import pandas as pd
import numpy as np

# Les meta data sont stockés dans un fichier matlab, on va utiliser scipy pour pouvoir les charger
try :
    imdbMetaLoad = scipy.io.loadmat('image_data/imdb_data/imdb.mat')
    wikiMetaLoad = scipy.io.loadmat('image_data/wiki_data/wiki.mat')
except FileNotFoundError :
    print("Fichier no trouvé, changez le path!")

# Construction des dataframes pandas
imdbData  = imdbMetaLoad["imdb"]
attributs = ["dob", "photo_taken", "full_path", "gender", "name", "face_location", "face_score", "second_face_score", "celeb_names", "celeb_id"]

# On stocke les informations dans un dictionnaire
image_info = {}

for i in range(0, len(attributs)):
    image_info[attributs[i]] = imdbData[0][0][i]


full_path = ['image_data/imdb_data/' + item for sublist in image_info['full_path'][0] for item in sublist]
nom = [item for list in image_info['name'][0] for item in list]
face_location = [item for list in image_info['face_location'][0] for item in list]
face_score = image_info['face_score'][0]
second_face_score = image_info['second_face_score'][0]

#On élimine les attributs qui nous intéresse par
image_data_final = {attributs[4]: nom, 'file_path': full_path, attributs[5]: face_location, attributs[6]: face_score, attributs[7]: second_face_score}
imdb_info = pd.DataFrame(image_data_final)

#On élimine la data corrompu
imdb_info = imdb_info[imdb_info['face_score'] != -np.inf]
# On élimine les images qui presente plus qu'un seul visage
imdb_info = imdb_info[imdb_info['second_face_score'].isna()]
imdb_info = imdb_info[imdb_info['face_score'] > 2]
#On stock les données dans un fichier csv
imdb_info.to_csv('resources/vectorisation/imdb_metadata.csv', index = False)

#####################################################################################################################################
#### Les données Wikipedia

wikiData  = wikiMetaLoad["wiki"]

# On stocke les informations dans un dictionnaire
wikip_info = {}
mtype = wikiData.dtype
wikiAttributs= list(mtype.names)


for i in range(0, len(wikiAttributs)):
    wikip_info[wikiAttributs[i]] = wikiData[0][0][i]

full_path = ['image_data/wiki_data/'+ item for sublist in wikip_info['full_path'][0] for item in sublist]
nom = [item for list in wikip_info['name'][0] for item in list]
wiki_face_location = [item for list in wikip_info['face_location'][0] for item in list]
wiki_face_score = wikip_info['face_score'][0]
wiki_second_face_score = wikip_info['second_face_score'][0]

#On élimine les attributs qui nous intéresse par
wiki_data_final = {wikiAttributs[4]: nom, 'file_path': full_path, wikiAttributs[5]: wiki_face_location, wikiAttributs[6]: wiki_face_score, wikiAttributs[7]: wiki_second_face_score}
wiki_info = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in wiki_data_final.items() ]))

#On élimine la data corrompu
wiki_info = wiki_info[wiki_info['face_score'] != -np.inf]
# On élimine les images qui presente plus qu'un seul visage
wiki_info = wiki_info[wiki_info['second_face_score'].isna()]
wiki_info = wiki_info[wiki_info['face_score'] >2]


wiki_info.to_csv('resources/vectorisation/wiki_metadata.csv', index = False)


