from yandex_music import Client
from config import *
import requests
from urllib.parse import quote
import os

client = Client(YANDEX_MUSIC_TOKEN)

def get_new():
    return client.new_releases()

def get_popular():
    return client.chart().chart.tracks

def search_music(
    query: str
):
    page = 0

    search_result = client.search(query, type_="track", page=page)
        
    if not search_result.tracks or not search_result.tracks.results:
        return None

    tracks = search_result.tracks.results

    return tracks


def download_track(track_id: str, quality='mp3', save_path='tracks'):
    """Скачать трек по ID
    Args:
        track_id (str): ID трека (например, '12345678')
        quality (str): Качество ('mp3' или 'hq')
        save_path (str): Папка для сохранения
    """
    try:
        # Получаем объект трека
        track = client.tracks(track_id)[0]
        
        # Получаем информацию для загрузки
        download_info = track.get_download_info()
        
        # Выбираем нужное качество
        for info in download_info:
            if info.codec == quality:
                direct_link = info.get_direct_link()
                break
        else:
            raise ValueError(f"Качество {quality} недоступно")
        
        # Создаем папку, если нужно
        os.makedirs(save_path, exist_ok=True)
        
        # Скачиваем файл
        filename = f"{track.title.replace('/', '-')}.{quality}"
        response = requests.get(direct_link)
        
        with open(os.path.join(save_path, filename), 'wb') as f:
            f.write(response.content)
            
        return f"{save_path}/{track.title}.mp3"
        
    except Exception as e:
        return f"Ошибка: {str(e)}"