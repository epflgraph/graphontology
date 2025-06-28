# Proposing changes to the ontology

While the current stable version of the ontology is the result of many rounds of iterative, semi-manual improvement,
some of its concepts may still be assigned to a suboptimal or even outright wrong category.
This document provides the format for proposing changes to the ontology through the creation of GitHub Issues on this repository.

## Using GraphAI to modify the ontology

Making arbitrary changes to the ontology is highly discouraged. The best way to figure out how to optimally change things is 
through the GraphAI ontology endpoints. Through these endpoints you can:

* Break up clusters
* Reassign clusters (whether existing ones or simply lists of concepts obtained by breaking up a cluster) to a different category
* Assign a new concept to the appropriate category and cluster

None of these endpoints actually change the ontology. What they do is present you with the closest category to a concept 
or set of concepts, and the best alternative sub-groupings of a set of concepts.

Through the SQL queries found in the `queries` subfolder in the root folder of this repository, you can 
make changes to your local version of the ontology, assuming you have loaded the dumps into a local database. 
These queries cover every case:
* Adding a new concept to an existing cluster
* Adding a new concept to a new cluster within a given category
* Splitting a set of concepts from their cluster and reassigning them to a new category
* Reassigning an entire cluster to a different category
* Even adding new depth 4 or 3 categories

These changes would, obviously, be made to your local version, and would decouple it from the official one.
If you would like your changes to be made to the reference version of the ontology, follow the instructions in the 
next section.

## Proposing modifications

If you have modifications to propose for the reference ontology, follow these steps.
1. Create an Issue on this repo, titled "Ontology modification proposal - DATE", where DATE is the current date. For example,
"ontology modification proposal - 2025-06-03".
2. Add a description justifying why you would like these modifications to be made. **Make sure your justification is
strong, otherwise your proposal would be rejected!**
3. Propose your desired modifications as a list.

Five types of modification are permitted:
* [ADD]: Add a concept.
* [REMOVE]: Remove a concept entirely.
* [SPLIT]: Split a cluster, move a subset of its concepts to another category.
**The provided concepts must all be in the same cluster**.
* [MOVE]: Move a cluster to another category.
* [MERGE]: Merge two clusters. **The two clusters must be in the same category**.

### Example of a modification proposal GitHub Issue

Here is an example detailing what information you should provide for each type of modification. The concepts,
clusters, and categories used are fictitious and are there simply for demonstration purposes: 

-----------------------------
Ontology modification proposal - 2025-06-03

We are an astrophysics research center, and as a research scientist in the center I went through the 
ontology and found there to be a few wrong assignments and a few missing concepts when it 
comes to telescopes. Also, I believe that one concept is too specific and has polluted the
parent category and would best be removed.

List of modifications:

[ADD]
* Concept: Telescope type 1
* Category: telescopes

[REMOVE]
* Concept: Telescope maintenance

[ADD]
* Concept: Telescope construction
* Cluster: 187

[MOVE]
* Cluster: 591
* Category: space-travel

[SPLIT]
* Concepts:
   * Telescope type 2
   * Telescope type 3
   * Telescope type 8
* Category: telescopes

[MERGE]
* Clusters:
   * 221
   * 198

-----------------------------

If all the modifications proposed above are accepted, the following changes will be made to the ontology:
* "Telescope type 1" will be added to a **new cluster** in the category "telescopes".
* "Telescope maintenance" will be removed from the ontology.
* "Telescope construction" will be added to existing cluster "187" (in whatever category "187" is attached to).
* Cluster "591" will be detached from its current category and attached to the category "space-travel".
* "Telescope type 2", "Telescope type 3", and "Telescope type 8" will be detached from their current cluster and 
category, and added to a new cluster in the category "telescopes". **This will be rejected if the three concepts 
aren't in the same cluster to begin with**.
* Clusters "221" and "198" will be merged. **This will be rejected if the 
two clusters are not attached to the same category**.
