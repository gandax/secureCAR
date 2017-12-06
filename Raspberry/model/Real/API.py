from math import tan as tan
from math import sin as sin
from math import cos as cos
from math import pi  as pi

########################################################################
# Relation 1 du modele odométrique
########################################################################
# Entrées:
# Rroue : rayon de la roue, en mètres.
# phimes: variation de l'angle mesurée sur l'odomètre en une période
#         d'échantillonnage, en degrés.

# Sortie:
# dmes  : distance parcourue par la roue en une période d'échantillonn-
#         age, en mètres.
########################################################################

def relation1(Rroue,phimes):
    dmes = phimes * (pi/180) * Rroue
    return dmes

########################################################################
# Relation 2 du modele odométrique
########################################################################
# Entrées:
# d1mes: distance parcourue par la roue 1 (la roue droite) de la voi-
#        ture en une période d'échantillonage, en mètres.
# d2mes: distance parcourue par la roue 2 (la roue gauche) de la voi-
#        ture en une période d'échantillonage, en mètres.

# Sortie:
# d  : distance parcourue par le milieu du train arrière de la voitu-
#      re en une période d'échantillonnage, en mètres.
########################################################################

def relation2(d1mes,d2mes):
    if(d1mes != 0):
        d = 0.5 * abs(d1mes + d2mes) * (d1mes / abs(d1mes))
    elif(d2mes != 0):
        d = 0.5 * abs(d1mes + d2mes) * (d2mes / abs(d2mes))
    else:
        d = 0
    return d

########################################################################

#----------------------------------------------------------------------#
#                           CAS VOITURE TOUT DROIT                     #
#----------------------------------------------------------------------#

########################################################################
#Relation 6 du modèle odométrique pour thetaprime quand la voiture va tout droit
########################################################################
#Entrées:
#-theta: angle de la voiture par rapport à l'horizontale à l'instant t (voir modèle papier sur le Drive), en radians.
#Sortie:
#-thetaprime: angle de la voiture par rapport à l'horizontale à l'instant t+Te (voir modèle papier sur le Drive), en radians.
########################################################################

def relation6thetaprimetoutdroit(theta):
    thetaprime = theta
    return thetaprime

########################################################################
# Relation 6 du modèle odométrique pour xprime quand la voiture va tout droit
########################################################################
#Entrées:
#-x: position en abscisse du centre du train arrière de la voiture,
#        à l'instant t, en mètres.
#-d: distance parcourue par le milieu du train arrière de la voitu-
#      re en une période d'échantillonnage, en mètres.
#-theta: angle de la voiture par rapport à l'horizontale à l’instant t (voir modèle papier sur le Drive), en radians.
#Sortie:
#-xprime: position en abscisse du centre du train arrière de la voiture à l'instant t+Te, en mètres.
########################################################################

def relation6xprimetoutdroit(x,d,theta):
    xprime = x + d*cos(theta)
    return xprime

########################################################################
# Relation 6 du modèle odométrique pour yprime quand la voiture va tout droit
########################################################################
#Entrées:
#-y: position en ordonnée du centre du train arrière de la voiture,
#        à l'instant t, en mètres.
#-d: distance parcourue par le milieu du train arrière de la voitu-
#      re en une période d'échantillonnage, en mètres.
#-theta: angle de la voiture par rapport à l'horizontale à l’instant t (voir modèle papier sur le Drive), en radians.
#Sortie:
#-yprime: position en ordonnée du centre du train arrière de la voiture à l'instant t+Te, en mètres.
########################################################################

def relation6yprimetoutdroit(y,d,theta):
    yprime = y + d*sin(theta)
    return yprime

########################################################################

#----------------------------------------------------------------------#
#                           CAS VOITURE TOURNE                         #
#----------------------------------------------------------------------#

########################################################################
# Relation 3 du modele odomètrique
########################################################################
# Entrées:
# alpha: angle du volant mesuré sur le potard, positif q-
#        uand il est tourné vers la gauche,en radians.
# d    : distance parcourue par le milieu du train arrière de la voitu-
#        re en une période d'échantillonnage, en mètres.
# L    : longueur entre le train arrière et le train avant de la voitu-
#        re, en mètres.

# Sortie:
# beta : variation de theta durant une période d'échantillonnage, posi-
#        ve quand la voiture tourne à gauche, en radians.
########################################################################

def relation3(alpha,d,L):
    beta = (d / L) * tan(alpha)
    return beta

########################################################################
# Relation 4 du modele odomètrique
########################################################################
# Entrées:
# alpha: angle du volant mesuré sur le potard, positif q-
#        uand il est tourné vers la gauche,en radians.
# L    : longueur entre le train arrière et le train avant de la voitu-
#        re, en mètres.

# Sortie:
# R :    rayon de courbure du virage de la voiture, en mètres.
########################################################################

