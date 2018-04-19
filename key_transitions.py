"""Key-transition probabilities

This probabilities were computed from a very
simple model of bidimensional key distance:

a 	C 	c 	Eb 	eb 	Gb 	gb
e 	G 	g 	Bb 	bb 	Db 	db
b 	D 	d 	F 	f 	Ab 	ab
f# 	A 	a 	C 	c 	Eb 	eb
c# 	E 	e 	G 	g 	Bb 	bb
g# 	B 	b 	D 	d 	F 	f
d# 	F# 	f# 	A 	a 	C 	c

C is in the middle, the distance to every key
is computed from the geometric distance in
that bidimensional representation.

In total, there are 9 different groups of keys,
each group is least likely to be the next key,
i.e., it is further away from C:

C
G F a c
d e f g
Bb D A Eb
bb Ab E b
B Db
f# eb
ab c#
F#
"""

key_transitions = [
	9/132, 4/132, 6/132, 6/132, 5/132, 8/132,
	1/132, 8/132, 5/132, 6/132, 6/132, 4/132,
	8/132, 2/132, 7/132, 3/132, 7/132, 7/132,
	3/132, 7/132, 2/132, 8/132, 5/132, 5/132
]
