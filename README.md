# Klim's GL Tools

This custom Python library offers a suite of functions to simplify drawing operations using OpenGL. It's designed to make creating basic geometric shapes and some more complex drawings like gradients straightforward.

## Installation

You can install Klim’s GL Tools manually, or by using pip:
```bash
pip3 install git+https://github.com/Kennisoan/klim-gl-tools.git
```
Then import `klim_gl_tools` in your code and you're ready to go:
```python
import klim_gl_tools as kt
```

## Shapes
Below, you'll find a brief overview of each function available in the library, alongside some usage examples.

### Rectangle
Draws a solid-color rectangle. Great for simple shapes or backgrounds.
```python
rect(x, y, width, height, color)
# Example (creates a recangle with bottom-left corner at (5px, 10px) with 100px width and 50px height with HEX-color #FF5733):
rect(5, 10, 100, 50, "#FF5733")
```

### Rectangle with a top-down gradient
Creates a rectangle with a vertical gradient. Ideal for backgrounds with a bit more flair.
```python
rectGradient(x, y, width, height, startColor, endColor)
# Example (creates a recangle with bottom-left corner at (5px, 10px) with 100px width and 50px height with a top-down gradient from #FFFFFF to #FF5733):
rectGradient(5, 10, 100, 50, "#FFFFFF", "#FF5733")
```

### Ellipse
Draws an ellipse or circle, specified by its bounding box.
```python
ellipse(x, y, width, height, color, segments=100)
# Example (creates an ellipse in a bounding box with bottom-left corner at (5px, 10px) with 100px width and 50px height with a top-down gradient from #FFFFFF to #FF5733):
ellipse(5, 10, 100, 50, "#FF5733", segments=100)
```
The shape is approximated using polygons, you can control amount of segemnts that make up the shape using `segments` (100 by default).

### Polygon
Renders a filled polygon from a list of vertices. Use it for custom shapes. Specify vertices in an array like this: `[(x1,y1), (x2,y2), ...]`.
```python
polygon(vertices, color, xoffset=0.0, yoffset=0.0)
```
Use `xoffset` and `yoffset` to offset the whole shape by x and y axes.

### Tessellate shape
Similar to `polygon`, but for complex (non-convex) shapes that require tessellation to render correctly. Specify vertices in an array like this: `[(x1,y1), (x2,y2), ...]`.
```python
tessellate(vertices, color, xoffset=0.0, yoffset=0.0)
```
Use `xoffset` and `yoffset` to offset the whole shape by x and y axes.

## Other Tools

### HEX to RGB
```python
useHex(hex)
```
Converts a HEX color code into RGB format, making it easy to use web colors directly in OpenGL.

### SVG Path to vertices
```python
useSvgPath(path)
```
Convets SVG path string (`<path d="..."/>`) into a vertex array that can be used with `polygon` and `tessellate`.
