import streamlit as st
import diff_match_patch as dmp_module
from io import StringIO
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import os

load_dotenv()

file1_name = "file1.txt"
file2_name = "file2.txt"

dirname = os.path.dirname(__file__)
file1_path = os.path.join(dirname, "input-files/" + file1_name)
file2_path = os.path.join(dirname, "input-files/" + file2_name)

def ai_compare_files():
    client = OpenAI()

    file1 = client.files.create(
        file=open(file1_path, "rb"),
        purpose='assistants'
    )

    file2 = client.files.create(
        file=open(file2_path, "rb"),
        purpose='assistants'
    )

    assistant = client.beta.assistants.create(
        name="schemahelper",
        instructions="You are a helpful text comparison assistant. You compare two files against each other and display the differences in an easy to understand way.",
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}],
        file_ids=[file1.id, file2.id]
    )

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Compare the two .txt files " + file1_name + " and " + file2_name + " against each other and display the differences in their schemas."
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    time.sleep(120)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    f = open("output-files/output.txt", "w")
    output_string = 'Schema AI Response:\n\n'
    for message_output in messages.data:
        output_string = output_string + str(message_output.content[0].text.value) + '\n'

    f.write(output_string)
    f.close()

    st.write(output_string, unsafe_allow_html=True)

    file_deletion_status1 = client.beta.assistants.files.delete(
        assistant_id=assistant.id,
        file_id=file1.id
    )

    file_deletion_status2 = client.beta.assistants.files.delete(
        assistant_id=assistant.id,
        file_id=file2.id
    )

st.set_page_config(layout="wide", page_title="Schema Comparison Tool")

st.write("## Compare Two Database Definition Files")
st.write(
    "This application allows you to compare two text files. It is specifically designed to compare database definition files (.sql or .df), but any text file will work."
)
st.write(
    "The 'Check the Difference' button compares files with a similar structure. For example, comparing two .sql files. It is useful for viewing how a database schema might change. This might be useful during application upgrades, or when comparing UAT vs Production environments."
)

st.write(
    "The 'Compare Schema' button compares files with a different structure. For example, comparing one .df file and one .sql file. It is useful for comparing the schema of a source system to a datawarehouse."
)

#st.sidebar.write("## Sidebar:")

col1, col2 = st.columns(2)
my_upload1 = col1.file_uploader("Upload the first schema", type=["txt", "sql", "df"])
my_upload2 = col2.file_uploader("Upload the second schema", type=["txt", "sql", "df"])

if my_upload1 is not None:
    if not os.path.exists("input-files"):
        os.makedirs("input-files")
    bytes_data1 = my_upload1.getvalue()
    # To convert to a string based IO:
    stringio1 = StringIO(my_upload1.getvalue().decode("utf-8"))
    # To read file as string:
    string_data1 = stringio1.read()
    col1.write(string_data1)

    f1 = open(file1_path, "w")
    f1.write(string_data1)
    f1.close()

if my_upload2 is not None:
    if not os.path.exists("input-files"):
        os.makedirs("input-files")
    bytes_data2 = my_upload2.getvalue()
    # To convert to a string based IO:
    stringio2 = StringIO(my_upload2.getvalue().decode("utf-8"))
    # To read file as string:
    string_data2 = stringio2.read()
    col2.write(string_data2)

    f2 = open(file2_path, "w")
    f2.write(string_data2)
    f2.close()

if st.button('Check the Difference'):
    if not os.path.exists("output-files"):
        os.makedirs("output-files")
    dmp = dmp_module.diff_match_patch()
    diff = dmp.diff_main(string_data1, string_data2)
    dmp.diff_cleanupSemantic(diff)
    html_diff = dmp.diff_prettyHtml(diff)
        
    st.write(html_diff, unsafe_allow_html=True)

    with open("output-files/diff.html", "w") as file:
        file.write(html_diff)


if st.button('Compare Schema'):
    if not os.path.exists("output-files"):
        os.makedirs("output-files")
    ai_compare_files()