import numpy as np;
import matplotlib.pyplot as plt
from GP import *;

x=np.arange(-5,5.1,.1); # intilizes as array to be numbers from -5 to 5 with increments of .1
func_set=[add,subtract,divide,multiply]; # function set of add,subtract,divide,multiply from GP.py
term_set=[i for i in range(-5,6)]; # adds constants from -5 to 5
for i in range(-5,6): # adds x 5 times so it the term_set is not dominated by constants
	term_set.append(x);

test=GP_Program(term_set,func_set); # initilizes instance of the GP_program class

y=x*x+x+1; #y=x^2+x+1
root=test.run(500,300,2,y); #runs the GP algorithm with a 500 population size for 300 generations and max depth of 2
print(test.fitness(y,root));


			
plt.plot(x,y,color="green"); # Plots the correct data with the color green
plt.plot(x,test.tree_interpreter(root),color="blue"); #plots the apporixamated function with the color blue

plt.show()
