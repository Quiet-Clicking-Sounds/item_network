# Item Network

A simple package for working with linked networks.

This package contains two modules, the network module contains
the `LinkedNetwork` class for creating a network; and the visualization module
which can be used to quickly create a

### Creating a network:

```python 
from itemnetwork import LinkedNetwork
my_network = LinkedNetwork(
    ignore_key_equality_error=False,
    keep_order=False)
```

`ignore_key_equality_error =`\
`True` the network will silently drop any pair of keys which share a hash
value.  
`False` the network will raise a `ValueError` if it encounters a pair of items
which have the same hash values

`keep_order = `\
`True` hash comparison will care about order thus `Link(a,b)` is not equal to
`Link(b,a)`\
`False` hash comparison will ignore the order of input arguments,
thus `Link(a,b)` is equal to `Link(b,a)`

### Adding items to a network:

```python 
from itemnetwork import LinkedNetwork

my_network = LinkedNetwork()
my_network.add_link('a', 'b')
my_network.add_link('a', 'c', count=1)  # optional increment
my_network.add_multiple_links([
    ('a', 'b'),
    ('b', 'c'),
    ('c', 'd')])
```

`LinkedNetwork.add_link()` requires 2 arguments for each end of the link, and a
count for adding multiple links  
`LinkedNetwork.add_multiple_links` requires a list of argument tuples, this 
improves performance over a standard for loop using `collections.Counter`.

### Printing a LinkedNetwork
```python 
>>> my_network.print_links()
a b 2
b c 1
c d 1
```
`LinkedNetwork.print_links()` takes no arguments and prints all links in the 
format: " **str(a) str(b) count** "

## quick_plot()

*quick_plot will only be available if the additional dependency **matplotlib** has 
been installed.*

`quick_plot()` is an extra part of the module that allows for quickly getting 
a visual representation of a network. 

```python 
from matplotlib import pyplot as plt
from random import randint
from itemnetwork import LinkedNetwork, quick_plot

# network setup
my_network = LinkedNetwork(ignore_key_equality_error=True)
# ignore_key_equality_error=True ignores an item if a == b (you can't connect self to self in a link)
for _ in range(100):
    my_network.add_link(a=randint(1, 10), b=randint(1, 10))

# quick plot
fig, axis = plt.subplots()
quick_plot(my_network,fig, axis)
plt.show()
```

![quickplot output image](\test_network.png)