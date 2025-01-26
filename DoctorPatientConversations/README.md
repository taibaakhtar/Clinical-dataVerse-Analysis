# Doctor-Patient Conversation Data Analysis
This project involves analyzing a Doctor-Patient conversation dataset, focusing on exploratory data analysis (EDA) and natural language processing (NLP). The primary tasks include:

### Text Length Analysis & Word Cloud: 
We perform an analysis of the text length and visualize the most frequent words used in the conversations with a word cloud.
### Sentiment Analysis: 
Sentiment analysis is carried out to understand the emotional tone of the conversations.
### NLP Preprocessing: 
This includes tokenization, stemming, and removal of stop words to clean and prepare the data for further analysis.
Additionally, the project tackles the following problem statements:

### Classifying Conversation Types: 
We aim to classify the conversations into categories such as general or emergency queries. Due to the lack of labeled data, k-means clustering is applied to group the queries and identify their nature. Once the text data is converted into numerical data, a classification model is trained to handle new queries.

Identifying and Correlating Illnesses with Symptoms: Using Named Entity Recognition (NER), we extract illnesses from the conversations and explore how these conditions relate to physical challenges like weakness or difficulty in daily activities. A heatmap is used to visualize the correlation between diseases and symptoms, providing insights that aid in diagnosis.
This analysis helps uncover patterns in doctor-patient interactions, making it easier to understand common concerns and improve the diagnostic process.
