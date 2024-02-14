# Multi-Format Schema Comparison Tool

## Description

This tool allows you to compare schemas across different formats. It is powered by an OpenAI Assistant and supports SQL, JSON, Progress, and Text based schemas. It is intended to ensure consistency across different systems and data formats.

## Purpose
Existing schema comparison tools (such as Azure Data Studio's Schema Compare extension and SQL Server Data Tools (SSDT) Schema Compare utility) have two main limitations:
- Need to connect to the database (or dacpac/bacpac) to perform the comparison
- Struggle to compare dramatically different formats such as SQL vs Progress
By utilising an LLM, novel data schemas can be compared. This comes with the tradeoff of being less precise.

#### Existing tooling
- [Azure Data Studio Schema Compare extension](https://learn.microsoft.com/en-us/azure-data-studio/extensions/schema-compare-extension)
- [SQL Server Data Tools (SSDT) Schema Compare utility](https://learn.microsoft.com/en-us/sql/ssdt/how-to-use-schema-compare-to-compare-different-database-definitions?view=sql-server-ver16)


## Local Installation
Please note the application is hosted on Streamlit [here](https://schema-comparison-tool.streamlit.app/)
1. Clone the repository: `git clone https://github.com/JackRolfe/schema-comparison-tool.git`
2. Navigate to the project directory: `cd schema-comparison-tool`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the application: `streamlit run main.py`

## Usage
Some example files have been provided in the "examples" folder. These use the example of a Student table with some basic information on either an Admissions or Enrollments schema.

### Diff Checking
- This application can be used to Diff Check your files. This is useful for comparing similar files, such as two postgres SQL files between environments. It has less functionality than a tool such as [Diffchecker](https://www.diffchecker.com/), however can be ran locally for free.
- Upload the two data schema files you would like to compare and click the "Check the Difference" button.

### Schema Comparison
- Enter you OpenAI API Key into the "OpenAI API Key" field (for security, it is recommended to create a new key specifically for using this application).
- Upload the two data schema files you would like to compare and click the "Compare Schema" button.

## Application Architecture
The application uses:
- [Streamlit](https://streamlit.io/)
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)

## Alternative Implementation
This application can be implemented using the [OpenAI Playground](https://platform.openai.com/playground)
- Create a new assistant and paste the contents of "assistant_instructions.txt" into the Instructions area.
- In the user input area (where it says "Enter your message..."), input your two schemas in the below format. The agent will respond with the differences between the schemas.
```
Schema 1
---
CREATE TABLE "admissions"."student"
(
    "student_id" serial,
    "student_first_name" text,
    "student_last_name" text,
    "student_profile_url" text,
    PRIMARY KEY ("student_id"),
    UNIQUE ("student_profile_url")
);
---  


Schema 2
---
{
  "tableName": "StudentData",
  "schema": "enrollments",
  "columns": {
      "StudentId": {
          "type": "serial",
          "constraints": ["PRIMARY KEY"]
      },
      "StudentFirstName": {
          "type": "text"
      },
      "StudentLastName": {
          "type": "text"
      },
      "StudentProfileUrl": {
          "type": "text",
          "constraints": ["UNIQUE"]
      }
  }
}
---
```