# StarFinder
 Final year project : Which celebrity looks like you the most?

<h3 >Dataset: </h3> 
<p>Nous avons utilisé la dataset du ETH Zürich's Computer Vision Lab https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/ , cette dataset contient 524,230 images des 100,000 célébrités  les plus populaires sur IMDB et wikipedia.</p>

<h3>Model : </h3>
<p>Nous avons utilisé un modèle FaceNet pré-entrainé pour calculer la représentation vectorielle de l'ensemble de notre dataset</p>
<p>Une implémentation Keras du modèle ainsi que l'ensemble des poids est incluse dans le dossier ressources</p>

<h3>Les algorithmes :</h3>

<p>Le fichier loadMetaData : Ce fichier permet de lire le fichier de méta-data qui contient les informations sur la dataset des célébrités, éliminer toutes les images qui n’ont pas un nom correspondant, éliminer toutes les images qui présentes plus qu’un seul visage, éliminer toutes les images avec un face-score < 2 (images flous), puis stocker le fichier sous format CSV. 
Tout cette partie est réalisée à l’aide de la librairie Pandas, cette dernière permet de manipuler efficacement les fichiers CSV, on pourrait faire des contraintes sur des colonnes pour supprimer toute les entrées qui satisfaisant pas la contrainte etc. </p>

<p>Le fichier calculVectData : Ce fichier permet d’abord de loader notre modèle pré-entrainé FaceNet, parcourir l’ensemble de nos images de célébrités et calculer leur représentation vectorielle, puis stocker le tout sous format CSV.</p>

<p>Le fichier calculVectUser : Ce fichier fait la même chose que calculVectData sauf que nous le lançons à chaque fois pour calculer le vecteur correspondant à l’image de notre utilisateur. </p>

<p>Le fichier Main : C’est le fichier qui lance tous les autres, il permet d’abord à l’utilisateur de loader son image, puis il la passe dans le réseau FaceNet pour obtenir la représentation vectorielle, puis comparer ce vecteur aux vecteurs des célébrités en calculant la distance cosinus.  </p>

<h3>L'évaluation du programme :</h3>

<p>Le fichier modelEvaluation : Dans ce fichier nous avons mis le nom de 30 célébrités qui possèdent plus que 5 sur la dataset, nous avons choisi des célébrités qui sont jeunes d’âge pour éviter toute confusion, en effet si on utilise des célébrités âgées, nous savons si leurs photos sur la dataset sont des vieilles ou des nouvelles.
Pour chacun célébrité parmi les 30, on excute notre programme pour retourner les 5 célébrités qui lui ressemble le plus, puis nous calculons un score qui égale au nombre de bonnes prédictions faites sur le nombre total de prédiction = 5. Finalement nous additionnons les scores de toutes les photos pour obtenir un score final.</p>
