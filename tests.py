import unittest
import ksi_shikimori_parse


class TestGetAnimeList(unittest.TestCase):

    def test_get_anime_list(self):
        nickname = ''
        type1 = 'completed'
        list1 = ksi_shikimori_parse.get_anime_list(nickname, type1)
        list2 = []
        self.assertEqual(list1, list2)

    def test_csv_anime_list(self):
        nickname = ''
        type1 = 'completed'
        list1 = ksi_shikimori_parse.get_csv_anime_list(nickname, type1)
        file = open(list1, 'r')
        list2 = file.readlines()
        self.assertEqual(
            ['shikimori_id,en_name,ru_name,rewatches,score,watched_episodes,typ'
             'e\n'], list2)
        file.close()


if __name__ == '__main__':
    unittest.main()
