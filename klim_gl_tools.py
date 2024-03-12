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

def useSvgPath(path: str) -> list:
	"""Convert SVG <path> tag to vertex array
	Args:
		path (str): The <path> tag as a string
	Returns:
		list[tuple]: Vertex array
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

class Rectangle:
	"""
	Rectangle.
	"""
	def __init__(self):
		self.val_position = [0, 0]
		self.val_size = [0, 0]
		self.val_colors = ["#000000"]
	
	# Shorthands
		
	def __x(self):
		return self.val_position[0]
	def __y(self):
		return self.val_position[1]
	def __w(self):
		return self.val_size[0]
	def __h(self):
		return self.val_size[1]
		
	# Modifiers
	
	def position(self, x: float, y: float):
		"""
		Sets position by x and y coordinates.
		"""
		self.val_position = [x, y]
		return self
		
	def size(self, width, height = None):
		"""
		Sets width and height.
		"""
		if height is None: height = width
		self.val_size = [width, height]
		return self
	
	def fill(self, color):
		"""
		Sets a solid fill color (HEX).
		"""
		self.val_colors = [color]
		return self
	
	def gradient(self, colorFrom, colorTo):
		"""
		Applies a linear gradient from top to bottom.
		"""
		self.val_colors = [colorFrom, colorTo]
		return self
	
	def draw(self):
		"""
		Draws the shape.
		"""
		glBegin(GL_QUADS)
		
		if len(self.val_colors) == 1:
			startColor = self.val_colors[0]
			endColor = self.val_colors[0]
		else:
			startColor = self.val_colors[0]
			endColor = self.val_colors[1]
		
		glColor3f(*useHex(startColor))
		glVertex2f(self.__x(), self.__y())  # Bottom Left
		glVertex2f(self.__x() + self.__w(), self.__y())  # Bottom Right
		
		glColor3f(*useHex(endColor))
		glVertex2f(self.__x() + self.__w(), self.__y() + self.__h())  # Top Right
		glVertex2f(self.__x(), self.__y() + self.__h())  # Top Left
		
		glEnd()

class Ellipse:
		"""
		Ellipse.
		"""
		def __init__(self):
			self.val_position = [0, 0]
			self.val_size = [0, 0]
			self.val_color = "#000000"
			self.val_segments = 100
		
		# Shorthands
			
		def __x(self):
			return self.val_position[0]
		def __y(self):
			return self.val_position[1]
		def __w(self):
			return self.val_size[0]
		def __h(self):
			return self.val_size[1]
			
		# Modifiers
		
		def position(self, x: float, y: float):
			"""
			Sets position by x and y coordinates.
			"""
			self.val_position = [x, y]
			return self
			
		def size(self, width, height = None):
			"""
			Sets width and height.
			"""
			if height is None: height = width
			self.val_size = [width, height]
			return self
		
		def quality(self, segments):
			"""
			Sets the draw quality of shape in amount of segments used.
			"""
			self.val_segments = segments
			return self
		
		def fill(self, color):
			"""
			Sets a solid fill color (HEX).
			"""
			self.val_color = color
			return self
		
		def draw(self):
			"""
			Draws the shape.
			"""
			x_center = self.__x() + self.__w() / 2
			y_center = self.__y() + self.__h() / 2
			radius_x = self.__w() / 2
			radius_y = self.__h() / 2
			glColor3f(*useHex(self.val_color))
			theta = 0
			step = 2 * math.pi / self.val_segments
			
			glBegin(GL_POLYGON)
			for _ in range(self.val_segments):
				x = x_center + radius_x * math.cos(theta)
				y = y_center + radius_y * math.sin(theta)
				glVertex2f(x, y)
				theta += step
			
			glEnd()

class Polygon:
	"""
	Draws a complex shape described by vertices.
	"""
	def __init__(self):
		self.val_vertices = [(0,0)]
		self.val_position = [0, 0]
		self.val_color = "#000000"
		self.val_tessellate = False
	
	# Shorthands
		
	def __x(self):
		return self.val_position[0]
	def __y(self):
		return self.val_position[1]
		
	# Modifiers
	
	def useVertexArray(self, array: list):
		"""
		Builds shape from a vertex array of shape: [(x1,y1), (x2,y2), ...].
		"""
		self.val_vertices = array
		return self
	
	def useSvgPath(self, path: str):
		"""
		Builds shape from SVG path data (<path d="..." />).
		"""
		self.val_vertices = useSvgPath(path)
		return self
	
	def position(self, x: float, y: float):
		"""
		Offsets position by x and y coordinates.
		"""
		self.val_position = [x, y]
		return self
	
	def tessellate(self):
		"""
		Applies tessellation to the shape.
		"""
		self.val_tessellate = True
		return self
	
	def fill(self, color):
		"""
		Sets a solid fill color (HEX).
		"""
		self.val_color = color
		return self
	
	def draw(self):
		"""
		Draws the shape.
		"""
		
		if not self.val_tessellate:
			glColor3f(*useHex(self.val_color))
			glBegin(GL_POLYGON)
			for vertex in self.val_vertices:
				glVertex2f(vertex[0] + self.__x(), vertex[1] + self.__y())
			
			glEnd()
		else:
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
			
			glColor3f(*useHex(self.val_color))
			gluTessBeginPolygon(tess, None)
			gluTessBeginContour(tess)
			for vertex in self.val_vertices:
				vertex3 = (vertex[0] + self.__x(), vertex[1] + self.__y(), 0)
				gluTessVertex(tess, vertex3, vertex3)
			gluTessEndContour(tess)
			gluTessEndPolygon(tess)
			gluDeleteTess(tess)

class Tree:
	"""
	A simple tree with solid or gradient fill.
	"""
	def __init__(self):
		self.val_position = [0, 0]
		self.val_size = [0, 0]
		self.val_colors = ["#000000"]
	
	# Shorthands
		
	def __x(self):
		return self.val_position[0]
	def __y(self):
		return self.val_position[1]
	def __w(self):
		return self.val_size[0]
	def __h(self):
		return self.val_size[1]
		
	# Modifiers
	
	def position(self, x: float, y: float):
		"""
		Sets position by x and y coordinates.
		"""
		self.val_position = [x, y]
		return self
		
	def size(self, height):
		"""
		Sets height of the tree.
		"""
		self.val_size = [0, height]
		return self
	
	def fill(self, color):
		"""
		Sets a solid fill color (HEX).
		"""
		self.val_colors = [color]
		return self
	
	def gradient(self, colorFrom, colorTo):
		"""
		Applies a linear gradient from top to bottom to trunk (foliage is colored with `colorFrom`).
		"""
		self.val_colors = [colorFrom, colorTo]
		return self
	
	def draw(self):
		"""
		Draws the shape.
		"""
		original_foliage_height = 46
		original_trunk_height = 8
		original_total_height = original_foliage_height + original_trunk_height
		
		scale_factor = self.__h() / original_total_height
		foliage_height = original_foliage_height * scale_factor
		trunk_height = original_trunk_height * scale_factor
		
		Polygon() \
			.useVertexArray([
				(self.__x() - 15 * scale_factor, self.__y() - trunk_height),
				(self.__x(), self.__y() - foliage_height - trunk_height),
				(self.__x() + 15 * scale_factor, self.__y() - trunk_height)
			]) \
			.fill(self.val_colors[0]) \
			.draw()
		
		colors = [self.val_colors[0], self.val_colors[0]]
		if len(self.val_colors) == 2:
			colors = [self.val_colors[1], self.val_colors[0]]
		
		Rectangle() \
			.position(self.__x() - 4 * scale_factor, self.__y()) \
			.size(8 * scale_factor, -trunk_height) \
			.gradient(*colors) \
			.draw()
