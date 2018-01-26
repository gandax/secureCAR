from math import tan as tan
from math import sin as sin
from math import cos as cos
from math import pi  as pi

########################################################################
# Relation 1 du modele odometrique
########################################################################
# Entrees:
# Rroue : rayon de la roue, en metres.
# phimes: variation de l'angle mesuree sur l'odometre en une periode
#         d'echantillonnage, en degres.

# Sortie:
# dmes  : distance parcourue par la roue en une periode d'echantillonn-
#         age, en metres.
########################################################################

def relation1(Rroue,phimes):
    dmes = phimes * (pi/180) * Rroue
    return dmes

########################################################################
# Relation 2 du modele odometrique
########################################################################
# Entrees:
# d1mes: distance parcourue par la roue 1 (la roue droite) de la voi-
#        ture en une periode d'echantillonage, en metres.
# d2mes: distance parcourue par la roue 2 (la roue gauche) de la voi-
#        ture en une periode d'echantillonage, en metres.

# Sortie:
# d  : distance parcourue par le milieu du train arriere de la voitu-
#      re en une periode d'echantillonnage, en metres.
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
#Relation 6 du modele odometrique pour thetaprime quand la voiture va tout droit
########################################################################
#Entrees:
#-theta: angle de la voiture par rapport a l'horizontale a l'instant t (voir modele papier sur le Drive), en radians.
#Sortie:
#-thetaprime: angle de la voiture par rapport a l'horizontale a l'instant t+Te (voir modele papier sur le Drive), en radians.
########################################################################

def relation6thetaprimetoutdroit(theta):
    thetaprime = theta
    return thetaprime

########################################################################
# Relation 6 du modele odometrique pour xprime quand la voiture va tout droit
########################################################################
#Entrees:
#-x: position en abscisse du centre du train arriere de la voiture,
#        a l'instant t, en metres.
#-d: distance parcourue par le milieu du train arriere de la voitu-
#      re en une periode d'echantillonnage, en metres.
#-theta: angle de la voiture par rapport a l'horizontale a l’instant t (voir modele papier sur le Drive), en radians.
#Sortie:
#-xprime: position en abscisse du centre du train arriere de la voiture a l'instant t+Te, en metres.
########################################################################

def relation6xprimetoutdroit(x,d,theta):
    xprime = x + d*cos(theta)
    return xprime

########################################################################
# Relation 6 du modele odometrique pour yprime quand la voiture va tout droit
########################################################################
#Entrees:
#-y: position en ordonnee du centre du train arriere de la voiture,
#        a l'instant t, en metres.
#-d: distance parcourue par le milieu du train arriere de la voitu-
#      re en une periode d'echantillonnage, en metres.
#-theta: angle de la voiture par rapport a l'horizontale a l’instant t (voir modele papier sur le Drive), en radians.
#Sortie:
#-yprime: position en ordonnee du centre du train arriere de la voiture a l'instant t+Te, en metres.
########################################################################

def relation6yprimetoutdroit(y,d,theta):
    yprime = y + d*sin(theta)
    return yprime

########################################################################

#----------------------------------------------------------------------#
#                           CAS VOITURE TOURNE                         #
#----------------------------------------------------------------------#

########################################################################
# Relation 3 du modele odometrique
########################################################################
# Entrees:
# alpha: angle du volant mesure sur le potard, positif q-
#        uand il est tourne vers la gauche,en radians.
# d    : distance parcourue par le milieu du train arriere de la voitu-
#        re en une periode d'echantillonnage, en metres.
# L    : longueur entre le train arriere et le train avant de la voitu-
#        re, en metres.

# Sortie:
# beta : variation de theta durant une periode d'echantillonnage, posi-
#        ve quand la voiture tourne a gauche, en radians.
########################################################################

def relation3(alpha,d,L):
    beta = (d / L) * tan(alpha)
    return beta

########################################################################
# Relation 4 du modele odometrique
########################################################################
# Entrees:
# alpha: angle du volant mesure sur le potard, positif q-
#        uand il est tourne vers la gauche,en radians.
# L    : longueur entre le train arriere et le train avant de la voitu-
#        re, en metres.

# Sortie:
# R :    rayon de courbure du virage de la voiture, en metres.
########################################################################

import math
def relation4(alpha,L):
    R = L / tan(alpha)
    return R

