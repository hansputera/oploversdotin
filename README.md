# Oploverz[dot]in

**Scrape [oploverz.in](https://www.oploverz.in) with beautifulsoup4 python**

# Usage

1. Mencari semua daftar anime beserta informasinya berdasarkan genre.
```py
animes = getAnimesByGenre(action) 
print(animes)
```

2. Mencari semua daftar anime dari series.
```py
animes = getAnimesBySeries()
print(animes)
```

3. Mencari semua daftar anime dari on-going anime.
```
animes = getAnimesOngoing()
print(animes)
```


# Result

`getAnimeByGenre(action)`


```
[
	{
		"genreType": GenreType,
		"anime_detail": {
			"name": String,
			"url": String,
			"description": String,
			"info": {
				"title": String,
				"url": String,
				"date": String,
				"episode": Int
			}
		}
	}, {
		...
	}
]
```

`getAnimesBySeries()`

```
[
	{
		"character": String,
		"animes": [
			{
				"name": String,
				"url": String
			}, {
				...
			}
		]
	}, {
		...
	}
]
```

Dan lainnya bisa dicoba langsung ya!