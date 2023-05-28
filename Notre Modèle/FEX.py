
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#equations préalables pour l'equation Q

#Nécessaire pour calculer F(t)
FEX_0 = 1
FEX_10 = 1

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
# Création d'un widget pour l'utilisateur modifier la valeur du paramètre
a = st.slider('Valeur de a', 0.0, 5.0, 0.5, 0.1)

# Création des données pour la courbe en utilisant la valeur de a
t = np.linspace(0, 15, 100)
y = a*FEX(t)


# Tracé de la courbe
fig, ax = plt.subplots()
ax.plot(t, y)
ax.set_xlabel('t')
ax.set_ylabel('y')
ax.set_title('Courbe en fonction de a')
st.pyplot(fig)