import yt_dlp
import vk_api
import os
from dotenv import load_dotenv


load_dotenv()

VK_TOKEN = os.getenv('VK_TOKEN')

video_id_lst = []
with open('videos_to_download.txt', 'r') as file:
    for line in file:
        video_id_lst.append(line)


def upload_to_vk(filename, title, description):
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    upload = vk_api.VkUpload(vk_session)
    upload.video(video_file=filename, name=title, description=description, group_id=46206916, album_id=1)
    print(f'Видео {title} сохранено в ВК')


def log_add(video_id, download_result, upload_result=None, title=None):
    with open('transfer_log.txt', 'a', encoding='utf-8') as file:
        file.write(f'{video_id.rstrip()} {title.rstrip()}. Download: {download_result}. Upload: {upload_result}\n')

options = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s'  # Путь и имя файла
        }

for video_id in video_id_lst:
    url = 'https://youtu.be/' + video_id
    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title')
            description = info_dict.get('description')
            filename = ydl.prepare_filename(info_dict)
            download_result = 'success'
            print("Видео успешно загружено в максимальном качестве!")
            try:
                upload_to_vk(filename, title, description)
                upload_result = 'success'
                log_add(video_id, download_result, upload_result, title)
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Файл {filename} успешно удален.")
                else:
                    print(f"Файл {filename} не найден.")
            except Exception as e:
                upload_result = f'failure: {e.rstrip()}'
                log_add(video_id, download_result, upload_result, title)
        except Exception as e:
            download_result = f'failure: {e.rstrip()}'
            log_add(video_id, download_result)
        #    print(f"{video_id}: {e}")
