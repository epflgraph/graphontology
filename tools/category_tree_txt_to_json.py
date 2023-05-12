#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, json

# Check number of input arguments and display syntax
if len(sys.argv)!=3:
	print('Syntax: python category_tree_txt_to_json.py input.txt output.json')
	exit(-1)

# Get input and output file paths from arguments
InputFilePath  = sys.argv[1]
OutputFilePath = sys.argv[2]

# Initialise category tree dictionary
CategoryTree = dict()

# Open input file for reading
with open(InputFilePath) as fid:

	# Loop over all tree branches and leafs
	for line in fid.read().split('\n'):
		
		# Decompose text line into category parameters
		Match = re.findall(r'(\s*.*)\[(.*)\](\{(.*)\}\{(.*)\})?$', line)
		
		# Is there a regex match?
		if len(Match)>0:
		
			# Extract category parameters from regex match
			[CategoryString, Permalink, Dummy, ShortDescription, LongDescription] = Match[0]

			# Parse category name, calculate category depth, and generate category ID
			CategoryString = CategoryString.rstrip()
			CategoryDepth  = int((len(CategoryString)-len(CategoryString.lstrip()))/4)
			CategoryName   = CategoryString.lstrip()
			CategoryID     = CategoryName.lower().replace(' ', '-').replace(':', '-').replace('/', '-').replace('(', '-').replace(')', '-').replace('--', '-')

			# Create dictionary item to add as branch or leaf
			DictItem = {CategoryID : {
							'name'              : CategoryName,
							'depth'             : CategoryDepth,
							'permalink'         : Permalink,
							'short_description' : ShortDescription,
							'long_description'  : LongDescription,
							'children'          : {}
						}}

			# Append category or leaf to correct branch level
			if CategoryDepth==0:
				CategoryTree.update(DictItem)
				c0 = CategoryID

			elif CategoryDepth==1:
				CategoryTree[c0]['children'].update(DictItem)
				c1 = CategoryID

			elif CategoryDepth==2:
				CategoryTree[c0]['children'][c1]['children'].update(DictItem)
				c2 = CategoryID

			elif CategoryDepth==3:
				CategoryTree[c0]['children'][c1]['children'][c2]['children'].update(DictItem)
				c3 = CategoryID

			elif CategoryDepth==4:
				CategoryTree[c0]['children'][c1]['children'][c2]['children'][c3]['children'].update(DictItem)
				c4 = CategoryID

			elif CategoryDepth==5:
				CategoryTree[c0]['children'][c1]['children'][c2]['children'][c3]['children'][c4]['children'].update(DictItem)
				c5 = CategoryID

	# END OF LOOP

# Write category tree to output JSON file
with open(OutputFilePath, 'w') as fid:
	fid.write(json.dumps(CategoryTree, indent=4))

# Exit with success
exit(0)
