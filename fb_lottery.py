import requests
import random
import csv


class FbLottery(object):
    def __init__(self):
        self.ACCESS_TOKEN = ''
        self.page_url = 'https://www.facebook.com/pycone2016'
        self.post_time = '2017-06-24T04:34:54+0000'
        self.lucky_man_num = 5

    def get_page_id(self):
        url = 'https://graph.facebook.com/v2.9/{0}/?access_token={1}'.format(
            self.page_url, self.ACCESS_TOKEN)
        data = requests.get(url).json()
        return data['name'], data['id']

    def get_page_post(self, page_id):
        url = 'https://graph.facebook.com/v2.9/{0}/posts?access_token={1}'.format(
            page_id, self.ACCESS_TOKEN)
        data = requests.get(url).json()
        return data

    def get_lottery_post_id(self, page_posts):
        for post in page_posts['data']:
            if (post['created_time'] == self.post_time):
                return post['id']

    def get_lottery_post_message(self, lottery_post_id):
        url = 'https://graph.facebook.com/v2.9/{0}/comments?limit=1000&access_token={1}'.format(
            lottery_post_id, self.ACCESS_TOKEN)
        data = requests.get(url).json()
        fans = []
        for message in data['data']:
            fan = {}
            fan['message'] = message['message']
            fan['created_time'] = message['created_time']
            fan['name'] = message['from']['name']
            fan['id'] = message['from']['id']
            fans.append(fan)
        return fans

    def draw_lucky_man(self, fans):
        lucky_men = []
        random.shuffle(fans)
        for i in range(self.lucky_man_num):
            lucky_men.append(fans.pop())

        with open('lucky_man.csv', 'w', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'id', 'created_time', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for lucky_man in lucky_men:
                writer.writerow(lucky_man)


def main():
    fl = FbLottery()
    page_name, page_id = fl.get_page_id()
    page_posts = fl.get_page_post(page_id)
    lottery_post_id = fl.get_lottery_post_id(page_posts)
    fans = fl.get_lottery_post_message(lottery_post_id)
    fl.draw_lucky_man(fans)


if __name__ == '__main__':
    main()
