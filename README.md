
# NEWS SENTIMENT ANALYSIS PIPELINE

 AWS-based pipeline that fetches news using an external API, performs sentiment analysis using TextBlob, stores raw data in S3 and structured insights in Amazon RDS, and displays results on a fully containerized Streamlit dashboard hosted on ECS Fargate.

---

## 📊 Architecture Diagram
![NEWS SENTIMENT ANALYSIS](https://github.com/akshay-1111/News_sentiment_pipeline/blob/03107089537bf9cd267c1fa6120c811f6c8bfe7e/news_sentiment_pipeline.jpeg)

**Flow:**  
**Lambda** → **S3 + RDS** → **ECR → ECS (Streamlit Dashboard)**


---

## Architecture

### ✅ Lambda (API Fetch + Sentiment)
- Fetches latest news from NewsAPI every few minutes (via EventBridge).
- Performs sentiment analysis using TextBlob.
- Writes:
  - Raw JSON → **S3**
  - Structured news with sentiment → **Amazon RDS (PostgreSQL)**

### ✅ Amazon RDS (PostgreSQL)
- Stores structured news articles.
- Table includes `title`, `url`, `description`, `published_at`, and `sentiment`.

- 
### ✅ Amazon ECR (Elastic Container Registry)
- Stores the Docker image built from the Streamlit app.
- Used as the image source for ECS deployment.

### ✅ Amazon ECS (Fargate) + Streamlit
- Dockerized Streamlit app connects to RDS and visualizes the latest news with sentiment.
- Deployed via ECS Fargate.
- Accessible via public IP.

---

## ⚙️ Technologies

- AWS Lambda + EventBridge
- Amazon RDS (PostgreSQL)
- Amazon S3 (raw storage)
- Amazon ECS Fargate
- Docker + Amazon ECR
- Python + Streamlit + TextBlob
- (Optional) SSH Bastion EC2 for secure RDS access

---

##  Prerequisites

-  IAM roles for Lambda, ECS task execution, S3, and RDS access.
-  sg,subnets creation
-  PostgreSQL DB created on RDS (with public access disabled).
-  A Bastion EC2 instance in public subnet (to access RDS(in postgressql) securely).
-  NewsAPI key (https://newsapi.org/)

## Project Structure and File Descriptions
- lambda_function.py	             =     AWS Lambda function that fetches  news using an external API, performs sentiment analysis using TextBlob, stores raw data in S3 and structured insights in Amazon RDS

  
- streamlit_dashboard/app.py       =     Streamlit app that reads news data from PostgreSQL and visualizes news sentiment
  
- streamlit_dashboard/Dockerfile   =	   Dockerfile for containerizing the Streamlit app (runs on port 8501)
  
- requirments.txt                  =     dependencies required by  Lambda_function.py
  
- app.py/requirements.txt          =     dependencies for your Streamlit dashboard


## 📊 Streamlit dashboard
![Streamlit dashboard](https://github.com/akshay-1111/News_sentiment_pipeline/blob/687f779793b599612c1e4a3c34fb51741df79fa9/streamlit_dashboard.png)

