import random
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
import yaml

app = Flask(__name__)
Swagger(app)

# Заглушки для методов API
students = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
quizzes = [{"id": 1, "title": "Python Quiz", "questions": ["What is Python?", "How do you define a function in Python?"]}]

# Определение спецификаций YAML для каждого метода
# Метод для получения списка всех студентов
GET_ALL_STUDENTS_SPEC = {
    "description": "Get a list of all students",
    "responses": {
        "200": {
            "description": "A list of all students",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}

# Метод для создания нового студента
CREATE_STUDENT_SPEC = {
    "description": "Create a new student",
    "parameters": [
        {
            "name": "name",
            "in": "formData",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "New student created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

# Метод для получения информации о конкретном студенте
GET_STUDENT_SPEC = {
    "description": "Get information about a specific student",
    "parameters": [
        {
            "name": "student_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "Information about the student",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

# Метод для получения списка всех тестов
GET_ALL_QUIZZES_SPEC = {
    "description": "Get a list of all quizzes",
    "responses": {
        "200": {
            "description": "A list of all quizzes",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"}
                    }
                }
            }
        }
    }
}

# Метод для создания нового теста
CREATE_QUIZ_SPEC = {
    "description": "Create a new quiz",
    "parameters": [
        {
            "name": "title",
            "in": "formData",
            "type": "string",
            "required": True
        },
        {
            "name": "questions",
            "in": "formData",
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "New quiz created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"}
                }
            }
        }
    }
}

# Метод для получения списка всех студентов
@app.route('/students', methods=['GET'])
@swag_from(GET_ALL_STUDENTS_SPEC)
def get_all_students():
    return jsonify(students)

# Метод для создания нового студента
@app.route('/students', methods=['POST'])
@swag_from(CREATE_STUDENT_SPEC)
def create_student():
    data = {"id": len(students) + 1, "name": request.form["name"]}
    students.append(data)
    return jsonify({"message": "Student added successfully"})

# Метод для получения информации о конкретном студенте
@app.route('/students/<int:student_id>', methods=['GET'])
@swag_from(GET_STUDENT_SPEC)
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404

# Метод для получения списка всех тестов
@app.route('/quizzes', methods=['GET'])
@swag_from(GET_ALL_QUIZZES_SPEC)
def get_all_quizzes():
    return jsonify(quizzes)

# Метод для создания нового теста
@app.route('/quizzes', methods=['POST'])
@swag_from(CREATE_QUIZ_SPEC)
def create_quiz():
    data = {"id": len(quizzes) + 1, "title": request.form["title"], "questions": request.form.getlist("questions")}
    quizzes.append(data)
    return jsonify({"message": "Quiz added successfully"})

# Добавим простой маршрут для проверки доступности сайта
@app.route('/', methods=['GET'])
def home():
    return "Ура, эта штука мне поддалась, благо есть куча документаций :D"


# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

