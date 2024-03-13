class useVertexArrayMixin:
	def useVertexArray(self, array: list):
		"""
		Builds shape from a vertex array of shape: [(x1,y1), (x2,y2), ...].
		"""
		self._vertices = array
		return self

class useSvgPathMixin:
	def useSvgPath(self, path: str):
		"""
		Builds shape from SVG path data (<path d="..." />).
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
			
		self._vertices = points
		return self
