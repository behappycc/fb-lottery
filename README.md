# Facebook 粉絲團留言抽獎小幫手

A Python script retrieving comments from a specific post of a fan page for drawing

## [教學影片及 Live Demo](https://www.facebook.com/pycone2016/videos/1848676842125769/)

## 透過 Facebook Graph API 擷取公開粉絲團貼文下方的留言，從中隨機選取得獎者

## Run

```python
python3 fb_lottery.py
```

## 說明

```python
# 提供粉絲團網址及 User token
fl = FbLottery('https://www.facebook.com/pycone2016', ACCESS_TOKEN)

# 以發文內容關鍵字查找抽獎貼文
lottery_post = fl.get_lottery_post('松果城市抽獎活動開跑囉')

# 可先印出貼文確認無誤
# print('抽獎貼文:\n {0}'.format(lottery_post['message']))

# 取得該篇貼文下方留言
lottery_post_comments = fl.get_post_comments(lottery_post['id'])

# 隨機選取 10 篇留言
# fl.draw(lottery_post_comments, 10)
```