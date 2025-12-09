# models/student.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import get_connection
from utils.validators import validate_email, validate_phone
from psycopg2 import IntegrityError, DataError
import re

def add_student(name, email, phone=None, department_id=None):
    """
    Add a new student to the database.
    
    Args:
        name (str): Student's full name
        email (str): Unique email address
        phone (str, optional): Phone number
        department_id (int, optional): Department ID
    
    Returns:
        int: New student ID if successful, None if failed
    """
    # Validate inputs
    if not name or not email:
        print("Error: Name and email are required.")
        return None
    
    if not validate_email(email):
        print("Error: Invalid email format.")
        return None
    
    if phone and not validate_phone(phone):
        print("Error: Invalid phone format.")
        return None
    
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Insert query with optional phone and department
        query = """
            INSERT INTO students (name, email, phone, department_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        
        cursor.execute(query, (name, email, phone, department_id))
        student_id = cursor.fetchone()[0]
        
        conn.commit()
        print(f"Student '{name}' added successfully with ID: {student_id}")
        return student_id
        
    except IntegrityError as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            if "email" in str(e):
                print(f"Error: Email '{email}' already exists.")
            elif "phone" in str(e):
                print(f"Error: Phone '{phone}' already exists.")
        else:
            print(f"Database error: {e}")
        return None
        
    except DataError as e:
        conn.rollback()
        print(f"Data validation error: {e}")
        return None
        
    except Exception as e:
        conn.rollback()
        print(f"Unexpected error: {e}")
        return None
        
    finally:
        cursor.close()
        conn.close()

def get_student_by_id(student_id):
    """
    Get a single student by ID.
    
    Args:
        student_id (int): Student ID
    
    Returns:
        dict: Student data or None if not found
    """
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT s.id, s.name, s.email, s.phone, 
                   s.created_at, s.updated_at,
                   d.name as department_name
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.id
            WHERE s.id = %s;
        """
        
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3],
                'created_at': result[4],
                'updated_at': result[5],
                'department_name': result[6]
            }
        return None
        
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None
        
    finally:
        cursor.close()
        conn.close()

def get_all_students():
    """
    Get all students with department names.
    
    Returns:
        list: List of student dictionaries
    """
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT s.id, s.name, s.email, s.phone, 
                   s.created_at, s.updated_at,
                   d.name as department_name
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.id
            ORDER BY s.name;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        students = []
        for row in results:
            students.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'created_at': row[4],
                'updated_at': row[5],
                'department_name': row[6]
            })
        
        return students
        
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []
        
    finally:
        cursor.close()
        conn.close()

def update_student(student_id, **kwargs):
    """
    Update student fields. Only updates provided fields.
    
    Args:
        student_id (int): Student ID to update
        **kwargs: Fields to update (name, email, phone, department_id)
    
    Returns:
        bool: True if successful, False if failed
    """
    # Validate and filter update fields
    allowed_fields = {'name', 'email', 'phone', 'department_id'}
    update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not update_fields:
        print("Error: No valid fields to update.")
        return False
    
    # Validate email if provided
    if 'email' in update_fields and not validate_email(update_fields['email']):
        print("Error: Invalid email format.")
        return False
    
    # Validate phone if provided
    if 'phone' in update_fields and update_fields['phone'] and not validate_phone(update_fields['phone']):
        print("Error: Invalid phone format.")
        return False
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        values = list(update_fields.values())
        values.append(student_id)  # For WHERE clause
        
        query = f"""
            UPDATE students 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s;
        """
        
        cursor.execute(query, values)
        
        if cursor.rowcount == 0:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        
        conn.commit()
        print(f"Student ID {student_id} updated successfully.")
        return True
        
    except IntegrityError as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            if "email" in str(e):
                print(f"Error: Email already exists.")
            elif "phone" in str(e):
                print(f"Error: Phone number already exists.")
        else:
            print(f"Database error: {e}")
        return False
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating student: {e}")
        return False
        
    finally:
        cursor.close()
        conn.close()

def delete_student(student_id):
    """
    Delete a student by ID.
    
    Args:
        student_id (int): Student ID to delete
    
    Returns:
        bool: True if successful, False if failed
    """
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = "DELETE FROM students WHERE id = %s;"
        cursor.execute(query, (student_id,))
        
        if cursor.rowcount == 0:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        
        conn.commit()
        print(f"Student ID {student_id} deleted successfully.")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting student: {e}")
        return False
        
    finally:
        cursor.close()
        conn.close()

def search_students(name_query=None, department_id=None):
    """
    Search students by name (partial match) or department.
    
    Args:
        name_query (str, optional): Name to search for (partial match)
        department_id (int, optional): Department ID to filter by
    
    Returns:
        list: List of matching student dictionaries
    """
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        # Base query with joins
        query = """
            SELECT s.id, s.name, s.email, s.phone, 
                   s.created_at, s.updated_at,
                   d.name as department_name
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.id
            WHERE 1=1
        """
        
        conditions = []
        params = []
        
        # Add name search condition (partial match, case-insensitive)
        if name_query:
            conditions.append("s.name ILIKE %s")
            params.append(f"%{name_query}%")
        
        # Add department filter
        if department_id:
            conditions.append("s.department_id = %s")
            params.append(department_id)
        
        # Combine conditions
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY s.name;"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        students = []
        for row in results:
            students.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'created_at': row[4],
                'updated_at': row[5],
                'department_name': row[6]
            })
        
        return students
        
    except Exception as e:
        print(f"Error searching students: {e}")
        return []
        
    finally:
        cursor.close()
        conn.close()

# Test function
def test_student_operations():
    """Test all student operations"""
    print("Testing student operations...")
    
    # First, create a test department
    from models.department import add_department, delete_department
    
    dept_id = add_department("Test Department for Students")
    if not dept_id:
        print(" Could not create test department. Testing student without department...")
        dept_id = None
    
    # Test add student (with or without department)
    student_id = add_student("Test Student", "test@example.com", "1234567890", dept_id)
    if student_id:
        print(f"✓ Added student with ID: {student_id}")
        
        # Test get by ID
        student = get_student_by_id(student_id)
        if student:
            print(f"✓ Retrieved student: {student['name']}")
        
        # Test update
        if update_student(student_id, name="Updated Name"):
            print("✓ Updated student name")
        
        # Test search
        results = search_students(name_query="Updated")
        if results:
            print(f"✓ Found {len(results)} matching students")
        
        # Test delete
        if delete_student(student_id):
            print("✓ Deleted test student")
    
    # Clean up test department
    if dept_id:
        delete_department(dept_id)
        print("✓ Cleaned up test department")
    
    print("Student operations test completed.")

if __name__ == "__main__":
    test_student_operations()
