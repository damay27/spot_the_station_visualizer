import requests
from bs4 import BeautifulSoup
import re


def retrive(country, state, city, duration, appearAngle, disappearAngle, highestAngle):

	returnList=[]

	#create the url
	url='https://spotthestation.nasa.gov/sightings/xml_files/'+country+'_'+state+'_'+city+'.xml'
	
	#make request and get data from the resonse
	response=requests.get(url)
	soup=BeautifulSoup(response.text, 'lxml')
	sightings=soup.find_all('item')

	nextSighting={}

	for sighting in sightings:
		
		#extract and format the description
		description=sighting.find('description').text
		description=description.replace('\n', '')
		description=description.replace('\t', '')
		description=description.split('<br/>')
		
		#regex for date
		match=re.match('Date: (\D.+)', description[0])
		
		if match:
			nextSighting['date']=match.group(1).strip()
		else:
			raise ValueError('NO MATCHING DATE STRING')
		
		
		#regex for time
		match=re.match('Time: (\d.+)', description[1])
		
		if match:
			nextSighting['time']=match.group(1).strip()
		else:
			raise ValueError('NO MATCHING TIME STRING')
		

		#regex for duration
		match=re.match(r'Duration: (.+) minute', description[2])

		if(match):
			
			if match.group(1)=='less than  1' and duration>0:
				nextSighting['duration']=match.group(1)
			elif match.group(1).isnumeric() and int(match.group(1) )>=duration:
				nextSighting['duration']=match.group(1)
			else:
				continue
		else:
			raise ValueError('NO MATCHING DURATION STRING')
		
		#regex for highest angle
		match=re.match(r'Maximum Elevation: (.+)° ', description[3])

		if match:
			if match.group(1).isnumeric() and int( match.group(1) )>=highestAngle:
				nextSighting['highestAngle']=match.group(1)
			else:
				continue
		else:
			raise ValueError('NO MATCHING MAX ELIVATION STRING')

		
		#regex for approach angle
		match=re.match('Approach: (.+)° above (\D)', description[4])
		
		if match:
			
			if int( match.group(1) )>=appearAngle:
				nextSighting['approachAngle']=match.group(1)
				nextSighting['approachDirection']=match.group(2)
			else:
				continue
		else:
			raise ValueError('NO MATCHING APPROACH ANGLE STRING')


		#regex for departure angle
		match=re.match('Departure: (.+)° above (\D)', description[5])

		if match:
			
			if int(match.group(1))>=disappearAngle:
				nextSighting['departureAngle']=match.group(1)
				nextSighting['departureDirection']=match.group(2)
			else:
				continue

		else:
			raise ValueError('NO MATCHING DEPARTURE ANGLE STRING')

		
		#if all the data is with in range add the sighting to the list
		returnList.append( nextSighting.copy() )
		

	return returnList





