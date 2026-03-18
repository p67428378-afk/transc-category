# Automated Transaction Categorization System

This project implements a full-stack application for automated transaction categorization using an LLM-based engine.

## Project Structure

- `frontend/`: Contains the React-based web dashboard.
- `backend/`: Contains the FastAPI application for API endpoints.
- `data_engineering/`: Contains the Python/Pandas ETL pipeline.

## Setup and Installation

Detailed setup instructions will be provided within each service's respective README file.

## Development

### Prerequisites

- Docker
- Docker Compose

### Running the Application Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/transc-category.git
    cd transc-category
    ```

2.  **Set up environment variables:**
    Create `.env` files in `backend/`, `data_engineering/`, and `frontend/` based on their respective `.env.example` files.

3.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

    This will start:
    - PostgreSQL database
    - Backend API (FastAPI)
    - Frontend (React)
    - ETL Service (can be triggered manually or via API)

## API Documentation

The Backend API documentation (Swagger UI) will be available at `/docs` when the backend service is running.

## Contributing

Refer to the `CONTRIBUTING.md` for guidelines on how to contribute to this project.
