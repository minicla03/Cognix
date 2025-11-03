from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

chat = Blueprint("chat", __name__)


@chat.route("/createChat", methods=["POST"])
@jwt_required()
def create_chat():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return make_response(jsonify({"message": "User id required"}), 400)

    try:
        # TODO: logica per creare chat
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return make_response(jsonify({"message": "Chat created successfully"}), 201)


@chat.route("/addDocument", methods=["POST"])
@jwt_required()
def add_document():
    document = request.json
    if not document:
        return make_response(jsonify({"message": "Document required"}), 400)

    try:
        # TODO: logica per aggiungere documento
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"message": "Document added successfully"}), 201


@chat.route("/removeDocument", methods=["DELETE"])
@jwt_required()
def remove_document():
    document = request.json
    if not document:
        return make_response(jsonify({"message": "Document required"}), 400)

    try:
        # TODO: logica per rimuovere documento
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"message": "Document removed successfully"}), 200


@chat.route("/doQuestion", methods=["POST"])
@jwt_required()
def do_question():
    question = request.json
    if not question:
        return make_response(jsonify({"message": "Question required"}), 400)

    try:
        # TODO: logica per rispondere alla domanda (RAG pipeline)
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"answer": "Not implemented"}), 200


@chat.route("/createFlashcard", methods=["POST"])
@jwt_required()
def create_flashcard():
    data = request.json
    if not data:
        return make_response(jsonify({"message": "Data required"}), 400)

    try:
        # TODO: logica flashcard
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"message": "Flashcard created successfully"}), 201


@chat.route("/createQuiz", methods=["POST"])
@jwt_required()
def create_quiz():
    data = request.json
    if not data:
        return make_response(jsonify({"message": "Data required"}), 400)

    try:
        # TODO: logica quiz
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"message": "Quiz created successfully"}), 201


@chat.route("/retrieveFlashcard", methods=["GET"])
@jwt_required()
def retrieve_flashcard():
    # Se vuoi parametri GET, usa request.args.get("param")
    try:
        # TODO: logica retrieve flashcard
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"flashcards": []}), 200


@chat.route("/retrieveQuiz", methods=["GET"])
@jwt_required()
def retrieve_quiz():
    try:
        # TODO: logica retrieve quiz
        pass
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

    return jsonify({"quizzes": []}), 200
