

##########################REFAIRE L EN TETE#########################


# Calcul d’un step du modèle odométrique 
#Entrées:
#-phi1mes: variation de l'angle mesurée sur l'odomètre de la roue 1 en une période
#         d'échantillonnage, en degrés.
#-phi2mes: variation de l'angle mesurée sur l'odomètre de la roue 2 en une période
#         d'échantillonnage, en degrés.
#-alpha: angle du volant mesuré sur le potard, positif q-
#        uand il est tourné vers la gauche,en radians.
#-x    : position en abscisse du centre du train arrière de la voiture,
#        à l'instant t, en mètres.
#-y    : position en ordonnée du centre du train arrière de la voiture,
#        à l'instant t, en mètres.
#-theta: angle de la voiture par rapport à l'horizontale (voir schéma s-
#        ur le Drive) à l'instant t, en radians.
#-Rroue : rayon de la roue, en mètres.
#-L    : longueur entre le train arrière et le train avant de la voitu-
#        re, en mètres.
#-Te: période d'échantillonnage Te, en secondes.

#Sortie:
#-liste_return: liste contenant:
#   -xprime: position en abscisse du centre du train arrière de la voiture à l'instant t+Te, en mètres.
#   -yprime: position en ordonnée du centre du train arrière de la voiture à l'instant t+Te, en mètres.
#   -thetaprime: angle de la voiture par rapport à l'horizontale à l'instant t+Te (voir modèle papier sur le Drive), en radians.
#   -v: vitesse moyenne de la voiture durant la période d'échantillonnage Te.


from math import tan as tan
from math import sin as sin
from math import cos as cos
from math import pi  as pi
from numpy import array as array
import matplotlib.pyplot as plt


from API import relation1, relation2, relation3, relation4, relation5xc, relation5yc, relation6thetaprimevirage, relation6xprimevirage, relation6yprimevirage, relation7, relation6thetaprimetoutdroit, relation6xprimetoutdroit, relation6yprimetoutdroit
from modelestep import modelestep

def predict_lignedroite(phi,alpha,x,y,theta,Rroue,L,Te,n):
    
    x_n = x + n*phi*(pi/180)*Rroue*cos(theta)
    y_n = y + n*phi*(pi/180)*Rroue*sin(theta)
    
    theta_n = theta
    
    x_n_1 = x + (n-1)*phi*(pi/180)*Rroue*cos(theta)
    y_n_1 = y + (n-1)*phi*(pi/180)*Rroue*sin(theta)    
    v_n = pow( (x_n - x_n_1), 2) + pow( (y_n - y_n_1), 2)
    v_n = pow(v_n, 0.5)/Te
    if phi != 0:
        v_n = v_n * phi / abs(phi)
    
    liste_return = [x_n,y_n,theta_n,v_n]
    return liste_return



def predict_virage(phi,alpha,x,y,theta,Rroue,L,Te,n):
    
    x_n = x - (L/tan(alpha))*sin(theta) + (L/tan(alpha))*sin(theta + tan(alpha)* (n*phi*(pi/180)*Rroue) /L)
    y_n = y + (L/tan(alpha))*cos(theta) - (L/tan(alpha))*cos(theta + tan(alpha)* (n*phi*(pi/180)*Rroue) /L)
    
    theta_n = theta + tan(alpha)*(n*phi*(pi/180)*Rroue)/L
    
    x_n_1 = x - (L/tan(alpha))*sin(theta) + (L/tan(alpha))*sin(theta + tan(alpha)*((n-1)*phi*(pi/180)*Rroue) /L)
    y_n_1 = y + (L/tan(alpha))*cos(theta) - (L/tan(alpha))*cos(theta + tan(alpha)*((n-1)*phi*(pi/180)*Rroue) /L)
    
    v_n = pow( (x_n - x_n_1), 2) + pow( (y_n - y_n_1), 2)
    v_n = pow(v_n, 0.5)/Te
    if phi != 0:
        v_n = v_n * phi / abs(phi)
    
    liste_return = [x_n,y_n,theta_n,v_n]
    return liste_return



def testsimsim(phi_1st_half, phi_2nd_half, alpha_1st_half, alpha_2nd_half, x0, y0, theta0, V0, Rroue, L, Te, nb_steps_1st_half, nb_steps_2nd_half):

    import matplotlib.pyplot as plt
    from numpy import array as array


    #initialisation#######################################
    
    #point de depart
    tab = [x0,y0,theta0,V0]
    tabX = [tab[0]]
    tabY = [tab[1]]
    tabTheta = [tab[2]]
    tabV = [tab[3]]
    tabT = [0]
    
    #prediction############################################
    firstprediction = predict_lignedroite(phi_1st_half,alpha_1st_half,tab[0],tab[1],tab[2],Rroue,L,Te,nb_steps_1st_half)
        
    secondprediction = predict_virage(phi_2nd_half,alpha_2nd_half,firstprediction[0],firstprediction[1],firstprediction[2],Rroue,L,Te,nb_steps_2nd_half)
    
    
    
    ############################################
    
    
    
        
    
    
    for k in range (0,nb_steps_1st_half) :
        tab = modelestep(phi_1st_half,phi_1st_half,alpha_1st_half,tab[0],tab[1],tab[2],Rroue,L,Te)
    
        tabX.append(tab[0])
        tabY.append(tab[1])
        tabTheta.append(tab[2])
        tabV.append(tab[3])
        tabT.append(Te*(k+1))
        
    for j in range (0,nb_steps_2nd_half) :
        tab = modelestep(phi_2nd_half,phi_2nd_half,alpha_2nd_half,tab[0],tab[1],tab[2],Rroue,L,Te)
    
        tabX.append(tab[0])
        tabY.append(tab[1])
        tabTheta.append(tab[2])
        tabV.append(tab[3])
        tabT.append(Te*(j+1 + nb_steps_1st_half))
    
    
    plt.figure()
    plt.plot(tabX,tabY,'ro')
    plt.plot(x0,y0,'g.')
    plt.plot(firstprediction[0],firstprediction[1],'g.')
    plt.plot(secondprediction[0],secondprediction[1],'g.')
    #plt.axis([-4,4,-4,4])
    plt.title("Car position")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.show()
    
    tabT
    tabTheta
    
    plt.figure()
    plt.plot(tabT,tabTheta,'ro')
    plt.plot(0,theta0,'g.')
    plt.plot(tabT[nb_steps_1st_half],firstprediction[2],'g.')
    plt.plot(tabT[nb_steps_1st_half + nb_steps_2nd_half],secondprediction[2],'g.')
    plt.title("Car orientation")
    plt.ylabel("Theta(rad)")
    plt.xlabel("t(s)")
    plt.show()
    
    plt.figure()
    plt.plot(tabT,tabV,'ro')
    plt.plot(0,V0,'g.')
    plt.plot(tabT[nb_steps_1st_half],firstprediction[3],'g.')
    plt.plot(tabT[nb_steps_1st_half + nb_steps_2nd_half],secondprediction[3],'g.')
    plt.title("Car speed")
    plt.ylabel("V(m/s)")
    plt.xlabel("t(s)")
    plt.show()
    



