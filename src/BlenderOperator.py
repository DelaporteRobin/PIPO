import os
import sys
import json
import traceback


class BlenderOperator:
	def blender_identify(self):
		print("ask for identification")

	def blender_hello(self):
		print("Hello world")

	def blender_create_cube(self):
		print("trying to create the perfect cube!")
		exec("bpy.ops.mesh.primitive_cube_add()")