
from threading import Thread

class ReturnThread(Thread):
	def __init__(self, target=None):
		Thread.__init__(self, target=target)
		self.__result = None
		
		
	
	def run(self):
		try:
			if self._target is not None:
				self.__result = self._target(*self._args, **self._kwargs)
		finally:
			del self._target, self._args, self._kwargs
		

	def join(self, timeout=None):
		super(ReturnThread, self).join(timeout)
		return self.__result