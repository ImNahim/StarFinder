import pandas as pd
from main import main

list_de_test = ['Rihanna', 'Steven Yeun', 'Alexis Bledel', 'Jack Black', 'Tom Hiddleston', 'Orlando Bloom', 'Megan Fox', 'Sarah Shahi', 'Amanda Seyfried', 'Yvonne Strahovski', 'Abbie Cornish', 'Beyoncé Knowles', 'Bryan Cranston', 'Aaron Paul', 'Ryan Gosling', 'Chris Evans', 'Tom Hardy', 'Priyanka Chopra', 'Shakira', 'Adam Levine', 'Kristen Stewart', 'Idris Elba', 'Justin Bieber', 'Emilia Clarke', 'Jake Gyllenhaal', 'Jennifer Lawrence', 'Vincent Kartheiser', 'Anna Kendrick', 'Margot Robbie']
dictionnaire = {}
print(len(list_de_test))
score_final: int=0

for item in list_de_test:
    dictionnaire[item] = 0

all_meta_data = pd.read_csv("resources/vectorisation/all_metadata_v.csv")

for test in list_de_test:
    for item in all_meta_data["name"]:
        if item == test:
            dictionnaire[item] += 1


def verifier_occurrence(data_frame, name):
    j = 0
    for i in range(5):
        instance = data_frame.iloc[i]
        nom = instance['name']
        if nom == name:
            j += 1
    print(f"{name} : {j/5}")
    global score_final
    score_final = score_final+ j/5


for item in dictionnaire.keys():
    try:
        path = "images_evaluatuion/" + item + ".jpg"
        df = main(path)
        verifier_occurrence(df, item)
    except:
        print(f"can't open {path}")
        continue


score_final = score_final/len(list_de_test)
print(f'score final = {score_final}')