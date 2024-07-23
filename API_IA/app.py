import numpy as np
import cv2 as cv
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import linear, relu, sigmoid
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.regularizers import l2
from tensorflow.keras.losses import SparseCategoricalCrossentropy
import tensorflow_hub as hub
import datetime
import easyocr
import re
from flask import Flask, request ,jsonify
from flask_cors import CORS

#Fonction necessaires-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def read_img(img):
    """
    Cette fonction convertie l'image en RGB et applique une rotation dessus si cela est nécessaire

    Args:
        img(np.array(m,n,3)) : c'est une image
    Return:
        img(np.array(m,n,3)) : image transformé
    """
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    height, width, channels = img.shape
    if(height < width):
        img = np.rot90(img, k=3)
        pass
    return img

def creation_xTrain(img):
    """
    Cette fonction normlaise l'image et le place dans un tableau numpy. Cet action est nécessaire pour adapter l'entrer du modèle en tensorflow avec numpy

    Args:
        img(np.array(m,n,3)) : l'image  à traiter
    Return:
        np.array([(m,n,3)])
    """
    x_train = []
    #normalisation de l'image
    img = img/255
    x_train.append(img)
    return np.array(x_train)


def transformation(img):
    """
    Cette fonction convertit l'image en (224,224) car c'est la taille d'image que le modèle demande

    Args:
        img(np.array(m,n,3)) : image à convertir
    Return:
        img(np.array(224,224,3)): image convèrtie
    """
    new_width =  224
    new_height = 224
    new_dimensions = (new_width, new_height)
    img_new = cv.resize(img,new_dimensions,interpolation = cv.INTER_LINEAR)
    return img_new

def traitement_image(img,coords):
    """
    Cette fonction créer une nouvelle image à partir de l'image original et les coordonnées prédit par le modèle. Normalement la nouvelle image crée est juste une partie de l'image de la facture
    qui contient les parties importantes

    Args:
        img(np.array(m,n,3)): image original de la facture
        coords(array(4,1)): les coordonnées de la partie importante(top, bottom, left, rigth) qui est encore en pour l'image en (224,224,3)

    Return:
        newImg(np.array(x,y,3)): image de la partie importante
    """
    height, width, channels = img.shape
    top = int((coords[0] * height) / 224)
    bottom = int((coords[1] * height) / 224)
    left = int((coords[2] * width) / 224)
    #Cette condition if est ajoutée parce que parfois la prédiction n'inclut pas le prix qui se situe tout au fond à droite donc il faut un peu pousser l'image à droite
    if(coords[3] + 20 <= width):
        coords[3] +=20
    rigth = int((coords[3] * width) / 224)

    newImg = img[top:bottom, left:rigth]
    return newImg

def jaccard_similarity(str1, str2):
    """
    Cette fonction permet de calculer la similarité entre deux chaines de caratères en utilisant le coefficient de similarité de Jaccard( intersection / union)

    Args:
        str1(String)
        str2(String)
    Return:
        Boolean
    """
    set1 = set(str1.lower())
    set2 = set(str2.lower())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection/ union
    seuil = 0.7
    if similarity >= seuil:
        return True
    else:
        return False


def traitement_OCR(img,reader):
    """
    Cette fonction utilise easyOCR pour transformer l'image en texte et applique quelque modification au texte obtenus

    Args:
        img(np.array(x,y,3)) : image de la partie importante
        reader(easyOCR object): lecteur de easyOCR
    Return:
        textArray(array(m,1)): contient les textes
        bboxArray(array(m,1)): contient les positions du texte sur l'image
    """
    text_facture = reader.readtext(img)
    textArray = []
    bboxArray = []
    nombreInsertion = -1
    iteration = 1
    hauteur = [10000]
    total = 'sous-total'
    for(bbox,text,prob) in text_facture:
        y = bbox[2][1]
        text_float =  text.replace(" ","")
        text_float = text_float.replace(",",".")
        try:
            test = float(text_float)
            text = str(test)
            test = False
        except:
            test = True       
        if abs(hauteur[iteration-1] - y) < 20 and test: # Si le text n'est que la suite du texte precedent et qu'il n'est pas un float
            textArray[nombreInsertion] = textArray[nombreInsertion] + " " + text
        else:
            if(jaccard_similarity(total,text)):
                break  
            else:
                textArray.append(text)
                hauteur.append(y)
                bboxArray.append(bbox)
                nombreInsertion +=1
                iteration += 1
    return textArray,bboxArray

