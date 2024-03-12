# Klim's GL Tools

Klim's GL Tools is a custom Python library designed to streamline the process of creating graphical elements with OpenGL. It simplifies the task of drawing basic geometric shapes and executing more intricate designs, such as gradients.

## Installation

Klim’s GL Tools can be installed either manually or via pip with the following command:
```bash
pip3 install git+https://github.com/Kennisoan/klim-gl-tools.git
```
After installation, import the desired elements from the library to start utilizing its features.
```python
from klim_gl_tools import Rectangle ...
```

## Getting Started

At the heart of Klim’s GL Tools are two core concepts: objects and modifiers. Objects are the visual elements, such as shapes or figures, that you intend to display. Modifiers, on the other hand, are used to alter the appearance or behavior of these objects.

Consider the following example:
```python
Rectangle() \
  .position(0, 50) \
  .size(100, 50) \
  .fill("#FFD266") \
  .draw()
```
In this snippet, `Rectangle` represents the object, while `.position()`, `.size()`, and `.fill()` are modifiers that define the rectangle's characteristics.

The `.draw()` modifier is unique as it does not modify the object's attributes but instead renders the object onto the screen. It is crucial to apply this modifier last to ensure all other modifications are reflected in the final display.

Different objects support various modifiers, tailored to their specific characteristics. For detailed information on the objects and applicable modifiers, refer to the [Objects](#objects) and [Modifiers](#modifiers) sections.

## Objects

The table below outlines the available objects along with their descriptions and applicable modifiers:

| Object     | Description               | Modifiers                                                   |
|------------|---------------------------|-------------------------------------------------------------|
| `Rectangle`| A rectangle shape.        | `.position()`<br>`.size()`<br>`.fill()`<br>`.gradient()`<br>`.draw()` |
| `Ellipse`  | An ellipse shape.         | `.position()`<br>`.size()`<br>`.quality()`<br>`.fill()`<br>`.draw()` |
| `Polygon`  | A complex polygon shape.  | `.useVertexArray()`<br>`.useSvgPath()`<br>`.position()`<br>`.tessellate()`<br>`.fill()`<br>`.draw()` |
| `Tree`     | A simple tree with fill.  | `.position()`<br>`.size()`<br>`.fill()`<br>`.gradient()`<br>`.draw()` |

## Modifiers

Modifiers are instrumental in defining the properties and behaviors of objects. Below is a table summarizing each modifier and its purpose:

| Modifier           | Description                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------|
| `draw()`           | Renders the object onto the screen or canvas. Apply this last to ensure all modifications are displayed. |
| `position(x, y)`       | Sets the object's location with `x` and `y` coordinates.                                      |
| `size(width, height)`           | Determines the object's dimensions. Accepts width and height, using the width if height is omitted. |
| `fill(hex-string)`           | Colors the object with a solid color, specified by a HEX code.                                |
| `gradient([hex-string, hex-string])`       | Creates a vertical gradient by transitioning between two HEX-coded colors.                    |
| `quality(n)`        | Adjusts the rendering quality of the object for finer control over its appearance.            |
| `useVertexArray(data)` | Builds the shape using an array of vertex points.     |
| `useSvgPath(data)`     | Builds the shape using SVG path data.              |
| `tessellate()`     | Applies tessellation to the shape, breaking it into smaller geometrical figures.   |
