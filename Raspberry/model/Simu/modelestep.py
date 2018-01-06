#coding : utf8



from math import tan as tan
from math import sin as sin
from math import cos as cos
from math import pi  as pi
from numpy import array as array

from API import relation1, relation2, relation3, relation4, relation5xc, relation5yc, relation6thetaprimevirage, relation6xprimevirage, relation6yprimevirage, relation7, relation6thetaprimetoutdroit, relation6xprimetoutdroit, relation6yprimetoutdroit

def modelestep(phi1mes,phi2mes,alpha,x,y,theta,Rroue,L,Te):
    d1mes = relation1(Rroue,phi1mes)
    d2mes = relation1(Rroue,phi2mes)
    d = relation2(d1mes,d2mes)
    if abs(alpha) < 5*pi/180:
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

