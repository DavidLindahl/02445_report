from openai import OpenAI
import openai
import os
import time
import replicate
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
from scipy.stats import kendalltau
import json

# Load the file
filepath = "Questions/Objecitve_Questions.txt"  # Objective
# filepath = "Subjective_Questions.txt" # Subjective"
df = pd.read_table(filepath)

# Make it one list withh all strings
prompts = []
for listo in df.to_numpy():
    prompts.append(listo[0])
# Define preprompt
pre_prompt = """Please provide a ranked list of the top 10 [category] in the following format, when a category is given. It should NOT include the ordered number in front of the answer. Ensure consistency in output by using a single format for each item, avoiding any additional descriptors or alterations. Each response should be a comma-separated list of names or items, with no extra text or commentary. If a ranking result has both a title and a year/date, only give the title. We are testing the output for consitiency. Therefor evey ranking item needs to ONLY INCLUDE THE TITLE. No paranthesis with any addition information (such as location, date, year etc.)

[Item 1], [Item 2], [Item 3], [Item 4], [Item 5],[Item 6], [Item 7], [Item 8], [Item 9], [Item 10]

Do not provide any additional text or context for the question. Ensure that identical queries return consistent results.

Example:

Q: wealthiest people in the world in 2024.
A: Elon Musk, Bernard Arnault, Jeff Bezos, Mark Zuckerberg, Larry Ellison, Larry Page, Sergey Brin, Warren Buffett, Bill Gates, Steve Ballmer

Q: fastest speed of land animals.
A: Cheetah, Pronghorn Antelope, Springbok, Wildebeest, Lion, Blackbuck, American Quarter Horse, Brown Hare, Greyhound, Kangaroo  * Strictly give the list. Don’t do a new line, this is going into python and will be separated. * Under no circumstances should you include ANY context. Only the answer. This is important, since we will comparing strings using python. No paranthesis explaining that this is an exception. No notes talking about something important about the pick on the rank list.

Q: most terrible TV show remakes of all time
A: The Inbetweeners, Knight Rider, Charlie's Angels, Ironside, The Munsters (Mockingbird Lane), MacGyver, Fantasy Island, Heroes Reborn, Charmed, Baywatch
NOT A: The Inbetweeners (US), Skins (US), Knight Rider (2008), Charlie's Angels (2011), The IT Crowd (US), Ironside (2013), The Munsters Today, Heroes Reborn, Baywatch Nights, MacGyver (2016)
"""

api_key_gpt = ""

client = OpenAI(api_key=api_key_gpt)

# LLama 2 API key
os.environ["REPLICATE_API_TOKEN"] = ""

temperature = 0.2


def get_response_gpt(pre_prompt, prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": pre_prompt,
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

models_gpt = {
    "gpt-4o": "gpt-4o",
    # "gpt-4-turbo": "gpt-4-turbo",

    # "gpt-3.5-turbo": "gpt-3.5-turbo", 
}

# Get all model_ids
all_model_ids = list(models_gpt.keys())

num_repeats = 11


# dictionary to store responses for every prompt and model
responses = {prompt: {rep: str for rep in range(num_repeats)} for prompt in prompts}

# Insert which prompts we wiould like
count = 0
total = len(prompts) * num_repeats * len(all_model_ids)

for prompt in prompts:
    for i in range(num_repeats):
        response_gpt = get_response_gpt(pre_prompt, prompt, model="gpt-4o")
        responses[prompt][i] = response_gpt
        count += 1
        if count % 15 == 0:
            print(f"{count}/{total}")

# Save the responses
# Convert the data dictionary to a pandas DataFrame
df = pd.DataFrame(responses)

# Save the DataFrame to a CSV file
df.to_csv("Prompts/Objective_Prompts_Temp_02.csv", index=False)

