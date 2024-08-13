# 📖 Book2dial: Generating Teacher Student Interactions from Textbooks for Cost-Effective Development of Educational Chatbots

[ACL 2024 Findings paper](https://aclanthology.org/2024.findings-acl.578/)
[ACL 2024 Video](https://www.youtube.com/watch?v=l1QCl7ENnWU)



[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

📖 Book2dial is grounded in textbooks from four domains: math, business, science, and social science. Our dataset contains teacher-student interactions that take the form of conversational question-answering (QA) interactions, where curious students ask teachers questions about the textbook content, and teachers provide answers based on the textbook.

# Description
In this project, we propose a framework for generating synthetic teacher-student interactions grounded in textbooks. Our approaches capture one aspect of learning interactions where curious students with partial knowledge interactively ask a teacher questions about the material in the textbook. We highlight various quality criteria such dialogues should fulfill and compare several approaches relying on either prompting or fine-tuning large language models. We provide evidence in our paper to show our generated dialogue dataset can be used to fine-tune educational chatbots.

# Citation
Please cite the following:
> Junling Wang, Jakub Macina, Nico Daheim, Sankalan Pal Chowdhury, and Mrinmaya Sachan. 2024. Book2Dial: Generating Teacher Student Interactions from Textbooks for Cost-Effective Development of Educational Chatbots. In Findings of the Association for Computational Linguistics ACL 2024, pages 9707–9731, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.

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
