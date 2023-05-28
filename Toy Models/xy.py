import numpy as np
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

# Fonctions pour calculer xn+1 et yn+1
def next_x(xn, yn, a):
    return yn + 1 - a * xn**2

def next_y(xn, yn, b):
    return b * xn

# Fonction pour générer les valeurs xn, yn
def generate_values(x0, y0, a, b, num_iterations):
    xn_values = [0] * num_iterations
    yn_values = [0] * num_iterations
    
    xn_values[0] = x0
    yn_values[0] = y0
    
    for i in range(1, num_iterations - 1, 1):
        xn = next_x(xn_values[i-1], yn_values[i-1], a)
        yn = next_y(xn_values[i-1], yn_values[i-1], b)
        
        if abs(xn) > 1e+100 or abs(yn) > 1e+100:
            st.warning("Les valeurs de xn ou yn sont devenues trop grandes. Veuillez ajuster les paramètres.")
            break
        
        xn_values[i] = xn
        yn_values[i] = yn
        
    return xn_values, yn_values


# Fonction pour tracer les valeurs xn ou yn
def plot_values(values, title, column, xlim, ylim):
    fig = go.Figure(go.Scatter(x=list(range(len(values))), y=values, mode='lines'))
    fig.update_layout(title=title, xaxis_title="Itération", yaxis_title="Valeurs", width=400, height=400)
    fig.update_xaxes(range=xlim)
    fig.update_yaxes(range=ylim)
    column.plotly_chart(fig)


    
def plot_coordinates(x_values, y_values, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='(xn, yn)'))
    fig.update_layout(title=title, xaxis_title="xn", yaxis_title="yn", width=800, height=800)
    st.plotly_chart(fig)


# Fonction pour tracer la trajectoire (xn, yn) avec des flèches de couleur différente à chaque itération
def plot_trajectory(x_values, y_values, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='(xn, yn)'))
    colors = px.colors.qualitative.Alphabet
    for i in range(len(x_values)-1):
        fig.add_annotation(x=x_values[i], y=y_values[i], ax=x_values[i+1], ay=y_values[i+1],
                           arrowhead=2, arrowsize=1.5, arrowwidth=1.5, arrowcolor=colors[i%len(colors)],
                           showarrow=True)
    fig.update_layout(title=title, xaxis_title="xn", yaxis_title="yn", width=800, height=800)
    st.plotly_chart(fig)
    
    
# Fonction principale
# Fonction principale
def main():
    st.title("Graphique interactif pour xn et yn")
    
    # Curseurs pour x0, y0, a et b
    x0 = st.sidebar.slider("Valeur initiale x0", min_value=0.1, max_value=2.0, value=0.5, step=0.01)
    y0 = st.sidebar.slider("Valeur initiale y0", min_value=0.1, max_value=2.0, value=0.5, step=0.01)
    a = st.sidebar.slider("Valeur de a", min_value=1.0, max_value=1.8, value=1.4, step=0.01)
    b = st.sidebar.slider("Valeur de b", min_value=0.1, max_value=0.5, value=0.3, step=0.01)

    # Input pour le nombre d'itérations
    num_iterations = st.sidebar.number_input("Nombre d'itérations", min_value=1, value=100)

    # Générer les valeurs xn, yn
    xn_values, yn_values = generate_values(x0, y0, a, b, num_iterations)

    # Créer deux colonnes
    col1, col2 = st.columns(2)

    # Tracer les valeurs xn et yn côte à côte
    # Tracer les valeurs xn et yn côte à côte
    xlim = (0, num_iterations)
    ylim = (min(min(xn_values), min(yn_values)), max(max(xn_values), max(yn_values)))
    plot_values(xn_values, f"Valeurs de xn pour x0={x0}, y0={y0}, a={a}, b={b}", col1, xlim, ylim)
    plot_values(yn_values, f"Valeurs de yn pour x0={x0}, y0={y0}, a={a}, b={b}", col2, xlim, ylim)

    # Tracer la trajectoire (xn, yn)
    fig = go.Figure()
    # Ajouter un bouton pour activer/désactiver les flèches
    show_arrows = st.checkbox("Afficher les flèches", value=True)

    if show_arrows:
        # Couleur initiale
        color = 'red'

        # Ajouter la première flèche
        fig.add_trace(go.Scatter(x=[xn_values[0]], y=[yn_values[0]], mode='markers', marker=dict(size=8, color=color), name='marker 0'))

        # Ajouter les flèches suivantes avec une couleur différente à chaque fois
        for i in range(1, len(xn_values)):
            # Calculer la couleur de la flèche en fonction de l'itération
            color = f"rgba({(i*10)%255},{(i*50)%255},{(i*100)%255}, 0.7)"

            fig.add_trace(go.Scatter(x=[xn_values[i-1], xn_values[i]], y=[yn_values[i-1], yn_values[i]],
                         mode='lines', line=dict(color=color), name='marker {}'.format(i)))
            fig.add_trace(go.Scatter(x=[xn_values[i]], y=[yn_values[i]], mode='markers',
                         marker=dict(size=8, color=color), name='line {}'.format(i)))

        fig.update_layout(title=f"Trajectoire de (xn, yn) pour x0={x0:.2f}, y0={y0:.2f}, a={a:.2f}, b={b:.2f}",
                        xaxis_title="xn", yaxis_title="yn", width=800, height=700)
    else:
        # Couleur initiale
        color = 'red'

        # Ajouter la première flèche
        fig.add_trace(go.Scatter(x=[xn_values[0]], y=[yn_values[0]], mode='markers', marker=dict(size=8, color=color), name='marker 0'))
        
        # Ajouter les flèches suivantes avec une couleur différente à chaque fois
        for i in range(1, len(xn_values)):
            # Calculer la couleur de la flèche en fonction de l'itération
            color = f"rgba({(i*10)%255},{(i*50)%255},{(i*100)%255}, 0.7)"

            fig.add_trace(go.Scatter(x=[xn_values[i]], y=[yn_values[i]], mode='markers', 
                                     marker=dict(size=8, color=color), name='marker {}'.format(i)))

        fig.update_layout(title=f"Trajectoire de (xn, yn) pour x0={x0:.2f}, y0={y0:.2f}, a={a:.2f}, b={b:.2f}",
                        xaxis_title="xn", yaxis_title="yn", width=800, height=700)
    st.plotly_chart(fig)





if __name__ == "__main__":
    main()
