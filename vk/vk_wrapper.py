import json
import os
import random
import csv

import joblib
import vk_api

mem = joblib.Memory(cachedir='./tmp/vk', verbose=0)


class VkWrapper:
    """
    Wrapper class for working with VK api. Simplifies some common methods, handles auth and stuff
    TODO parallelism
    TODO caching
    """

    USER_ALL_FIELDS = 'photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, ' \
                      'photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, ' \
                      'has_mobile, contacts, site, education, universities, schools, status, last_seen, ' \
                      'followers_count, common_count, occupation, nickname, relatives, relation, personal, ' \
                      'connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, ' \
                      'can_post, can_see_all_posts, can_see_audio, can_write_private_message, ' \
                      'can_send_friend_request, is_favorite, timezone, screen_name, maiden_name, ' \
                      'crop_photo, career, military '

    def __init__(self, users=None):
        # memory = joblib.Memory(cachedir='./tmp/vk', verbose=0)
        memory = None
        if not users:
            # Using last session saved by vk_api
            usernames = json.load(open('./tmp/vk.json'))['usernames']
            self.sessions = [vk_api.VkApi(login=username) for username in usernames]
        else:
            self.sessions = [vk_api.VkApi(user['login'], user['password']) for user in users]

        for session in self.sessions:
            session.auth(token_only=True)

    @property
    def api(self):
        return random.choice(self.sessions).get_api()

    @staticmethod
    def _get_array(method, params, limit=100, fetch_limit=None):
        """
        Load large list of entries that do not fit into one query limit
        TODO use execute

        :param method: API method to call
        :param params: query parameters (count and offset will be overriden)
        :param limit: max number of entries per query
        :param fetch_limit: total number of entries to fetch
        :return: list of entries
        """

        params = dict(params)
        params.update({'count': limit})
        resp = method(**params)
        count = resp['count']
        if fetch_limit is not None:
            count = min(fetch_limit, count)

        items = resp['items']

        for i in range(limit, count, limit):
            params.update({'offset': i})
            print(i)
            items += method(**params)['items']

        return items

    def get_info(self, uid):
        resp = self.api.users.get(user_ids=str(uid), fields=self.USER_ALL_FIELDS)
        return resp[0]

    def get_wall(self, uid, posts_limit=None):
        wall = self._get_array(self.api.wall.get, dict(
            owner_id=uid,
            filter='owner',
            extended=False
        ), fetch_limit=posts_limit)

        for post in wall:
            post.pop('attachments', None)
            if 'copy_history' in post:
                for repost in post['copy_history']:
                    repost.pop('attachments', None)

        return wall

    def get_photo(self, uid):
        return self.api.users.get(user_ids=str(uid), fields='photo_max_orig')[0]['photo_max_orig']

    def get_groups(self, uid):
        return self._get_array(self.api.groups.get, dict(user_id=uid, extended=0), limit=1000)

    def get_member_ids(self, gid):
        return self._get_array(self.api.groups.getMembers, dict(group_id=gid, sort='id_asc'), limit=1000)
