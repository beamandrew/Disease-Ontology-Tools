import sys
import argparse

class OBONode():
	def __init__(self):
		self.UMLSCUI  = None
		self.DOID     = None
		self.is_a     = None
		self.MESH     = None
		self.name     = None
		self.alt_ids  = None
		self.synonyms = None

def start_of_new_term(line):
	return "[Term]" in line

def end_of_terms(line):
	return "[Typedef]" in line

def get_DOID(term_info):
	for line in term_info:
		if line[0:3] == "id:":
			return line.rstrip().split("DOID:")[-1]

def get_UMLSCUI(term_info):
	cuis = []
	for line in term_info:
		if line[0:15] == "xref: UMLS_CUI:":
			cuis.append(line.rstrip().split("UMLS_CUI:")[-1])
	return cuis

def get_is_a(term_info):
	is_a = []
	for line in term_info:
		if line[0:5] == "is_a:":
			is_a.append(line.rstrip().split(" ! ")[-1].lower())
	return is_a

def get_MESH(term_info):
	m = []
	for line in term_info:
		if line[0:10] == "xref: MSH:":
			m.append(line.rstrip().split("MSH:")[-1])
	return m

def get_name(term_info):
	for line in term_info:
		if line[0:5] == "name:":
			return line.rstrip().split(": ")[-1].lower()

def get_alt_ids(term_info):
	ids = []
	for line in term_info:
		if line[0:7] == "alt_id:":
			ids.append(line.rstrip().split(": ")[-1])
	return ids

def get_synonyms(term_info):
	syns = []
	for line in term_info:
		if line[0:8] == "synonym:" and "EXACT" in line:
			syns.append(line.rstrip().split("\"")[1].lower())
	return syns

def is_obsolete(term_info):
	for line in term_info:
		if "is_obsolete: true" in line:
			return True
	return False

def parse_term_info(term_info):
	N          = OBONode()
	N.UMLSCUI  = get_UMLSCUI(term_info)
	N.DOID     = get_DOID(term_info)
	N.is_a     = get_is_a(term_info)
	N.MESH     = get_MESH(term_info)
	N.name     = get_name(term_info)
	N.alt_ids  = get_alt_ids(term_info)
	N.synonyms = get_synonyms(term_info)
	return N

def parse_DO_obo(obo_file):
	obo       = []
	started   = False
	term_info = []
	inputOboFile = open(obo_file, 'r')
	for line in inputOboFile:
		# after we read the last term block, we need to know to stop
		# since we will not see another [Term] to indicate when to stop
		if end_of_terms(line):
			N = parse_term_info(term_info)
			obo.append(N)
			break
		# skip the file headers and lines until the first term
		while not start_of_new_term(line) and not started:
			line = next(inputOboFile)
		# until we see a new term start, collect the current term's info
		if not start_of_new_term(line) and started:
			term_info.append(line)
		# need an 'elif' instead of 'else' to deal with first term
		elif started:
			if not is_obsolete(term_info):
				N = parse_term_info(term_info)
				obo.append(N)
			term_info = []
		# will occur when we finish reading the headers and are ready to read
		# the first term
		else:
			started = True
	return obo

def parent_child_relationships(obo):
	# a key to a value is a "is_a" relationship propagating up the hierarchy
	# example: key = bacterial pneumonia, value = pnemonia
	# Many keys can map to the same value, and a value itself may serve as
	# a key to another value.
	# Any key may have multiple parents, o.is_a is a list
	parents_of = {}
	for o in obo:
		parents_of[o.name] = o.is_a

	# Any key may have multiple children (unless it's a leaf term)
	children_of = {}
	for k, vs in parents_of.iteritems():
		for v in vs:
			if v in children_of:
				children_of[v].append(k)
			else:
				children_of[v] = [k]

	return parents_of, children_of

def term_to_syns(obo):
	syns = {}
	for o in obo:
		syns[o.name] = o.synonyms
	return syns

def write_DOID_DB(obo, outfileName):
	outfile = open(outfileName, 'w')
	outfile.write("TERM\tDOID\n")
	for o in obo:
		outfile.write("\"{}\"\t\"DOID{}\"\n".format(o.name, o.DOID))
		for s in o.synonyms:
			outfile.write("\"{}\"\t\"DOID{}\"\n".format(s, o.DOID))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", required=True, help="The DO OBO file")
	parser.add_argument("-o", required=True, help="Output file")
	args = parser.parse_args()
	# returns a list of OBONodes
	utilities.announce("Parsing OBO")
	obo = parse_DO_obo(args.d)

	#write_DOID_DB(obo, args.o)










