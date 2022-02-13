

import requests
from bs4 import BeautifulSoup
import datetime

MONTHS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]

class MoonPhase():
	"""
	Getting Moon phase from Observatoire Royal de Belgique
	"""


	def __init__(self,year) -> None:
		self.year = year
		self.url = "http://robinfo.oma.be/fr/astro-info/lune/phases-de-la-lune-to_replace/"
		self.moon_phase_dico = {}


	def _get_httml_page(self):
		"""
		return httml page from http://robinfo.oma.be/fr/astro-info/lune/phases-de-la-lune-2022/
		this page contains all moon phase for this year 
		"""
		
		response = requests.get(self.url.replace("to_replace",str(self.year)))
		return response

	def get_page(self):
		"""
		return moon phase by scrapping self.url
		"""

		page_resp = self._get_httml_page()

		if page_resp.status_code == 200: # page get correctly

			moon_phase = self._extract_moon_phase(page_resp.content)

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
			items = [ tuple(item.replace("</th></tr>","").strip().split("à")) for item in items if item]
			self.moon_phase_dico[lunation_number] = items
		

if __name__ == "__main__":
	year = datetime.datetime.today().year
	print(year)
	moon_phase = MoonPhase(year)
	moon_phase.scrapping()