# -------- Vector2D.py --------
# Helper for calculating and maniupulating 2D vectors
# ---------------------------

# Definitions
UP		= [0, -1]
RIGHT	= [1, 0]
DOWN 	= [0, 1]
LEFT 	= [-1, 0]

# Add Vectors
def AddVectors( v1, v2 ):
	vout = range( 2 )
	for i in range( 2 ):
		vout[i] = v1[i] + v2[i]
	return vout

# Subtract Vectors
def SubtractVectors( v1, v2 ):
	vout = range( 2 )
	for i in range( 2 ):
		vout[i] = v1[i] - v2[i]
	return vout

# Multiply Vectors
def MultiplyVectors( v1, v2 ):
	vout = range( 2 )
	for i in range( 2 ):
		vout[i] = v1[i] * v2[i]
	return vout

# Divide Vectors
def DivideVectors( v1, v2 ):
	vout = range( 2 )
	for i in range( 2 ):
		vout[i] = v1[i] / v2[i]
	return vout