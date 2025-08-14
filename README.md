# Fine-tuning BERT for Sentiment Analysis of Indihome Tweets

This project is a proof-of-concept for fine-tuning a BERT model to classify the sentiment of tweets about Indihome, a major Indonesian internet service provider. The goal is to create a model that can accurately categorize tweets as positive, negative, or neutral.

The project is divided into the following main parts:

1.  **Crawling:** A script to collect tweets with the keyword "indihome".
2.  **Preprocessing:** Jupyter notebooks for data cleaning, labeling, and merging.
3.  **Training:** A Jupyter notebook to fine-tune the BERT model on the labeled data.
4.  **API:** A FastAPI application to serve the fine-tuned model for sentiment analysis.

## Folder Structure

```
.
├── fastapi_app.py
├── requirements.txt
├── test_script.py
├── best_model
│   ├── config.json
│   ├── model.safetensors
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.txt
├── crawling
│   ├── install_dependencies.sh
│   └── run_tweet.sh
├── data
│   ├── indihome_tweet_data_for_training.csv
│   ├── data_awal
│   └── data_with_sentiment
├── preprocessing
│   ├── labeling.ipynb
│   └── merge_file.ipynb
├── training
│   └── bert_sentiment_training.ipynb
└── venv
```

## How to Run

### 1. Crawling

To collect tweets, you need to have `tweet-harvest` installed. You can install it by running the `install_dependencies.sh` script in the `crawling` folder.

```bash
cd crawling
sh install_dependencies.sh
```

Then, you can run the `run_tweet.sh` script to start crawling. You need to set your Twitter authentication token in the script.

```bash
sh run_tweet.sh
```

### 2. Preprocessing

The preprocessing steps are done in Jupyter notebooks. You can find them in the `preprocessing` folder.

*   `labeling.ipynb`: This notebook is used to label the sentiment of the tweets. It uses the OpenAI API to classify the sentiment of each tweet.
*   `merge_file.ipynb`: This notebook is used to merge the labeled data into a single CSV file.

### 3. Training

The training process is also done in a Jupyter notebook. You can find it in the `training` folder.

*   `bert_sentiment_training.ipynb`: This notebook is used to fine-tune the BERT model on the labeled data. It uses the `transformers` library from Hugging Face.

### 4. API

The fine-tuned model is served using a FastAPI application. To run the API, you need to install the dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

Then, you can run the `fastapi_app.py` script.

```bash
python fastapi_app.py
```

The API will be running at `http://localhost:8000`. You can access the documentation at `http://localhost:8000/docs`.

## Dependencies

The dependencies for this project are listed in `requirements.txt`.

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
torch>=1.9.0
transformers>=4.21.0
scikit-learn>=1.0.0
pandas>=1.3.0
numpy>=1.21.0
tqdm>=4.62.0
pydantic>=2.0.0
python-multipart>=0.0.5
```
