from flask import Flask, render_template, request
from openai.types import Completion
import openai
import envist
from mtranslate import translate  # for translation

app: Flask = Flask(__name__)
env: envist.Envist = envist.Envist()

# Set your OpenAI API key here
openai.api_key: str = env.get('OPENAI_API')

client: openai.OpenAI = openai.OpenAI(
    api_key=env.get('OPENAI_API'),
)


def english_to_bangla(text: str) -> str:
    '''Translate English to Bangla'''

    translator: str = translate(text, 'bn', 'en')
    return translator


def get_medicine_info(medicine_name: str) -> str:

    # Create a message to send to ChatGPT
    message: str = (
        f"You are a user searching for information about the medicine {medicine_name}. "
        f"Please provide details about {medicine_name}, including its group name, brand, and possible side effects. Return a formatted string with spacific points which I can render in HTML page, don't return any markdown format, give me pure HTML table as proper convensions. I know you are an AI, I will varify your answer answer so just answer the question don't explain it. Just answer the question aquirately. Thanks."
    )

    chat_completion: Completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message
            }
        ],
        model="gpt-3.5-turbo",
    )
    medicine_info: str = chat_completion.choices[0].message.content
    # return english_to_bangla(medicine_info)
    return medicine_info


@app.route("/", methods=["GET", "POST"])
def index() -> str:

    if request.method == "POST":
        medicine_name: str = request.form["medicine_name"]
        if medicine_name:
            medicine_info: str = get_medicine_info(medicine_name)
            # print(medicine_info)

        return render_template("index.html",
                               medicine_info=medicine_info,
                               medicine_name=medicine_name.title())

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
