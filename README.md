# Project_2

Repo for Metis project 2.

The goal of this project was to use linear regression techniques to predict card prices for Magic: the Gathering (MTG).

MTG has been around since 1993, but this project focuses on cards legal in the Modern competitive format, which includes cards from 2004 to the present day. Reasoning for this specification is a) it limits the card pool to just ~15,000 entries and b) it provides a framework in which to consider factors that may affect a card's price, including both supply choices (such as card rarity and how many times a card has been printed) as well as in-game mechanical differences among cards that may affect demand.

To answer the question of what aspects affect card price, data were scraped from Cardkingdom.com using BeautifulSoup and Selenium. A LassoCV linear regression model was then run to examine the relationship between feature variables and target variable (price).

This repo contains 2 Jupyter notebooks. The first is for scraping and cleaning data from CardKingdom.com. The second is contains code to run a regression analysis of scraped data. 

This repo also contains a .py file of all functions created for this project.

Read my blog post about this project: https://noah-jaffe.medium.com/using-linear-regression-to-predict-the-price-of-magic-the-gathering-cards-56634ab5e926
