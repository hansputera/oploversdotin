from main import getAnimesByGenre, getAnimesOngoing, getAnimesBySeries, searchAnime

#	Get animes by genre.
data = getAnimesByGenre("action")
print(data)

# Get Animes by on-going lists.
data1 = getAnimesOngoing()
print(data1)

# Get Animes by Series
data2 = getAnimesBySeries()
print(data2)

# Search anime
narutoResults = searchAnime("naruto")
print(narutoResults)