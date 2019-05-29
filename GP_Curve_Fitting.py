import random
from inspect import signature
from math import floor;

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
		method takes on two values grow or full. These affects the method in which the trees are grown
	"""
	expr=[];
	func=None;
	if max_d==0 or (method=="grow" and random.random()<(len(term_set)/(len(term_set)+len(func_set)))):
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
	

def prefix_add(str,starting_index,term_set,func_map):
	if starting_index>=len(str):
		return None,-1; 
  
	a=str[starting_index];
    #while True:  
        #q = None; 
 
        
  
        # If the character is an operand 
	if a in term_set: 
		return Node(a),starting_index; 
         
	func=func_map[a];
        #Build the left sub-tree
		
	new_index=starting_index
	new_node= Node(a);
	children=[];
	new_q=None;
	for i in range(arity(func)):
		new_child,new_q = prefix_add(str, new_index + 1,term_set,func_map); 
		children.append(new_child);
		new_index=new_q;
        #Build the right sub-tree 
        #q = add(&(*p)->right, q + 1);
	#print(children);
	new_node.setChildren(children);
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

str=gen_random_expr(func_set,term_set,3,'full');
#str=['subtract', 'a', 'divide', 'c', 'a'];
func_map={func.__name__:func for func in func_set};
starting_index=0;
# print(str,"\n");
root,_=prefix_add(str,starting_index,term_set,func_map);
# #print(root.data)
# inorder(root);
def initial_population(population_size,term_set,func_set,max_d):
	""" Creates a population speicifed by population size"""
	mid=floor(population_size/2);
	population=[];
	func_map={func.__name__:func for func in func_set};
	for i in range(mid):
		str=gen_random_expr(func_set,term_set,max_d,'grow');
		root,_=prefix_add(str,0,term_set,func_map);
		population.append(root);
	for i in range(mid+1,population_size):
		str=gen_random_expr(func_set,term_set,max_d,'full');
		root,_=prefix_add(str,0,term_set,func_map);
		population.append(root);
	return population;

def tree2array(root):
	array=[root];
	
	for i in range(len(root.children)):
		array=array+tree2array(root.children[i]);
	return array;
print(str,"\n");	
print(tree2array(root));
	
def point_mutation(root):
			pass