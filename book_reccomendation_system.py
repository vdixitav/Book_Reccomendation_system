# -*- coding: utf-8 -*-
"""Book Reccomendation System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aKfLtlB2jUIM4RHm_RjBZBdGDtQHR1Oa
"""

import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

books = pd.read_csv("/content/Books.csv", on_bad_lines='skip', encoding='latin-1')
# Replace 'error_bad_lines' with 'on_bad_lines' and set to 'skip' to ignore bad lines

books.head()

books.columns

books=books[["ISBN","Book-Title","Year-Of-Publication","Publisher"]]

books.rename(columns={"Book-Title":'title',"Book-Author":'author',"Year-Of-Publication":'year',"Publisher":'publisher'},inplace=True)

books.head()

users = pd.read_csv("/content/Users.csv", on_bad_lines='skip', encoding='latin-1')

users.head()

users.rename(columns={"User-ID":'user_id',"Location":'location',"Age":'age'},inplace=True)

users.head()

ratings = pd.read_csv("/content/Ratings.csv", on_bad_lines='skip', encoding='latin-1')

ratings.head()

ratings.rename(columns={"User-ID":'user_id',"ISBN":'isbn',"Book-Rating":'book_rating'},inplace=True)

ratings.head()

books.shape # shape -info about books

users.shape

ratings.shape

"""# USING COLLABRATIVE FILTERING"""

ratings.head(2)

x=ratings["user_id"].value_counts()>200

y=x[x].shape

y.index

x = ratings["user_id"].value_counts() > 200
y = x[x].index  # Get the index of users with more than 200 ratings
ratings = ratings[ratings["user_id"].isin(y)]  # Filter ratings based on 'y'

ratings.shape

ratings.rename(columns={'isbn':'ISBN'},inplace=True)

ratings.head()

books.head()

# joining books and rating dataset with commen coloumn ISBN

ratings_with_books=ratings.merge(books,on="ISBN")

ratings_with_books.head()

ratings_with_books.shape

# books having 50 rating

number_rating=ratings_with_books.groupby('title')["book_rating"].count().reset_index()

number_rating.head()

number_rating.rename(columns={'book_rating':'number_of_ratings'},inplace=True)

number_rating.head()

final_rating=ratings_with_books.merge(number_rating,on="title")

final_rating.head()

final_rating.shape

final_rating.head()

final_rating=final_rating['number_of_ratings']>=50

final_rating.shape

final_rating = final_rating.drop_duplicates() # Remove duplicates and assign the result back to final_ratings
final_rating.shape

final_rating.shape

pt = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')

pt.fillna(0,inplace=True)

pt

from sklearn.metrics.pairwise import cosine_similarity

similarity_scores = cosine_similarity(pt)

similarity_scores.shape

def recommend(book_name):
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return data

recommend('1984')

pt.index[545]

import pickle
pickle.dump(popular_df,open('popular.pkl','wb'))

books.drop_duplicates('Book-Title')

pickle.dump(pt,open('pt.pkl','wb'))
pickle.dump(books,open('books.pkl','wb'))
pickle.dump(similarity_scores,open('similarity_scores.pkl','wb'))