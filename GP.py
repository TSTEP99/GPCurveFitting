import random;
from inspect import signature;
from math import floor;
from random import shuffle;
from copy import deepcopy;

def arity(func):
	"""Returns the arity or number of parameters of a function"""
	sig = signature(func);
	params = sig.parameters
	return len(params);
#the following four functions are primarily used for testing
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
#print(str,"\n");
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
	
def subtree_mutation(root,func_set,term_set,max_d):
	"""Creates a subtree mutation replacing part of 
	the tree with a randomly generated subtree"""
	new_d=random.randint(0,max_d); #generates a random height for the new subtree to be added may edit this to prevent subtrees of height 0
	func_map={func.__name__:func for func in func_set} #generates a function map
	
	method= "grow" if random.randint(0,1) else "full"; #randomly chooses whether to use "full" or "grow"
	str=gen_random_expr(func_set,term_set,new_d,method); # generates a random prefix expression
	new_node,_=prefix_add(str,0,term_set,func_map); #generates a new node for the random subtree
	array=tree2array(root); # gets the nodes of the original tree as a array using tree2array
	rand_root=random.choice(array); #randomly selects a node from the tree.
	rand_root.setChildren(new_node.getChildren()); #changes it values in the random node to match that of the new subtree.
	rand_root.setData(new_node.getData());
	
def tree_divider(root):
	"""divides the roots in an expression tree into two categories,
	internal nodes and leaves"""
	array=tree2array(root); #gets the roots into and array in prefix order
	functions=[]; #initlizes array for internal nodes
	leaves=[];#intilizes an array for leaves
	for i in range(len(array)): #Goes the array representation of the expression tree and places each node into its corresponding categories depending on whether or not they have children
		if not array[i].getChildren():
			leaves.append(array[i]);
		else:
			functions.append(array[i]);
		
	return functions,leaves; # returns a tuple of arrays

def crossover(parent1,parent2,func_set,term_set):
	"""Implements recombination by determining a random crossover point in parent
	and replacing with a subtree from parent2"""
	
	functions,leaves=tree_divider(parent1);  #divides the trees into two sets, internal nodes and leaves
	array=tree2array(parent2); #gets the ndoes in parent2 as an array
	
	rand_root=random.choice(array); # gets the nodes in rand_root and creates a deepcopy
	copy_root= deepcopy(rand_root);
	
	if random.random()<.9: # makes the crossover point a leaf or function as determined by the the probability determined  by J.R. Koza
		crossover_point=random.choice(functions); 
		crossover_point.setChildren(copy_root.getChildren()); # changes data at crossover point
		crossover_point.setData(copy_root.getData());
	else:
		crossover_point=random.choice(leaves);
		crossover_point.setChildren(copy_root.getChildren()); #similar as above
		crossover_point.setData(copy_root.getData());
	
	

	
	
