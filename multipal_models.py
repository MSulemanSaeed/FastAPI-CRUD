from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./multipal_model.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for SQLAlchemy models
Base = declarative_base()

# create database model for Person

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    father_name = Column(String, index=True)
    profession = Column(String, index=True)

# create database model for Student
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    father_name = Column(String, index=True)
    class_name = Column(String, index=True)

# create database model for Employee
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    father_name = Column(String, index=True)
    department = Column(String, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home_page():
    return {"Testing CRUD on Multipal Models in FastAPI"}

# Pydantic model for request body validation

class PersonCreate(BaseModel):
    name: str
    father_name: str
    profession: str

class StudentCreate(BaseModel):
    name: str
    father_name: str
    class_name: str

class EmployeeCreate(BaseModel):
    name: str
    father_name: str
    department: str


#CRUD on Person

@app.post("/persons/")
def create_person(person: PersonCreate):
    db = SessionLocal()
    db_person = Person(name=person.name, father_name=person.father_name, profession=person.profession)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/person/{person_id}")
def read_person(person_id: int):
    db = SessionLocal()
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code= 404, detail= "Person is not available")
    return person

@app.put("/person/{person_id}")
def update_person(person_id: int, person: PersonCreate):
    db = SessionLocal()
    db_person = db.query(Person).filter(Person.id == person_id).first()
    db_person.name = person.name
    db_person.father_name = person.father_name
    db_person.profession = person.profession
    db.commit()
    db.refresh(db_person)
    return db_person

@app.delete("/person/{person_id}")
def delete_person(person_id: int):
    db = SessionLocal()
    db_person = db.query(Person).filter(Person.id == person_id).first()
    db.delete(db_person)
    db.commit()
    return {"message": "Person deleted successfully"}


#CRUD on Student

@app.post("/students/")
def create_student(student: StudentCreate):
    db = SessionLocal()
    db_student = Student(name=student.name, father_name=student.father_name, class_name=student.class_name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/student/{student_id}")
def read_student(student_id: int):
    db = SessionLocal()
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code= 404, detail= "Student is not available")
    return student

@app.put("/student/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    db = SessionLocal()
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db_student.name = student.name
    db_student.father_name = student.father_name
    db_student.class_name = student.class_name
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/student/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

# CRUD on Employee

@app.post("/employees/")
def create_emoloyee(employee: EmployeeCreate):
    db = SessionLocal()
    db_employee = Employee(name=employee.name, father_name=employee.father_name, department=employee.department)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employee/{emoloyee_id}")
def read_employee(employee_id: int):
    db = SessionLocal()
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code= 404, detail="Employee is not available")
    return employee

@app.put("/employee/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeCreate):
    db = SessionLocal()
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    db_employee.name = employee.name
    db_employee.father_name = employee.father_name
    db_employee.department = employee.department
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
    db = SessionLocal()
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}