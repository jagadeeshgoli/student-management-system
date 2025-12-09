# models/department.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import get_connection
from psycopg2 import IntegrityError

def add_department(name):
    """
    Add a new department.
    
    Args:
        name (str): Department name
    
    Returns:
        int: New department ID if successful, None if failed
    """
    if not name or not name.strip():
        print("Error: Department name is required.")
        return None
    
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        query = "INSERT INTO departments (name) VALUES (%s) RETURNING id;"
        cursor.execute(query, (name.strip(),))
        dept_id = cursor.fetchone()[0]
        
        conn.commit()
        print(f"Department '{name}' added successfully with ID: {dept_id}")
        return dept_id
        
    except IntegrityError as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            print(f"Error: Department '{name}' already exists.")
        else:
            print(f"Database error: {e}")
        return None
        
    except Exception as e:
        conn.rollback()
        print(f"Unexpected error: {e}")
        return None
        
    finally:
        cursor.close()
        conn.close()

def get_department_by_id(dept_id):
    """
    Get department by ID.
    
    Args:
        dept_id (int): Department ID
    
    Returns:
        dict: Department data or None if not found
    """
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        query = "SELECT id, name, created_at FROM departments WHERE id = %s;"
        cursor.execute(query, (dept_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'created_at': result[2]
            }
        return None
        
    except Exception as e:
        print(f"Error fetching department: {e}")
        return None
        
    finally:
        cursor.close()
        conn.close()

def get_all_departments():
    """
    Get all departments.
    
    Returns:
        list: List of department dictionaries
    """
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        query = "SELECT id, name, created_at FROM departments ORDER BY name;"
        cursor.execute(query)
        results = cursor.fetchall()
        
        departments = []
        for row in results:
            departments.append({
                'id': row[0],
                'name': row[1],
                'created_at': row[2]
            })
        
        return departments
        
    except Exception as e:
        print(f"Error fetching departments: {e}")
        return []
        
    finally:
        cursor.close()
        conn.close()

def update_department(dept_id, name):
    """
    Update department name.
    
    Args:
        dept_id (int): Department ID
        name (str): New department name
    
    Returns:
        bool: True if successful, False if failed
    """
    if not name or not name.strip():
        print("Error: Department name is required.")
        return False
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = "UPDATE departments SET name = %s WHERE id = %s;"
        cursor.execute(query, (name.strip(), dept_id))
        
        if cursor.rowcount == 0:
            print(f"Error: Department with ID {dept_id} not found.")
            return False
        
        conn.commit()
        print(f"Department ID {dept_id} updated successfully.")
        return True
        
    except IntegrityError as e:
        conn.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            print(f"Error: Department name '{name}' already exists.")
        else:
            print(f"Database error: {e}")
        return False
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating department: {e}")
        return False
        
    finally:
        cursor.close()
        conn.close()

def delete_department(dept_id):
    """
    Delete department by ID.
    Note: This will set student.department_id to NULL due to ON DELETE SET NULL constraint.
    
    Args:
        dept_id (int): Department ID to delete
    
    Returns:
        bool: True if successful, False if failed
    """
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = "DELETE FROM departments WHERE id = %s;"
        cursor.execute(query, (dept_id,))
        
        if cursor.rowcount == 0:
            print(f"Error: Department with ID {dept_id} not found.")
            return False
        
        conn.commit()
        print(f"Department ID {dept_id} deleted successfully.")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting department: {e}")
        return False
        
    finally:
        cursor.close()
        conn.close()

# Test function
def test_department_operations():
    """Test all department operations"""
    print("Testing department operations...")
    
    # Test add
    dept_id = add_department("Test Department")
    if dept_id:
        print(f"✓ Added department with ID: {dept_id}")
        
        # Test get by ID
        dept = get_department_by_id(dept_id)
        if dept:
            print(f"✓ Retrieved department: {dept['name']}")
        
        # Test update
        if update_department(dept_id, "Updated Department"):
            print("✓ Updated department name")
        
        # Test get all
        all_depts = get_all_departments()
        print(f"✓ Found {len(all_depts)} departments")
        
        # Test delete
        if delete_department(dept_id):
            print("✓ Deleted test department")
    
    print("Department operations test completed.")

if __name__ == "__main__":
    test_department_operations()