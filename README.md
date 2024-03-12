# Klim's GL Tools

This custom Python library offers a suite of functions to simplify drawing operations using OpenGL. It's designed to make creating basic geometric shapes and some more complex drawings like gradients and low-poly trees straightforward. Below, you'll find a brief overview of each function available in the library, alongside some usage examples.

## Installation

You can install Klim’s GLUT Tools manually, or by using pip:
```bash
pip install git+https://github.com/Kennisoan/klim-glut-tools.git
```
or
```bash
pip3 install git+https://github.com/Kennisoan/klim-glut-tools.git
```

## Shapes

### Rectangle
```python
rect(x, y, width, height, color)
```
Draws a solid-color rectangle. Great for simple shapes or backgrounds.

### Rectangle with a top-down gradient
```python
rectGradient(x, y, width, height, startColor, endColor)
```
Creates a rectangle with a vertical gradient. Ideal for backgrounds with a bit more flair.

### Ellipse
```python
ellipse(x, y, width, height, color, segments=100)
```
Draws an ellipse or circle (when width equals height), specified by its bounding box.

### Polygon
```python
polygon(vertices, color, xoffset=0.0, yoffset=0.0)
```
Renders a filled polygon from a list of vertices. Use it for custom shapes.

### Tessellate shape
```python
tessellate(vertices, color, xoffset=0.0, yoffset=0.0)
```
Similar to `polygon`, but for complex shapes that require tessellation to render correctly.

### Low-poly tree
```python
tree(x, y, height, color, root_color)
```
Draws a stylized, low-poly tree. Useful for adding simple natural elements to a scene.

## Other Tools

### useHex
```python
useHex(hex)
```
Converts a HEX color code into RGB format, making it easy to use web colors directly in OpenGL.

## Examples

Here are a few examples to get you started:

### Drawing a Simple Rectangle
```python
rect(10, 10, 100, 50, '#FF5733')
```
