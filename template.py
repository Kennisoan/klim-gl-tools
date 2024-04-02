from OpenGL.GL import *
from OpenGL.GLUT import *
from klim_gl_tools import *

# Display Function
def RenderScene():
	glClear(GL_COLOR_BUFFER_BIT)
	glClearColor(1.0, 1.0, 1.0, 1.0)
	
	# Place your objects here
	
	# For example: Draw a path that renders the word "Hello" in a handwritten style
	Polygon() \
		.path(useSvgPath('<path d="M71 21L70 25L67 28H64L61 27L60 23V15L63 8L65 7L66 7L67 10L65 17L61 24L57 28L52 29L50 27L49 24V18L50 12L52 8L54 7L55 8L56 10L55 15L52 21L46 28L41 29L38 27L36 25V22L36 19L39 17L41 18L43 20L41 24L36 27L31 29L29 27L29 24V19L27 18L24 19L21 28L23 10L24 8L27 7L28 9L28 14L23 21L15 27L7 32L-3 36V72L102 73V2L93 12L85 17L81 19L77 18M71 21L73 18L77 18M71 21L71 26L74 29L77 28L79 26L80 23L79 20L77 18"/>')) \
		.position(0, 32) \
		.stroke(6, '#007AFF') \
		.draw()
	# This example creates a polygon in the shape of a handwritten "Hello".
	# The `.path()` modifier defines path for the polygon shape.
	# The `.position()` modifier sets the starting position of the path on the canvas.
	# The `.stroke()` modifier specifies the stroke width and color.
	# Finally, `.draw()` renders the path on the canvas.
	
	glFlush()
	

def ChangeSize(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, 100.0, 100.0, 0.0, 1.0, -1.0);
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutCreateWindow(b"Hello world!")
	glClearColor(1.0, 1.0, 1.0, 1.0)
	glutDisplayFunc(RenderScene)
	glutReshapeFunc(ChangeSize)
	glutMainLoop()

if __name__ == "__main__":
		main()
