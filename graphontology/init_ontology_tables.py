from graphontology.utils.common_utils import import_mysql_from_dump, verify_table_existence
import argparse, glob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump', type=str, required=True, help="Path of uncompressed MySQL dump file.")
    args = parser.parse_args()

    # Execute CREATE TABLE statements first
    import_mysql_from_dump(f"{args.dump}/CREATE_TABLEs.sql")

    # Fetch entire tree of SQL dumps (recursively)
    sql_file_tree = glob.glob(f"{args.dump}/**/*.sql", recursive=True)

    # Exclude CREATE TABLE statements
    sql_file_tree = sorted([f for f in sql_file_tree if 'CREATE_TABLEs.sql' not in f])

    # Print all files to process
    for k, sql_file in enumerate(sql_file_tree):
        print(f"Importing SQL file {k + 1}/{len(sql_file_tree)}: {sql_file.split('/')[-1]} ...")
        import_mysql_from_dump(sql_file)

    # Success
    print('All SQL files were imported successfully.')
    
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

if __name__ == "__main__":
    main()