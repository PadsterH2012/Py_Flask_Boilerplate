# Py_Flask_Boilerplate

A boilerplate for Flask applications with user authentication and PostgreSQL database integration.

## Features

- User registration and login system
- PostgreSQL database integration
- Docker containerization
- Simple dashboard for logged-in users
- Responsive design with CSS

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Py_Flask_Boilerplate.git
   cd Py_Flask_Boilerplate
   ```

2. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

3. Access the application at `http://localhost:5000`

## Project Structure

```
Py_Flask_Boilerplate/
├── backend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   ├── static/
│   │   └── css/
│   │       └── base.css
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Usage

- Visit the homepage at `http://localhost:5000`
- Register a new user account
- Log in with your credentials
- Access the dashboard

## Development

To make changes to the application:

1. Modify the Flask application in `backend/app.py`
2. Update HTML templates in `backend/templates/`
3. Add or modify CSS in `backend/static/css/`
4. Rebuild and restart the Docker containers to see your changes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
