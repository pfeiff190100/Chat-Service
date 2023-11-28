# Chat-Service
Basic Implementation for a Chat-Service using Flask

## Usage

### User Registration
- URL: /register
- Method: POST
- Data Params:
    - username: string
    - password: string
- Success Response:
    - Code: 201
    - Content: {'message': 'Registered successfully'}
- Error Response:
    - Code: 400
    - Content: {'message': 'Bad Request', 'error': 'Missing username or password'}

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
    - Code: 400
    - Content: {'message': 'Bad Request', 'error': 'Missing username or password'}
    - Code: 401
    - Content: {'message': 'Unauthorized', 'error': 'Invalid credentials'}

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
    - body: string
- Success Response:
    - Code: 201
    - Content: {'message': 'Message sent'}
- Error Response:
    - Code: 400
    - Content: {'message': 'Bad Request', 'error': 'Missing recipient or body'}
    - Code: 400
    - Content: {'message': 'Bad Request', 'error': 'Invalid body'}
    - Code: 404
    - Content: {'message': 'Not Found', 'error': 'Recipient not found'}

### Get Messages
- URL: /get_messages
- Method: POST
- Data Params:
    - recipient: string (username of the recipient)
- Success Response:
    - Code: 200
    - Content: {'messages': messages_data, 'message': 'Messages retrieved'}
- Error Response:
    - Code: 400
    - Content: {'message': 'Bad Request', 'error': 'Missing recipient'}
    - Code: 404
    - Content: {'message': 'Not Found', 'error': 'Recipient not found'}