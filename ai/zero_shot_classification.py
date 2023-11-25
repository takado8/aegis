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
datafile_with_embedding_path = "../data/testdata1_with_embedding.csv"
input_datapath = "../data/testdata1.csv"


def load_dataset():
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
    df["embedding"] = df.comment.apply(lambda x: get_embedding(text=x, model=embedding_model))
    print('Saving file.')
    df.to_csv(datafile_with_embedding_path)
    print(df)
    print(f'Result saved at: {datafile_with_embedding_path}')


def zero_shot():
    df = pd.read_csv(datafile_with_embedding_path)
    df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)

    def evaluate_embeddings_approach(labels, model, df):
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
        print(df['predicted_label'])


    labels = ['komentarz jest ofensywny', 'komentarz jest przyjazny i przyjacielski',
              'komentarz jest neutralny']

    evaluate_embeddings_approach(labels=labels, model=embedding_model, df=df)


# df = load_dataset()
# df = filter_out_too_long_entries(df)
# embedding(df)
zero_shot()