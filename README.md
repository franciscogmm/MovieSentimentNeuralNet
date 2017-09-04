# MovieSentimentNeuralNet
Analyzed Youtube move trailer performance and relationship with Box Office ROI performance using sentiment analysis and a neural network model

This was submitted as a project for my Big Data Analytics class in my MS Business Analytics program. The original title is “Exploring the Association of Movie Trailer Performance on YouTube and Box Office Success”. My other teammates are Yi Cai, Michael Friscia, and Zheyu Tian. This project was done for educational purposes only. 

Due to policies of thenumbers.com regarding their data, that particular data set won’t be uploaded.

Also, I'm only uploading my code.

### Check this link out for the neural network that I optimized using genetic algorithms: https://github.com/franciscogmm/ImprovingNeuralNetsWithGeneticAlgorithms

## Problem Statement
The purpose of this study is to determine if there is a correlation between the performance of trailers on YouTube and Hollywood movie sales.

## Data Collection
- Data was collected from YouTube, using its proprietary API, and from thenumbers.com
- Youtube – trailer performance and comments
- thenumbers.com – Movie Box Office data
- 32.4GB (when comments are expanded into 1 line per comment)
- 1,713 movies
- 5,244 trailers
- 2,979,511 comments

## Variable Selection
The ROI variable had to be created.

## Hypothesis and Rationale
- There is a positive correlation between Youtube movie trailer performance indicators  and Box office performance/Video Sales.
  - Rationale: “Likes” = Sales
- There is a positive correlation between Movie trailer comment sentiments and Box office/Video Sales  performance.
  - Rationale: If trailers are viewed in a positive manner, then people will be more likely to watch the movie. 
  
## Conceptual Model
- After data extraction using Python, data was transformed using Python. Output files were CSV and TXT files.
- Three sentiment models were implemented in the project: polarity-based sentiment models by using Bing Liu’s and Harvard IV-4 dictionaries, and Naive Bayes Classifier: NLTK Sentiment model.
  - To process part of the sentiment analysis, Apache Spark was used.
- The sentiment scores were also used to help identify the ROI of each movie using a neural network model.

## Sentiment Analysis
Two models were implemented for sentiment analysis.
- a polarity-based model using Bing Liu’s and a Harvard dictionary, which nets the counts of positive and negative words that can be found in each comment, and
- the NLTK Sentiment Analyzer using the Vader dictionary, which is a rule-based approach
- Scores were scaled and centered to zero to maintain positive scores > 0 and negative scores < 0. The scale is [-1,1].

## Predicting Box Office ROI Performance using Neural Net
- ROI performance was classified using four bins:
  - Poor (less than the 25% quantile)
  - Passing (between 25% and 50% quantile)
  - Ok (between the 50% and 75% quantile)
  - Great (above the  75% quantile)
- Neural Net implemented using R
- ROI Performance ~ countsComments + countsViews + Ratio_of_Likes_and_Dislikes + ProdBudget + genre + MPAArating + MovieStudio + BingLiuSentiment + HarvardSentiment + VadeSentiment

## Read the analysis at https://dataontherocks.wordpress.com/2017/05/04/exploring-the-association-of-movie-trailer-performance-on-youtube-and-box-office-success-using-neural-net-python-and-r/
