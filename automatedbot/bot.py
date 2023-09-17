import json
import requests
from faker import Faker
import random
from collections import defaultdict

FILE_NAME = 'config.json'
START_URL = 'http://127.0.0.1:8000/'


def retrieve_config_for_the_bot_from_file(filename):
    with open(f'{filename}', 'r') as config_file:
        config_data = json.load(config_file)

    return config_data


def create_users(number_of_users):
    create_users_endpoint = 'users/signup/'
    created_users = []
    fake_users = Faker()

    for user in range(number_of_users):
        user_data = {

            'username': fake_users.user_name(),
            'first_name': fake_users.first_name(),
            'last_name': fake_users.last_name(),
            'email': fake_users.email(),
            'password': fake_users.password(),

        }

        response = requests.post(START_URL + create_users_endpoint, data=user_data)

        if response.status_code == 201:
            created_users.append(user_data)

        else:
            print(f'Failed to create user: {user_data["username"]}! Status code: {response.status_code}')

    return created_users


def login_user(users):
    login_users_endpoint = 'api/token/'
    users_to_login = {}
    access_tokens = []

    for i in range(len(users)):
        users_to_login[users[i].get('username')] = users[i].get('password')

    for username, password in users_to_login.items():

        user_data = {
            'username': username,
            'password': password,
        }
        response = requests.post(START_URL + login_users_endpoint, data=user_data)
        if response.status_code == 200:
            jwt_token = response.json().get('access')
            access_tokens.append(jwt_token)

    return access_tokens


def create_posts(jwt_tokens, max_posts_per_user):
    create_posts_endpoint = 'posts/create-post/'
    created_posts = {}
    fake_posts = Faker()

    for jwt_token in jwt_tokens:
        headers = {'Authorization': f'Bearer {jwt_token}'}
        posts_to_create = random.randint(1, max_posts_per_user)

        for post in range(posts_to_create):
            post_data = {
                'title': fake_posts.sentence(),
                'body': fake_posts.paragraph(),
                    }

            response = requests.post(START_URL + create_posts_endpoint, data=post_data, headers=headers)
            if response.status_code == 201:
                post_id = response.json().get('id')
                created_posts[int(post_id)] = post_data

            else:
                print(f'Failed to create post!. Status code: {response.status_code}')

    return created_posts


def like_posts(logged_users, ids_of_created_posts, max_likes_per_user):
    ids_of_posts = list(ids_of_created_posts.keys())
    activity = defaultdict()
    for jwt_token in logged_users:

        likes = random.randint(1, max_likes_per_user)

        for like in range(likes):
            post_to_like = random.choice(ids_of_posts)
            headers = {'Authorization': f'Bearer {jwt_token}'}
            response = requests.patch(START_URL + f'posts/{post_to_like}/like/', headers=headers)

            if response.status_code == 200:
                # as we can like and unlike post with the same url, like will appear if quantity of actions WAS % 2 == 0
                # for example: 1 action with url - post like
                #              2 action with url - post unlike

                if post_to_like not in activity.keys():
                    activity[post_to_like] = ['liked post!']

                elif len(activity[post_to_like]) % 2 == 0:
                    activity[post_to_like].append('liked post!')
                else:
                    activity[post_to_like].append('unliked post!')
            else:
                print(f'Failed to like post! Status code: {response.status_code}, {response}, {response.content}')

    return activity


def start_bot(config_file):
    work_result = {}
    config = retrieve_config_for_the_bot_from_file(config_file)
    number_of_users = config.get('number_of_users')
    max_posts_per_user = config.get('max_posts_per_user')
    max_likes_per_user = config.get('max_likes_per_user')

    created_users = create_users(number_of_users)
    logged_users = login_user(created_users)
    created_posts_ids = create_posts(logged_users, max_posts_per_user)
    liked_posts = like_posts(logged_users, created_posts_ids, max_likes_per_user)

    work_result['created_users'] = created_users
    work_result['created_posts'] = created_posts_ids
    work_result['liked_posts'] = liked_posts

    return work_result


def save_bot_results(**kwargs):
    filename = 'bot_results.json'

    result = {}
    result['created_users'] = kwargs.get('created_users')
    result['created_posts'] = kwargs.get('created_posts')
    result['liked_posts'] = kwargs.get('liked_posts')

    with open(filename, 'w') as result_file:
        json.dump(result, result_file, indent=4)


if __name__ == '__main__':
    bot_activate = start_bot(FILE_NAME)
    save_bot_results(created_users=bot_activate['created_users'], created_posts=bot_activate['created_posts'],
                     liked_posts=bot_activate['liked_posts'])