import math
def relation4(alpha,L):
    R = L / tan(alpha)
    return R

########################################################################
# Relation 5 du modele odomètrique pour le calcul de xc
########################################################################
# Entrées:
# R :    rayon de courbure du virage de la voiture, en mètres.
# theta: angle de la voiture par rapport à l'horizontale (voir schéma s-
#        ur le Drive) à l'instant t, en radians.
# x    : position en abscisse du centre du train arrière de la voiture,
#        à l'instant t, en mètres.

# Sortie:
# xc   : position en abscisse du centre de rotation de la voiture, à
#        l'instan t, en mètres.
########################################################################

def relation5xc(R,theta,x):
    xc = x - R * sin(theta)
    return xc

########################################################################
# Relation 5 du modele odomètrique pour le calcul de yc
########################################################################
# Entrées:
# R :    rayon de courbure du virage de la voiture, en mètres.
# theta: angle de la voiture par rapport à l'horizontale (voir schéma s-
#        ur le Drive) à l'instant t, en radians.
# y    : position en ordonnée du centre du train arrière de la voiture,
#        à l'instant t, en mètres.

# Sortie:
# yc   : position en ordonnée du centre de rotation de la voiture, à
#        l'instant t, en mètres.
########################################################################

def relation5yc(R,theta,y):
    yc = y + R * cos(theta)
    return yc

########################################################################
# Relation 6 du modèle odométrique pour thetaprime quand la voiture tourne
########################################################################
#Entrées:
#-theta: angle de la voiture par rapport à l'horizontale à l'instant t (voir modèle papier sur le Drive), en radians.
#-beta: variation de l'angle de la voiture par rapport à l'horizontale entre l'instant t et l'instant t+Te(voir modèle papier sur le Drive), en radians.
#Sortie:
#-thetaprime: angle de la voiture par rapport à l'horizontale à l'instant t+Te (voir modèle papier sur le Drive), en radians.
########################################################################

def relation6thetaprimevirage(theta,beta):
    thetaprime = theta + beta
    return thetaprime

########################################################################
# Relation 6 du modèle odométrique pour xprime quand la voiture tourne
########################################################################
#Entrées:
#- xc : position en abscisse du centre de rotation de la voiture, en mètres.
#-R: longueur du rayon de rotation de la voiture, en mètres.
#-theta: angle de la voiture par rapport à l'horizontale à l’instant t (voir modèle papier sur le Drive), en radians.
#-beta: variation de l'angle de la voiture par rapport à l'horizontale durant une période d’échantillonnage Te(voir modèle papier sur le Drive), en radians.
#Sortie:
#-xprime: position en abscisse du centre du train arrière de la voiture à l'instant t+Te, en mètres.
########################################################################

def relation6xprimevirage(xc,R,theta,beta):
    xprime = xc + R*sin(theta + beta)
    return xprime

#########################################################################
# Relation 6 du modèle odométrique pour yprime quand la voiture tourne
#########################################################################
#Entrées:
#- yc : position en ordonnée du centre de rotation de la voiture, en mètres.
#-R: longueur du rayon de rotation de la voiture, en mètres.
#-theta: angle de la voiture par rapport à l'horizontale à l'instant t(voir modèle papier sur le Drive), en radians.
#-beta: variation de l'angle de la voiture par rapport à l'horizontale durant une période d’échantillonnage Te(voir modèle papier sur le Drive), en radians.
#Sortie:
#-yprime: position en ordonnée du centre du train arrière de la voiture à l'instant t+Te, en mètres.
##########################################################################

def relation6yprimevirage(yc,R,theta,beta):
    yprime = yc - R*cos(theta + beta)
    return yprime

##########################################################################
# Relation 7 du modèle odométrique
##########################################################################
#Entrées:
#-xprime: position en abscisse du centre du train arrière de la voiture à l'instant t+Te, en mètres.
#-yprime: position en ordonnée du centre du train arrière de la voiture à l'instant t+Te, en mètres.
#-x: position en abscisse du centre du train arrière de la voiture à l'instant t, en mètres.
#-y: position en ordonnée du centre du train arrière de la voiture à l'instant t, en mètres.
#-d: distance "angulaire" parcourue par le train arrière durant la période d'échantillonnage Te, en mètres.
#-Te: période d'échantillonnage Te, en secondes.
#Sortie:
#-v: vitesse moyenne de la voiture durant la période d'échantillonnage Te.
##########################################################################

def relation7(xprime,yprime,x,y,d,Te):
    if d == 0:
        v = 0
    else:
        aux_x = (x - xprime) ** 2
        aux_y = (y - yprime) ** 2
        aux_v =  (aux_x + aux_y) ** 0.5
        aux_v2 = aux_v / Te
        v = aux_v2 * abs(d) / d
    
    return v

##########################################################################

