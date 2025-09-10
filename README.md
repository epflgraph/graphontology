# GraphOntology

This repository is dedicated to EPFLGraph's GraphOntology, the tree of knowledge
comprised of over 40,000 Wikipedia pages. The scripts and queries within this 
repo allow you to:
1. Load and view the ontology.
2. Run the ontology endpoints on [GraphAI](https://github.com/epflgraph/graphai) -- useful if you are running a local instance of GraphAI.
3. Modify the ontology locally.
4. Propose changes to the original ontology using GitHub Issues.

## Setup

To be able to use the scripts in the repo, first install `graphontology` using `pip install .` or 
`pip install -e .` if editable mode is desired.

Now create a `config.ini` file in the same root directory that looks like the following:
```
[elasticsearch]
host: localhost
port: 9201
username: esuser
password: espass
cafile: /path/to/es/cafile.crt

[database]
host: localhost
port: 23306
user: mysqluser
password: mysqlpass
```
Now you are ready to run any of the scripts. **To prepare the database and Elasticsearch indexes for 
a local instance of GraphAI, follow these loading instructions.**

### Loading the ontology for GraphAI

If you plan to run a local instance of GraphAI, for the `/ontology` endpoints 
to be enabled you need to have the ontology's tables in your database.

These tables should be in the database `graph_ontology`, and consist of the following tables:
```
Nodes_N_Concept
Nodes_N_Category
Edges_N_Concept_N_Concept_T_Undirected
Edges_N_ConceptsCluster_N_Concept_T_ParentToChild
Edges_N_Category_N_ConceptsCluster_T_ParentToChild
Edges_N_Category_N_Category_T_ChildToParent
Edges_N_Category_N_Concept_T_AnchorPage
Edges_N_Concept_N_Concept_T_Embeddings
```

The [GraphOntology data dump](https://zenodo.org/records/15726975) contains all of these.

In order to load them into your local database, download the dump, decompress it, and run the following:
```
python init_ontology_tables.py --dump /path/to/dump
```

or, if running as a module, run from the root folder:
```
python -m graphontology.init_ontology_tables --dump /path/to/dump
```

The script will automatically check whether you got everything imported correctly and let you know 
if something has gone wrong.

### Loading the concept detection index for GraphAI
The concept detection index is a [compressed dump](https://drive.google.com/file/d/1U9K_QmKLTMOu4qYevZmp04icmUiwjtZW/view?usp=sharing) of the `concepts_detection` index used by GraphAI's `/text` endpoints, created using [Elasticdump](https://github.com/elasticsearch-dump/elasticsearch-dump). It is a tar.gz file containing a folder with three JSON dumps: one for the analyzer, one for the mapping, and one for the data.

To restore them (assuming your ES server is running on, or mapped to, localhost:9201 and secured with authentication), first install elasticdump according to the [instructions](https://github.com/elasticsearch-dump/elasticsearch-dump/blob/master/README.md), then run:
```
elasticdump \
  --input=~/concepts_detection/concepts_detection_mapping.json \
  --output=https://YOURUSERNAME:YOURPASSWORD@127.0.0.1:9201/concepts_detection \
  --type=mapping
elasticdump \
  --input=~/concepts_detection/concepts_detection_analyzer.json \
  --output=https://YOURUSERNAME:YOURPASSWORD@127.0.0.1:9201/concepts_detection \
  --type=analyzer
elasticdump \
  --input=~/concepts_detection/concepts_detection_data.json \
  --output=https://YOURUSERNAME:YOURPASSWORD@127.0.0.1:9201/concepts_detection \
  --type=data
```

Be patient as the import may take a while (the data contains over 1.5 million documents, which are the concepts).

## Proposing changes to the ontology
If you want to propose modifications to the ontology, refer to the README file in the `data` subfolder.
