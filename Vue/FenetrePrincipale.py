
import plotly.graph_objs as go
import plotly

import networkx as nx

# TODO : Afficher le résultat dans une fenêtre Tkinter

class FenetrePrincipale:

    def FPafficherReseau(self, _reseau, _name):

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

        plotly.offline.plot(fig, filename=_name + '.html')
