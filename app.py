from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "jordan"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

RESPONSES = []


@app.route("/")
def show_start_survey():
    """Show start survey button"""
    return render_template("survey-start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clears the responses"""

    RESPONSES = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_answers():
    """Save response and go to next question"""

    # listens to the choice that the user selects
    choice = request.form["answer"]

    # adds the choice to the RESPONSES
    RESPONSES.append(choice)

    if len(RESPONSES) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(RESPONSES)}")


@app.route("/questions/<int:id>")
def show_question(id):
    """Display current question"""

    if RESPONSES is None:
        return redirect("/")

    if len(RESPONSES) != id:
        flash(f"Invalid question id: {id}")
        return redirect(f"/questions/{len(RESPONSES)}")

    if len(RESPONSES) == len(survey.questions):
        return redirect("/complete")

    # accesses the question via index number
    question = survey.questions[id]
    return render_template("question.html", question=question, question_num=id)


@app.route("/complete")
def show_complete():
    """Show completion page"""

    return render_template("complete.html")
