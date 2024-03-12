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
Renders a filled polygon from a list of vertices. Use it for custom shapes. Specify vertices in an array like this: `[(x1,y1), (x2,y2), ...]`.

### Tessellate shape
```python
tessellate(vertices, color, xoffset=0.0, yoffset=0.0)
```
Similar to `polygon`, but for complex shapes that require tessellation to render correctly. Specify vertices in an array like this: `[(x1,y1), (x2,y2), ...]`.

### Low-poly tree
```python
tree(x, y, height, color, root_color)
```
Draws a stylized, low-poly tree. Useful for adding simple natural elements to a scene.

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

## Examples

Here are a few examples to get you started:

### Drawing a Simple Rectangle
```python
rect(10, 10, 100, 50, '#FF5733')
```
