# Data Modeling with Postgres
This repository contains the code for the first project in Udacity's Data Engineering Nanodegree program.

# How to use
## Install
The project uses [`poetry`](https://python-poetry.org/) as package manager. You need to have it installed before proceeding.

```bash
poetry install
```

# Changes to template code
- Updated database credentials to use local instance (database `sparkifydb`, user `postgres` and password `1234`)
- Error handling at the transaction level in `etl.py`. The template code would only commit at the end of `process_data()`, but since errors happened during the execution (e.g. uniqueness or not null constraints violated), it was not possible to proceed without rolling back all steps. To solve that, I've implemented the `execute()` method that treats each execution individually and handles known exceptions, printing the information on the screen for visibility. With that, I was able to successfully insert the "good" records while responsibly ignoring bad quality data.

# TODOs
- Configure local Postgres with original credentials to enable easier review + document how to setup with Docker
- Estimate LOE of topics to "make the project stand out" and implement some of them if feasible within the timeframe
- Final review against project rubric
    - Change log json read with tip provided [here](https://classroom.udacity.com/nanodegrees/nd027/parts/f7dbb125-87a2-4369-bb64-dc5c21bb668a/modules/a7801de4-ee3f-4531-b887-82dea67f47a6/lessons/01995bb4-db30-4e01-bf38-ff11b631be0f/concepts/a5609601-2314-4d8b-a7cf-e40048b3ee96)