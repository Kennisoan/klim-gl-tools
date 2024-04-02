# Klim’s GL Tools

Klim's GL Tools is a custom Python library designed to streamline the process of creating graphical elements with OpenGL. It simplifies the task of drawing basic geometric shapes and executing more intricate designs, such as gradients.

## Installation

Klim’s GL Tools can be installed either manually or via pip with the following command:
```bash
pip3 install git+https://github.com/Kennisoan/klim-gl-tools.git
```
After installation, import the desired elements from the library to start utilizing its features.
```python
from klim_gl_tools import Rectangle, ...
```

Note: Klim’s GL Tools assumes a coordinate system that starts at the top-left corner of the canvas, with x increasing to the right and y increasing downwards. This orientation is crucial for positioning and transforming objects correctly within your projects.


## Getting Started

At the heart of Klim’s GL Tools are two core concepts: objects and modifiers. Objects are the visual elements, such as shapes or figures, that you intend to display. Modifiers, on the other hand, are used to alter the appearance or behavior of these objects.

### Example:
Let's create a rectangle and customize it:
```python
Rectangle() \
  .position(0, 50) \
  .size(100, 50) \
  .fill("#FFD266") \
  .draw()
```
Here, `Rectangle` is the object. The methods `.position()`, `.size()`, and `.fill()` are modifiers that define its characteristics. The `.draw()` method is crucial as it renders the object on the screen, showcasing all preceding modifications.

