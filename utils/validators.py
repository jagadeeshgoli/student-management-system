# utils/validators.py
import re

def validate_email(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email to validate
    
    Returns:
        bool: True if valid, False if invalid
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """
    Validate phone number (10-15 digits, optional country code).
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if valid, False if invalid
    """
    if not phone:
        return True  # Phone is optional
    
    if not isinstance(phone, str):
        return False
    
    # Remove common separators and check if all digits
    clean_phone = re.sub(r'[-\s+().]', '', phone)
    return clean_phone.isdigit() and 10 <= len(clean_phone) <= 15

def validate_name(name):
    """
    Validate name (2-50 characters, letters, spaces, hyphens, apostrophes only).
    
    Args:
        name (str): Name to validate
    
    Returns:
        bool: True if valid, False if invalid
    """
    if not name or not isinstance(name, str):
        return False
    
    pattern = r'^[a-zA-Z\s\'-]{2,50}$'
    return bool(re.match(pattern, name.strip()))

def validate_department_name(name):
    """
    Validate department name (2-100 characters, letters, spaces, hyphens, numbers only).
    
    Args:
        name (str): Department name to validate
    
    Returns:
        bool: True if valid, False if invalid
    """
    if not name or not isinstance(name, str):
        return False
    
    pattern = r'^[a-zA-Z0-9\s\'-]{2,100}$'
    return bool(re.match(pattern, name.strip()))

# Test function
def test_validators():
    """Test all validator functions"""
    print("Testing validators...")
    
    # Email tests
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    assert validate_email("") == False
    print("✓ Email validators passed")
    
    # Phone tests
    assert validate_phone("1234567890") == True
    assert validate_phone("123-456-7890") == True
    assert validate_phone("+1-123-456-7890") == True
    assert validate_phone("123") == False
    assert validate_phone(None) == True  # Optional field
    print("✓ Phone validators passed")
    
    # Name tests
    assert validate_name("John Doe") == True
    assert validate_name("O'Connor") == True
    assert validate_name("Jean-Luc") == True
    assert validate_name("A") == False
    assert validate_name("") == False
    print("✓ Name validators passed")
    
    # Department name tests
    assert validate_department_name("Computer Science") == True
    assert validate_department_name("CS-2024") == True
    assert validate_department_name("A") == False
    assert validate_department_name("") == False
    print("✓ Department name validators passed")
    
    print("All validators test completed successfully!")

if __name__ == "__main__":
    test_validators()