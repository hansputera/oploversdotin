from cloudscraper import create_scraper
from bs4 import BeautifulSoup
from re import sub

class Oploverz:
	baseURL = "https://www.oploverz.in"

	# Endpoints
	endpoints = {
		"ongoing": "ongoing-series",
		"series": "series",
		"genres": [
			"action",
			"adventure",
			"cars",
			"comedy",
			"demons",
			"drama",
			"ecchi",
			"fantasy",
			"game",
			"harem",
			"historical",
			"horror",
			"infinite",
			"isekai",
			"josei",
			"kids",
			"klockworx",
			"magic",
			"martial-arts",
			"mecha",
			"military",
			"movic",
			"music",
			"mystery",
			"parody",
			"police",
			"psychological",
			"romance",
			"samurai",
			"school",
			"sci-fi",
			"seinen",
			"shoujo",
			"shounen",
			"shounen-duration-1-hr",
			"showgate",
			"slice-of-life",
			"sotsu",
			"space",
			"sports",
			"super-power",
			"supernatural",
			"thriller",
			"tutorial",
			"vampire",
			"warner-bros"
		]
	}

	# functions

	def getGenreURL(genreName: str) -> str or None:
		if genreName.lower() not in Oploverz.endpoints.get("genres"):
			return None
		else:
			return f"{Oploverz.baseURL}/genres/{genreName.lower()}"

# Request handle
def request(url: str):
	scraper = create_scraper()
	response = scraper.get(url)

	if response.reason != "OK":
		return None
	else:
		return response

# Get animes by genre.
def getAnimesByGenre(genre: str):
	genreURL = Oploverz.getGenreURL(genre)
	if genreURL is None:
		return None
	else:
		animes = []
		response = request(genreURL)
		if response is None:
			return None
		else:
			html = response.text
			soup = BeautifulSoup(html, "html5lib")

			pageElement = soup.find('div', class_="page")
			titleGenre = pageElement.findNext('h1').text.replace("\"Genre\"", "").strip()

			genreAnimes = pageElement.findNext('ul', class_="listres").find_all('li')
			for animeElement in genreAnimes:
				thumbnail = animeElement.findNext('img').attrs['src']
				anime_detail = {
					"name": animeElement.findNext('h2').text.strip(),
					"url": animeElement.findNext('h2').findNext('a').attrs['href'],
					"description": animeElement.findNext('div', class_="desc").text.strip()
				}

				anime_detail['info'] = getAnimeByUrl(anime_detail['url'])

				animes.append({
					"genreType": titleGenre,
					"anime_detail": anime_detail,
					"thumbnail": thumbnail
				})
			return animes


# Get On-Going animes.
def getAnimesOngoing():
	response = request(f"{Oploverz.baseURL}/{Oploverz.endpoints.get('ongoing')}")

	if response is None:
		return None
	else:
		animes = []
		html = response.text
		soup = BeautifulSoup(html, "html5lib")

		# Collecting animes.
		for animeElement in soup.find('div', class_="page").findNext('ul').find_all('li'):
			thumbnail = animeElement.findNext('img').attrs['src']
			anime_detail = {
				"name": animeElement.findNext('h2').text.strip(),
				"url": animeElement.findNext('h2').findNext('a').attrs['href']
			}

			anime_detail['info'] = getAnimeByUrl(anime_detail['url'])

			meta_data = animeElement.find_all('span')
			
			type_ = meta_data[0].text.strip().split(" ")[1]
			genres = []
			if meta_data[1].findNext('b') != None:
				genres_ = meta_data[1].find_all('a')
				for genreElement in genres_:
					genres.append({
						"name": genreElement.text.strip(),
						"url": genreElement.attrs['href']
					})
			
			animes.append({
				"anime_detail": anime_detail,
				"type": type_,
				"genres": genres,
				"thumbnail": thumbnail
			})
		return animes

# Animes by Series.
def getAnimesBySeries():
	response = request(f"{Oploverz.baseURL}/{Oploverz.endpoints.get('series')}")
	
	html = response.text
	soup = BeautifulSoup(html, "html5lib")
	animes = []

	seriesElement = soup.find('div', class_="postbody").find_all('div', class_="movlist")

	for serieElement in seriesElement:
		serieCharacter = serieElement.findNext('div', class_="alpha").attrs['id']
		serie_animes = []

		serieAnimesElement = serieElement.findNext('ul').find_all('li')
		for animeElement in serieAnimesElement:
			name = animeElement.find('a').text.strip()
			url = animeElement.find('a').attrs['href']
			serie_animes.append({
				"name": name,
				"url": url
			})
		
		animes.append({
			"character": serieCharacter,
			"animes": serie_animes
		})
	return animes


