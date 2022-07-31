# Chesstopia

> ## Chesstopia is the submission of team spiffy-sphinxes for the python discord summer codejam 2022
____
# Chesstopia has two different game modes

- ## Confusing Chess

- ### Confusion chess is a game mode which allows players piece layout to be different than the standard chess piece layout. This pushes the players skill because they won't know the piece layout and what pieces they'll get until the game starts. Hence standard openings won't work in this game mode

- ### How does this apply to the theme? At first, this may seem like a bug, but it actaully allows players to focus on thier positonal thinking instead of memorising openings.

____

- ## Magic Chess

- ### Magic chess is a game mode which allows players to by pass move validation sometimes. Players can take this to their advantage by making moves that are not valid in the standard chess

- ### How does this apply to the theme? This may seem like a bug, but allowing illegal moves for some pieces leads to super fun, and crazy positions.


# Setup

- ### Run `git clone https://github.com/Sanyok6/Chesstopia.git` to clone the repo

- ### And then you will need to setup the frontend and the backend

## Setting up the backend
> ### Make sure to have `pipenv` installed using `pip install pipenv`
> ### python 3.10 is required

#### Run the following commands
```
cd Chesstopia
pipenv install
pipenv shell
cd src/backend
python manage.py migrate
python manage.py runserver
```

> ### Note use `python3` if you are on linux.
> ### You can optionally create a superuser https://docs.djangoproject.com/en/4.0/intro/tutorial02/#creating-an-admin-user

## Setting up the frontend
> ### Make sure to have node.js and npm installed
> #### Note: Make sure the backend is running before the frontend

#### Run the following commands

> ### Make sure to install `pnpm` using `npm install -g pnpm`
```
cd Chesstopia/src/frontend
pnpm install
pnpm dev
```

### Now visit the given url in the console
