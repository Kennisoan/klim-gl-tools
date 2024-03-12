from OpenGL.GL import *
from OpenGL.GLU import *
import math

def useHex(hex: str):
	"""Convert HEX color code to RGB format.
	Args:
		hex (str): The HEX color code as a string starting with '#'.
	Returns:
		tuple[float, float, float]: A tuple containing three floats (R, G, B) ranging from 0.0 to 1.0.
	"""
	return tuple(int(hex.lstrip('#')[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def useSvgPath(path: str):
	"""Convert SVG <path> tag to vertex array
	Args:
		path (str): The <path> tag as a string
	Returns:
		array[tuple]: Vertex array
	"""
	
	path_data = path.split('"')[1]
	points = []
	current_pos = (0, 0)
	
	commands = []
	arg = ''
	for char in path_data:
		if char.isalpha():
			if arg:
				commands.append(arg)
			arg = char
		else:
			arg += char
	commands.append(arg)
	
	for command in commands:
		cmd_type = command[0]
		args = list(map(float, command[1:].split()))
		
		if cmd_type == 'M':  # MoveTo command
			for i in range(0, len(args), 2):
				current_pos = (args[i], args[i+1])
				points.append(current_pos)
		elif cmd_type == 'L':  # LineTo command
			for i in range(0, len(args), 2):
				current_pos = (args[i], args[i+1])
				points.append(current_pos)
		elif cmd_type == 'H':  # Horizontal LineTo
			for x in args:
				current_pos = (x, current_pos[1])
				points.append(current_pos)
		elif cmd_type == 'V':  # Vertical LineTo
			for y in args:
				current_pos = (current_pos[0], y)
				points.append(current_pos)
		# For simplicity, we ignore curves (C, S, Q, T, A) and assume closed paths (Z) return to the start
	
	return points

# ========================================

def rect(x: float, y: float, width: float, height: float, color: str) -> None:
	"""Draw a rectangle with the given color.
	Args:
		x (float): X-origin point.
		y (float): Y-origin point.
		width (float): The width of the rectangle.
		height (float): The height of the rectangle.
		color (str): The HEX color code for the rectangle.
	"""
	glColor3f(*useHex(color))
	glRectf(x, y, x + width, y + height)

def rectGradient(x: float, y: float, width: float, height: float, startColor: str, endColor: str) -> None:
	"""Draw a rectangle with a vertical gradient.
	Args:
		x (float): X-origin point.
		y (float): Y-origin point.
		width (float): The width of the rectangle.
		height (float): The height of the rectangle.
		startColor (str): The HEX color code for the start of the gradient.
		endColor (str): The HEX color code for the end of the gradient.
	"""
	glBegin(GL_QUADS)

	glColor3f(*useHex(startColor))
	glVertex2f(x, y)  # Bottom Left
	glVertex2f(x + width, y)  # Bottom Right
	
	glColor3f(*useHex(endColor))
	glVertex2f(x + width, y + height)  # Top Right
	glVertex2f(x, y + height)  # Top Left

	glEnd()
	
def ellipse(x: float, y: float, width: float, height: float, color: str, segments: int = 100) -> None:
	"""Draw an ellipse specified by the bottom-left point and its width and height.
	Args:
		x (float): X-coordinate of the bounding box.
		y (float): Y-coordinate of the bounding box.
		width (float): Width of the bounding box of the ellipse.
		height (float): Height of the bounding box of the ellipse.
		color (str): The HEX color code for the ellipse.
		segments (int, optional): The number of segments used to approximate the ellipse. Default is 100.
	"""
	x_center = x + width / 2
	y_center = y + height / 2
	radius_x = width / 2
	radius_y = height / 2
	glColor3f(*useHex(color))
	theta = 0
	step = 2 * math.pi / segments
	
	glBegin(GL_POLYGON)
	for _ in range(segments):
		x = x_center + radius_x * math.cos(theta)
		y = y_center + radius_y * math.sin(theta)
		glVertex2f(x, y)
		theta += step
	
	glEnd()

def polygon(vertices, color: str, xoffset: float = 0.0 , yoffset: float = 0.0) -> None:
	"""Draw a filled polygon shape from a list of vertex positions.
	Args:
		vertices (list[tuple[float, float]]): A list of tuples, each representing the x and y coordinates of a vertex.
		color (str): The HEX color code for the polygon.
		xoffset (float): global offset by x axis.
		yoffset (float): global offset by y axis.
	"""
	glColor3f(*useHex(color))
	glBegin(GL_POLYGON)
	for vertex in vertices:
		glVertex2f(vertex[0] + xoffset, vertex[1] + yoffset)
	
	glEnd()

def tessellate(vertices, color, xoffset: float = 0.0 , yoffset: float = 0.0):
	"""Draw a filled polygon shape from a list of vertex positions.
	Args:
		vertices (list[tuple[float, float]]): A list of tuples, each representing the x and y coordinates of a vertex.
		color (str): The HEX color code for the polygon.
		xoffset (float): global offset by x axis.
		yoffset (float): global offset by y axis.
	"""
	def vertexCallback(vertex):
		glVertex3dv(vertex)

	def beginCallback(mode):
		glBegin(mode)

	def endCallback():
		glEnd()

	def combineCallback(coords, vertex_data, weight):
		return coords

	tess = gluNewTess()
	gluTessCallback(tess, GLU_TESS_VERTEX, vertexCallback)
	gluTessCallback(tess, GLU_TESS_BEGIN, beginCallback)
	gluTessCallback(tess, GLU_TESS_END, endCallback)
	gluTessCallback(tess, GLU_TESS_COMBINE, combineCallback)
	
	glColor3f(*useHex(color))
	gluTessBeginPolygon(tess, None)
	gluTessBeginContour(tess)
	for vertex in vertices:
		vertex3 = (vertex[0] + xoffset, vertex[1] + yoffset, 0)
		gluTessVertex(tess, vertex3, vertex3)
	gluTessEndContour(tess)
	gluTessEndPolygon(tess)
	gluDeleteTess(tess)

def tree(x: float, y: float, height: float, color: str, root_color: str):
	"""Draw a low-poly tree
	Args:
		x (float): X-coordinate of the tree root.
		y (float): Y-coordinate of the tree root.
		height (float): Tree height.
		color (str): The HEX color code for the tree.
		root_color (str): The HEX color code for the tree trunk (root).
	"""
	original_foliage_height = 46
	original_trunk_height = 8
	original_total_height = original_foliage_height + original_trunk_height
	
	scale_factor = height / original_total_height
	foliage_height = original_foliage_height * scale_factor
	trunk_height = original_trunk_height * scale_factor
	
	polygon([
		(x - 15 * scale_factor, y - trunk_height),
		(x, y - foliage_height - trunk_height),
		(x + 15 * scale_factor, y - trunk_height)
	], color)
	
	rectGradient(x - 4 * scale_factor, y, 8 * scale_factor, -trunk_height, root_color, color)
