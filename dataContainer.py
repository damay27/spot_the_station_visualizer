class dataContainer:
	
	approachAngle=0
	approachDirection=''
	departureAngle=0
	departureDirection=''
	maxAngle=''
	duration=''
	time=''
	date=''
	
	dataList=[]
	
	index=0
	
	def __init__(self, dataList):

		self.dataList=dataList

		
		#extract the data from the returned list
		self.approachAngle=float(dataList[self.index]['approachAngle'])
		self.approachDirection=dataList[self.index]['approachDirection']
		self.departureAngle=float(dataList[self.index]['departureAngle'])
		self.departureDirection=dataList[self.index]['departureDirection']
		self.maxAngle=dataList[self.index]['highestAngle']
		self.duration=dataList[self.index]['duration']
		self.time=dataList[self.index]['time']
		self.date=dataList[self.index]['date']
		
	def updateData(self):
		
		#extract the data from the returned list
		self.approachAngle=float(self.dataList[self.index]['approachAngle'])
		self.approachDirection=self.dataList[self.index]['approachDirection']
		self.departureAngle=float(self.dataList[self.index]['departureAngle'])
		self.departureDirection=self.dataList[self.index]['departureDirection']
		self.maxAngle=float(self.dataList[self.index]['highestAngle'])
		self.duration=self.dataList[self.index]['duration']
		self.time=self.dataList[self.index]['time']
		self.date=self.dataList[self.index]['date']
	
	#shift the internal index 1 right
	def indexRight(self):
		self.index+=1
		
		if self.index>len(self.dataList)-1:
			self.index=0
			
		self.updateData()
	
	#shift the internal index 1 left	
	def indexLeft(self):

		self.index-=1
		
		if self.index<0:
			self.index=len(self.dataList)-1
		
		self.updateData()
