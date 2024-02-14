# Multi-Format Schema Comparison Tool

## Description

This tool allows you to compare schemas across different formats. It is powered by an OpenAI Assistant and supports SQL, JSON, Progress, and Text based schemas. It is intended to ensure consistency across different systems and data formats.

## Purpose
Existing schema comparison tools (such as Azure Data Studio's Schema Compare extension [1] and SQL Server Data Tools (SSDT) Schema Compare utility [2]) have two main limitations:
- Need to connect to the database (or dacpac/bacpac) to perform the comparison
- Struggle to compare dramatically different formats such as SQL vs Progress

[1] `https://learn.microsoft.com/en-us/azure-data-studio/extensions/schema-compare-extension`
[2] `https://learn.microsoft.com/en-us/sql/ssdt/how-to-use-schema-compare-to-compare-different-database-definitions?view=sql-server-ver16`


## Installation

1. Clone the repository: `git clone https://github.com/JackRolfe/schema-comparison-tool.git`
2. Navigate to the project directory: `cd schema-comparison-tool`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the application: `streamlit run main.py`

## Usage
TODO