# New World Cooking Database
## _Web scraper for NW food and recipes_

I needed to quickly get all the recipes in one place, so I decided to build a web scraper that creates a database of everything needed to craft every recipe in the game.

## Requirements

- [Python] - I used the 3.9.7 version
- [MySQL] - The output will be a MySQL database
- [Docker] - The program is very easy to install and deploy in a Docker container.

## Installation

You can change the database url depending on your needs
```sh
docker build -t nwcookingdb .
docker run -e DATABASE_URL="mysql://root:psw@127.0.0.1:3306/db" nwcookingdb
```
