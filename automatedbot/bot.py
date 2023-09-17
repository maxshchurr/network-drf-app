import json
import requests
from faker import Faker
import random


FILE_NAME = 'config.json'
START_URL = 'http://127.0.0.1:8000/'


def retrieve_config_for_the_bot_from_file(filename):
    with open(f'{filename}', 'r') as config_file:
        config_data = json.load(config_file)

    return config_data


def create_user():
    create_users_endpoint = 'users/signup/'
    fake_users = Faker()

    user_data = {

            'username': fake_users.user_name(),
            'first_name': fake_users.first_name(),
            'last_name': fake_users.last_name(),
            'email': fake_users.email(),
            'password': fake_users.password(),

    }

    response = requests.post(START_URL + create_users_endpoint, data=user_data)

    if response.status_code == 201:
        print(f'User created: {user_data}')
        jwt_token = response.json().get('token').get('access')

        if jwt_token:
            print(f'JWT token: {jwt_token}')
            return jwt_token
    else:
        print(f'Failed to create user: {user_data["username"]}! Status code: {response.status_code}')


def create_post(jwt_token):
    create_post_endpoint = 'posts/create-post/'
    fake_post = Faker()
    headers = {'Authorization': f'Bearer {jwt_token}'}

    post_data = {
        'title': fake_post.sentence(),
        'body': fake_post.paragraph(),
    }

    response = requests.post(START_URL + create_post_endpoint, data=post_data, headers=headers)
    if response.status_code == 201:
        print('Post created successfully')
        post_id = response.json().get('id')
        print('Id of created post', post_id)

        return post_id
    else:
        print(f'Failed to create post!. Status code: {response.status_code}')


def create_posts(number_of_users, max_posts_per_user):
    jwt_tokens = []
    created_posts = []
    for user in range(number_of_users):
        jwt_token = create_user()
        numbers_of_posts = random.randint(1, max_posts_per_user)
        for post in range(numbers_of_posts):

            if jwt_token:
                created_posts.append(create_post(jwt_token))
                jwt_tokens.append(jwt_token)

    return jwt_tokens, created_posts


def like_posts(max_likes_from_user, users, posts):
    for jwt_token in users:
        likes_by_user = random.randint(1, max_likes_from_user)
        for like in range(likes_by_user):
            headers = {'Authorization': f'Bearer {jwt_token}'}
            post_to_like = random.choice(posts)
            response = requests.patch(START_URL + f'posts/{post_to_like}/like/', headers=headers)

            if response.status_code == 200:
                print(f'Post {post_to_like} was liked successfully')
            else:
                print(f'Failed to like post! Status code: {response.status_code}, {response}')


def start_bot(config_file):
    config = retrieve_config_for_the_bot_from_file(config_file)
    number_of_users = config.get('number_of_users')
    max_posts_per_user = config.get('max_posts_per_user')
    max_likes_per_user = config.get('max_likes_per_user')

    if max_posts_per_user and max_posts_per_user and max_likes_per_user:
        users, posts = create_posts(number_of_users, max_posts_per_user)
        like_posts(max_likes_per_user, users, posts)
    else:
        print('Check config file. Looks like one of the requested parameters wasnt specified')


if __name__ == '__main__':
    start_bot(FILE_NAME)
