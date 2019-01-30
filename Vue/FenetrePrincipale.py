import os

import PyQt5
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

import plotly.graph_objs as go
import plotly

import networkx as nx

# TODO : Afficher le résultat dans une fenêtre
from Vue import fenetreprincipaledesign_ui


class FenetrePrincipale(QtWidgets.QMainWindow, fenetreprincipaledesign_ui.Ui_MainWindow):

    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        fenetreprincipaledesign_ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self._view = QWebEngineView()

        # Signaux
        # self.FPD_bouton_generer_reseau.coonect(self.FPDActiongenerer)

    def lancer(self):

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../donnees/reseau/reseau_000.html"))
        local_url = QUrl.fromLocalFile(file_path)

        self._view.load(local_url)

        self.FPD_layout_gauche_haut.addWidget(self._view)

    def FPafficherReseau(self, _reseau, _path, _name):

        _pos = nx.get_node_attributes(_reseau.R_graphe, 'pos')

        _dmin = 1
        _ncenter = 0
        for n in _pos:
            _x, _y = _pos[n]
            _d = (_x - 0.5) ** 2 + (_y - 0.5) ** 2
            if _d < _dmin:
                _ncenter = n
                _dmin = _d

        _p = nx.single_source_shortest_path_length(_reseau.R_graphe, _ncenter)



        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in _reseau.R_graphe.edges():
            x0, y0 = _reseau.R_graphe.node[edge[0]]['pos']
            x1, y1 = _reseau.R_graphe.node[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

        for node in _reseau.R_graphe.nodes():
            x, y = _reseau.R_graphe.node[node]['pos']
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        for node, adjacencies in enumerate(_reseau.R_graphe.adjacency()):
            node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = '# of connections: ' + str(len(adjacencies[1])) + '\n' + str(_reseau.R_graphe.node[node]['pos'])
            node_trace['text'] += tuple([node_info])

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='<br>Network graph made with Python',
                            titlefont=dict(size=16),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        html = plotly.offline.plot(fig, auto_open=False, output_type='div')
        html = """<html><head><meta charset="utf-8" /></head><body><script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>""" + \
                html + """<script type="text/javascript">window.addEventListener("resize", function(){Plotly.Plots.resize(document.getElementById("611e9c72-ed73-4e6f-b171-1737e84f4735"));});</script></body></html>"""

        _path = os.path.abspath(os.path.join(os.path.dirname(__file__), _path))
        if not os.path.exists(_path):
            os.makedirs(_path)
        with open(_path + "\\" + _name + ".html", 'w+') as f:
            f.write(html)
