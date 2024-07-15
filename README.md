# First Web Scraping Project

## Overview

This project is a web scraping application that scrapes data from a specified website based on configurations stored in a Redis database. The extracted data is then persisted in a MongoDB database.

![Architecture](/pics/architecture.png)


## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)


## Installation

### Prerequisites

- Python 3.x
- Poetry
- Docker

### Clone the Repository

```bash
git clone https://github.com/robinsonlovatto/first_web_scraping_project.git
cd first_web_scraping_project
```

### Install Dependencies

Use the package manager Poetry to install the required Python packages.

```bash
# to create and activate the virtual env
poetry shell
# to install the dependencies
poetry install
```

## Configuration

### Docker (Redis + MongoDB)
Run the command below to start a Redis container and a MongoDB container.

```bash
docker compose up -d 
```

### .env variables
Create your .env file based on .env-example file. Make sure your database variables are correct. Only the variables in the "required" section are mandatory.

### Stores configuration on Redis
Run the command below to insert the configuration for the stores MercadoLivre and Amazon on Redis.

```bash
python src/redis_store_config.py
```

## Usage
```bash
python src/start.py
```
The code below in the start.py may be changed to scrap any store (as long it was configured in Redis) and keywords.
```bash
from browser.crawler.generic_crawler import GenericBrowserCrawler


store_to_scrap = "MercadoLivre"
keywords_to_search = "nintendo"

m1 = GenericBrowserCrawler(store_to_scrap).crawl(keywords_to_search)

store_to_scrap = "Amazon"
keywords_to_search = "playstation 5"

m2 = GenericBrowserCrawler(store_to_scrap).crawl(keywords_to_search)
```    
        