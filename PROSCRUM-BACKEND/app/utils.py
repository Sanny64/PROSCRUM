import bcrypt

def hash(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    string_hashed_password = hashed_password.decode('utf-8')
    return string_hashed_password

def verify(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_enc)

from .mockups import my_rounds, courses_list

def find_round(round_number: int):
    for round in my_rounds:
        if round.round_number == round_number:
            return round
        
def find_course(id: int):
    for course in courses_list:
        if course.course_id == id:
            return course
        
def find_index_round(round_number):
    for i, r in enumerate(my_rounds):
        print(f"i: {i}, r: {r}")
        if r.round_number == round_number:
            return i

def find_index_course(id):
    for i, c in enumerate(courses_list):
        print(f"i: {i}, c: {c}")
        if c.course_id == id:
            return i