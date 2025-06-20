from db_cache_manager.db import DB
from graphontology.utils.config import config
from graphontology.definitions import DATA_DIR
from collections import defaultdict
import os
import json


full_tree_query = """
SELECT f.to_id AS level0_category_id, g.to_id AS level1_category_id, a.to_id AS level2_category_id,
       b.to_id AS level3_category_id, b.from_id AS level4_category_id,
	   c.to_id AS cluster_id, d.to_id AS concept_id, e.name AS name
    FROM graph_ontology.Edges_N_Category_N_Category_T_ChildToParent f
    INNER JOIN graph_ontology.Edges_N_Category_N_Category_T_ChildToParent g
    INNER JOIN graph_ontology.Edges_N_Category_N_Category_T_ChildToParent a
    INNER JOIN graph_ontology.Edges_N_Category_N_Category_T_ChildToParent b
    INNER JOIN graph_ontology.Edges_N_Category_N_ConceptsCluster_T_ParentToChild c
    INNER JOIN graph_ontology.Edges_N_ConceptsCluster_N_Concept_T_ParentToChild d
    INNER JOIN graph_ontology.Nodes_N_Concept e
    ON f.from_id=g.to_id AND g.from_id=a.to_id AND a.from_id=b.to_id AND b.from_id=c.from_id AND c.to_id=d.from_id AND d.to_id=e.id;
"""


def generate_tree_json():
    db_man = DB(config['database'])
    data = db_man.execute_query(full_tree_query)
    data = [
        {
            "category_name_0": entry[0],
            "category_name_1": entry[1],
            "category_name_2": entry[2],
            "category_name_3": entry[3],
            "category_name_4": entry[4],
            "cluster_id": entry[5],
            "concept_id": entry[6],
            "concept_name": entry[7]
        }
        for entry in data
    ]

    # Create nested defaultdicts
    def nested_dict():
        return defaultdict(nested_dict)

    nested = nested_dict()

    # Populate the nested structure
    for entry in data:
        c0 = entry["category_name_0"]
        c1 = entry["category_name_1"]
        c2 = entry["category_name_2"]
        c3 = entry["category_name_3"]
        c4 = entry["category_name_4"]
        cluster = entry["cluster_id"]
        concept = entry["concept_name"]

        concepts = nested[c0][c1][c2][c3][c4].setdefault(cluster, [])
        concepts.append(concept)

    # Convert defaultdict to normal dict for output
    def to_dict(d):
        if isinstance(d, defaultdict):
            return {k: to_dict(v) for k, v in d.items()}
        return d

    nested_dict_output = to_dict(nested)
    with open(os.path.join(DATA_DIR, 'ontology_structure.json'), 'w') as f:
        json.dump(nested_dict_output, f)


if __name__ == '__main__':
    generate_tree_json()
