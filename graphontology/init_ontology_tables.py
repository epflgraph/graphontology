from graphontology.utils.init_ontology_tree import init_ontology_tree
from graphontology.utils.common_utils import import_mysql_from_dump, verify_table_existence
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump', type=str, default=None)
    args = parser.parse_args()
    if args.dump is None:
        print('WARNING: No dump file provided. Only ontology tree tables will be loaded. '
              'GraphAI ontology endpoints will not work.')
        init_ontology_tree()
    else:
        import_mysql_from_dump(args.dump)
        # Dump-specific existence checks
        embedding_exists = verify_table_existence('Edges_N_Concept_N_Concept_T_Embeddings')
        if not embedding_exists:
            print('WARNING: Concept to concept embedding similarity table not found. Closest match algorithms '
                  'in ontology endpoints will not be able to use embeddings.')
    concept_node_exists = verify_table_existence('Nodes_N_Concept')
    category_node_exists = verify_table_existence('Nodes_N_Category')
    concept_concept_edge_exists = verify_table_existence('Edges_N_Concept_N_Concept_T_Undirected')
    concept_cluster_edge_exists = verify_table_existence('Edges_N_ConceptsCluster_N_Concept_T_ParentToChild')
    cluster_category_edge_exists = verify_table_existence('Edges_N_Category_N_ConceptsCluster_T_ParentToChild')
    category_category_edge_exists = verify_table_existence('Edges_N_Category_N_Category_T_ChildToParent')
    category_concept_anchor_edge_exists = verify_table_existence('Edges_N_Category_N_Concept_T_AnchorPage')
    if not all([concept_node_exists,
                category_node_exists,
                concept_concept_edge_exists,
                concept_cluster_edge_exists,
                cluster_category_edge_exists,
                category_category_edge_exists,
                category_concept_anchor_edge_exists]):
        print('ERROR: Missing table(s) due to nonexistent or incomplete dump or a botched loading process. '
              'GraphAI ontology endpoints will not function properly.')