Different objects support various modifiers, tailored to their specific characteristics. For detailed information on the objects and applicable modifiers, refer to the [Objects](#objects) and [Modifiers](#modifiers) sections.

Integrate your objects into a display function to see them rendered in your application. For an example on how this can be done with GLUT, refer to `template.py`.

## Objects

The table below outlines the available objects along with their descriptions and applicable modifiers:

### Basic shapes

<table>
  <tr>
    <th>Object</th>
    <th>Generic Modifiers</th>
    <th>Specific Modifiers</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>Rectangle</code></td>
    <td rowspan="3">
      <a href="#position"><code>.position()</code></a><br>
      <a href="#rotation"><code>.rotation()</code></a><br>
      <a href="#fill"><code>.fill()</code></a><br>
      <a href="#stroke"><code>.stroke()</code></a><br>
      <a href="#gradient"><code>.gradient()</code></a><br>
      <a href="#mask"><code>.mask()</code></a><br>
      <a href="#draw"><code>.draw()</code></a>
    </td>
    <td><a href="#size"><code>.size()</code></a></td>
    <td>A rectangular shape.</td>
  </tr>
  <tr>
    <td><code>Ellipse</code></td>
    <td>
      <a href="#size"><code>.size()</code></a><br>
      <a href="#quality"><code>.quality()</code></a>
    </td>
    <td>An ellipse shape. Adjust its segment count with <code>.quality()</code> to change the amount of segments used to represent the ellipse (default is 100).</td>
  </tr>
  <tr>
    <td><code>Polygon</code></td>
    <td>
      <a href="#path"><code>.path()</code></a><br>
      <a href="#tessellate"><code>.tessellate()</code></a>
    </td>
    <td>A complex polygon shape. Use <code>.tessellate()</code> on non-convex shapes to allow them to be displayed properly. Tessellated shapes don't support <code>.gradient()</code>.</td>
  </tr>
</table>

### Misc

<table>
  <tr>
    <th>Object</th>
    <th>Generic Modifiers</th>
    <th>Specific Modifiers</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>Tree</code></td>
    <td>
      <a href="#position"><code>.position()</code></a><br>
      <a href="#gradient"><code>.gradient()</code></a><br>
      <a href="#draw"><code>.draw()</code></a>
    </td>
    <td><a href="#height"><code>.height()</code></a></td>
    <td>A simple tree with a gradient from roots to foliage. Use <code>.height()</code> to set its height in pixels.</td>
  </tr>
</table>

## Modifiers

Modifiers are instrumental in defining the properties and behaviors of objects. Below is a table summarizing each modifier and its purpose:

#### `.position()`
Changes the shapes position on canvas. Uses `x` and `y` as input. If `y` is omitted, `x` is used for both values. The shapes's position center is considered to be (0, 0).
```python
.position(10, 20) # Positions object at 10x and 20y
.position(5) # Positions object at 5x and 5y
.position() # Positions object at 0x and 0y (default)
```

#### `.rotation()`
Applies rotation to the shape. Uses angle as input. By default, the object is rotated around its center, but an anchor point can be specified with relative `x` and `y` coordinates.
```python
.rotation(45) # Rotates object 45° around its center
.position(90, anchor=(0,0)) # Rotates object 90° around (0,0) point
.position(90, (0,0)) # Rotates object 90° around (0,0) point
```

#### `.fill()`
Applies a solid color fill to a shape. Uses HEX color string as inout.
```python
.fill("#FF0000") # Fills object with a red color
.fill() # Fills object with a black color (default)
```

#### `.gradient()`
Applies a linear gradient to a shape. Uses HEX color strings and an integer angle as inout.
```python
.gradient("#FF0000", "#000FF") # Applies a red-to-blue gradient
.gradient("#FF0000", "#0FF00", "#000FF", angle=90) # Applies a multi-color gradient
.gradient("#FF0000", "#0FF00", "#000FF", angle=90) # Applies a multi-color gradient, rotated by 90 degrees
```

#### `.stroke()`
Applies a stoke to a shape. Takes stroke width and color as optional inputs,
```python
.stroke(3, "#FF0000") # Adds a 3px red stroke
.stroke(color="#0000FF") # Adds a 1px blue stroke
.stroke() # Adds a 1px black stroke (default)
```

#### `.mask()`
Applies a stipple mask to a shape. Accepts a pattern presented as a byte array, and a color as an optional input.
```python
.mask(pattern, "#FF0000") # Applies a red stipple mask.
.mask(pattern) # Applies a black stipple mask (default).
```

#### `.draw()`
Renders the object onto the screen or canvas. Apply this last to ensure all modifications are displayed.

### Shape-specific modifiers

#### `.size()`
Sets the size of `Recatngle` anf `Ellipse`. Uses `width` and `height` as input. If `height` is omitted, `width` is used for both values.
```python
.size(10) # Sets the object width and height to 10px
.size(10, 20) # Sets the object width to 10px and height to 20px
.size() # Sets the object width and height to opx (default)
```

#### `.path()`
Describes a `Polygon` using an array of vertices. Accetps array of vertices as a list of tuples.
```python
.path([(10,0), (20,10), (0,10)]) # Describes a triangle
.path([(0,0), (0,20), (20,20), (20,0)]) # Describes a square
```

#### `.quality()`
Sets amount of segments used to describe an `Ellipse`. Accepts amount of segments as an integer. Make sure to __use this modifier first__ to ensure that the ellipse is generated properly and all modifiers work correctly.
```python
.quality(16) # Sets quality to 16 segments
.quality() # Sets quality to 100 segments (default)
```

#### `.tessellate()`
Enables tessellation for `Polygon` objects to correctly render non-convex polygon shapes with OpenGL. Tessellation is disabled by default.

#### `.height()`
Sets the height for `Tree` object. Accepts height as integer.
```python
.height(20) # Sets the tree height to 20px
```

## Utilities

#### `useSvgPath()`
Allows to use SVG `<path/>` as a vertex array.
```python
.path(useSvgPath('<path d="M30 10.5L0 20H86V0.5H66.5L41 10.5H30Z"/>')) # Uses SVG path as vertex array input of `.path()`
```

### `useRgb()`
Allows to use an RGB color instead of HEX.
```python
.fill(useRgb(1.0, 0.0, 0.0)) # Uses red RGB color as a color input of fill
```

### `useImageAsPattern()`
Allows to use an image file as a stipple pattern. Accepts path to a file, and a threshold as an optional input. To change image's threshold, provide a thresold value from 0.0 to 1.0.
```python
.mask(useImageAsPattern('images/pattern.png')) # Uses a png image as a stipple pattern
.mask(useImageAsPattern('images/pattern.png'), threshold=0.75) # Uses a png image as a stipple pattern with a 75% threshold
```
