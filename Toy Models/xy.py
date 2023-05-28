import numpy as np
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

# Fonction qui génère la liste xn et yn
def generate_values(x0, y0, a, b, n):
    xn = [x0]
    yn = [y0]
    for i in range(n):
        next_xn = yn[i] + 1 - a*xn[i]**2
        next_yn = b * xn[i]
        if abs(next_xn) > 1e+100 or abs(next_yn) > 1e+100:
            print("Les valeurs de xn ou yn sont devenues trop grandes. Arrêt de la génération.")
            break
        xn.append(next_xn)
        yn.append(next_yn)
    return xn, yn, list(range(len(xn)))


# Fonction pour tracer les valeurs (xn, n) ou (yn, n)
def plot_values(values, title, column, xlim, ylim):
    fig = go.Figure(go.Scatter(x=list(range(len(values))), y=values, mode='lines'))
    fig.update_layout(title=title, xaxis_title="Itération", yaxis_title="Valeurs", width=400, height=400)
    fig.update_xaxes(range=xlim)
    fig.update_yaxes(range=ylim)
    column.plotly_chart(fig)

# Fonction pour tracer la trajectoire de (xn, yn, n) en 3D
def plot_trajectory3D(xn_values, yn_values, n_values, title):
    color_scale = px.colors.sequential.Aggrnyl

    data = []
    for i in range(1, len(xn_values)):
        color = color_scale[int(np.interp(n_values[i], [n_values[0], n_values[-1]], [0, len(color_scale)-1]))]
        trace = go.Scatter3d(
            x=yn_values[i-1:i+1],
            y=n_values[i-1:i+1],
            z=xn_values[i-1:i+1],
            mode='lines',
            line=dict(color=color, width=2),
        )
        data.append(trace)

    trace2 = go.Scatter3d(
        x=yn_values,
        y=n_values,
        z=xn_values,
        mode='markers',
        marker=dict(
            size=4,
            color=n_values,  # set color to an array/list of desired values
            colorscale=color_scale,  # choose a colorscale
            opacity=0.7
        ),
        name='Points'
    )
    data.append(trace2)

    layout = go.Layout(
        scene=dict(xaxis_title='yn', yaxis_title='n', zaxis_title='xn'),
        width=1000,
        height=900,
        title=title
    )

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)
    




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

    # Générer les valeurs xn, yn et n
    xn_values, yn_values, n_values = generate_values(x0, y0, a, b, num_iterations)

    # Créer deux colonnes
    col1, col2 = st.columns(2)

    # Tracer les valeurs xn et yn côte à côte
    xlim = (0, num_iterations)
    ylim = (min(min(xn_values), min(yn_values)), max(max(xn_values), max(yn_values)))
    plot_values(xn_values, f"évolution de xn ", col1, xlim, ylim)
    plot_values(yn_values, f"évolution de yn ", col2, xlim, ylim)

    # Tracer la trajectoire (xn, yn)
    fig = go.Figure()
    # Ajouter un bouton pour activer/désactiver les flèches
    show_arrows = st.checkbox("Afficher les flèches", value=False)


    if show_arrows:
        # Créer une gamme de couleurs pour les flèches
        color_scale = px.colors.sequential.Aggrnyl

        # Ajouter la première flèche
        fig.add_trace(go.Scatter(x=[xn_values[0]], y=[yn_values[0]], mode='markers', marker=dict(size=8, color=color_scale[0]), name='marker 0'))

        # Ajouter les flèches suivantes avec une couleur différente à chaque fois
        for i in range(1, len(xn_values)):
            color = color_scale[int(i/len(xn_values)*len(color_scale))]

            fig.add_trace(go.Scatter(x=[xn_values[i-1], xn_values[i]], y=[yn_values[i-1], yn_values[i]],
                        mode='lines', line=dict(color=color), name='marker {}'.format(i)))
            fig.add_trace(go.Scatter(x=[xn_values[i]], y=[yn_values[i]], mode='markers',
                        marker=dict(size=8, color=color), name='line {}'.format(i)))

        fig.update_layout(title=f"Trajectoire de (xn, yn) pour",
                        xaxis_title="xn", yaxis_title="yn", width=800, height=700)
    else:
        # Créer une gamme de couleurs pour les flèches
        color_scale = px.colors.sequential.Aggrnyl

        # Ajouter la première flèche
        fig.add_trace(go.Scatter(x=[xn_values[0]], y=[yn_values[0]], mode='markers', marker=dict(size=8, color=color_scale[0]), name='marker 0'))
        
        # Ajouter les flèches suivantes avec une couleur différente à chaque fois
        for i in range(1, len(xn_values)):
            color = color_scale[int(i/len(xn_values)*len(color_scale))]

            fig.add_trace(go.Scatter(x=[xn_values[i]], y=[yn_values[i]], mode='markers', 
                                    marker=dict(size=8, color=color), name='marker {}'.format(i)))

        fig.update_layout(title=f"Trajectoire de (xn, yn)",
                        xaxis_title="xn", yaxis_title="yn", width=800, height=700)
    st.plotly_chart(fig)


    # Tracer la trajectoire 3D avec un sous-ensemble des points
    plot_trajectory3D(xn_values, yn_values, n_values, f"Trajectoire 3D de (xn, yn, n)")


if __name__ == "__main__":
    main()
