"""Key-transition probabilities

These probabilities were computed from a very
simple model of bidimensional key distance:

D	d 	F 	f 	Ab 	ab 	Cb 	cb 	Ebb 	
A	a 	C 	c 	Eb 	eb 	Gb 	gb 	Bbb 	
E	e 	G 	g 	Bb 	bb 	Db 	db 	Fb
B	b 	D 	d 	F 	f 	Ab 	ab 	Cb
F#	f# 	A 	a 	C 	c 	Eb 	eb 	Gb
C#	c# 	E 	e 	G 	g 	Bb 	bb 	Db
G#	g# 	B 	b 	D 	d 	F 	f 	Ab
D#	d# 	F# 	f# 	A 	a 	C 	c 	Eb
A#	a# 	C# 	c# 	E 	e 	G 	g 	Bb

C is in the middle, the distance to every key
is computed from the geometric distance in
that bidimensional representation.

In total, there are 9 different groups of keys,
each group is least likely to be the next key,
i.e., it is further away from C:

C
G F a c
d e f g
D Eb A Bb
E Ab bb b
Db B
eb f#
c# ab
F#

a
C A d e
D E F G
c f# g b
Bb B c# f
g# bb
Eb F#
C# Ab
d#

c
C Eb f g
F G Ab Bb
d eb bb a
Db D e ab
db b
A Gb
Cb E
f#  
"""

key_transitions = [
	9/132, 4/132, 6/132, 6/132, 5/132, 8/132,
	1/132, 8/132, 5/132, 6/132, 6/132, 4/132,
	8/132, 2/132, 7/132, 3/132, 7/132, 7/132,
	3/132, 7/132, 2/132, 8/132, 5/132, 5/132
]

neighbour_level = [
	1,6,4,4,5,2,9,2,5,4,4,6,
	2,8,3,7,3,3,7,3,8,2,5,5
]