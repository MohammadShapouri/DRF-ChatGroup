import string
import random


class RandomLinkGenerator:
	def __init__(self, allowed_chars=string.ascii_letters + string.digits, length=16):
		self.allowed_chars = allowed_chars
		self.length = length


	def __call__(self):
		return self.generate()


	def generate(self):
		return random.choice(string.ascii_letters) + ''.join(random.choice(self.allowed_chars) for i in range(self.length))


CallableRandomLinkGenerator = RandomLinkGenerator()