# Get anime information by url.

def getAnimeByUrl(url: str):
	response = request(url)
	if response == None:
		return None
	else:
		html = response.text
		soup = BeautifulSoup(html, "html5lib")
		anime_desc = soup.find('div', class_="animeinfos").findNext('div', class_="imgdesc")

		# Anime structure.
		image = anime_desc.findNext('img').attrs['src']
		name = anime_desc.findNext('span', class_="desc").findNext('b').text.split("Sinopsis")[1].strip()
		sinopsiss = []
		for sinopsisText in anime_desc.findNext('span', class_="desc").find_all('p'):
			sinopsiss.append(sinopsisText.text.strip())
		
		# Anime Info, and Episodes.
		anime_info = soup.find('div', class_="animeinfos").findNext('div', class_="listinfo")
		meta = ""

		for metaElement in anime_info.findNext('ul').find_all('li'):
			meta += f"{metaElement.text.strip()}\n"
		
		episodesElement = soup.find('div', class_="animeinfos").findNext('div', class_="episodelist").findNext('ul').find_all('li')

		episodes = []
		for episodeElement in episodesElement:
			url = episodeElement.find('span', class_="leftoff").findNext('a').attrs['href']
			title = episodeElement.find('span', class_="lefttitle").findNext('a').text.strip()
			date_ = episodeElement.find('span', class_="rightoff").text.strip()
			episode = episodeElement.find('span', class_="leftoff").text.split('Episode')[1].strip()

			episodes.append({
				"title": title,
				"url": url,
				"date": date_,
				"episode": int(episode)
			})
		
		return {
			"name": name,
			"image": image,
			"sinopsis": "".join(sinopsiss),
			"episodes": episodes
		}


# Search anime
def searchAnime(anime: str):
	response = request(f"{Oploverz.baseURL}/?s={anime}")
	if response is None:
		return None
	else:
		html = response.text
		soup1 = BeautifulSoup(html, "html5lib")

		if (soup1.find('div', class_="postbody").findNext('ul').findNext('li') is None):
			return None

		if (soup1.find('div', class_="postbody").findNext('ul').findNext('div', class_="pagination").findNext('div', class_="wp-pagenavi") is None):
			videosElement = soup1.find('div', class_="postbody").findNext('ul').find_all('li')
			videos = []
			for videoElement in videosElement:
				thumbnail = videoElement.find('div', class_="thumb").findNext('a').findNext('img').attrs['src']

				url = videoElement.find('div', class_="dtl").findNext('h2').findNext('a').attrs['href']
				
				title = videoElement.find('div', class_="dtl").findNext('h2').text.strip()
				release = videoElement.find('div', class_="dtl").findNext('span').findNext('span').text.strip().replace('Rilis hari Minggu, ', '').split('Lihat daftar isi')[0].strip()
				videos.append({
					"title": title,
					"url": url,
					"thumbnail": thumbnail,
					"release": release
				})
			return [{
				"page": 1,
				"videos": videos
			}]

		posts = soup1.find('div', class_="postbody").findNext('ul').findNext('div', class_="pagination").findNext('div', class_="wp-pagenavi").find_all('a')

		index = 0
		lastIndex = str(posts[-1].attrs['href']).translate({ord(c) : ""  for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})


		lastIndex = int(sub(r"[\s||a-z||A-Z]", "", str(lastIndex)))

		def getPage(pageNum: int):
			return f"https://www.oploverz.in/page/{pageNum}/?s={anime}"
		
		pages = []

		for _ in range(lastIndex):
			index = index+1
			resPage = request(getPage(index))
			htmlPage = resPage.text
			soup = BeautifulSoup(htmlPage, "html5lib")
			videosElement = soup.find('div', class_="postbody").findNext('ul').find_all('li')
			videos = []
			for videoElement in videosElement:
				thumbnail = videoElement.find('div', class_="thumb").findNext('a').findNext('img').attrs['src']

				url = videoElement.find('div', class_="dtl").findNext('h2').findNext('a').attrs['href']
				
				title = videoElement.find('div', class_="dtl").findNext('h2').text.strip()
				release = videoElement.find('div', class_="dtl").findNext('span').findNext('span').text.strip().split('Lihat daftar isi')[0].split(',', 1)[1].strip()

				videos.append({
					"title": title,
					"url": url,
					"thumbnail": thumbnail,
					"release": release
				})
			print(f"Found {len(videos)} videos for page {index}")
			pages.append({
				"page": index,
				"videos": videos
			})
		return pages

