# 📖 Book2dial: Generating Teacher Student Interactions from Textbooks for Cost-Effective Development of Educational Chatbots

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

📖 Book2dial is grounded in textbooks from four domains: math, business, science, and social science. Our dataset contains teacher-student interactions that take the form of conversational question-answering (QA) interactions, where curious students ask teachers questions about the textbook content, and teachers provide answers based on the textbook.

# Description
Educational chatbots are a promising tool for assisting student learning. However, the development of effective chatbots in education has been challenging, as high-quality data is seldom available in this domain. In this paper, we propose a framework for generating synthetic teacher-student interactions grounded in a set of textbooks. Our approaches capture one aspect of learning interactions where curious students with partial knowledge interactively ask a teacher questions about the material in the textbook. We highlight various quality criteria that such dialogues should fulfill and compare several approaches relying on either prompting or finetuning large language models. We use synthetic dialogues to train educational chatbots and show the benefits of further fine-tuning in different educational domains. However, human evaluation shows that our best data synthesis method still suffers from hallucinations and tends to reiterate information from previous conversations. Our findings offer insights for future efforts in synthesizing conversational data that strikes a balance between size and quality. We will open-source our data and code.

# Dataset
The dataset is available in the data folder. It contains 889 conversations generated from the Persona(High Info) model. We will release more data later. 
Please note that each row in the file consists of full conversations between a teacher and a student in JSON format.

![dataset-evaluation](images/evaluation.png)

## Data Structure
- `title` - the title of the current textbook chapter
- `history` - content of this conversation
- `qas` - list of question and answer pairs
- `uid` - unique identifier of the conversation

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
