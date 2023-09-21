from flask import Flask,render_template, request
import numpy as np

import pickle

top50_df = pickle.load(open("C:\\Users\\Advait\\Desktop\\Code Playground\\2nd Try Book recommendation System\\top50.pkl", 'rb'))
pt = pickle.load(open("C:\\Users\\Advait\\Desktop\\Code Playground\\2nd Try Book recommendation System\\pt.pkl",'rb'))
books = pickle.load(open("C:\\Users\\Advait\\Desktop\\Code Playground\\2nd Try Book recommendation System\\books.pkl",'rb'))
similarity_scores = pickle.load(open("C:\\Users\\Advait\\Desktop\\Code Playground\\2nd Try Book recommendation System\\similarity_scores.pkl",'rb'))
book_title_list = pickle.load(open("C:\\Users\\Advait\\Desktop\\Code Playground\\2nd Try Book recommendation System\\book_title_list.pkl",'rb'))

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html',
                           book_name = list(top50_df['Book-Title'].values),
                           author = list(top50_df['Book-Author'].values),
                           image = list(top50_df['Image-URL-M'].values),
                           votes = list(top50_df['Review Count'].values),
                           rating = [round(float(value), 1) for value in top50_df['Avg Rating'].values]
,
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
                        
@app.route('/recommend_books', methods = ["post"])
def recommend():
    user_input = request.form.get('user_input')

    index = np.where(pt.index == user_input )[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key = lambda x:x[1], reverse = True)[1:11]
    data =[]
    for i in similar_items:
        item = []
        tempy_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(tempy_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(tempy_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(tempy_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)
    return render_template('recommend.html', data = data)

@app.route('/fetch_suggestions', methods=['POST'])
def fetch_suggestions():
    user_input = request.form.get('user_input')

    # Replace this with your logic to fetch book suggestions based on user_input
    # You can query a database or use any other data source
    # For now, I'll provide a simple example
    suggestions = book_title_list

    # Create an HTML list of suggestions
    suggestion_list = '<ul>'
    for suggestion in suggestions:
        suggestion_list += f'<li>{suggestion}</li>'
    suggestion_list += '</ul>'

    return suggestion_list


if __name__ == '__main__':
    app.run(debug = True)