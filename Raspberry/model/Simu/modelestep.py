# Calcul d’un step du modele odometrique 
#Entrees:
#-phi1mes: variation de l'angle mesuree sur l'odometre de la roue 1 en une periode
#         d'echantillonnage, en degres.
#-phi2mes: variation de l'angle mesuree sur l'odometre de la roue 2 en une periode
#         d'echantillonnage, en degres.
#-alpha: angle du volant mesure sur le potard, positif q-
#        uand il est tourne vers la gauche,en radians.
#-x    : position en abscisse du centre du train arriere de la voiture,
#        a l'instant t, en metres.
#-y    : position en ordonnee du centre du train arriere de la voiture,
#        a l'instant t, en metres.
#-theta: angle de la voiture par rapport a l'horizontale (voir schema s-
#        ur le Drive) a l'instant t, en radians.
#-Rroue : rayon de la roue, en metres.
#-L    : longueur entre le train arriere et le train avant de la voitu-
#        re, en metres.
#-Te: periode d'echantillonnage Te, en secondes.

#Sortie:
#-liste_return: liste contenant:
#   -xprime: position en abscisse du centre du train arriere de la voiture a l'instant t+Te, en metres.
#   -yprime: position en ordonnee du centre du train arriere de la voiture a l'instant t+Te, en metres.
#   -thetaprime: angle de la voiture par rapport a l'horizontale a l'instant t+Te (voir modele papier sur le Drive), en radians.
#   -v: vitesse moyenne de la voiture durant la periode d'echantillonnage Te.


from math import tan as tan
from math import sin as sin
from math import cos as cos
from math import pi  as pi

from API import relation1, relation2, relation3, relation4, relation5xc, relation5yc, relation6thetaprimevirage, relation6xprimevirage, relation6yprimevirage, relation7, relation6thetaprimetoutdroit, relation6xprimetoutdroit, relation6yprimetoutdroit

def modelestep(phi1mes,phi2mes,alpha,x,y,theta,Rroue,L,Te):
    d1mes = relation1(Rroue,phi1mes)
    d2mes = relation1(Rroue,phi2mes)
    d = relation2(d1mes,d2mes)
    if abs(alpha) < 3.14/180:
        xprime = relation6xprimetoutdroit(x,d,theta)
        yprime = relation6yprimetoutdroit(y,d,theta)
        thetaprime = relation6thetaprimetoutdroit(theta)
    else:
        beta = relation3(alpha,d,L)
        R = relation4(alpha,L)
        xc = relation5xc(R,theta,x)
        yc = relation5yc(R,theta,y)
        xprime = relation6xprimevirage(xc,R,theta,beta)
        yprime = relation6yprimevirage(yc,R,theta,beta)
        thetaprime = relation6thetaprimevirage(theta,beta)
    v = relation7(xprime,yprime,x,y,d,Te)
    
    liste_return = [xprime,yprime,thetaprime,v]

    return liste_return

