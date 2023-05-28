import numpy as np
import streamlit as st
import plotly.graph_objs as go
import math

####################

# Fonction pour créer les périodes de temps
def create_time_periods(start_year, end_year, step):
    num_periods = (end_year - start_year) // step
    periods = []
    
    for i in range(num_periods):
        period = np.arange(start_year + i * step, start_year + (i + 1) * step)
        periods.append(period)
        
    return periods










####################

# Fonctions

# R(t)
def R(t, rho):
    return 1 / (1 + rho) ** t

# A(t) et Ag(t)
def A(t, delta_a):
    A = A_0
    for i in range(1, t + 1):
        A = A / (1 - Ag(i - 1, delta_a))
    return A

# Ag(t)
def Ag(t, delta_a):
    return Ag_0 * math.exp(-delta_a * t) * math.exp(-delta_b * t)

# Paramètres constants
A_0 = 0.0303220
Ag_0 = 0.16
delta_b = 0.2

# L(t)
def L(t, L_0, L_T_max):
    if (t == 0):
        return L_0
    else:
        return (L(t - 1, L_0, L_T_max) * L_T_max) ** 0.5

# Paramètres constants
L_0 = 6411


# sigma(t)
def sigma(t, sigma_0, sigma_g_0, sigma_d1, sigma_g):
    if t == 0:
        return sigma_0
    return sigma(t - 1, sigma_0, sigma_g_0, sigma_d1, sigma_g) * (1 - sigma_g(t - 1, sigma_g_0, sigma_d1))

def sigma_g(t, sigma_g_0, sigma_d1):
    if (t == 0):
        return sigma_g_0 * (1 - sigma_d1)
    return sigma_g(t - 1, sigma_g_0, sigma_d1) * (1 - sigma_d1)

# Paramètres constants
sigma_0 = 0.14452
sigma_g_0 = 0.158

# phi(t)
def phi(t, phi_5, phi_10, phi_15, phi_max):
    if t < 5:
        return phi_5 + (1 - phi_5) * np.exp(-0.25 * t)
    elif t < 10:
        return phi_10 + (phi_5 - phi_10) * np.exp(-0.25 * (t - 5))
    elif t < 15:
        return phi_15 + (phi_10 - phi_15) * np.exp(-0.25 * (t - 10))
    elif t >= 15:
        return phi_max + (phi_15 - phi_max) * np.exp(-0.25 * (t - 15))

# Function: BC(t)
def BC(t, BC_0, BC_g):
    if t < 15:
        return BC_0
    return BC_0 * (1 - BC_g) ** (t - 15)

# Paramètres constants
BC_0 = 1.26

####################

# Fonctions pour tracer les graphiques

