from streamlit_extras.stylable_container import stylable_container
import streamlit as st
import diff_match_patch as dmp_module
from io import StringIO
import time
from openai import OpenAI

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

OPENAI_API_KEY = st.text_input('OpenAI API Key', 'OPENAI_API_KEY')
if OPENAI_API_KEY:
    client = OpenAI(api_key = OPENAI_API_KEY)


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def ai_compare_files(schema_1: str, schema_2: str) -> str:
    try:
        assistant_instructions = open("assistant_instructions.txt", "r").read()
    except:
        return "Error: Could not load assistant_instructions text file."

    assistant = client.beta.assistants.create(
        name = "schemahelper",
        instructions = assistant_instructions,
        model="gpt-4-turbo-preview"
    )

    thread = client.beta.threads.create()

    schema_input ="""
Schema 1
---
""" + schema_1 + """
---


Schema 2
---
""" + schema_2 + """
---"""

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content = schema_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run = wait_on_run(run, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    output_string = 'Schema AI Response:\n\n'
    for message_output in messages.data:
        output_string = output_string + str(message_output.content[0].text.value) + '\n'
    
    response = client.beta.assistants.delete(assistant.id)

    return output_string

col1, col2 = st.columns(2)
my_upload1 = col1.file_uploader("Upload the first schema", type=["txt", "sql", "df", "json"])
my_upload2 = col2.file_uploader("Upload the second schema", type=["txt", "sql", "df", "json"])

if my_upload1 is not None:
    stringio1 = StringIO(my_upload1.getvalue().decode("utf-8"))
    string_data1 = stringio1.read()
    col1.code(string_data1)

if my_upload2 is not None:
    stringio2 = StringIO(my_upload2.getvalue().decode("utf-8"))
    string_data2 = stringio2.read()
    col2.code(string_data2)

if 'difference_clicked' not in st.session_state:
    st.session_state.difference_clicked = False

def click_difference_button():
    st.session_state.difference_clicked = True

st.button('Check the Difference', on_click=click_difference_button)

if st.session_state.difference_clicked:
    dmp = dmp_module.diff_match_patch()

    # Using LBYL instead of EAFP because "try: var" writes to screen
    string_data1_exists = 'string_data1' in locals() or 'string_data1' in globals()
    string_data2_exists = 'string_data2' in locals() or 'string_data2' in globals()

    if string_data1_exists == True and string_data2_exists == True:
        diff = dmp.diff_main(string_data1, string_data2)
        dmp.diff_cleanupSemantic(diff)
        html_diff = dmp.diff_prettyHtml(diff)

        # Styled container import because native streamlit doesn't allow container background colour changes
        with stylable_container(
            key="container_with_background",
            css_styles="""
                {
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    background: rgb(248, 249, 251)
                }
                """,
        ):
            st.markdown(html_diff, unsafe_allow_html=True)
            st.download_button(
                label="Download Diff",
                data=html_diff,
                file_name='schema_diff.html'
            )

if 'compare_clicked' not in st.session_state:
    st.session_state.compare_clicked = False

def click_compare_button():
    st.session_state.compare_clicked = True

st.button('Compare Schema', on_click=click_compare_button)

if st.session_state.compare_clicked:
    ai_response = ai_compare_files(string_data1, string_data2)
    st.code(ai_response)
    st.download_button(
        label="Download AI Response",
        data=ai_response,
        file_name='ai_schema_diff.txt'
    )