# AISimPoker

The poker player behavior simulator. 

## About

Poker is a card game widely spread throughout the world, being recognized for requiring mathematical, cognitive, and behavioral skills from its players. Despite the innumerable variations created over time, the hierarchy of cards, and the primitive concepts of strategy, have always remained present, leaving room for countless theories and discussions on how to play poker. This work aims to analyze the game history of poker players in Texas Hold'em modality, to evaluate the performance of the possible characteristics extracted from the data, and of the machine learning models for behavior prediction. We developed an application that applies the feature extraction strategies from the logs and allows simulating matches in the most varied situations within the tournament, presenting promising results on the use of the XGBoost classifier.

## Current Features

- Interprets and parse poker logs into structured JSON data.
- Use the current designed data features to train a XBoost model.
- Exposes the train and eval endpoints in a REST API

## TODOs

- Integration tests
- Add more data features (e.g. previous actions summary)
- Support different models
- Analytics report
- Game simulation?
- UI?

## How to run

1. Install Docker and docker-compose
2. Run `docker-compose up -d`
3. Use the endpoints avaibable in the postman.json file
