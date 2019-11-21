Run
===

```sh
export FLASK_APP=flaskr.main
flask init-db
flask run
```
# REST API
---
# Manual
---
# Sign up/Log out
| Action | Method | Command | JSON properties required |
| - | - | - | - |
| Sign up | POST | http://www.example.com/auth/register | username, password |
| Log out | GET | http://www.example.com/auth/logout |
# Interaction with posts
| Action | Method | Command | JSON properties required |
| - | - | - | - |
| Get all posts | GET | http://www.example.com/posts |
| Get specific post | GET | http://www.example.com/posts/`id` |
| Create post | POST | http://www.example.com/posts | title, body |
| Update post | PUT | http://www.example.com/posts/`id` | title, body|
| Delete post | DELETE | http://www.example.com/posts/`id` |
# Interaction with comments
| Action | Method | Command | JSON properties required |
| - | - | - | - |
| Get all comments of the post | GET | http://www.example.com/posts/`id`/comments |
| Get specific comment of the post | GET | http://www.example.com/posts/`id`/comments/`id` |
| Create comment for the post | POST | http://www.example.com/posts/`id`/comments | text | 
| Update comment of the post | PUT | http://www.example.com/posts/`id`/comments/`id` | text |
| Delete post | DELETE | http://www.example.com/posts/`id` |