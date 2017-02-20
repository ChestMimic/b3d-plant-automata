bl_info = {
	"name":"Plant Automata",
	"description":"Generate plants",
	"version":(0,1,0),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Object",
	"author":"Mark Fitzgibbon"
}

import random

import bpy
from bpy.props import StringProperty, IntProperty

class Rule:
	'''
	Definition of an individual rule for an L System
	'''
	def __init__(self, value, ruling, probablility = 1):
		self.value = value
		self.ruling = [(ruling, probablility )]
		pass

	def pickRuling(self, seed = None):
		random.seed(seed)
		num = random.random()

		flag = 0.0
		for r in self.ruling:
			flag += r[1]
			if flag >= num:
				return r[0]
		return None


class LSystem:
	'''
	Defines an L_System Grammar to be used with Strings
	'''
	def __init__(self):
		'''
		Initialize an empty L-System ruleset.
		'''
		self.rules = {}

	def getRule(self, value):
		"""
		Locate the rule accosiated with given string.
		value -- desired key to be analyzed
		"""
		if value in self.rules:
			return self.rules[value]
		else:
			return None

	def addRule(self, var, rule = None):
		"""
		Attempt to add a new variable as a constant (no rule) or variable (rule defined) 
		var -- the variable to attempt to add
		rule -- the rule the variable is associated with. If None, var is assumed to be a constant
		"""
		if rule is None:
			#self.appendCons(var)
			self.rules[var] = var
		elif (var in self.rules):
			raise  RuleConflictError(
				var, self.rules.get(var), 
				"Rule is already defined")
		else:
			#self.appendVar(var)
			self.rules[var] = rule

	def perform(self, axiom):
		"""
		Perform one generation's worth of rule executions
		Current implementation assumes each rule is for one character.
		axiom -- String to be performed with
		""" 
		#trueAxi = list(axiom)
		output = ""
		for char in list(axiom):
			output += self.getRule(char)
		return output

	def generate(self, n, axiom):
		"""
		Generate an output string for this L_System.
		n -- Number of generations to perform.
		axiom -- initial string to perform with
		"""
		res = axiom
		while( n > 0):
			res = self.perform(res)
			n = n-1
		return res

	def toString(self):
		res = "["
		for r in list(self.rules.keys()):
			res += "{" + r + "->" + self.rules[r] + "}"
		res += "]"
		return res

class Error:
	"""
	Base exceptions for this module
	"""
	pass

class RuleConflictError(Error):
	"""
	Raised when a user attempts to create a rule that conflicts with a previously defined rule
	
	Attributes:
        faultyRule --
        existantRule --
        message -- explanation of the error
    """
	def __init__(self, faultyRule, existantRule, message):
		self.faultyRule = faultyRule
		self.existantRule = existantRule
		self.message = message

def GalapagosBlenderTurtle(rule):
	#A = Step North
	#B = Draw Cube
	#Also, never do this
	for c in rule:
		if c == 'A':
			bpy.ops.mesh.primitive_cube_add(location=bpy.context.scene.cursor_location)
		if c == 'B':
			tup = bpy.context.scene.cursor_location
			tup[1] += 3
			bpy.context.scene.cursor_location = tup

class LSysOperator(bpy.types.Operator):
	bl_idname = "object.automata"
	bl_label = "L System Automata"
	bl_optons = {'REGISTER', 'UNDO'}

	startingChain = StringProperty(
		name = "Initial String",
		default = "A")

	generations = IntProperty(
		name = "Generations",
		min = 1,
		default = 4)

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	
	def execute(self, context):
		sys = LSystem()
		sys.addRule('A', 'AB')
		sys.addRule('B', 'A')

		codex = sys.generate(self.generations, self.startingChain)
		GalapagosBlenderTurtle(codex)
		return {'FINISHED'}

def register():
	bpy.utils.register_class(LSysOperator)

def unregister():
	bpy.utils.unregister_class(LSysOperator)

if __name__ == "__main__":
	register()