########################################################################
# Relation 5 du modele odometrique pour le calcul de xc
########################################################################
# Entrees:
# R :    rayon de courbure du virage de la voiture, en metres.
# theta: angle de la voiture par rapport a l'horizontale (voir schema s-
#        ur le Drive) a l'instant t, en radians.
# x    : position en abscisse du centre du train arriere de la voiture,
#        a l'instant t, en metres.

# Sortie:
# xc   : position en abscisse du centre de rotation de la voiture, a
#        l'instan t, en metres.
########################################################################

def relation5xc(R,theta,x):
    xc = x - R * sin(theta)
    return xc

########################################################################
# Relation 5 du modele odometrique pour le calcul de yc
########################################################################
# Entrees:
# R :    rayon de courbure du virage de la voiture, en metres.
# theta: angle de la voiture par rapport a l'horizontale (voir schema s-
#        ur le Drive) a l'instant t, en radians.
# y    : position en ordonnee du centre du train arriere de la voiture,
#        a l'instant t, en metres.

# Sortie:
# yc   : position en ordonnee du centre de rotation de la voiture, a
#        l'instant t, en metres.
########################################################################

def relation5yc(R,theta,y):
    yc = y + R * cos(theta)
    return yc

########################################################################
# Relation 6 du modele odometrique pour thetaprime quand la voiture tourne
########################################################################
#Entrees:
#-theta: angle de la voiture par rapport a l'horizontale a l'instant t (voir modele papier sur le Drive), en radians.
#-beta: variation de l'angle de la voiture par rapport a l'horizontale entre l'instant t et l'instant t+Te(voir modele papier sur le Drive), en radians.
#Sortie:
#-thetaprime: angle de la voiture par rapport a l'horizontale a l'instant t+Te (voir modele papier sur le Drive), en radians.
########################################################################

def relation6thetaprimevirage(theta,beta):
    thetaprime = theta + beta
    return thetaprime

########################################################################
# Relation 6 du modele odometrique pour xprime quand la voiture tourne
########################################################################
#Entrees:
#- xc : position en abscisse du centre de rotation de la voiture, en metres.
#-R: longueur du rayon de rotation de la voiture, en metres.
#-theta: angle de la voiture par rapport a l'horizontale a l’instant t (voir modele papier sur le Drive), en radians.
#-beta: variation de l'angle de la voiture par rapport a l'horizontale durant une periode d’echantillonnage Te(voir modele papier sur le Drive), en radians.
#Sortie:
#-xprime: position en abscisse du centre du train arriere de la voiture a l'instant t+Te, en metres.
########################################################################

def relation6xprimevirage(xc,R,theta,beta):
    xprime = xc + R*sin(theta + beta)
    return xprime

#########################################################################
# Relation 6 du modele odometrique pour yprime quand la voiture tourne
#########################################################################
#Entrees:
#- yc : position en ordonnee du centre de rotation de la voiture, en metres.
#-R: longueur du rayon de rotation de la voiture, en metres.
#-theta: angle de la voiture par rapport a l'horizontale a l'instant t(voir modele papier sur le Drive), en radians.
#-beta: variation de l'angle de la voiture par rapport a l'horizontale durant une periode d’echantillonnage Te(voir modele papier sur le Drive), en radians.
#Sortie:
#-yprime: position en ordonnee du centre du train arriere de la voiture a l'instant t+Te, en metres.
##########################################################################

def relation6yprimevirage(yc,R,theta,beta):
    yprime = yc - R*cos(theta + beta)
    return yprime

##########################################################################
# Relation 7 du modele odometrique
##########################################################################
#Entrees:
#-xprime: position en abscisse du centre du train arriere de la voiture a l'instant t+Te, en metres.
#-yprime: position en ordonnee du centre du train arriere de la voiture a l'instant t+Te, en metres.
#-x: position en abscisse du centre du train arriere de la voiture a l'instant t, en metres.
#-y: position en ordonnee du centre du train arriere de la voiture a l'instant t, en metres.
#-d: distance "angulaire" parcourue par le train arriere durant la periode d'echantillonnage Te, en metres.
#-Te: periode d'echantillonnage Te, en secondes.
#Sortie:
#-v: vitesse moyenne de la voiture durant la periode d'echantillonnage Te.
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

