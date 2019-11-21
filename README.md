# ICO_Viability_Index
Analyzing various successful and unsuccessful ICOs for predictive success features.


# Original Brainstorming Ideas
After initial weekend of research and data gathering, the team has worked out feasibility of project and agrees to a minimal viable product as described below.
1. Is a dashboard - single page that is accessible to general public or clients.
2. End user is a person not exactly super knowledgeable in cypto looking to get into investments in new coins, and needs guidance on what to look at more closely and what to absolutely avoid.  
3. Content of Dashboard - high level overview
    - Top is a highlight of viable ICOs/crypto products that are new to market that score highly in our scoring.
    - Middle is a highlight of new ICOs/crypto products that are new to market and score poorly, likely should be avoided.
    - Bottom *could* be coins in the past that we score, and a backtest to how we did (score versus how they ended up doing)
4. Defining a successful coin
    - Features that may be important that occur during ICO
        1. Git Commits
        2. Are you listed?
        3. Where are you listed?
        4. Target funding amount
        5. Marketing / lobbying intensity
        6. Sentiment analysis on:
            1. Public chatter (amount / intensity)
            2. News media
        7. Corporate governence
            1. Audited Financials?
            2. Board of Directors?
            3. Prior history of founders
            4. Credit rating?
    - Features to collect that track success after launch
        1. Was/is it listed? 
        2. Duration of listing
        3. What is the market cap and price trajectory/history?  Is current price greater or less than initial launch?
        4. Trading activity
        5. Sentiment analysis on:
            1. Public chatter (amount / intensity)
            2. News media

5. Minimal Viable Project - features that are attainable (we have less than two weeks to complete this project)
    - The team's work over the weekend determined the following are relatively easy to access and work with
        1. List of ICOs, incluing their funding round at launch... target funding is intermittant
        2. Current list of ICOs still trading, their market cap and volume
        3. Twitter data (API) with some limitations on history
        4. News feeds (API) with some limitations on volume
        5. Underlying hash algorithm that the ICO is built on

6. Creating the model .... *this needs to be pseudocoded*
    - Random forrest to help us determine features that are important?

7. Create the dashboard

# Limitations
After testing various API's to gather data, it became apparent that the most meaningful data required investment. As a result, sentiment analysis was done only on current periods to use as a proxy of what could be done at the time of an ICO launch. Furthermore, a lot of data needed to be collected manually, which wasn't attainable in the time alloted.

Determining post ICO success was also a sticking point. What is a successful ICO? We ultimately went with the simplest idea that a coin/token that was still actively trading counted as a success. A ratio of the price over the recipricole of longevitiy would result in an idex that would be higher for all coins/tokens with longer lifespans. Any score above the mean was marked as 1 (Successful); below the mean 0 (Unsuccessful).

# Final Model
The final set of features that went into our neural net were: Country, Platform, News Sentiments, and Twitter Sentiments. Using a series of nested for loops, we tested all parameters of the neural net to find the best combination for the highest accuracy. The final dataset used for the train/test portion of the model was on ICO's older than 360 days. Various iterations of the model resulted in an accuracy of at least 90%.

# Final Conclusions
Though the model showed high accuracy, when used to predict on the dataset of ICO's less than 360 days, all ICO's were predicted to be successful. It's unclear as to why this might be the case. If given more time, we definitely would have liked to pursue further investigation and also run a random forest or PCA to see which components were the most impactful.

# Dashboard


