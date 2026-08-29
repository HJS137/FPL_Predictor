# Winning FPL (or at least not losing) with AI

## Script Aims

This Script aims to provide a comprehensive guide on how to leverage AI tools and techniques to improve performance in Fantasy Premier League (FPL). The goal is to help users make informed decisions, optimize their team selections, and ultimately enhance their chances of success in the game.

### Table of Contents
1. Introduction to FPL and AI   
2. Understanding FPL Scoring and Rules
3. Data Collection and Analysis       
4. AI Tools for FPL Decision Making
5. Player Performance Prediction Models
6. Team Selection Strategies
7. Transfer and Captaincy Decisions
8. Risk Management and Injury Analysis
9. Case Studies and Examples


## Proposed plan

### Part 1  - 29/08/2026

Load the dataset through an FPL API and perform an initial analysis of player statistics, team performance, and historical data. This will involve cleaning the data, identifying key metrics, and visualizing trends to inform decision-making.

1. Fetch and parse pulls 3MB of JSON data from the FPL API. Then turns it into nested python dictionaries and lists.

2. Survey the top level. Loop the ten keys, print how much is behind each. This is how `elements: 622` is found.

3. Drill onto record. Take `players[0]`, print every field with `.items()`, then build the `element_type` -> position lookup fromt he `element_types` and use it to decode that player.


Its important to read values from the API but verify against observed points. 

At this stage there is useful constaints confirmed such as squad total spend, squad team lmit and max extra free


