from typing import List

class MovingAverage:
	n: int
	items: List[float] = []

	def __init__(self, n: int):
		self.n = n

	def add(self, item: float):
		self.items.append(item)
		if len(self.items) > self.n:
			self.items.pop(0)

	def average(self) -> float:
		return sum(self.items) / float(self.n)
	
# class FastQueue(Queue(0)):
# 	# def __init__(self, maxsize: int = 0, *, ctx: Any = ...) -> None:
# 	# 	super().__init__(maxsize, ctx=ctx)

# 	def get(self) -> Any | None:
# 		if self.empty():
# 			return None
# 		else:
# 			return self.get()
# 		# try:
# 		# 	return self.queue.get_nowait()
# 		# except:
# 		# 	return None
		
# 	# def put(self, value: Any):
# 	# 	self.queue.put(value)
