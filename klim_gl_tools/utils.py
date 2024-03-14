import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *

def useHex(hex: str):
	"""Convert HEX color code to RGB format.
	Args:
		hex (str): The HEX color code as a string starting with '#'.
	Returns:
		tuple[float, float, float]: A tuple containing three floats (R, G, B) ranging from 0.0 to 1.0.
	"""
	return tuple(int(hex.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))

def useRgb(rgb: tuple):
	"""Convert RGB format to HEX color code.
	Args:
		rgb (tuple[float, float, float]): A tuple containing three floats (R, G, B) ranging from 0.0 to 1.0.
	Returns:
		str: The HEX color code as a string starting with '#'.
	"""
	return '#' + ''.join(f'{int(round(c * 255)):02x}' for c in rgb)

def interpolate_color(color1, color2, fraction):
	"""Linearly interpolates between two colors."""
	return tuple(color1[i] + (color2[i] - color1[i]) * fraction for i in range(3))

def apply_gradient(vertices, colors, angle):
	"""Applies a gradient to the vertices of a polygon, assuming colors are HEX codes."""
	# Convert HEX colors to RGB
	colors_rgb = [useHex(color) for color in colors]

	# Determine bounding box
	min_x = min(vertices, key=lambda v: v[0])[0]
	max_x = max(vertices, key=lambda v: v[0])[0]
	min_y = min(vertices, key=lambda v: v[1])[1]
	max_y = max(vertices, key=lambda v: v[1])[1]

	# Calculate gradient direction
	angle_rad = np.radians(angle)
	dir_x = np.cos(angle_rad)
	dir_y = np.sin(angle_rad)

	# Normalize and project vertices onto gradient direction
	projected = []
	for x, y in vertices:
		nx = (x - min_x) / (max_x - min_x) if (max_x - min_x) else 0
		ny = (y - min_y) / (max_y - min_y) if (max_y - min_y) else 0
		projection = nx * dir_x + ny * dir_y
		projected.append(projection)

	# Normalize projections to [0, 1]
	min_proj = min(projected)
	max_proj = max(projected)
	projected = [(p - min_proj) / (max_proj - min_proj) for p in projected]

	# Interpolate colors based on projections
	num_colors = len(colors_rgb)
	vertex_colors = []
	for p in projected:
		segment = p * (num_colors - 1)
		left_color_idx = int(np.floor(segment))
		right_color_idx = int(np.ceil(segment))
		fraction = segment - left_color_idx
		color = interpolate_color(colors_rgb[left_color_idx], colors_rgb[min(right_color_idx, num_colors - 1)], fraction)
		vertex_colors.append(useRgb(color))

	return vertex_colors

def draw_polyon_boject(obj):
	"""
	Draw a polygon object with specified obj._render_passes.

	Args:
	- obj: The object to be drawn.
	"""
	x, y = obj._position
	
	if 'fill' in obj._render_passes:
		glBegin(GL_POLYGON)
		for vertex, color in zip(obj._vertices, obj._vertex_colors):
			glColor3f(*useHex(color))
			glVertex2f(vertex[0] + x, vertex[1] + y)
		glEnd()
	
	if 'mask' in obj._render_passes:
		# Implement mask drawing logic here
		glColor3f(*useHex(obj._mask[1]))
		glEnable(GL_POLYGON_STIPPLE)
		glPolygonStipple(obj._mask[0])
		glBegin(GL_POLYGON)
		for vertex in obj._vertices:
			glVertex2f(vertex[0] + x, vertex[1] + y)
		glEnd()
		glDisable(GL_POLYGON_STIPPLE)
	
	if 'stroke' in obj._render_passes:
		glLineWidth(obj._stroke[0])
		glColor3f(*useHex(obj._stroke[1]))
		glBegin(GL_LINE_LOOP)
		for vertex in obj._vertices:
			glVertex2f(vertex[0] + x, vertex[1] + y)
		glEnd()

def useImageAsPattern(image_path, threshold = 0.5):
	img = Image.open(image_path)
	img = img.resize((32, 32))
	img = img.convert("L")

	threshold = int(threshold * 255)
	img = img.point(lambda p: p > threshold and 1)

	img_array = np.array(img)
	stipple_pattern = bytearray(32 * 4)

	for i, row in enumerate(img_array):
		row_as_int = 0
		for bit in row:
			row_as_int = (row_as_int << 1) | bit
		stipple_pattern[i*4:i*4+4] = int(row_as_int).to_bytes(4, 'big')

	return stipple_pattern
