# imports
import pandas as pd
import numpy as np
from ast import literal_eval
from ai.embedding_utils import  get_embedding
from sklearn.metrics import PrecisionRecallDisplay
import tiktoken
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.metrics import classification_report

### embedding

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191
datafile_with_embedding_path = "../data/wiatraki_comments_with_embedding.csv"
input_datapath = "../data/wiatraki_comments.csv"
# input_datapath = "../data/testdata1_eng.csv"


def load_dataset():
    print('Loading dataset.')
    df = pd.read_csv(input_datapath, index_col=0)
    df = df[["comment"]]
    df = df.dropna()
    return df


def filter_out_too_long_entries(df):
    encoding = tiktoken.get_encoding(embedding_encoding)
    df["n_tokens"] = df.comment.apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens <= max_tokens]
    print(f'dataset length: {len(df)}')
    return df


def embedding(df):
    # Ensure you have your API key set in your environment per the README: https://github.com/openai/openai-python#usage
    # This may take a few minutes
    print('Starting embedding...')
    df["embedding"] = df.comment.apply(lambda x: get_embedding(text=x.lower(), model=embedding_model))
    print('Saving file.')
    df.to_csv(datafile_with_embedding_path)
    print(df)
    print(f'Result saved at: {datafile_with_embedding_path}')


def zero_shot(labels, model, df=None):
    print('starting zero-shot classification.')
    if not df:
        df = pd.read_csv(datafile_with_embedding_path)
    df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)

    label_embeddings = {label: get_embedding(label, model=model) for label in labels}

    def label_score(review_embedding, label_embeddings):
        # Compute cosine similarity with each label's embedding and pick the highest one
        scores = {label: cosine_similarity([review_embedding], [embedding])[0][0] for label, embedding in
                  label_embeddings.items()}
        print(scores)
        return max(scores, key=scores.get)

    # Apply the function to each review embedding in the DataFrame
    df['predicted_label'] = df["embedding"].apply(lambda x: label_score(x, label_embeddings))

    print('Predicted labels:')
    for label, comment in zip(df['predicted_label'], df['comment']):
        print(f'{label}: {comment}')


if __name__ == '__main__':
    # df = load_dataset()
    # df = filter_out_too_long_entries(df)
    # embedding(df)
    labels1 = ['komentarz jest ofensywny', 'komentarz jest przyjazny i przyjacielski',
              'komentarz jest neutralny']

    labels_emotions = ['offensive to others',
                       'positive and friendly',
                        'neutral emotionally', 'negative']
    labels_satisfaction = ['komentarz na youtube jest nacechowany negatywnie', 'komentarz na youtube jest nacechowany pozytywnie',
                           'komentarz na youtube jest neutralny']
    zero_shot(labels1, embedding_model)
