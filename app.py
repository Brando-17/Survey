from flask import Flask , request , render_template , redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtention
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['secret'] = "never-tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtention(app)
Responses = 'responses'

@app.route('/')
def survey_start():
    return render_template('survey_start.html', survey = survey)

@app.route('/begin', methods=["POST"])
def start_survey():

    session[Responses] = []

    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def answer_question():
    choice = request.form['answer']

    responses = session[Responses]
    responses.append(choice)
    session[Responses] = responses

    if(len(responses)== len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route('/questions/<int:qid>')
def show_question():
    responses = session.get(Responses)
    if(responses is None):
        return redirect("/")
    if(len(responses)==len(survey.questions)):
        return redirect("/complete")
    if(len(responses) != qid):
        flash(f"Invalid questions id: {qid}")
    question = survey.questions[qid]
    return render_template("question.html",question_num=qid, question=question)
    
@app.route('/complete')
def complete():
    return render_template("completion.html")