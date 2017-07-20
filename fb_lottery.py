import requests
import random
import csv


class FbLottery(object):
    def __init__(self, page_url, token):
        self.graph_api_url = 'https://graph.facebook.com/v2.9'
        self.access_token = token
        self.page_url = page_url
        self.page_id = self.get_page_id()
        self.retrieve_limit = 1000

    def get_page_id(self):
        url = self.graph_api_url + '/{0}/?access_token={1}'.format(
            self.page_url, self.access_token)
        data = requests.get(url).json()
        return data['id']

    def get_page_posts(self):
        url = self.graph_api_url + '/{0}/posts?access_token={1}'.format(
            self.page_id, self.access_token)
        data = requests.get(url).json()
        return data['data']

    def get_lottery_post(self, title):
        all_posts = self.get_page_posts()
        for post in all_posts:
            if title in post['message']:  # Also can use post['created_time'] to locate the post
                return post

    def get_post_comments(self, post_id):
        url = self.graph_api_url + '/{0}/comments?limit={1}&access_token={2}'.format(
            post_id, self.retrieve_limit, self.access_token)
        data = requests.get(url).json()
        return data['data']

    def draw(self, comments, num_of_prize):
        fans = list()
        user_ids = set()
        for comment in comments:
            if comment['from']['id'] in user_ids:
                continue
            else:
                user_ids.add(comment['from']['id'])
                fans.append({
                    'message': comment['message'],
                    'created_time': comment['created_time'],
                    'name': comment['from']['name'],
                    'id': comment['from']['id']
                })
        random.shuffle(fans)
        draws = fans[:num_of_prize]
        with open('draw.csv', 'w', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'id', 'created_time', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for draw in draws:
                print(draw)
                writer.writerow(draw)


if __name__ == '__main__':
    ACCESS_TOKEN = 'YOUR_TOKEN'
    fl = FbLottery('https://www.facebook.com/pycone2016', ACCESS_TOKEN)
    lottery_post = fl.get_lottery_post('松果城市抽獎活動開跑囉')
    # print('抽獎貼文:\n {0}'.format(lottery_post['message']))
    lottery_post_comments = fl.get_post_comments(lottery_post['id'])
    fl.draw(lottery_post_comments, 10)
