import numpy as np;
import matplotlib.pyplot as plt
from GP import *;

x=np.arange(-5,5.1,.1);
func_set=[add,subtract,divide,multiply];
term_set=[i for i in range(-5,6)];
for i in range(-5,6):
	term_set.append(x);

test=GP_Program(term_set,func_set);

y=x*x+x+1;
root=test.run(500,300,2,y);
print(test.fitness(y,root));


			
plt.plot(x,y,color="green");
plt.plot(x,test.tree_interpreter(root),color="blue");

plt.show()
