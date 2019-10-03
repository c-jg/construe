# Construe
Construe is a web application that uses AI and machine learning to read through thousands of YouTube comments and gather relevant data.

Construe reads through thousands of comments in just seconds and displays important information in charts that make it easy to understand your audience. 

### Features
- Scans through thousands of comments in seconds
- Gathers keyphrases, concepts, entities, spam, and sentiment
- Displays data in graphs and charts

### About
Built on Django using Google Cloud Platform PostgreSQL server.  Hosted on GCP App Engine.  Comments are retrieved using the YouTube Data API.  Comment analysis done using NLTK, Scikit Learn trained model, and IBM Watson API.  Payments handled by Stripe.  Account handling done using Django Allauth.  The website HTML/CSS is using Bootstrap and Evie theme.  ChartsJS is used for the dashboard charts as well as some of the charts on the various pages.

### Website Screenshots
The site is currently inactive.

![](Screenshots/Screen%20Shot%202019-10-02%20at%203.55.22%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%203.55.31%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%203.55.39%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%203.56.00%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%203.56.11%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%203.56.30%20PM.png)

#### Dashboard Screenshots

![](Screenshots/Screen%20Shot%202019-10-02%20at%204.11.14%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%204.11.27%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%204.11.35%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%204.11.53%20PM.png)

![](Screenshots/Screen%20Shot%202019-10-02%20at%204.12.03%20PM.png)

### Extra
This is the first project I've done using most of these libraries so there are many parts to improve on.  The templates are a bit messy as well as a few of the dashboard scripts.  When creating this, I was not very concerned about always keeping things clean, but more so getting things working as fast as possible so I could understand how they work and apply them to more advanced projects.  
