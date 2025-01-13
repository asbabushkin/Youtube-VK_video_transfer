
def get_video_lst():
    lst = []
    with open('videos_to_download.txt', 'r') as file:
        for line in file:
            lst.append(line.rstrip())
    return lst


def check_skipped_video():
    skipped_video = []
    video_id_lst = get_video_lst()

    with open('success_log.txt', 'r', encoding='utf-8') as file:
        success_data = file.read()

    with open('failure_log.txt', 'r', encoding='utf-8') as file:
        failure_data = file.read()

    for i in video_id_lst:
        if i not in success_data and i not in failure_data:
            skipped_video.append(i)

    if len(skipped_video) == 0:
        return True
    else:
        with open('skipped_video.txt', 'w', encoding='utf-8') as file:
            for i in skipped_video:
                file.write(i + '\n')
        return False

