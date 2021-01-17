from main import searchAnime
from time import sleep
from os import system


def start():
	anime = input("Masukan anime: ")
	if anime == "":
		print("Masukan anime yg benar!")
		sleep(1)
		system("clear")
		start()
	else:
		data = searchAnime(anime)
		if data == None:
			print("Data anime tidak ditemukan!")
			sleep(2)
			system("clear")
			start()
		else:
			sleep(1)
			system("clear")
			print(f"Berhasil menemukan {len(data)} halaman.")
			sleep(0.5)

			# print all results.
			for page in data:
				print(f"Page {page['page']} ada {len(page['videos'])} video.")
				sleep(1)
				for video in page['videos']:
					print(
					f"""
					======================================
					Anime: {video['title']}
					URL: {video['url']}
					Rilis: {video['release']}
					Thumbnail: {video['thumbnail']}
					======================================

					""")
					sleep(2)
start()