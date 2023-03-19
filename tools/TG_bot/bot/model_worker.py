import pickle
import os
import io
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from lightgbm import LGBMClassifier
import scipy.sparse as sparse
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from tools.raw_data_prepare.graph_preparator import get_graph_features
from collections import Counter
import seaborn as sns
# import matplotlib.pyplot as plt
import asyncio
from settings import DEFAULT_MODEL_NAME, logger


async def predict_class_in_text(raw_assm_and_cfg):
    # get asm raw code and cfg data in separate lists
    raw_assm_text, cfg_assm, instr_count = zip(*[(x[0], x[1], len(x[0])) for x in raw_assm_and_cfg])
    # get instaructins count and put it to DataFrame
    instructions_count = pd.DataFrame(instr_count, columns=["inst_count"])
    # clean code and put it to DataFrame
    asm_cod = pd.DataFrame(clean_raw_asm_code(raw_assm_text), columns=["code"])
    # get graph characteristics and put them to DataFrame
    graph_dada = pd.DataFrame(get_graph_features(cfg_assm), columns=["vcount", "diameter", "girth", "radius", "average_path_length", "transitivity_avglocal_undirected"])
    # concatenate all data
    all_dataframe = pd.concat((instructions_count, asm_cod, graph_dada), axis=1)

    model         = pickle.load(open(os.path.join(os.path.dirname(__file__), '../../../models_pickle/{}.pkl'.format(DEFAULT_MODEL_NAME)), 'rb'))
    tfidf_coder   = pickle.load(open(os.path.join(os.path.dirname(__file__), '../../../models_pickle/data_transformers/tfidf_1_3.pkl'), 'rb'))
    label_encoder = pickle.load(open(os.path.join(os.path.dirname(__file__), '../../../models_pickle/data_transformers/label_encoder.pkl'), 'rb'))
    
    transformed_data = tfidf_coder.transform(all_dataframe["code"])

    X_sparse = sparse.hstack((sparse.csr_matrix(transformed_data),
                               all_dataframe[["vcount", "diameter", "girth", "radius", "average_path_length", "transitivity_avglocal_undirected"]]))
                               #  , instructions_count["inst_count"] ))
    counter = Counter(label_encoder.inverse_transform(model.predict(X_sparse)))

    return (counter)


def clean_raw_asm_code(raw_code: list) -> list:
    # clean raw asm code
    # TODO: 1. remove "'" and ather artefacts 
    #       2. Replace this code to raw_data_prepare module
    func_body = []
    for line in raw_code:
        func_body.append(str([elem.strip() for elem in line.split("\n")]))
    logger.info("Cleaned {} functions".format(len(func_body)))
    return func_body


async def predict_class_in_photo(raw_assm_and_cfg, title_photo=""):
    data_for_plot = await predict_class_in_text(raw_assm_and_cfg)
    key_list = [key for key, _ in data_for_plot.most_common(8)]
    val_list = [val for _, val in data_for_plot.most_common(8)]

    swarm_plot = sns.barplot(x=key_list, y=val_list)
    swarm_plot.set_title(title_photo)
    sns.despine(offset=10, trim=True)
      
    buf = io.BytesIO()
    fig = swarm_plot.get_figure()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()
