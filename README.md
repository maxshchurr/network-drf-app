# network-drf-app
Using django and django rest framework with jwt token authentication to create single network app


So the main goal was to create simple app with jwt authentication and permissions for users, provide some basic functionality such as: 
1) signup/login user
2) create own post, get posts/get post by id
3) like/unlike post
4) get some analitycs about quantity of liked posts for the provided date range
5) get infro about user activity (when was loged in, when was last request to the server)

Login of created user. Provides refresh and access tokens back
<img width="1267" alt="Screenshot 2023-09-18 at 13 53 57" src="https://github.com/maxshchurr/network-drf-app/assets/90902303/ea650e13-abf9-4ae2-a2d5-38b2b874d541">


Posts endpoint with detailed info about post
<img width="1245" alt="Screenshot 2023-09-18 at 13 50 15" src="https://github.com/maxshchurr/network-drf-app/assets/90902303/1073609e-3b8e-4900-8221-36e629ae18ae">


Post like/unlike functionality. Post will be unlicked if it was already liked by this user
<img width="1214" alt="Screenshot 2023-09-18 at 13 52 14" src="https://github.com/maxshchurr/network-drf-app/assets/90902303/47cdf3c2-d65a-4e8c-bece-73a1d1984134">


This created user has no permission to create post as he is not in "networkusers" group
<img width="1205" alt="Screenshot 2023-09-18 at 13 55 08" src="https://github.com/maxshchurr/network-drf-app/assets/90902303/7f707cc3-8b29-43bb-9c4c-53f3956bba53">


Like activity endpoint
<img width="1178" alt="Screenshot 2023-09-18 at 14 16 58" src="https://github.com/maxshchurr/network-drf-app/assets/90902303/7314856a-a3c8-4f06-a523-3b2e422018bc">



Automated bot for signup user/create posts/like/unlike posta

Here is a snippet from bot_results.json file which contains operations performed by bot

<img width="1162" alt="Screenshot 2023-09-18 at 14 21 27" src="https://github.com/maxshchurr/network-drf-app/assets/90902303/c259b7c8-0719-4c3a-b79b-5a82ac99f74b">
