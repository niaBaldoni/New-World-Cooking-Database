# New World Cooking Database
## _Web scraper for NW food and recipes_

I needed to quickly get all the recipes in one place, so I decided to build a web scraper that creates a database of everything needed to craft every recipe in the game.

The scraper first retrieves every recipe, then it cycles through every recipe to retrieve information about every item required (where to obtain it and in what quantities). This way, it's possible to execute simple queries on the resulting Database to see how many of each item is required to craft a certain amount of the desired food, and where to find them.

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
