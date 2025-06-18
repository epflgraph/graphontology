import json
import os
from db_cache_manager.db import DB
from graphontology.utils.config import config
from graphontology.definitions import DATA_DIR


def create_category_node_table():
    db_manager = DB(config['database'])
    drop_query = "DROP TABLE IF EXISTS `graph_ontology`.`Nodes_N_Category`;"
    create_query = """
    CREATE TABLE `graph_ontology`.`Nodes_N_Category` (
      `institution_id` enum('Ont','EPFL','ETHZ','PSI','Empa','Eawag','WSL') COLLATE utf8mb4_unicode_ci default 'Ont',
      `object_type` enum('Category','Chart','Concept','Course','Dashboard','Exercise','External person','Hardware','Historical figure','Lecture','Learning module','MOOC','News','Notebook','Person','Publication','Specialisation','Startup','Strategic area','StudyPlan','Unit','Widget') COLLATE utf8mb4_unicode_ci DEFAULT 'Category',
      `object_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `depth` int unsigned NOT NULL,
      `reference_page_id` int unsigned NOT NULL,
      `reference_page_key` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `reference_page_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `row_id` int NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`id`),
      UNIQUE KEY `row_id` (`row_id`),
      KEY `name` (`name`),
      KEY `depth` (`depth`),
      KEY `anchor_page_id` (`reference_page_id`),
      KEY `anchor_page_key` (`reference_page_key`),
      KEY `institution_id` (`institution_id`),
      KEY `object_type` (`object_type`),
      KEY `object_id` (`object_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2231 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    try:
        db_manager.execute_query(drop_query)
        db_manager.execute_query(create_query)
        return True
    except Exception:
        return False


def create_category_edge_table():
    db_manager = DB(config['database'])
    drop_query = "DROP TABLE IF EXISTS `graph_ontology`.`Edges_N_Category_N_Category_T_ChildToParent`;"
    create_query = """
    CREATE TABLE `graph_ontology`.`Edges_N_Category_N_Category_T_ChildToParent` (
      `from_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `to_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `row_id` int NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`from_id`,`to_id`),
      UNIQUE KEY `row_id` (`row_id`),
      KEY `from_id` (`from_id`),
      KEY `to_id` (`to_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2227 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    try:
        db_manager.execute_query(drop_query)
        db_manager.execute_query(create_query)
        return True
    except Exception:
        return False


def create_category_cluster_edge_table():
    db_manager = DB(config['database'])
    drop_query = "DROP TABLE IF EXISTS `graph_ontology`.`Edges_N_Category_N_ConceptsCluster_T_ParentToChild`;"
    create_query = """
    CREATE TABLE `graph_ontology`.`Edges_N_Category_N_ConceptsCluster_T_ParentToChild` (
      `from_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `to_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `row_id` int NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`from_id`,`to_id`),
      UNIQUE KEY `row_id` (`row_id`),
      KEY `from_id` (`from_id`),
      KEY `to_id` (`to_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=4814 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    try:
        db_manager.execute_query(drop_query)
        db_manager.execute_query(create_query)
        return True
    except Exception:
        return False


def create_cluster_concept_edge_table():
    db_manager = DB(config['database'])
    drop_query = "DROP TABLE IF EXISTS `graph_ontology`.`Edges_N_ConceptsCluster_N_Concept_T_ParentToChild`;"
    create_query = """
    CREATE TABLE `graph_ontology`.`Edges_N_ConceptsCluster_N_Concept_T_ParentToChild` (
      `from_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `to_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `row_id` int NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`from_id`,`to_id`),
      UNIQUE KEY `row_id` (`row_id`),
      KEY `from_id` (`from_id`),
      KEY `to_id` (`to_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=40064 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    try:
        db_manager.execute_query(drop_query)
        db_manager.execute_query(create_query)
        return True
    except Exception:
        return False


def create_concept_node_table():
    db_manager = DB(config['database'])
    drop_query = "DROP TABLE IF EXISTS `graph_ontology`.`Nodes_N_Concept`;"
    create_query = """
    CREATE TABLE `graph_ontology`.`Nodes_N_Concept` (
      `institution_id` enum('Ont','EPFL','ETHZ','PSI','Empa','Eawag','WSL') COLLATE utf8mb4_unicode_ci DEFAULT 'Ont',
      `object_type` enum('Category','Chart','Concept','Course','Dashboard','Exercise','External person','Hardware','Historical figure','Lecture','Learning module','MOOC','News','Notebook','Person','Publication','Specialisation','Startup','Strategic area','StudyPlan','Unit','Widget') COLLATE utf8mb4_unicode_ci DEFAULT 'Concept',
      `object_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
      `id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
      `is_ontology_category` tinyint(1) NOT NULL,
      `is_ontology_concept` tinyint(1) NOT NULL,
      `is_ontology_neighbour` tinyint(1) NOT NULL,
      `is_noise` tinyint(1) NOT NULL DEFAULT '0',
      `is_unused` tinyint(1) NOT NULL,
      `row_id` int NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`id`),
      UNIQUE KEY `row_id` (`row_id`),
      KEY `name` (`name`),
      KEY `is_ontology_category` (`is_ontology_category`),
      KEY `is_ontology_concept` (`is_ontology_concept`),
      KEY `is_ontology_neighbour` (`is_ontology_neighbour`),
      KEY `is_unused` (`is_unused`),
      KEY `is_noise` (`is_noise`),
      KEY `institution_id` (`institution_id`),
      KEY `object_type` (`object_type`),
      KEY `object_id` (`object_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=6234605 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    try:
        db_manager.execute_query(drop_query)
        db_manager.execute_query(create_query)
        return True
    except Exception:
        return False


def init_ontology_tree():
    with open(os.path.join(DATA_DIR, 'ontology_structure.json'), 'r') as f:
        tree_contents = json.load(f)
    create_category_node_table()
    create_category_edge_table()
    create_category_cluster_edge_table()
    create_cluster_concept_edge_table()
    create_concept_node_table()
    # TODO add the actual loading of tables from the JSON
