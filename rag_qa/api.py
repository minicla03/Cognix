from fastapi import FastAPI

qa_api = FastAPI()

@qa_api.post("create_user")

@qa_api.post("create_chat")
def create_chat():

@qa_api.post("/add_document")
def add_document(document: dict):

@qa_api.delete("/remove_document")
def remove_document(document: dict):

@qa_api.post("/do_question")
def do_question(question: dict):

@qa_api.post("/create_flashcard")
def create_flashcard(question: dict):

@qa_api.post("/create_quiz")
def create_quiz(question: dict):


@qa_api.get("/retrieve_flashcard")
def retrieve_flashcard(question: dict):

@qa_api.get("/retrieve_quiz")
def retrieve_quiz(question: dict):
