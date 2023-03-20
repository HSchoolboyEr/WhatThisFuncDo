import igraph
import os
import pandas as pd
import math


def get_graph_features(raw_cfg):
    graph_all_item_char = []
    for graph_item_in_gml in raw_cfg:
        try:
            os.remove("/tmp/gml.gml")
        except FileNotFoundError:
            pass

        with open("/tmp/gml.gml", "a") as bibfile:
            for line in graph_item_in_gml:
                bibfile.writelines(line)
        try:
            g = igraph.read("/tmp/gml.gml")
        except igraph._igraph.InternalError:
            raise AttributeError('Incorrect QML format')    
        finally:
            os.remove("/tmp/gml.gml")
        graph_one_item_char = []
        graph_one_item_char.append(0 if (pd.isna(g.vcount())) else g.vcount())
        # graph_one_item_char.append( 0 if (pd.isna(g.degree(0))) else g.degree(0))
        graph_one_item_char.append(0 if (pd.isna(g.diameter())) else g.diameter())
        graph_one_item_char.append(g.girth() if (not (pd.isna(g.girth())) and not(math.isinf(g.girth()))) else 0)  # inf
        graph_one_item_char.append(0 if (pd.isna(g.radius())) else g.radius())
        graph_one_item_char.append(0 if (pd.isna(g.average_path_length())) else g.average_path_length())
        graph_one_item_char.append(0 if (pd.isna(g.transitivity_avglocal_undirected())) else g.transitivity_avglocal_undirected())
        graph_all_item_char.append(graph_one_item_char)

    return graph_all_item_char
