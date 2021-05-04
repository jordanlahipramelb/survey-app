from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "jordan"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_start_survey():
    """Show start survey button"""
    return render_template("survey-start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clears the responses"""

    session["responses"] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_responses():
    """Save response and go to next question"""

    # listens to the choice that the user selects
    choice = request.form["answer"]

    # for a list stored in the session, you’ll need to rebind the name in the session in order to append the choice to the list.
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:id>")
def show_question(id):
    """Display current question"""

    # gets the responses session list
    responses = session.get("responses")

    if responses is None:
        return redirect("/")

    # this will redirect user to the last question they have not answered.
    if len(responses) != id:
        flash(f"Invalid id: {id}")
        return redirect(f"/questions/{len(responses)}")

    if len(responses) == len(survey.questions):
        return redirect("/complete")

    # accesses the question via index number
    question = survey.questions[id]
    return render_template("question.html", question=question, question_num=id)


@app.route("/complete")
def show_complete():
    """Show completion page"""

    return render_template("complete.html")
