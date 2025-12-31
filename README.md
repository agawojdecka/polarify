# Polarify

Polarify is a detailed sentiment analysis platform that enables users to organize and interpret feedback efficiently. It allows you to group opinions into specific projects and uses Google's Generative AI to automatically assess the emotional tone of text, categorizing it as positive, neutral, or negative.

## 🚀 Key Features

*   **Clean Architecture**: The codebase is structured into distinct layers (Domain, Repository, Service, API) to separate concerns, improve maintainability, and facilitate testing.
*   **Sentiment Analysis**: Leverages **Google Gemini (GenAI)** to analyze the sentiment of user opinions.
*   **Authentication**: Secure user authentication using Token Based Authentication.
*   **Project Management**: Create and manage projects to organize sentiment analysis tasks.
*   **Modern Tech Stack**: Built with FastAPI for high performance and Poetry for dependency management.
*   **Containerization**: Fully Dockerized application with PostgreSQL database.

## 🛠️ Tech Stack

*   **Language**: [Python 3.13](https://www.python.org/)
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Database**: [PostgreSQL](https://www.postgresql.org/)
*   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
*   **AI/ML**: [Google Generative AI SDK](https://ai.google.dev/)
*   **Package Manager**: [Poetry](https://python-poetry.org/)
*   **Containerization**: [Docker](https://www.docker.com/) & Docker Compose
*   **Testing**: [Pytest](https://docs.pytest.org/)

## 🏗️ Architecture

This project strictly follows the **Clean Architecture** approach:

*   **Domain Layer** (`app/domain`): Contains logic-less models and data structures.
*   **Repository Layer** (`app/repository`): Handles raw database interactions and data persistence.
*   **Service Layer** (`app/services`): Implements the business logic and orchestration.
*   **API Layer** (`app/api`): Handles HTTP requests, input validation (Pydantic), and routing.

This separation ensures that business logic is decoupled from external frameworks and database details.

## 🏁 Getting Started

### Prerequisites

*   **Python 3.13+**
*   **Poetry**
*   **Docker & Docker Compose**
*   A **Google Gemini API Key** (for sentiment analysis features)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd polarify
    ```

2.  **Environment Setup:**

    Create a `.env` file based on `.env.example` in the root directory. You can use an example or configure it manually:

3.  **Install Dependencies:**

    ```bash
    poetry install
    ```

4.  **Start Database:**

    Use Docker Compose to start the PostgreSQL database and pgAdmin (optional):

    ```bash
    docker-compose up -d
    ```

    *The database will be available at `localhost:5433`.*

5.  **Run the Application:**

    You can run the application using `fastapi` CLI or `uvicorn`:

    ```bash
    poetry run uvicorn main:app --port=8000 --reload
    ```

    The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### API Documentation

Once the application is running, you can access the interactive API documentation (Swagger UI) at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Testing

To run the test suite:

```bash
poetry run pytest
```
