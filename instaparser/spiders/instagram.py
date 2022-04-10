import scrapy
import json
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    inst_login = 'Onliskill_udm'
    inst_passw = '#PWD_INSTAGRAM_BROWSER:10:1649271346:ARdQAENSWUmccOM/EbFtyEqSlWjK/mGNZSin2zibiWymXiFay2XizFgs9caCBhCs8UX/HmuCi3usYDQyjWejEQ0SQShbCXnKuNyNwUkk9SMs6CkDTYmY+4iZxrha979FplhAMuHwZhobZ/vZMuI='

    # user_for_parse = 'techskills_2022'
    users_for_parse = [
        'rsbor.gatchina',
        'ecofest_gatchina',
    ]

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        print()

        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_passw},
                                 headers={'X-CSRFToken': csrf_token,
                                          })

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:

            for username in self.users_for_parse:
                # print(f'== !!!!! ====== user: {username}===========')
                yield response.follow(f'/{username}/',
                                      callback=self.user_parse,
                                      cb_kwargs={'username': username})
        else:
            print("DON'T LOGIN")

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)

        variables = {'id': user_id,
                     'first': 12}

        # FOLLOWERS
        url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&search_surface=follow_list_page'
        cb_kwargs = {'username': username,
                     'user_id': user_id,
                     'variables': deepcopy(variables),
                     }
        yield response.follow(url_followers,
                              callback=self.followers_parse,
                              cb_kwargs=cb_kwargs)


        # FOLLOWINGS
        url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12'
        cb_kwargs = {'username': username,
                     'user_id': user_id,
                     'variables': deepcopy(variables)
                     }
        yield response.follow(url_following,
                              callback=self.following_parse,
                              cb_kwargs=cb_kwargs)

        # print('PARSE STARTED!!!')

    # =====================  ITEMS CREATING  STARTS HERE  ===================================================
    def followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        followers = j_data.get('users')
        next_max_id = j_data.get('next_max_id', '')
        # print(f'================================ next_max_id: {next_max_id} ==========================')

        url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&max_id={next_max_id}&search_surface=follow_list_page'

        if next_max_id:
            yield response.follow(url,
                                  callback=self.followers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': variables,
                                             })

        for follower in followers:
            item = InstaparserItem(
                username=username,
                user_id=user_id,
                follow_id=follower.get('pk'),
                follow_name=follower.get('username'),
                follow_type='follower',
                photo=follower.get('profile_pic_url'),
                post_data=follower                  # сохраняем на всякий случай
            )
            print()
            yield item

    def following_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        followings = j_data.get('users')
        next_max_id = j_data.get('next_max_id')
        # print(f'================================ next_max_id: {next_max_id} ==========================')

        url = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&max_id={next_max_id}'
        if next_max_id:
            yield response.follow(url,
                                  callback=self.following_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': variables
                                             })
        for following in followings:
            item = InstaparserItem(
                username=username,
                user_id=user_id,
                follow_id=following.get('pk'),
                follow_name=following.get('username'),
                follow_type='following',
                photo=following.get('profile_pic_url'),
                post_data=following                  # сохраняем на всякий случай
            )
            print()
            yield item



    # =================================================================================================================
    # def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
    #     print()
    #     j_data = response.json()
    #     page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
    #     if page_info.get('has_next_page'):
    #         variables['after'] = page_info.get('end_cursor')
    #
    #         url = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
    #
    #         yield response.follow(url,
    #                               callback=self.user_posts_parse,
    #                               cb_kwargs={'username': username,
    #                                          'user_id': user_id,
    #                                          'variables': deepcopy(variables)})
    #
    #     posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
    #     for post in posts:
    #         item = InstaparserItem(
    #             user_id=user_id,
    #             username=username,
    #             photo=post.get('node').get('display_url'),
    #             likes=post.get('node').get('edge_media_preview_like').get('count'),
    #             post_data=post.get('node')                  # сохраняем на всякий случай
    #         )
    #         yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]


'''
1) Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей и собирать данные об их подписчиках и подписках.
2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект нужно извлечь:
    - имя, 
    - id, 
    - фото 
    - (остальные данные по желанию). 
    Фото можно дополнительно скачать.
4) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
5) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
6) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

Для выполнения данной работы необходимо делать запросы в апи инстаграм с указанием заголовка User-Agent : 'Instagram 155.0.0.37.107'
'''