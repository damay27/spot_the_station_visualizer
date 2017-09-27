import pygame
import math
import getData
import sys
import dataContainer

pygame.init()

def centerText(x, y, text):
	
	x=int( x - (text.get_rect().width/2) )
	y=int( y - (text.get_rect().height/2) )
	
	return (x, y)
		


#set the font
font=pygame.font.SysFont(None, 30)



#get the data from the server

country=input('Enter contry: ')
country=country.replace(' ', '_')

state=input('Enter state/province: ')
state=state.replace(' ', '_')

city=input('Enter city: ')
city=city.replace(' ', '_')


try:
	duration=int( input('Minium duration: ') )
	appearAngle=int( input('Minimum appearance angle: ') )
	disappearAngle=int( input('Minimum disappearance angle: ') )
	highestAngle=int( input('Minimum highest angle: ') )
	dataList=getData.retrive(country, state, city, duration, appearAngle, disappearAngle, highestAngle)
except ValueError:
	print('INVALID INPUT')
	sys.exit()

if len(dataList)==0:
	print('No matching data found')
	sys.exit()

#get the spacestation data
data=dataContainer.dataContainer(dataList)
	

#load image files
background=pygame.image.load('background.png')
backgroundRect=background.get_rect()



#create window
windowSize=(640, 480)
window=pygame.display.set_mode(windowSize)

#set the starting point of the line
staticPoint=(int(windowSize[0]*.5), int(windowSize[1]*.8) )


#start the timer
timerTime=100
pygame.time.set_timer(pygame.USEREVENT+1, timerTime)



#initialize variables for the line
radius=windowSize[0]*.45



#set how far apart each point in the trail should be in degrees
trailSpacing=10

#create global variables that will be used later on
textColor=(0,0,100)

#variable to control when new data should be loaded and values recalculated
#this is set to true at the start so that the global variables will have their data loaded at the start
update=True

#variable used to end the loop when the program closes
running=True
while running:
	
	#if the data has changed updata the variables 
	#(note this block does not handle drawing anything)
	if update:
		
		#recalculate all the points
		angle=-data.approachAngle
		
		startingPoint=(int(math.cos(math.radians(angle))*radius), int(math.sin(math.radians(angle))*radius))
		endingPoint=(int(math.cos(math.radians(-180+data.departureAngle))*radius), int(math.sin(math.radians(-180+data.departureAngle))*radius))
		
		
		x=int(math.cos(math.radians(angle))*radius)
		y=int(math.sin(math.radians(angle))*radius)
		
		trailTicks=0
		trailList=[]
		
		#setup on screen text
		timeDateText=font.render(data.date+' '+data.time, False, textColor)
		timeDatePoint=centerText(windowSize[0]*.5, windowSize[1]*.9, timeDateText)
		
		durationText=font.render('Duration: '+data.duration+ ' min', False, textColor)
		durationPoint=centerText(windowSize[0]*.5, windowSize[1]*.8, durationText)
		
		approachText=font.render(str(data.approachAngle)+ ' degrees '+ data.approachDirection, False, textColor)
		approachPoint=centerText(windowSize[0]*.2, windowSize[1]*.5, approachText)
		
		departureText=font.render(str(data.departureAngle)+ ' degrees '+data.departureDirection, False, textColor)
		departurePoint=centerText(windowSize[0]*.8, windowSize[1]*.5, departureText)
		
		elevationText=font.render('Max elevation: '+str(data.maxAngle), False, textColor)
		elevationPoint=centerText(windowSize[0]*.5, windowSize[1]*.15, elevationText)
				
				
		update=False


	#get all of the events that have occured
	eventList=pygame.event.get()

	#loop through the events
	for event in eventList:

		if event.type == pygame.QUIT:
			running=False
			
			
		#when this event occurs it updates the position of moving objects and draws everything
		elif event.type == pygame.USEREVENT+1:
			
			#every tick increase the angle 1 degree and adjust the line
			x=math.cos(math.radians(angle))*radius
			x=int(x)
			y=math.sin(math.radians(angle))*radius
			y=int(y)
			angle-=1


			trailTicks+=1
			if trailTicks==trailSpacing:
				
				trailList.append( (x,y) )
				trailTicks=0
			
			
			#check and see if the angle is equal to the departure angle 
			#and if so reset the line and the trail
			if angle<(-180+data.departureAngle):
				angle=-data.approachAngle
				trailList=[]
				trailTicks=0
			
			
			#draw all the objects on the screen. this occurs once every tick
			window.fill( (0,0,0) ) 
			window.blit(background, backgroundRect)
			
			#loop through the list of points and draw a circle at each one
			for marker in trailList:
				
				#the position is calculated as an offset from the static point at the center
				pygame.draw.circle(window, (0,128,128), (staticPoint[0]+marker[0],staticPoint[1]+marker[1]), 5, 2)
				
			#draw circles at the starting and ending points
			pygame.draw.circle(window, (0,255,0), (staticPoint[0]+startingPoint[0], staticPoint[1]+startingPoint[1]), 7)
			pygame.draw.circle(window, (255,255,0), (staticPoint[0]+endingPoint[0], staticPoint[1]+endingPoint[1]), 7)

			#draw the line that sweeps accrosed the screen and place a circle at the end of it
			pygame.draw.line(window, (128, 128, 128), staticPoint, (staticPoint[0]+x,staticPoint[1]+y), 6)
			pygame.draw.circle(window, (255, 0, 0), (staticPoint[0]+x,staticPoint[1]+y), 7)
			
			
			
			#draw all of the text objects
			window.blit(timeDateText, timeDatePoint)
			window.blit(durationText, durationPoint)
			window.blit(approachText, approachPoint)
			window.blit(departureText, departurePoint)
			window.blit(elevationText, elevationPoint)
			
			pygame.display.update()
			
			
			
		elif event.type == pygame.KEYDOWN:
			
			update=False

			#if the right key was pressed increment the index 
			if event.key==pygame.K_RIGHT:
				
				data.indexRight()
				
				update=True
				
			
			#if the left key is pressed decrement the index
			if event.key==pygame.K_LEFT:
				
				data.indexLeft()
				
				update=True
				
			


	
