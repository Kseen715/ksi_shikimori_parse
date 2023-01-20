import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_anime_list(nickname, type='completed'):
    """
    get_anime_list(nickname, type='completed') - функция для получения списка 
    аниме по никнейму с указанным типом.

    Аргументы:
        - nickname (str) - никнейм пользователя;
        - type (str) - тип аниме (все/all, завершённое/completed, 
        смотрящееся/watching, планируемое/planned, 
        на паузе/on_hold, брошено/dropped).

    Возвращает:
        - anime_list (list) - список словарь-объектов, содержащих id shikimori, 
        англ. и рус. названия, число повторных просмотров, оценку, 
        кол-во просмотренных серий, общее кол-во серий, тип тайтла.
    """
    if type == 'all':
        type = 'completed,watching,rewatching,planned,on_hold,dropped'
    url = 'https://shikimori.one/' + nickname + \
        '/list/anime/mylist/' + type + '/order-by/rate_score'
    if type == 'completed,watching,rewatching,planned,on_hold,dropped':
        type = 'all'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53'
        '7.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    print(url)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    anime_list = []
    for anime in soup.find_all('tr', class_='user_rate'):
        # get <td class="num">Сериал</td></tr>
        anime_list.append({
            'shikimori_id': anime['data-target_id'],
            'en_name': anime['data-target_name'],
            'ru_name': anime['data-target_russian'],
            'rewatches': int(anime.find('span', class_='rewatches')
                             .text.split()[0]) if anime
            .find('span', class_='rewatches').text else 0,
            'score': anime.find('span', class_='current-value').text,
            'watched_episodes': anime
            .find_all('span', class_='current-value')[1].text,
            'total_episodes': anime
            .find_all('span', class_='misc-value')[0].text,
            'type': anime.find_all('td', class_='num')[2].text
        })
    return anime_list


def get_csv_anime_list(nickname, type='completed'):
    """
    get_csv_anime_list(nickname, type='completed') - функция для создания CSV-ф'
    'айла со списком аниме по имени пользователя и типу.

    Аргументы:
        - nickname (str): Имя пользователя;
        - type (str): Тип аниме. Значение по умолчанию - 'completed'.

    Возвращает:
        - csv_filename (str): Имя CSV-файла.
    """
    anime_list = get_anime_list(nickname, type)
    csv_filename = nickname + '_' + type + '_' + \
        datetime.now().strftime('%Y-%m-%d_%H-%M') + '.csv'
    with open(csv_filename, 'w', encoding='utf-8') as f:
        f.write('shikimori_id,en_name,ru_name,rewatches,score,watched_episodes,'
                'type\n')
        for anime in anime_list:
            f.write(str(anime['shikimori_id']) + ',"' +
                    str(anime['en_name']) + '","' +
                    str(anime['ru_name']) + '",' +
                    str(anime['rewatches']) + ',' +
                    str(anime['score']) + ',' +
                    str(anime['watched_episodes']) +
                    str(anime['total_episodes']) + ',' +
                    str(anime['type']) + '\n')
    return csv_filename
