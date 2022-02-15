"""
	1. Thread qui verfie que la page n'a pas changer
		Seulement modifier les elements qui ont changé pas besoin de remettre les autres trucs 

	2. Thread qui lance le bot tout les 2 jours +/-
	3. Moyen d'avoir le nb de jour restant avant la prochaine phase

		suprimmer une entre quand elle a un nb neg de jours restant ...

"""









from os import sep
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime

MONTHS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
PHASE_ID = ["New Moon","First Quarter","Full Moon","Last Quarter"]
NUMBER_OF_PHASE = 4
MAX_DAYS_TO_TAKE = 3

class MoonPhase():
	"""
	Getting Moon phase from Observatoire Royal de Belgique
	"""

	def __init__(self,year) -> None:
		self.year = year
		self.url = "http://robinfo.oma.be/en/astro-info/moon/moon-phases-to_replace/"
		self.moon_phase_dico = {}


		self._load_page()


	def _get_httml_page(self):
		"""
		return httml page from http://robinfo.oma.be/fr/astro-info/lune/phases-de-la-lune-2022/
		this page contains all moon phase for this year 
		"""
		
		response = requests.get(self.url.replace("to_replace",str(self.year)))
		return response

	def _load_page(self):
		"""
		Load moon phase by scrapping self.url
		the result is a dico wich associated lunation number with each moon phase : self.moon_phase_dico
		"""

		page_resp = self._get_httml_page()

		if page_resp.status_code == 200: # page get correctly
			self._extract_moon_phase(page_resp.content)

		else:
			print("IL Y A UNE ERREUR", page_resp.status_code)
			print(f"url : {page_resp.url}")

	def _extract_moon_phase(self,html_page):
		"""
		return dictionary associationg a lunation number with
		a 4-tuple containing date+hour for those moon phase Nouvelle lune,Premier quartier,Pleine lune,Dernier quartier.
		exemple 
		"January" : ("[02 janvier,19h33]","[09 janvier,19h11]","[18 janvier,00h48]","[25 janvier,14h40]")

		"""
		soup = BeautifulSoup(html_page,'html.parser')
		s = soup.find('div', class_='page-content')
		content = s.find_all('tr')[1:] # remove first line containt header of the table

		# go through to content on the page and get table elements
		for items in content:
			# numbre : Nouvelle lune : hour,Premier quartier : hour,Pleine lune : hour,Dernier quartier : hour
			items = str(items)
			items =  items.split("</th><th>")
			lunation_number = items[0].replace("<tr><th>","")
			items = items[1:]
			#just remove usless thing and split date and hour
			items = [ parse(item.replace("</th></tr>","").strip()) for item in items if item]
			self.moon_phase_dico[lunation_number] = items
		
	def _build_day_moon_phase(self,lunation_nb,days_left,date,phase_id):
		return (lunation_nb,days_left,date,PHASE_ID[phase_id])

	def moon_phase_of_the_day():
		pass


	def day_moon_phase(self,date_time):
		date_time = datetime.date.today()+datetime.timedelta(days=1)
		next_phase_date = -1
		days_take = 0
		for lun_number, date_moon_phase in self.moon_phase_dico.items():
			for phase_id in range(NUMBER_OF_PHASE):
				phase_day = date_moon_phase[phase_id]
				days_left = phase_day.date() - date_time

				if days_left.days > next_phase_date and days_take < MAX_DAYS_TO_TAKE:
					print(self._build_day_moon_phase(lun_number,days_left.days,phase_day,phase_id))
					next_phase_date = days_left.days
					days_take += 1




if __name__ == "__main__":
	year = datetime.datetime.today().year
	print(year)
	moon_phase = MoonPhase(year)
	moon_phase.day_moon_phase("ca")