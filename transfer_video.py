import yt_dlp
import vk_api
import os
from dotenv import load_dotenv
from check_log import check_skipped_video, get_video_lst



load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')

def upload_to_vk(filename, title, description):
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    upload = vk_api.VkUpload(vk_session)
    upload.video(video_file=filename, name=title, description=description, group_id=46206916, album_id=1)
    print(f'Видео {title} сохранено в ВК')

def log_add(video_id, download_result, upload_result='неприменимо', title='Название видео отсутствует'):
     if download_result == 'success' and upload_result == 'success':
         with open('success_log.txt', 'a', encoding='utf-8') as file:
             file.write(f'{video_id} {title}. Download: {download_result}. Upload: {upload_result}\n')
     else:
         with open('failure_log.txt', 'a', encoding='utf-8') as file:
             file.write(f'{video_id} {title}. Download: {download_result}. Upload: {upload_result}\n')

video_id_lst = get_video_lst()
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
            except Exception as e:
                upload_result = f'failure: {e}'
                log_add(video_id, download_result, upload_result, title)
        except Exception as e:
            download_result = f'failure: {e}'
            log_add(video_id, download_result)

if check_skipped_video():
    print('All videos have been processed, but check failure_log.txt')
else:
    print('Some videos missed. Check skipped_video.txt and failure_log.txt')