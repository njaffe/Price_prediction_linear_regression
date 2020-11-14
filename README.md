# Project_2: Using Linear Regression to Predict the Price of Magic: the Gathering Cards

## 1. Project Overview and repo contents
- The goal of this project was to use linear regression techniques to predict card prices for Magic: the Gathering (MTG).
- MTG has been around since 1993, but this project focuses on cards legal in the Modern competitive format, which includes cards from 2004 to the present day. Reasoning for this specification is a) it limits the card pool to just ~15,000 entries and b) it provides a framework in which to consider factors that may affect a card's price, including both supply choices (such as card rarity and how many times a card has been printed) as well as in-game mechanical differences among cards that may affect demand.
- This repo contains 2 Jupyter notebooks. The first is for scraping and cleaning data from CardKingdom.com. The second is contains code to run a regression analysis of scraped data. 
- This repo also contains a .py file of all functions created for this project.

## 2. Data Sources
- Cardkingdom.com
- Wikipedia.com

## 3. Basic Methodology
- Data were scraped using BeautifulSoup and Selenium
- A LassoCV linear regression model was then run to examine the relationship between feature variables and target variable (price)
- Model was cross-validated using K-fold CV within Scikit-Learn

## 4. Results summary
- 29% of variance in card prices was explained by the model and card prices were predicted within $1.50 mean absolute error
- Strongest predictive features were rarity and card color ([see basic Magic rules here](https://magic.wizards.com/en/game-info/gameplay/rules-and-formats/rules) or [here](https://en.wikipedia.org/wiki/Magic:_The_Gathering_rules)).

## 5. Tools and techniques used
- [Jupyter](https://jupyter.org/)
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [Scikit-learn](https://scikit-learn.org/stable/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/index.html)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium](https://www.selenium.dev/)
- [Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [K-fold cross validation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html)

## 6. [Read my blog post!](https://noah-jaffe.medium.com/using-linear-regression-to-predict-the-price-of-magic-the-gathering-cards-56634ab5e926)