# R(t)
def plot_R(t, rho, title):
    R_values = [R(i, rho) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=R_values, mode='lines', name='R(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de R(t)")
    st.plotly_chart(fig)
    
# A(t)
def plot_A(t, delta_a, title, column):
    A_values = [A(i, delta_a) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=A_values, mode='lines', name='A(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)",yaxis_title="Valeur de A(t)",
        width=400,
        height=400)
    column.plotly_chart(fig)

# Ag(t)
def plot_Ag(t, delta_a, title, column):
    Ag_values = [Ag(i, delta_a) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=Ag_values, mode='lines', name='Ag(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de Ag(t)",
        width=400,  
        height=400)
    column.plotly_chart(fig)

# L(t)
def plot_L(t, L_0, L_T_max, title):
    L_values = [L(i, L_0, L_T_max) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=L_values, mode='lines', name='L(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de L(t)",
                      width=650,
                      height=400)
    st.plotly_chart(fig)

# sigma(t)
def plot_sigma_g(t, sigma_g_0, sigma_d1, title, column):
    sigma_g_values = [sigma_g(i, sigma_g_0, sigma_d1) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=sigma_g_values, mode='lines', name='σg(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de σg(t)",
                      width=400,
                      height=400)
    column.plotly_chart(fig)
    
def plot_sigma(t, sigma_0, sigma_g_0, sigma_d1, sigma_g, title, column):
    sigma_values = [sigma(i, sigma_0, sigma_g_0, sigma_d1, sigma_g) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=sigma_values, mode='lines', name='σ(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de σ(t)",
                      width=400,
                      height=400)
    column.plotly_chart(fig)

def plot_phi(t, phi_5, phi_10, phi_15, phi_max, title):
    phi_values = [phi(i, phi_5, phi_10, phi_15, phi_max) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=phi_values, mode='lines', name='φ(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de φ(t)")
    st.plotly_chart(fig)

def plot_BC(t, BC_0, BC_g, title):
    BC_values = [BC(i, BC_0, BC_g) for i in t]
    fig = go.Figure(data=go.Scatter(x=t, y=BC_values, mode='lines', name='BC(t)'))
    fig.update_layout(title=title, xaxis_title="Temps (décennies)", yaxis_title="Valeur de BC(t)")
    st.plotly_chart(fig)
    



####################

# Fonction principale
def main():
    st.title("Graphiques interactifs")
    
    # Paramètres
    
    # Temps
    step = st.sidebar.number_input("Intervalle entre les périodes (en années)", min_value=1, value=10)
    
    start_year = 2005
    end_year = 2605
    time_periods = create_time_periods(start_year, end_year, step)
    time_range = np.arange(0, len(time_periods), step)
    
    # Slider pour ρ
    st.sidebar.header("Slider pour R(t)")
    rho = st.sidebar.slider("Valeur de ρ", min_value=0.0, max_value=1.0, value=0.0015, step=0.01)
    
    # Graphique de R(t)
    st.header("Graphe de R(t)")
    plot_R(time_range, rho, f"pour ρ = {rho}")
    
    # Slider pour Δₐ
    st.sidebar.header("Slider pour A(t)")
    delta_a = st.sidebar.slider("Valeur de Δₐ", min_value=0.05, max_value=1.5, value=0.9, step=0.01)

    # Graphiques
    col1, col2 = st.columns(2)

    # Graphique de A(t)
    col1.header("Graphe de A(t)")
    plot_A(time_range, delta_a, f"pour Δₐ = {delta_a}", col1)

    # Graphique de Ag(t)
    col2.header("Graphe de Ag(t)")
    plot_Ag(time_range, delta_a, f"pour Δₐ = {delta_a}", col2)
    
    # Slider pour L(0)
    st.sidebar.header("Slider pour L(t)")
    L_T_max = st.sidebar.slider("Valeur de L(Tmax)", min_value=8000, max_value=12000, value=8700, step=10)
    
    # Graphique de L(t)
    st.header("Graphe de L(t)")
    plot_L(time_range, L_0, L_T_max, f"pour L(0) = {L_0}  et  L(Tmax) = {L_T_max}")
    
    # Slider pour σd1
    sigma_d1 = st.sidebar.slider("Valeur de σd1", min_value=0.0, max_value=0.06, value=0.006, step=0.001)
    col3, col4 = st.columns(2)
        
    # Graphique de σg(t)
    col3.header("Graphe de σg(t)")
    plot_sigma_g(time_range, sigma_g_0, sigma_d1, f"pour σd1 = {sigma_d1}", col3)
    
    # Graphique de σ(t)
    col4.header("Graphe de σ(t)")
    plot_sigma(time_range, sigma_0, sigma_g_0, sigma_d1, sigma_g, f"pour σd1 = {sigma_d1}", col4)
    
    
    # Sliders pour phi(5), phi(10), and phi(15)
    st.sidebar.header("Slider pour φ(t)")
    phi_5 = st.sidebar.slider("Valeur de φ(5)", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
    phi_10 = st.sidebar.slider("Valeur de φ(10)", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
    phi_15 = st.sidebar.slider("Valeur de φ(15)", min_value=0.0, max_value=1.0, value=1.0, step=0.01)

    # Calcul de phi_max qui est la valeur maximale parmi phi(5), phi(10), and phi(15)
    phi_max = max(phi_5, phi_10, phi_15)
    
    # Graphique de φ(t)
    st.header("Graphe de φ(t)")
    plot_phi(time_range, phi_5, phi_10, phi_15, phi_max, f"pour φ(5) = {phi_5}, φ(10) = {phi_10}, φ(15) = {phi_15}")
    
    # Slider pour BCg
    st.sidebar.header("Slider pour BC(t)")
    BC_g = st.sidebar.slider("Valeur de BCg", min_value=0.0, max_value=0.2, value=0.05, step=0.01)
    
    # Graphique de BC(t)
    st.header("Graphe de BC(t)")
    plot_BC(time_range, BC_0, BC_g, f"pour BCg = {BC_g}")
    

if __name__ == "__main__":
    main()
