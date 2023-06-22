import os

import openai
import datetime
import csv
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        note = request.form["note"]
        timestamp = datetime.datetime.now()
        storeincsv(note, timestamp)
        response = openai.Completion.create(
            model="text-davinci-003",
            #messages=[{"role":"user", "content": note + "please provide the reminders."}],
            prompt=generate_prompt_note(note),
            max_tokens=200,
        )

        print("response is: "+ response.choices[0].text)
        print("finish reason : " + response.choices[0].finish_reason)
        #  return redirect(url_for("index", result=response.choices[0].text.replace("\n", "")))

    result = request.args.get("result")
    #print(result.chou)
    return render_template("index.html", result=result)
  
##model="ft-kf9PN9sWYTsBg5tbRVMc5xxi",
#store the data in a csv file
def storeincsv(note, timestamp):
    with open('notes.csv', 'a') as csvfile:
        fieldnames = ['note', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'note': note, 'timestamp': timestamp})

def generate_prompt(note):
    return """Suggest three names for an animal that is a superhero.


Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        note.capitalize()
    )

def generate_prompt_note(note):
    return note + "please provide the reminders and goals in a tabular format"
