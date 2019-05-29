import random
from inspect import signature
from math import floor;
from random import shuffle

def arity(func):
	"""Returns the arity or number of parameters of a function"""
	sig = signature(func);
	params = sig.parameters
	return len(params);

def add(a,b):
	"""returns the sum of two numbers"""
	return a+b;
def multiply(a,b):
	"""returns the product of two numbers"""
	return a*b;
def divide(a,b):
	"""returns the quotient of two numbers"""
	if b==0:
		return 0;
	else:
		return a/b;
def subtract(a,b):
	"""returns the difference of two numbers"""
	return a-b;
	

def choose_random_element(set):
	"""returns a random element in the given set"""
	index= random.randint(0,len(set)-1);
	return set[index];

def gen_random_expr(func_set,term_set,max_d,method):
	"""Generates a random prefix expression
		func_set is the set of functions
		term_set is the set of terms
		max_d is the max height of the tree
		method takes on two values grow or full.
		These affect the method in which the trees are created
	"""
	expr=[];
	func=None;
	if max_d==0 or (method=="grow" and random.random()<(len(term_set)/(len(term_set)+len(func_set)))): # the following is adopted from pseudocode from 
		expr= [choose_random_element(term_set)];
	else:
		func=choose_random_element(func_set);
		args=[];
		for i in range(0,arity(func)):
			args=args+gen_random_expr(func_set,term_set,max_d-1,method);
		expr=expr+[func.__name__];
		expr=expr+args;
	return expr;
class Node:
	def __init__(self,data=None,children=[]):
		self.data=data; #inilitzies data to None and children to empty vector if no parameters are specificed
		self.children=children;
	def getChildren(self):
		return self.children; #returns the  array of children
	def setChildren(self,children):
		self.children=children; #sets the children to the specified list;
	def getData(self):
		return self.data
	def setData(self,data):
		self.data=data;
	

def prefix_add(str,starting_index,term_set,func_map):
	"""Converts the prefix expression from gen_random_expr into an expression tree"""
	if starting_index>=len(str): #This is in the case where the starting_index exceeds the array. This case should not happen but just in case
		return None,-1; 
  
	a=str[starting_index]; #gets the element corrsponding to the starting index
 
	if a in term_set: #base case where the node is contains a term
		return Node(a),starting_index; 
         
	func=func_map[a];
		
	new_index=starting_index # temporary variables
	new_node= Node(a);
	children=[];
	new_q=None;
	for i in range(arity(func)): #creates tree out of the operands and makes them children
		new_child,new_q = prefix_add(str, new_index + 1,term_set,func_map); 
		children.append(new_child);
		new_index=new_q;

	new_node.setChildren(children); #sets the children array
	return new_node,new_q; 



def preorder(root):
	"""standard preorder traversal, mostly used for testing purposes"""
	if root!=None:
		#print(root);
		print(root.data);
		print();
		for i in range(len(root.children)):
			preorder(root.children[i]);
def inorder(root):
	"""standard inorder traversal, mostly used for testing purposes"""
	if root!=None:
		#print(root);
		if len(root.children)==2:
			inorder(root.children[0])
			print(root.data);
			print();
			inorder(root.children[1]);
		else:
			print(root.data);
			print();
			
			
		
# #The following is test code and can be ignored
func_set=[add,subtract,divide,multiply];
term_set=['a','b','c','d'];

#str=gen_random_expr(func_set,term_set,3,'full');
str=['subtract', 'a', 'divide', 'c', 'a'];
func_map={func.__name__:func for func in func_set};
starting_index=0;
print(str,"\n");
root,_=prefix_add(str,starting_index,term_set,func_map);
# #print(root.data)
# inorder(root);

def initial_population(population_size,term_set,func_set,max_d):
	""" Creates a population specified by population size using the 
	ramped half and half distribution i.e.
	using the grow method o generation for 
	half the population and the full method 
	for the other half"""
	mid=floor(population_size/2); #find roughly half the population
	population=[];# the empty population
	func_map={func.__name__:func for func in func_set};
	for i in range(mid):
		str=gen_random_expr(func_set,term_set,max_d,'grow'); # creates a tree using the grow method
		root,_=prefix_add(str,0,term_set,func_map);
		population.append(root);
	for i in range(mid+1,population_size):
		str=gen_random_expr(func_set,term_set,max_d,'full'); # creates a tree using the full method
		root,_=prefix_add(str,0,term_set,func_map);
		population.append(root);
	return population;

def tree2array(root):
	"""converts an tree to an array in prefix order"""
	array=[root];
	
	for i in range(len(root.children)):
		array=array+tree2array(root.children[i]);
	return array;
	
def point_mutation(root,func_set,term_set):
	"""creates a point mutation in the given tree. This code is very nasty
	and may not be the best in terms of time complexity may need to revise
	later"""
	array=tree2array(root); #gets the tree as an array
	node2change=random.choice(array); # selects a random node to be changed
	func_map={func.__name__:func for func in func_set} #gets the functions as a hash map
	data=node2change.getData(); # gets the data stored in the random node
	if data in func_map: #test if the data is a function or not
		func=func_map[data]; #gets the function that corresponds to the string in data
		shuffle(func_set);	#randomizes the function set
		if len(func_set)>1 and func_set[0]==func: #if the function in the first element in the array sets to the second element
			node2change.setData(func_set[1].__name__);	
		else:
			node2change.setData(func_set[0].__name__); # otherwise it sets to the first element in th3 shuffled array
	else:
		shuffle(term_set); #Does a very similar procedure but for the case where a node contains a term
		if len(term_set)>1 and term_set[0]==data:
			node2change.setData(term_set[1]);
		else:
			node2change.setData(term_set[0]);

		