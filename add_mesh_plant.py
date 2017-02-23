class Rule:
	'''
	Definition of an individual rule for an L System
	'''
	def __init__(self, value, ruling, probablility = 1):
		self.value = value
		self.ruling = [(ruling, probablility )]
		
	def pickRuling(self, roll=1):
		flag = 0.0
		for r in self.ruling:
			flag += r[1]
			if flag >= roll:
				return r[0]
		return None

	def fitRuleWeighting():
		pass


class  LinSysAutomata:
	'''
	Definition of a string based L System interpreter
	'''
	def __init__(self):
		self.rules = []

	def addRule(value, rule, weight):
		pass

	def removeRule(value):
		pass



if __name__ == '__main__':
	r1 = Rule('A', 'AB')
	r2 = Rule('B', 'A', 1)

	print(r1.value)
	print(r1.pickRuling(1))