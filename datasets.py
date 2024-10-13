from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String(100), nullable=False)
    employees = relationship("Employee", back_populates="department")

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String(100), nullable=False)
    employees = relationship("Employee", back_populates="job")

class Employee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    datetime = Column(String(100), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
