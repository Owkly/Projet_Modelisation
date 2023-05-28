import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#equations préalables pour l'equation Q




# Création d'un widget pour l'utilisateur modifier la valeur du paramètre
a = st.slider('Valeur de a', 0.0, 5.0, 0.5, 0.1)
phi_0 = st.slider('Valeur de phi0', 0.0, 1.0, 0.0, 0.1)
phi_5= st.slider('Valeur de phi5', 0.1, 1.0, 0.1, 0.1)
phi_10 = st.slider('Valeur de phi10', 0.2, 1.0, 0.2, 0.1)
phi_15 = st.slider('Valeur de phi15', 0.3, 1.0, 0.3, 0.1)
phi_max = st.slider('Valeur de phimax', 0.4, 1.0, 0.4, 0.1) #A DETERMINER §§§!!!!cd 


# Création des données pour la courbe en utilisant la valeur de a
#Nécessaire pour calculer F(t)

#FEX(t)
FEX_0 = 0.83
FEX_10 = 0.30

def FEX(t):
    y = np.zeros(t.size)
    for i in range(0,t.size):
        if (t[i] <= 10):
            y[i] = FEX_0 + 0.1 * (FEX_10 - FEX_0) * t[i]
        else: # t > 10
            y[i]=FEX_10
    return y

t = np.arange(0, 15, 1)
y = a*FEX(t)

# Tracé de la courbe
fig, ax = plt.subplots()
ax.plot(t, y)
ax.set_xlabel('t')
ax.set_ylabel('y')
ax.set_title('Courbe de FEX(t) avec differents a')
st.pyplot(fig)



#On veut récuperer les 3 phi dont on a besoin pour calculer MAT
#Les phi varient de 0 à 1 avec pour valeur par défaut 1
phi_0 = 0.7
phi_5= 0.6
phi_10 = 0.5
phi_15 = 0.3
phi_max = 4 #A DETERMINER §§§!!!!
def phi(t, phi_0, phi_5, phi_10, phi_15,phi_max):
    if t < 5:
        return phi_5 + (phi_0 - phi_5) * np.exp(-0.25 * t)
    elif t < 10:
        return phi_10 + (phi_5 - phi_10) * np.exp(-0.25 * t)
    elif t < 15:
        return phi_15 + (phi_10 - phi_15) * np.exp(-0.25 * t)
    else:
        return phi_max + (phi_max - phi_15) * np.exp(-0.25 * 25)
#Pour calculer MAT on a besoin de phi12,11,23 et 32
phi_11 = phi(11,phi_0, phi_5, phi_10, phi_15, phi_max)
phi_12 = phi(12,phi_0, phi_5, phi_10, phi_15, phi_max)
phi_23 = phi(23,phi_0, phi_5, phi_10, phi_15, phi_max)
phi_32 = phi(32,phi_0, phi_5, phi_10, phi_15, phi_max)
print(phi_11)
print(phi_12)
print(phi_23)
print(phi_32)


#MARCHE MAIS TRES LENT 
#On veut ici recupérer MAT
MAT_0= 787 #indice 0 de la matrice
MUP_0= 1600 #indice 1 de la matrice
MLO_0= 10100 #indice 2 de la matrice
def mat(t):
    
    
    matrice0=np.array([MAT_0,MUP_0,MLO_0])
    if (t <= 0):
        return matrice0 #Si t=0 On renvoie les valeurs initiales
    else : #Sinon on calcule les nouvelles valeurs pour t en fonction de t-1
        matrice=np.zeros(matrice0.size)
        MAT_minus = mat(t-1)[0]
        MUP_minus = mat(t-1)[1]
        MLO_minus = mat(t-1)[2]
        matrice[0] = phi_11*MAT_minus+phi_12*MUP_minus #RAJOUTER E(t-1)
        matrice[1] = (1-phi_11)*MAT_minus+(1-phi_12-phi_32)*MUP_minus+phi_23*MLO_minus
        matrice[2] = phi_32*MUP_minus+(1-phi_23)*MLO_minus
        return matrice
      

MAT_t = np.zeros(t.size)
for i in range(t.size):
    j=t[i]
    MAT_t[i]=mat(j)[0]



fig2,ax2 = plt.subplot()
ax2.plot(t,MAT_t)
ax2.set_xlabel('t')
ax2.set_ylabel('MAT')
ax2.set_title('Courbe de MAT avec differents phi')
st.pyplot(fig2)


