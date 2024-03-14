from OpenGL.GL import *
from OpenGL.GLU import *
import math
import warnings

from .mixins import *
from .utils import *

class Shape:
	def __init__(self):
		self._vertices = []
		self._vertex_colors = ['#000000']
		self._position = (0,0)
		self._rotation = 0
		self._stroke = [1, '#000000']
		self._mask = [[], '#000000']
		self._render_passes = []
	
	def position(self, x, y = None):
		"""
		Offsets position by x and y coordinates.
		"""
		if y is None: y = x
		self._position = (x, y)
		return self
	
	def fill(self, color):
		"""
		Sets a solid fill color (HEX).
		"""
		self._render_passes.append('fill')
		self._vertex_colors = [color for _ in self._vertices]
		return self
	
	def gradient(self, *colors, **kwargs):
		"""
		Applies a gradient to the shape based on the angle and the given colors.
		"""
		angle = kwargs.get('angle', 0)
		self._render_passes.append('fill')
		self._validate_vertex_colors()
		self._vertex_colors = apply_gradient(self._vertices, colors, angle)
		return self
	
	def stroke(self, width = 1, color = '#000000'):
		"""
		Applies a stroke
		"""
		self._render_passes.append('stroke')
		self._stroke = [width, color]
		return self
	
	def mask(self, pattern, color = '#000000'):
		self._render_passes.append('mask')
		self._mask = [pattern, color]
		return self
	
	def _validate_vertex_colors(self, warn=False):
		if len(self._vertex_colors) != len(self._vertices):
			self._vertex_colors = [self._vertex_colors[0] for _ in self._vertices]
			if warn: warnings.warn("Vertex colors were not applied properly.", RuntimeWarning)

class Polygon(Shape):
	"""
	Draws a complex shape described by vertices.
	"""
	def __init__(self):
		super().__init__()
		self._tessellate = False
	
	def path(self, vertex_array):
		"""
		Describes a shape using an array of vertices.
		"""
		self._vertices = vertex_array
		return self
	
	def tessellate(self):
		"""
		Applies tessellation to the shape.
		"""
		self._tessellate = True
		return self
	
	def draw(self):
		"""
		Draws the shape.
		"""
		x, y = self._position
		
		# Non-tessellated
		if self._tessellate == False:
			self._validate_vertex_colors(warn=True)
			draw_polyon_boject(self)
		
		# Tessellated
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

			gluTessBeginPolygon(tess, None)
			gluTessBeginContour(tess)
			for vertex, color in zip(self._vertices, self._vertex_colors):
				glColor3f(*useHex(color))
				vertex3 = (vertex[0] + x, vertex[1] + y, 0)
				gluTessVertex(tess, vertex3, vertex3)
			gluTessEndContour(tess)
			gluTessEndPolygon(tess)
			gluDeleteTess(tess)

class Rectangle(Shape):
	"""
	Rectangle.
	"""
	def size(self, width, height = None):
		"""
		Sets width and height.
		"""
		if height is None: height = width
		self._vertices = [(0, 0), (width, 0), (width, height), (0, height)]
		return self
	
	def draw(self):
		"""
		Draws the shape.
		"""
		self._validate_vertex_colors(warn=True)
		draw_polyon_boject(self)

class Ellipse(Shape):
	"""
	Ellipse.
	"""
	def __init__(self):
		super().__init__()
		self._quality = 100
	
	def quality(self, segments):
		"""
		Adjusts render quality of the shape.
		"""
		self._quality = segments
		return self
	
	def size(self, width, height = None):
		"""
		Sets width and height.
		"""
		if height is None: height = width
		x_center = width / 2
		y_center = height / 2
		radius_x = width / 2
		radius_y = height / 2
		
		theta = 0
		step = 2 * math.pi / self._quality
		
		self._vertices = []
		for _ in range(self._quality):
			x = x_center + radius_x * math.cos(theta)
			y = y_center + radius_y * math.sin(theta)
			self._vertices.append((x, y))
			theta += step
			
		return self
		
	def draw(self):
		"""
		Draws the shape.
		"""
		self._validate_vertex_colors(warn=True)
		draw_polyon_boject(self)
	
class Tree(Shape):
	"""
	Tree.
	"""
	def __init__(self):
		super().__init__()
		self._colors = ['#000000']
		self._height = 100
	
	def height(self, height):
		self._height = height
		return self
	
	def fill(self, color):
		self.val_colors = [color]
		return self
	
	def gradient(self, colorFrom, colorTo):
		self.val_colors = [colorFrom, colorTo]
		return self
	
	def draw(self):
		original_foliage_height = 46
		original_trunk_height = 8
		original_total_height = original_foliage_height + original_trunk_height

		scale_factor = self._height / original_total_height
		foliage_height = original_foliage_height * scale_factor
		trunk_height = original_trunk_height * scale_factor
		
		x, y = self._position

		Polygon() \
			.path([
				(x - 15 * scale_factor, y - trunk_height),
				(x, y - foliage_height - trunk_height),
				(x + 15 * scale_factor, y - trunk_height)
			]) \
			.fill(self.val_colors[0]) \
			.draw()

		colors = [self.val_colors[0], self.val_colors[0]]
		if len(self.val_colors) == 2:
			colors = [self.val_colors[1], self.val_colors[0]]

		Rectangle() \
			.position(x - 4 * scale_factor, y) \
			.size(8 * scale_factor, -trunk_height) \
			.gradient(*colors, angle=-90) \
			.draw()
