#!/usr/bin/env python
# coding: utf-8

# ## App SmartFace

# #### Objetivo: Construir uma aplicação que utiliza um dos serviços de Inteligência Artificial do Azure chamado Face Recoigner. Apos submeter uma foto no app de qualquer pessoa, o app reconhecer o rosto desenhando um retângulo ao redor da face
# #### Esse app foi construir para testar os conhecimentos adquiridos na certificação AI 900 da Microsoft e não deve ser utilizado de forma comercial.

# Passo 1 - Instalacao dos pacotes
#!pip install --upgrade azure-cognitiveservices-vision-face
#!pip install --upgrade pip setuptools wheel
#!pip install ecapture
#!pip install pygrabber==0.1


# Passo 2 - Importacao dos pacotes
import streamlit as st
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
#from python_code import faces
import os
import io
import random as rd
from io import BytesIO
from PIL import Image, ImageDraw
import pygame
import pygame.camera
from cv2 import *

#from pygrabber.dshow_graph import FilterGraph
#import numpy as np
#from matplotlib.image import imsave
#import ecapture as ec
import pathlib

# Passo 6 - Funcoes uteis
# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return ((left, top), (right, bottom))

def drawFaceRectangles(image_path,detected_faces) :
    # Download the image from the url
    # response = requests.get(single_face_image_url)
    # img = Image.open(BytesIO(image_path))
    img = Image.open(image_path)
    
    # For each face returned use the face rectangle and draw a red box.
    print('Desenhando os retângulos ao redor das faces')
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')
    # Mostrando a imagem
    img.show()
    img.close()

# Passo 6 - Detect faces
def analisarImagem(image_stream,image_path):
    # Chamar a conexao
    # Passo 3 - Chaves para autenticar no servico criado anteriormente (Cognitive Service).
    #chaveEndpoint = 'https://appsmartface.cognitiveservices.azure.com/'
    chaveEndpoint = 'https://servicoscognitivosdataminutes.cognitiveservices.azure.com/'
    chaveCliente = '1d8f8d3740424f68b053547fa23c0848'
    #chaveCliente = '9c60be189da54ba390038760f03e2ec3'

    # Passo 4 - Consumo da API.
    # Passo 5 - Criando classe FaceClient 
    face_client = FaceClient(chaveEndpoint, CognitiveServicesCredentials(chaveCliente))

    try:
        detected_faces = face_client.face.detect_with_stream(image = image_stream)
    #except APIErrorException or NewConnectionError:
    except Exception:
        st.write('Erro! Houve erro ao contratar a API')
    else:
        if not detected_faces:
            st.info('Nenhuma face encontrada na foto submetida')
            #raise Exception('Nenhuma face encontrada na foto submetida')
        else:
            print('Faces Encontradas')
            for face in detected_faces: 
                print('Face ID ' + face.face_id)
            drawFaceRectangles(image_path,detected_faces)  


def showExample():
    listExamples = ['teste.png']
    try:
        image_path = os.path.join('faces',rd.choice(listExamples))
        image_stream = open(image_path, "rb")
    except FileNotFoundError:
        st.error('Erro! Imagem nao foi carregada para analisar')
    else:
        analisarImagem(image_stream,image_path)



def callApiAzure(imagem):
    try:
        # Escreva ela no diretorio faces e leia de la
        #image_path = os.path.join('faces',imagem.name)
        # De fora da pasta 
        #st.write(pathlib.Path(__file__).parent.absolute())
        #os.chdir("faces")
        caminhoAbsoluto = os.path.abspath(imagem.name)
        st.write(caminhoAbsoluto)
        st.write(type(imagem))
        #image_path = os.path.join(imagem.name)
        #st.write(caminhoAbsoluto)
        #st.write(image_path)
        #st.write(os.path.posixpath)
        #image_path = os.path.append('faces')
        image_path = os.path.join(imagem.name)
        image_stream = open(image_path, "rb")
    except FileNotFoundError:
        st.error('Erro! Imagem nao foi carregada para analisar')
    else:
        # image_paths
        analisarImagem(image_stream,image_path)


def acionarCamera():
    flagCaptura = False
    st.info("Quando a câmera abrir, use a tecla ESPAÇO para tirar foto.")
    cam = cv2.VideoCapture(-1)
    st.write(cam)
    if not cam.isOpened():
        st.error('Erro ao conectar na Camera!')
        raise IOError("Cannot open webcam")
    else:
        cv2.namedWindow("prévia")
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Falha para capturar a foto")
                break
            cv2.imshow("prévia", frame)
            k = cv2.waitKey(1)
            if k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                flagCaptura = True
                # Fechar a camera
                cam.release()
                cv2.destroyAllWindows()
                del(cam)
                break
        #cam.release()
        #cv2.destroyAllWindows()

    # # Se realmente tirou a foto, então analise a mesma
    # if(flagCaptura == True):
    #     image_path = os.path.abspath(img_name)
    #     try:
    #          image_stream = open(image_path, "rb")
    #     except FileNotFoundError:
    #          st.error('Erro! Imagem nao foi carregada para analisar')
    #     else:
    #          analisarImagem(image_stream,image_path)

        # Se tirou foto       
        if(flagCaptura == True):
            image_path = os.path.abspath(img_name)
            try:
                image_stream = open(image_path, "rb")
            except FileNotFoundError:
                st.error('Erro! Imagem nao foi carregada para analisar')
            else:
                analisarImagem(image_stream,image_path)

    
    # cap = cv2.VideoCapture(0)
    # # Check if the webcam is opened correctly
    # image_path = "fotoExemplo.jpg"
    # flagCaptura = False

    # if not cap.isOpened():
    #     st.error('Erro ao conectar na Camera!')
    #     raise IOError("Cannot open webcam")
    # else:
    #     st.warning('Quando a camera abrir, pressione ENTER para tirar a FOTO!')

    # while True:
    #     ret, frame = cap.read()
    #     frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    #     cv2.imshow('Input', frame)
    #     #st.write(frame)
    #     c = cv2.waitKey(1)
    #     # Enter tira foto
    #     if c == 13:
    #         print('Foto tirada')
    #         # Salvar o frame
    #         flagCaptura = True
    #         break

    # # print('sss' + str(ret)) 
    # cap.release()
   

    # cv2.destroyAllWindows()
    
    

st.header('SmartFace')
st.subheader('Aplicativo de reconhecimento facial')

# abrir um exemplo
botaoMostrarExemplo = st.button('Clique ver um exemplo!')
if (botaoMostrarExemplo):
    showExample()


# botao upload
imagem = st.file_uploader(label = 'Ou selecione uma imagem de uma pessoa para analisar',
    type = ['png','jpg','gif','bmp'],
    accept_multiple_files = False)


#botao camera
botaotirarFoto = st.button('Clique aqui para tirar uma foto!')
if (botaotirarFoto):   
    acionarCamera()



# Checagem se foi selecionado algo
if(imagem is None):
    st.write('Uma imagem deve ser selecionada para efetuar a análise!')
else:
    # Checagem do tamanho do arquivo - The allowed image file size is from 1KB to 6MB.
    #  6M = 6291456bytes e 1kb = 1024 bytes
    if(imagem.size < 1024 or imagem.size > 6291456):
        st.error('A imagem deve ter tamanho entre 1 KB e 6 MB!')
        imagem = None
    else:
        callApiAzure(imagem)



