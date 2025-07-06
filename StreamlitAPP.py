import os
os.environ.pop("SSL_CERT_FILE", None)
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load json files
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQ Generator with LangChain")

#Create a form using st.form
with st.form("user_inputs"):
    #File upload
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "csv"])

    #Input Fields
    mcq_count = st.number_input("Number of MCQs to generate", min_value=3, max_value=10, value=5)

    #Subject
    subject = st.text_input("Subject", placeholder="Enter the subject of the MCQs")

    #Quiz Tone
    tone = st.text_input("Complexity Level of Questions",max_chars=20, placeholder="Simple")

    #Add Button
    button = st.form_submit_button("Generate MCQs")

    #Check if the buitton is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        try:
            text = read_file(uploaded_file)
            #Count tokens and the cost of API call
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                    "text":text,
                    "number": mcq_count,
                    "subject":subject,
                    "tone":tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
            #st.write(respomse)
        
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("An error occurred while generating MCQs. Please try again.")

        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: ${cb.total_cost}")
            if isinstance(response, dict):
                #Extract the quiz data from response
                quiz=response.get("quiz", None)
                if quiz is not None:
                    #Convert the quiz data to a table format
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)
                        #Display the review in a text box as well
                        st.text_area(label="Review", value=response["review"])
                    else:
                        st.error("An error occurred while processing the quiz data. Please check the input file format.")
            else:
                st.write(response)





