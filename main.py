from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

##CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)

class Book(db.Model):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
  author: Mapped[str] = mapped_column(String(250), nullable=False)
  rating: Mapped[float] = mapped_column(Float, nullable=False)

  def __repr__(self):
    return f'<Book {self.title}>'

with app.app_context():
  db.create_all()



@app.route('/', methods=['GET', 'POST'])
def home():
    books = db.session.query(Book).all()

    if request.method == 'POST':
        tmp = request.form.get("Sort")
        print(tmp)
        if tmp=="bytitle":
            books = db.session.query(Book).order_by(Book.title).all()
        if tmp=="byscoreAsc":
            books = db.session.query(Book).order_by(Book.rating).all()
        if tmp=="byscoreDesc":
            books = db.session.query(Book).order_by(Book.rating.desc()).all()

    db.session.query(Book.rating).all()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )

        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("changer.html", book=book_selected)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)