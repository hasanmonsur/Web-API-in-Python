from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data: In-memory database (a list of books)
books = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"}
]

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Book API!"})

# Get all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

# Get a book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Add a new book
@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    if "title" in new_book and "author" in new_book:
        new_book["id"] = books[-1]["id"] + 1 if books else 1
        books.append(new_book)
        return jsonify(new_book), 201
    return jsonify({"error": "Invalid data"}), 400

# Update a book by ID
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        data = request.json
        book.update({key: data[key] for key in data if key in book})
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Delete a book by ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)