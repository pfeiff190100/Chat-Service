# Chat-Service
Basic Implementation for a Chat-Service using Flask

# Usage

### User Registration
- URL: /register
- Method: POST
- Data Params:
    - username: string
    - password: string
- Success Response:
    - Code: 200
    - Content: {'message': 'Registered successfully'}

### User Login
- URL: /login
- Method: POST
- Data Params:
    - username: string
    - password: string
- Success Response:
    - Code: 200
    - Content: {'message': 'Logged in successfully'}
- Error Response:
    - Code: 200
    - Content: {'message': 'Invalid credentials'}

### User Logout
- URL: /logout
- Method: GET
- Success Response:
    - Code: 200
    - Content: {'message': 'Logged out successfully'}

### Send Message
- URL: /send_message
- Method: POST
- Data Params:
    - recipient: string (username of the recipient)
    - message: string
- Success Response:
    - Code: 200
    - Content: {'message': 'Message sent'}
- Error Response:
    - Code: 200
    - Content: {'message': 'Recipient not found'}