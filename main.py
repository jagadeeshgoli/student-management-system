# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.student import (
    add_student, get_student_by_id, get_all_students, 
    update_student, delete_student, search_students
)
from models.department import (
    add_department, get_department_by_id, get_all_departments,
    update_department, delete_department
)
from utils.validators import validate_email, validate_phone, validate_name, validate_department_name

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_menu(options):
    """Print numbered menu options"""
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Exit")

def get_user_input(prompt):
    """Get user input with basic validation"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input cannot be empty. Please try again.")

def department_menu():
    """Department management menu"""
    while True:
        clear_screen()
        print_header("Department Management")
        
        options = [
            "Add Department",
            "View All Departments", 
            "Update Department",
            "Delete Department",
            "Back to Main Menu"
        ]
        print_menu(options)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            # Add Department
            name = get_user_input("Enter department name: ")
            if validate_department_name(name):
                add_department(name)
            else:
                print("  Invalid department name format.")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # View All Departments
            departments = get_all_departments()
            if departments:
                print("\nAll Departments:")
                print("-" * 50)
                for dept in departments:
                    print(f"ID: {dept['id']:<3} | Name: {dept['name']:<30} | Created: {dept['created_at']}")
            else:
                print("No departments found.")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Update Department
            try:
                dept_id = int(get_user_input("Enter department ID to update: "))
                new_name = get_user_input("Enter new department name: ")
                if validate_department_name(new_name):
                    update_department(dept_id, new_name)
                else:
                    print(" Invalid department name format.")
            except ValueError:
                print("Invalid department ID.")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Delete Department
            try:
                dept_id = int(get_user_input("Enter department ID to delete: "))
                delete_department(dept_id)
            except ValueError:
                print("Invalid department ID.")
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            break  # Back to main menu
            
        elif choice == '0':
            print("Goodbye! ")
            sys.exit(0)
            
        else:
            print("  Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def student_menu():
    """Student management menu"""
    while True:
        clear_screen()
        print_header("Student Management")
        
        options = [
            "Add Student",
            "View All Students",
            "Search Students",
            "Update Student",
            "Delete Student",
            "View Student by ID",
            "Back to Main Menu"
        ]
        print_menu(options)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            # Add Student
            name = get_user_input("Enter student name: ")
            if not validate_name(name):
                print(" Invalid name format.")
                input("\nPress Enter to continue...")
                continue
                
            email = get_user_input("Enter student email: ")
            if not validate_email(email):
                print("  Invalid email format.")
                input("\nPress Enter to continue...")
                continue
            
            phone = input("Enter phone number (optional, press Enter to skip): ").strip()
            if phone and not validate_phone(phone):
                print(" Invalid phone format.")
                input("\nPress Enter to continue...")
                continue
            
            dept_choice = input("Enter department ID (optional, press Enter to skip): ").strip()
            department_id = None
            if dept_choice:
                try:
                    department_id = int(dept_choice)
                except ValueError:
                    print(" Invalid department ID.")
                    input("\nPress Enter to continue...")
                    continue
            
            add_student(name, email, phone if phone else None, department_id)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # View All Students
            students = get_all_students()
            if students:
                print("\nAll Students:")
                print("-" * 80)
                for student in students:
                    dept_name = student['department_name'] or "No Department"
                    print(f"ID: {student['id']:<3} | Name: {student['name']:<20} | "
                          f"Email: {student['email']:<25} | Dept: {dept_name}")
            else:
                print("No students found.")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Search Students
            print("\nSearch Options:")
            print("1. Search by name")
            print("2. Search by department")
            search_choice = input("Enter choice: ").strip()
            
            if search_choice == '1':
                name_query = get_user_input("Enter name to search: ")
                students = search_students(name_query=name_query)
            elif search_choice == '2':
                try:
                    dept_id = int(get_user_input("Enter department ID: "))
                    students = search_students(department_id=dept_id)
                except ValueError:
                    print(" Invalid department ID.")
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Invalid search option.")
                input("\nPress Enter to continue...")
                continue
            
            if students:
                print(f"\nFound {len(students)} student(s):")
                print("-" * 80)
                for student in students:
                    dept_name = student['department_name'] or "No Department"
                    print(f"ID: {student['id']:<3} | Name: {student['name']:<20} | "
                          f"Email: {student['email']:<25} | Dept: {dept_name}")
            else:
                print("No students found matching criteria.")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Update Student
            try:
                student_id = int(get_user_input("Enter student ID to update: "))
                
                print("\nWhat would you like to update?")
                print("1. Name")
                print("2. Email") 
                print("3. Phone")
                print("4. Department ID")
                update_choice = input("Enter choice: ").strip()
                
                updates = {}
                if update_choice == '1':
                    new_name = get_user_input("Enter new name: ")
                    if validate_name(new_name):
                        updates['name'] = new_name
                    else:
                        print(" Invalid name format.")
                        input("\nPress Enter to continue...")
                        continue
                        
                elif update_choice == '2':
                    new_email = get_user_input("Enter new email: ")
                    if validate_email(new_email):
                        updates['email'] = new_email
                    else:
                        print("Invalid email format.")
                        input("\nPress Enter to continue...")
                        continue
                        
                elif update_choice == '3':
                    new_phone = input("Enter new phone (or press Enter to clear): ").strip()
                    if new_phone and not validate_phone(new_phone):
                        print("Invalid phone format.")
                        input("\nPress Enter to continue...")
                        continue
                    updates['phone'] = new_phone if new_phone else None
                    
                elif update_choice == '4':
                    dept_input = input("Enter new department ID (or press Enter to clear): ").strip()
                    if dept_input:
                        try:
                            updates['department_id'] = int(dept_input)
                        except ValueError:
                            print("Invalid department ID.")
                            input("\nPress Enter to continue...")
                            continue
                    else:
                        updates['department_id'] = None
                else:
                    print("Invalid update option.")
                    input("\nPress Enter to continue...")
                    continue
                
                if updates:
                    update_student(student_id, **updates)
                else:
                    print("No updates provided.")
                    
            except ValueError:
                print(" Invalid student ID.")
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            # Delete Student
            try:
                student_id = int(get_user_input("Enter student ID to delete: "))
                delete_student(student_id)
            except ValueError:
                print(" Invalid student ID.")
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            # View Student by ID
            try:
                student_id = int(get_user_input("Enter student ID: "))
                student = get_student_by_id(student_id)
                if student:
                    print(f"\nStudent Details:")
                    print(f"ID: {student['id']}")
                    print(f"Name: {student['name']}")
                    print(f"Email: {student['email']}")
                    print(f"Phone: {student['phone'] or 'Not provided'}")
                    print(f"Department: {student['department_name'] or 'No Department'}")
                    print(f"Created: {student['created_at']}")
                    print(f"Updated: {student['updated_at']}")
                else:
                    print("Student not found.")
            except ValueError:
                print(" Invalid student ID.")
            input("\nPress Enter to continue...")
            
        elif choice == '7':
            break  # Back to main menu
            
        elif choice == '0':
            print("Goodbye!")
            sys.exit(0)
            
        else:
            print(" Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def main():
    """Main application entry point"""
    print("Welcome to Student Management System!")
    print("Connecting to database...")
    
    # Test database connection
    try:
        from config.db import test_connection
        test_connection()
        print("Database connection successful!")
        input("\nPress Enter to continue to main menu...")
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Please check your database configuration and try again.")
        return
    
    while True:
        clear_screen()
        print_header("Student Management System")
        
        options = [
            "Department Management",
            "Student Management", 
            "Exit"
        ]
        print_menu(options)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            department_menu()
        elif choice == '2':
            student_menu()
        elif choice == '3' or choice == '0':
            print("Goodbye! ")
            break
        else:
            print("  Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
