# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:22:49 2019

@author: Ales
"""

import numpy as np
from scipy.io.matlab import mio
import random

mnist=mio.loadmat('mnist-original.mat')
data = mnist['data']
réponse = mnist['label']

poids=np.random.normal(0,1,[784,10])

#   Permet de selectionner des données aléatoirement
def données_entrainement(nombre_de_données):
    les_données=[]
    les_réponses=[]
# matrice de nombres aléatoires
    rang = random.sample(range(len(data[0])), nombre_de_données)
    k=0
    for i in rang:
        les_données.append(data.T[i])
        les_réponses.append([ 0 for i in range (10) ])
        les_réponses[k][int(réponse[0][i])]=1
        k+=1
    return les_données,les_réponses

#   Calcule du gradient pour une erreur : Entropie Croisée
def gradient_cross(target,activation,entrée):
    taille=len(target)
    reponse=target.index(max(target))
    mat_entrée=[ entrée for i in range (taille) ]
    mat_activation=np.zeros((taille,taille))
# Crée une matrice dérivée partielle en diagonale
    for i in range (taille):
        mat_activation[i,i]=activation[i]
# gradient différent pour la réponse attendue
    mat_activation[reponse,reponse]=activation[reponse]-1
    gradient=np.dot(mat_activation,mat_entrée)
    return gradient

#   Calcule une approximation du gradient pour une erreur : Quadratique
def gradient_quad(target,activation,entrée):
    taille=len(target)
    reponse=target.index(max(target))
    mat_entrée=[ entrée for i in range (taille) ]
    mat_activation=np.zeros((taille,taille))
# Crée une matrice dérivée partielle en diagonale
    for i in range (taille):
        mat_activation[i,i]=activation[i]**2*(1-activation[i])+activation[i]
# sélectionne l'activation de la prédiction attendue ( car a un gradient différent )
    acti=activation[reponse]
    mat_activation[reponse,reponse]=-acti*(1-acti)**2-(1-acti)
    gradient=np.dot(mat_activation,mat_entrée)
    return gradient

#   Calcule l'activation
def stable_softmax(pre_acti):
    exps = np.exp(pre_acti - np.max(pre_acti))
    return exps / np.sum(exps)

#   Calcule l'activation sur une liste de pré-activation
def stable_softmax_list(pre_acti):
    for i in range (len(pre_acti)):
        pre_acti[:][i]=stable_softmax(pre_acti[:][i])
    return pre_acti    

#   Calcule la pré-activation
def pre_activation(donnée,poids):
    return np.dot(donnée,poids)

#   Calcule la sortie de chaque neurone
def prediction(donnée,poids):
    z=pre_activation(donnée,poids)
    y=stable_softmax(z)
    return np.round(y)

#   Compare les prédictions aux valeurs réelles ( donne un ratio de réussite )
def précision(prédictions,réponses):
    S=0
    for i in range (len(prédictions)):
        a=0
        for j in range (len(prédictions[i])):
            if prédictions[i][j]!=réponses[i][j]:
                a=0
                break
            else:
                a=1
        S+=a
    return S/len(prédictions)
    
#   Entrainement, modification des poids par la descente de gradient
def train(nombre_de_données,poids):
# epochs = nombre d'entrainement
    epochs=500
    learning_rate=0.1
    a=[]
    for epoch in range (epochs):
# Sélectionne les données à utiliser à chaque entrainement
        données=données_entrainement(nombre_de_données)
# Permet de visualiser les ameliorations en précision         
        if epoch %50==0:
            prédiction=stable_softmax_list(pre_activation(données[0],poids))
            print(précision(prédiction,données[1]),epoch)
   
        directions_gradient=np.zeros(poids.shape)
        z=pre_activation(données[0],poids)
        y=stable_softmax_list(z)

# Calule le gradient Commenter/Décommenter un des deux pour choisir le type d'erreur        
        for i in range (len(y)):
#            directions_gradient+=np.array(gradient_quad(données[1][i],y[i],données[0][i])).T         
            directions_gradient+=np.array(gradient_cross(données[1][i],y[i],données[0][i])).T
# Fait descendre le gradient            
        poids=poids - learning_rate * directions_gradient
        a=poids    
        prédiction=stable_softmax_list(pre_activation(données[0],poids))
        print(précision(prédiction,données[1]))
        
#        if précision(prédiction,données[1])>0.93:
#            return a
        
    return a     
