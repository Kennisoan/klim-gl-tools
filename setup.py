from setuptools import setup, find_packages

setup(
		name='klim-gl-tools',
		version='0.5.4dev',
		packages=find_packages(),
		description='A collection of tools for PyOpenGL projects',
		author='Klim Korovkin',
		author_email='klimkorovkin@yandex.ru',
		url='https://github.com/Kennisoan/klim-glut-tools',
		install_requires=[
				'PyOpenGL',
				'numpy',
				'pillow'
		],
)
