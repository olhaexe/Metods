import vk
from pymongo import MongoClient

mongo_client = MongoClient()

# cоздано приложение вконтакте, получен токен через запрос в адресную строку
accesstoken = '' # токен от живого аккаунта, удален из соображений безопасности

# открыть сессию, обязательно указать номер версии
session = vk.Session(access_token=accesstoken)
vk_api = vk.API(session, v='5.103')

# ссылки на пользователей
#link_head = 'https://vk.com/id' # использовать, если делать вывод ссылками
user1 = 'https://vk.com/liasanutiasheva'
user2 = 'https://vk.com/id81369279'
#user1 = 'https://vk.com/id1155344'
#user1 = 'https://vk.com/id556192'
#user1 = 'https://vk.com/id10123679'
#user2 = 'https://vk.com/piterskiy_org'
#user2 = 'https://vk.com/id6260455'
#user2 = 'https://vk.com/id3174515'
#user2 = 'https://vk.com/rusalka'
#user2 = 'https://vk.com/id543097317'
#user2 = 'https://vk.com/id62288402'

# получить id из ссылок
def id_get(user_link):
    if 'id' in user_link:
        user_id = int(user_link.split('id')[-1])
    else:
        user_name = user_link.split('/')[-1]
        user_id = vk_api.users.get(user_ids=user_name)[0]['id']
    return int(user_id)

user1_id = id_get(user1)
user2_id = id_get(user2)

# словари для сохранения цепочек - 6 рукопожатий
dict_list = [{}, {}, {}, {}, {}, {}]

# первичные списки друзей:
user1_friends_id = vk_api.friends.get(user_id=user1_id, count=10000)['items']
user2_friends_id = vk_api.friends.get(user_id=user2_id, count=10000)['items']

# проверяем, не друзья ли пользователи между собой
if user2_id in user1_friends_id:
    #friends_chain.append(user2_id)
    dict_list[0] = {'first_user': vk_api.users.get(user_ids=user1_id), 'second_user': vk_api.users.get(user_ids=user2_id)}
else:
    for user1_friend in user1_friends_id:
        if dict_list[1]:
            break
        try:
            user_friends_id = vk_api.friends.get(user_id=user1_friend, count=10000)['items']
            if user2_id in user_friends_id:
                dict_list[1] = {'first_user': vk_api.users.get(user_ids=user1_id),
                                 '1': vk_api.users.get(user_ids=user1_friend),
                                 'second_user': vk_api.users.get(user_ids=user2_id)}
                break
            else:
                if dict_list[2]:
                    break
                for user2_friend in user2_friends_id:
                    if user2_friend in user_friends_id:
                        dict_list[2] = {'first_user': vk_api.users.get(user_ids=user1_id),
                                             '1': vk_api.users.get(user_ids=user1_friend),
                                             '2': vk_api.users.get(user_ids=user2_friend),
                                             'second_user': vk_api.users.get(user_ids=user2_id)}
                        break
                    else:
                        if dict_list[3]:
                            break
                        mutual = vk_api.friends.getMutual(source_uid=user1_friend, target_uid=user2_friend)
                        if mutual:
                            dict_list[3] = {'first_user': vk_api.users.get(user_ids=user1_id),
                                                 '1': vk_api.users.get(user_ids=user1_friend),
                                                 '2': vk_api.users.get(user_ids=mutual[0]),
                                                 '3': vk_api.users.get(user_ids=user2_friend),
                                                 'second_user': vk_api.users.get(user_ids=user2_id)}
                            break
                        else:
                            if dict_list[4]:
                                break
                            for user in user_friends_id:
                                mutuals = vk_api.friends.getMutual(source_uid=user, target_uid=user2_friend)
                                if mutuals:
                                    dict_list[4] = {'first_user': vk_api.users.get(user_ids=user1_id),
                                                             '1': vk_api.users.get(user_ids=user1_friend),
                                                             '2': vk_api.users.get(user_ids=user),
                                                             '3': vk_api.users.get(user_ids=mutuals[0]),
                                                             '4': vk_api.users.get(user_ids=user2_friend),
                                                             'second_user': vk_api.users.get(user_ids=user2_id)}
                                    break
                                else:
                                    if dict_list[5]:
                                        break
                                    user_friends_friends_id = vk_api.friends.get(user_id=user, count=10000)['items']
                                    for user_friend in user_friends_friends_id:
                                        mutualss = vk_api.friends.getMutual(source_uid=user_friend,
                                                                                   target_uid=user2_friend)
                                        if mutualss:
                                            dict_list[5] = {'first_user': vk_api.users.get(user_ids=user1_id),
                                                                    '1': vk_api.users.get(user_ids=user1_friend),
                                                                    '2': vk_api.users.get(user_ids=user),
                                                                    '3': vk_api.users.get(user_ids=user_friend),
                                                                    '4': vk_api.users.get(user_ids=mutualss[0]),
                                                                    '5': vk_api.users.get(user_ids=user2_friend),
                                                                    'second_user': vk_api.users.get(user_ids=user2_id)}
                                            break
                                        else:
                                            pass
        except vk.exceptions.VkAPIError as e:
            pass

def process_item(item):
    database = mongo_client['vk_chain']
    collection = database[f'{user1_id} and {user2_id}']
    collection.insert_one(item)
    return item

for i, el in enumerate(dict_list):
    if el:
        print(f'Для пользователей с id {user1_id} и {user2_id} цепочка рукопожатий: {el}')
        process_item(el)
        break
    else:
        print(f'Связей {i} уровня нет')