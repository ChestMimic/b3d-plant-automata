bl_info = {
	"name":"Plant Automata",
	"description":"Generate plants",
	"version":(0,1,0),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Object",
	"author":"Mark Fitzgibbon"
}

import bpy

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

###EXCEPTIONS###
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

class GalapagosBlenderTurtle:
	def __init__(self, rule):
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
	
	def execute(self, context):
		sys = LSystem()
		sys.addRule('A', 'AB')
		sys.addRule('B', 'A')

		codex = sys.generate(4, 'A')
		roshi = GalapagosBlenderTurtle(codex)
		return {'FINISHED'}

def register():
	bpy.utils.register_class(LSysOperator)

def unregister():
	bpy.utils.unregister_class(LSysOperator)

if __name__ == "__main__":
	register()