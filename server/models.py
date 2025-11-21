from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        value = value.strip()

        if not value:    
            raise ValueError("Author name must not be empty.")
        
        # Name must be unique
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author:
            raise ValueError("Author name must be unique.")
    
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        # Value must exist, be digits only, and exactly 10 characters long
        if not value or not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        
        return value
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    # Title must not be empty
    @validates('title')
    def validate_title(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Post must have a non-empty title.")
          
        return value
    
    # Content must be at least 250 characters
    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value.strip()) < 250:
            raise ValueError("Content must be at least 250 characters.")
        
        return value
    
    # Summary must be at most 250 characters
    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value.strip()) > 250:
            raise ValueError("Summary must be at most 250 characters.")
        
        return value
    
    # Category must be "Fiction" or "Non-Fiction"
    @validates('category')
    def validate_category(self, key, value):
        allowed = ["Fiction", "Non-Fiction"]
        if value not in allowed:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
    
        return value
    
    # Title must contain clickbait phrase
    @validates('title')
    def validate_title(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Post must have a non-empty title.")
        
        clickbait_phrases = [
           "Won't Believe",
           "Secret",
           "Top",
           "Guess"
        ]

        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must contain clickbait phrase.")

        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
