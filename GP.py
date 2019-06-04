import random;
from inspect import signature;
from math import floor;
from random import shuffle;
from copy import deepcopy;
import numpy

#the following four functions are primarily used for testing
def add(a,b):
	"""returns the sum of two numbers"""
	return a+b;
def multiply(a,b):
	"""returns the product of two numbers"""
	return a*b;
def divide(a,b):
	"""returns the quotient of two numbers"""
	try:
		return a/b;
	except:
		return 0;
def subtract(a,b):
	"""returns the difference of two numbers"""
	return a-b;
	
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
class GP_Program:

	def __init__(self,term_set,func_set):
		self.term_set=term_set;
		self.func_set=func_set;
		self.func_map= {func.__name__: func for func in func_set};
		self.term_map={ str(i):term_set[i] for i in range(len(term_set))}

	def choose_random_element(self,set):
		"""returns a random element in the given set"""
		index= random.randint(0,len(set)-1);
		return set[index];

	def arity(self,func):
		"""Returns the arity or number of parameters of a function"""
		sig = signature(func);
		params = sig.parameters
		return len(params);

	def gen_random_expr(self,method,max_d):
		"""Generates a random prefix expression
			func_set is the set of functions
			term_set is the set of terms
			max_d is the max height of the tree
			method takes on two values grow or full.
			These affect the method in which the trees are created
		"""
		terms=[*self.term_map]
		funcs=[*self.func_map]
		expr=[];
		func=None;
		if max_d==0 or (method=="grow" and random.random()<(len(terms)/(len(terms)+len(funcs)))): # the following is adopted from pseudocode from 
			expr= [str(self.choose_random_element(terms))];
		else:
			func=self.choose_random_element(funcs);
			args=[];
			for i in range(0,self.arity(self.func_map[func])):
				args=args+self.gen_random_expr(method,max_d-1);
			expr=expr+[func];
			expr=expr+args;
		return expr;
	def prefix_add(self,string,starting_index):
		"""Converts the prefix expression from gen_random_expr into an expression tree"""
		if starting_index>=len(string): #This is in the case where the starting_index exceeds the array. This case should not happen but just in case
			return None,-1; 
	  
		a=string[starting_index]; #gets the element corresponding to the starting index
		
		#print(a); 
		if a in self.term_map:
			return Node(a),starting_index
			 
		func=self.func_map[a];
			
		new_index=starting_index # temporary variables
		new_node= Node(a);
		children=[];
		new_q=None;
		for i in range(self.arity(func)): #creates tree out of the operands and makes them children
			new_child,new_q = self.prefix_add(string, new_index + 1); 
			children.append(new_child);
			new_index=new_q;

		new_node.setChildren(children); #sets the children array
		return new_node,new_q; 


	def initial_population(self,population_size,max_d):
		""" Creates a population specified by population size using the 
		ramped half and half distribution i.e.
		using the grow method o generation for 
		half the population and the full method 
		for the other half"""
		mid=floor(population_size/2); #find roughly half the population
		population=[];# the empty population
		for i in range(mid):
			str=self.gen_random_expr('grow',max_d); # creates a tree using the grow method
			root,_=self.prefix_add(str,0);
			population.append(root);
		for i in range(mid,population_size):
			str=self.gen_random_expr('full',max_d); # creates a tree using the full method
			root,_=self.prefix_add(str,0);
			population.append(root);
		return population;

	def tree2array(self,root):
		"""converts an tree to an array in prefix order"""
		array=[root];
		
		for i in range(len(root.children)):
			array=array+self.tree2array(root.children[i]);
		return array;
		
	def point_mutation(self,root):
		"""creates a point mutation in the given tree. This code is very nasty
		and may not be the best in terms of time complexity may need to revise
		later"""
		root=deepcopy(root);
		array=self.tree2array(root); #gets the tree as an array
		node2change=random.choice(array); # selects a random node to be changed
		data=node2change.getData(); # gets the data stored in the random node
		if data in self.func_map: #test if the data is a function or not
			func=data; #gets the function that corresponds to the string in data
			shuffle(self.func_set);	#randomizes the function set
			if len(self.func_set)>1 and self.func_set[0]==func: #if the function in the first element in the array sets to the second element
				node2change.setData(self.func_set[1].__name__);	
			else:
				node2change.setData(self.func_set[0].__name__); # otherwise it sets to the first element in th3 shuffled array
		else:
			terms=[*self.term_map];
			shuffle(terms); #Does a very similar procedure but for the case where a node contains a term
			if len(terms)>1 and terms==data:
				node2change.setData(terms[1]);
			else:
				node2change.setData(terms[0]);
		return root;
		
	def subtree_mutation(self,root,max_d):
		"""Creates a subtree mutation replacing part of 
		the tree with a randomly generated subtree"""
		root=deepcopy(root);
		new_d=random.randint(0,max_d); #generates a random height for the new subtree to be added may edit this to prevent subtrees of height 0
		
		method= "grow" if random.randint(0,1) else "full"; #randomly chooses whether to use "full" or "grow"
		string=self.gen_random_expr(method,new_d); # generates a random prefix expression
		new_node,_=self.prefix_add(string,0); #generates a new node for the random subtree
		array=self.tree2array(root); # gets the nodes of the original tree as a array using tree2array
		rand_root=random.choice(array); #randomly selects a node from the tree.
		rand_root.setChildren(new_node.getChildren()); #changes it values in the random node to match that of the new subtree.
		rand_root.setData(new_node.getData());
		return root;
		
	def tree_divider(self,root):
		"""divides the roots in an expression tree into two categories,
		internal nodes and leaves"""
		array=self.tree2array(root); #gets the roots into and array in prefix order
		functions=[]; #initlizes array for internal nodes
		leaves=[];#intilizes an array for leaves
		for i in range(len(array)): #Goes the array representation of the expression tree and places each node into its corresponding categories depending on whether or not they have children
			if not array[i].getChildren():
				leaves.append(array[i]);
			else:
				functions.append(array[i]);
			
		return functions,leaves; # returns a tuple of arrays

	def crossover(self,parent1,parent2):
		"""Implements recombination by determining a random crossover point in parent
		and replacing with a subtree from parent2"""
		
		
		copy_parent1=deepcopy(parent1);
		functions,leaves=self.tree_divider(copy_parent1);  #divides the trees into two sets, internal nodes and leaves
		array=self.tree2array(parent2); #gets the ndoes in parent2 as an array
		
		rand_root=random.choice(array); # gets the nodes in rand_root and creates a deepcopy
		copy_parent2= deepcopy(rand_root);
		
		if random.random()<.9 and functions: # makes the crossover point a leaf or function as determined by the the probability determined  by J.R. Koza
			crossover_point=random.choice(functions); 
			crossover_point.setChildren(copy_parent2.getChildren()); # changes data at crossover point
			crossover_point.setData(copy_parent2.getData());
		else:
			crossover_point=random.choice(leaves);
			crossover_point.setChildren(copy_parent2.getChildren()); #similar as above
			crossover_point.setData(copy_parent2.getData());
		
		return copy_parent1;
	
	def tree_interpreter(self,root):
		#print(root);

		if root.getData() in self.term_map:
			return self.term_map[root.getData()];
		else:
			func=self.func_map[root.getData()];
			#print(root.getChildren());
			child1= self.tree_interpreter(root.getChildren()[0]);
			child2= self.tree_interpreter(root.getChildren()[1]);
			
			return func(child1,child2);
	def fitness(self,y,root):
		y_test=self.tree_interpreter(root);
		return -sum((y-y_test)**2) #returns the negative sum of squares
	def most_fit(self,array,y):
		if len(array)<1: #Returns None is array has length 0;
			return None;
		max_fit= self.fitness(y,array[0]); # gets the fitness of first element and treats it as the max
		max_root= array[0];
		
		for i in range(1,len(array)): # lops throught the rest of the elements to see if anything else is a possible substitute 
			fit_test= self.fitness(y,array[i]);
			if fit_test>max_fit: #Replaces is the fitness is greater
				max_root=array[i];
				max_fit=fit_test;
		return max_root;
	
	def run(self,population_size,generations,max_d,y):
		population=self.initial_population(population_size,max_d); #Initializes a population given a specific population_size and max depth
		mid= floor(len(population)/2);# finds the mid point to split the data set into two
		for i in range(generations): #the population reconstruction for a set number of generations
			parent1=self.most_fit(population[:mid],y); # selects the most fit from one half
			parent2=self.most_fit(population[mid:],y); #selects the most fit from the other
			new_population=[]; # initializes new population to be empty
			
			num_remainings= population_size; #makes sure the population is refilled to original size
			
			num_children= floor(.9*num_remainings); #adds roughly 90% as children of the two most fit
			
			for i in range(num_children):
				new_population.append(self.crossover(parent1,parent2));
			num_remainings=num_remainings-num_children;
			
			num_copy= floor(.8*num_remainings);
			
			for i in range(num_copy): # intilizes roughly 8 percent to be copies of the fit parents
				if i%2==0:
					population.append(parent1);
				else:
					population.append(parent2);
			num_remainings=num_remainings-num_copy;
			
			for i in range(num_remainings): #makes the rest mutations of any member in the population
				rand_root= random.choice(population)
				if random.randint(0,1):
					population.append(self.point_mutation(rand_root))
				else:
					population.append(self.subtree_mutation(rand_root,max_d));


		return self.most_fit(population,y); #returns the most fit in the population after generations has run
	
	
		
		
	
