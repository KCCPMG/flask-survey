from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "SHHHHHHHH"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def get_home():
  return render_template("home.html")


@app.route("/questions/<question_no>")
def show_question(question_no):
  if len(responses) >= len(satisfaction_survey.questions):
    return redirect("thank-you") 
  elif int(question_no) != len(responses):
    flash("Please complete the questions in the correct order!")
    return redirect(f"/questions/{len(responses)}")
  question = satisfaction_survey.questions[int(question_no)]
  return render_template("question.html", question=question)


@app.route("/answer", methods=["POST"])
def get_answer():
  responses.append(request.form["answer"])
  next_question_no = len(responses)
  if next_question_no >= len(satisfaction_survey.questions):
    return redirect("thank-you") 
  else:
    return redirect(f"/questions/{next_question_no}")


@app.route("/thank-you")
def get_thank_you():
  return render_template("thank-you.html") 