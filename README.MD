
# API CREATOR SIMPLE
## How to Use
```bash
$ git clone https://github.com/derymukti/pentools2.git
```
```bash
$ cd pentools
```
```bash
$ sudo pip install -r requrements.txt
```

## Config

Update config in config.json

## Basic CLI

Create new module

```bash
$ python manage.py create:module -n users
```

Run App
```bash
$ python manage.py run
```

## Basic api

### Create New User
[POST] http://localhost:8383/users/insert_something

```json
{
	"username":"pentools",
	"password":"1234",
	"email":"test@email.com"
}
```

### Get Users
[GET] http://localhost:8383/users/list_something

### Update User
[POST] http://localhost:8383/users/update_something

```json
{
	"id":"1",
	"username":"updateuser",
	"password":"updatepassword",
	"email":"update@email.com"
}
```