def creation_caracteristique(textArray,bboxArray):
    """
    Cette fonction crée des caratcéristiques importantes pour chaque mots dans notre texte afin de les utiliser pour la prochaine prédiction dans le prochain modèle

    Args:
        textArray(array(m,1))
        bboxArray(array(m,1))
    Return:
        np.array(m,12)
    """
    patternNombre = r'\d+' #trouve les premiers nombres avant une lettre alphabet
    patternMaj  = r'[A-Z]'
    patternMin = r'[a-z]'
    patternSpeciaux = r'[^a-zA-Z0-9\s\(\)]'
    lenTexte = []   #
    compteNombre = []
    compteMajuscule = []
    compteMiniscule = []
    compteSpeciaux = []
    isTexte = []#
    xWidth = []#
    xWdthMinus = []
    intermediare = -1
    iteration = 0
    for bbox in bboxArray:
        if intermediare < bbox[0][0]:
            intermediare = bbox[0][0]
    for text in textArray:
        len_texte = len(text)
        clean_text = re.sub(r'[^a-zA-Z0-9]','',text)
        nombre_de_chiffres = len(re.findall(patternNombre,clean_text))
        nombre_de_maj = len(re.findall(patternMaj,text))
        nombre_de_min = len(re.findall(patternMin,text))
        nombre_de_speciau = len(re.findall(patternSpeciaux,text))
        text_float =  text.replace(" ","")
        text_float = text_float.replace(",",".")
        try:
            test = float(text_float)
            is_texte = 0
        except:
            is_texte = 1
        lenTexte.append(len_texte)
        xWidth.append(bboxArray[iteration][0][0]/intermediare)
        xWdthMinus.append(int(intermediare-bboxArray[iteration][0][0]))
        isTexte.append(is_texte)
        compteNombre.append(nombre_de_chiffres)
        compteMajuscule.append(nombre_de_maj)
        compteMiniscule.append(nombre_de_min)
        compteSpeciaux.append(nombre_de_speciau)
        iteration +=1
    x = []
    for i in range(len(xWidth)):
        if(lenTexte[i] ==0):
            lenTexte[i] = 1
        x.append([xWidth[i],xWdthMinus[i],isTexte[i],lenTexte[i],compteNombre[i],compteNombre[i]/lenTexte[i],compteMajuscule[i],compteMajuscule[i]/lenTexte[i],
              compteMiniscule[i],compteMiniscule[i]/lenTexte[i],compteSpeciaux[i],compteSpeciaux[i]/lenTexte[i]])
    return np.array(x)

def EcritureImage(img, nom):
    cv.imwrite(nom + '.jpg', img)

def triArticlePrix(textes, valeurs):
    """
    Cette fonction rérupère et sépare les articles et prix dans le textes brutes vue par l'OCR à l'aide de la prédiction du modèle

    Args:
        textes(array(m,1)): toutes les textes que contiennent la facture
        valeurs(array(m,1)): valeurs pour dire si le texte est un prix(2), un article(1) ou inutile(0)

    Return:
        articles(array(n,1))
        prix(array(v,1))
    """
    iteration = 0
    articles = []
    prix = []
    for texte in textes:
        if(valeurs[iteration] == 1):
            articles.append(texte)
        elif valeurs[iteration] == 2:
            prix.append(texte)
        iteration += 1
    return articles,prix

#Main du programe------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Chargements de nos modeles
modelImage = tf.keras.models.load_model('/site/saved_models/modelImage')
modelTexte = tf.keras.models.load_model('/site/saved_models/modelTexte')
reader = easyocr.Reader(['en','fr'])
app = Flask(__name__)
CORS(app) #Activer CORS pour toutes les routes

@app.route('/', methods = ['POST'] )
def index():
    if 'image' not in request.files:
        return jsonify(success=False, message='Pas d image')
    
    file = request.files['image']
    if file.filename == '':
        return jsonify(success=False, message='Pas d image selectionner')
    
    if file:
        #Convertir le fichier en une image compatible avec OpenCV
        fileBytes = np.frombuffer(file.read(), np.uint8)
        img = cv.imdecode(fileBytes, cv.IMREAD_COLOR)
        #2eme etape:Utiliser le premier modele pour predire la partie importante de l'image
        imgOriginal = read_img(img)
        img = transformation(imgOriginal)
        x = creation_xTrain(img)
        coords = modelImage.predict(x)
        coords = coords[0]
        imgPredit = traitement_image(imgOriginal,coords)
        #3eme etape: Utiliser easyOCR pour lire l'image
        textArray,bboxArray = traitement_OCR(imgPredit,reader)
        #4eme etape: Creation des caracteristiques
        xTrain = creation_caracteristique(textArray,bboxArray)
        #5eme etape: Prediction des articles et des prix
        yPredict = modelTexte.predict(xTrain)
        yPredict = tf.nn.softmax(yPredict)
        max = []
        for prediction in yPredict:
            y = np.argmax(prediction)
            max.append(y.tolist())
        articles,prix = triArticlePrix(textArray,max)
        response = {
            "article": articles,
            "prix":prix
        }
        return jsonify(success=True, message=response)
    
    return jsonify(success=False, message = 'Upload echouer')

if __name__ == '__main__': 
    app.run(debug=True,host='0.0.0.0', port=3000)


