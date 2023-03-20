import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from tools.raw_data_prepare.graph_preparator import get_graph_features


def test_get_correct_graph_features():
    with open( os.path.join(os.path.dirname(__file__), 'positive_example.gml'), 'r') as pe:
        test_qraph = pe.readlines()
    text = str([*test_qraph])
    text = ' '.join(text.split(","))
    text = text.replace(r"\n", "\n")
    text = text.replace('\'', '') 
    assert [[28, 12, 3, 0, 4.302267002518891, 0.33928571428571425]] == get_graph_features([text[1:-1]])

def test_correct_parse_gml_file():
    with open( os.path.join(os.path.dirname(__file__), 'negative_example.gml'), 'r') as pe:
        test_qraph = pe.readlines()
    text = str([*test_qraph])
    text = ' '.join(text.split(","))
    text = text.replace(r"\n", "\n")
    text = text.replace('\'', '') 
    with pytest.raises(AttributeError):
        get_graph_features([text[1:-1]])