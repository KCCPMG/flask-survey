from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret secrets are no fun"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def get_home():
  return render_template("home.html")


@app.route("/start-survey", methods=["POST"])
def start_session():
  session["responses"] = []
  session.modified = True
  return redirect("/questions/0")


@app.route("/questions/<question_no>")
def show_question(question_no):
  if len(session["responses"]) >= len(satisfaction_survey.questions):
    return redirect("thank-you") 
  elif int(question_no) != len(session["responses"]):
    flash("Please complete the questions in the correct order!")
    return redirect(f'/questions/{len(session["responses"])}')
  question = satisfaction_survey.questions[int(question_no)]
  return render_template("question.html", question=question)


@app.route("/answer", methods=["POST"])
def get_answer():

  session["responses"].append(request.form["answer"])
  
  # Need to set session.modified to true to preserve change to session["responses"]. From the docs:
  """Be advised that modifications on mutable structures are not picked up automatically, in that situation you have to explicitly set the attribute to True yourself."""
  session.modified = True

  next_question_no = len(session["responses"])
  if next_question_no >= len(satisfaction_survey.questions):
    return redirect("thank-you") 
  else:
    return redirect(f"/questions/{next_question_no}")


@app.route("/thank-you")
def get_thank_you():
  return render_template("thank-you.html") 