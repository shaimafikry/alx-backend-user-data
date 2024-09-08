# alx-backend-user-data
from base64 import b64decode

def decode_base64_authorization_header(base64_authorization_header):
    try:
        # Convert the string to bytes (required for Base64 decoding)
        encoded = base64_authorization_header.encode('utf-8')
        
        # Decode the Base64-encoded bytes
        decoded64 = b64decode(encoded)
        
        # Convert the decoded bytes back to a UTF-8 string
        decoded = decoded64.decode('utf-8')
        
        return decoded  # Returns 'user:password'
    except BaseException:
        return None  # If anything goes wrong, return None

# Example usage
auth_header = "dXNlcjpwYXNzd29yZA=="
result = decode_base64_authorization_header(auth_header)

if result:
    print(f"Decoded: {result}")
else:
    print("Invalid Base64 string or decoding failed.")


To implement the `session_cookie` method in `api/v1/auth/auth.py`, we need to retrieve the session cookie from the incoming request based on the environment variable `SESSION_NAME`. The method will return the value of the session cookie or `None` if the request or cookie is not found.

### Step-by-Step Implementation

1. **Environment Variable**:
   - We'll use the `SESSION_NAME` environment variable to define the name of the session cookie.
   
2. **Accessing Cookies from Request**:
   - Flask's `request.cookies` is a dictionary-like object where cookies can be accessed by name using `.get()`.

### Code Implementation:

```python
import os
from flask import request

class Auth:
    """
    Auth class for handling authentication-related tasks, including session cookies.
    """

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie from the request.

        Args:
            request (object): The Flask request object.

        Returns:
            str: The value of the session cookie or None if not found.
        """
        # Return None if the request is None
        if request is None:
            return None
        
        # Get the name of the session cookie from the environment variable SESSION_NAME
        session_name = os.getenv('SESSION_NAME', '_my_session_id')

        # Return the value of the cookie with the name defined by session_name
        return request.cookies.get(session_name)
```

### Explanation:

1. **`session_cookie(self, request=None)`**:
   - **Input Validation**: If `request` is `None`, the method returns `None`.
   - **Environment Variable**: It uses `os.getenv('SESSION_NAME', '_my_session_id')` to fetch the name of the cookie from the environment variable `SESSION_NAME`. If `SESSION_NAME` is not set, it defaults to `_my_session_id`.
   - **Accessing Cookies**: The method uses `request.cookies.get(session_name)` to retrieve the session cookie value from the request.
   
2. **Environment Variable**:
   - The environment variable `SESSION_NAME` defines the name of the session cookie. If it's set to, say, `SESSION_NAME="my_session_cookie"`, then the cookie `my_session_cookie` will be fetched from the request.

### Example Usage:

You can test the `session_cookie` method with Flask as follows:

```python
from flask import Flask, request

app = Flask(__name__)

auth = Auth()

@app.route('/test_cookie', methods=['GET'])
def test_cookie():
    # Test the session_cookie method
    session_id = auth.session_cookie(request)
    return {'session_id': session_id}

if __name__ == '__main__':
    app.run(debug=True)
```

### Testing with `curl`:

1. Start your Flask application.
2. Send a request with the session cookie:
   ```bash
   curl -X GET http://127.0.0.1:5000/test_cookie -b "_my_session_id=12345"
   ```
   
   **Expected Output**:
   ```json
   {"session_id": "12345"}
   ```

If the `SESSION_NAME` environment variable is set, ensure to change the cookie name accordingly in the request.
