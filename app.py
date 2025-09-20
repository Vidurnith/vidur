import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
# A secret key is needed to use sessions, which store data across requests.
app.secret_key = 'a-super-secret-key-for-the-app'

# Expanded quiz data with points for each question
quiz_data = {
    1: {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4',
        'color': '#3498db', # Blue
        'points': 10
    },
    2: {
        'question': 'What is the capital of France?',
        'options': ['London', 'Berlin', 'Paris', 'Madrid'],
        'answer': 'Paris',
        'color': '#e74c3c', # Red
        'points': 10
    },
    3: {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Venus'],
        'answer': 'Mars',
        'color': '#f1c40f', # Yellow
        'points': 10
    },
    4: {
        'question': 'What do bees make?',
        'options': ['Milk', 'Honey', 'Silk', 'Bread'],
        'answer': 'Honey',
        'color': '#2ecc71', # Green
        'points': 15
    },
    5: {
        'question': 'How many continents are there?',
        'options': ['5', '6', '7', '8'],
        'answer': '7',
        'color': '#9b59b6', # Purple
        'points': 15
    }
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Store the user's name and initialize their score in the session
        session['name'] = request.form['name']
        session['score'] = 0
        return redirect(url_for('quiz', level=1))
    return render_template('index.html')

@app.route('/quiz/<int:level>')
def quiz(level):
    # Redirect to home if the name is not in the session (e.g., direct URL access)
    if 'name' not in session:
        return redirect(url_for('home'))

    if level not in quiz_data:
        return redirect(url_for('complete'))

    question_data = quiz_data[level]
    return render_template('quiz.html', 
                           level=level, 
                           question_data=question_data,
                           name=session.get('name'),
                           score=session.get('score'))

@app.route('/submit/<int:level>', methods=['POST'])
def submit(level):
    if 'name' not in session:
        return redirect(url_for('home'))

    user_answer = request.form.get('answer')
    correct_answer = quiz_data[level]['answer']
    points_for_question = quiz_data[level]['points']

    if user_answer == correct_answer:
        # Add points to the score in the session
        session['score'] += points_for_question
        flash(f'Correct! You earned {points_for_question} points!', 'success')
        next_level = level + 1
        if next_level > len(quiz_data):
            return redirect(url_for('complete'))
        else:
            return redirect(url_for('quiz', level=next_level))
    else:
        flash('Not quite, try this one instead!', 'error')
        # Even if wrong, move to the next question to keep the game moving
        next_level = level + 1
        if next_level > len(quiz_data):
            return redirect(url_for('complete'))
        else:
            return redirect(url_for('quiz', level=next_level))


@app.route('/complete')
def complete():
    if 'name' not in session:
        return redirect(url_for('home'))
        
    # Pass the name and final score to the completion page
    name = session.get('name')
    score = session.get('score')
    # Clear session data after the quiz is complete for a clean restart
    session.pop('name', None)
    session.pop('score', None)
    return render_template('complete.html', name=name, score=score)

if __name__ == '__main__':
    app.run(debug=True,port=5025)