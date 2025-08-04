# LiveBoard - A Real-time Collaborative Kanban Board

LiveBoard is a full-stack web application that mimics the core functionality of services like Trello, allowing users to collaborate on project boards in real-time. Built with Django Channels and WebSockets, this project serves as a powerful demonstration of modern, asynchronous backend architecture.

When one user moves a task card from "To Do" to "In Progress," the change is instantly reflected on the screens of all other team members viewing the same board, without needing a page refresh.



---

## Core Features

*   **Real-time Collaboration:** All board updates (moving cards, creating cards, etc.) are broadcast to connected users instantly using WebSockets.
*   **Multi-User Boards:** Users can be invited as members to multiple boards, with permissions restricting access to members only.
*   **Drag-and-Drop Interface:** Intuitive card management powered by SortableJS on the frontend.
*   **Persistent State:** All board, list, and card data is saved to a database, ensuring that the board state is preserved.
*   **User Authentication:** The application is built on Django's robust authentication system.

## Tech Stack

### Backend
*   **Python 3**
*   **Django & Django REST Framework**: For the core application logic and APIs.
*   **Django Channels**: To handle asynchronous protocols, primarily WebSockets.
*   **Daphne**: An ASGI server for running the application.
*   **Redis**: (Recommended for Production) The channel layer backend for robust, isolated message broadcasting. The project is configured to work with Redis.
*   **SQLite**: The default database for development.

### Frontend
*   **HTML5 & CSS3**
*   **Vanilla JavaScript**: To handle WebSocket connections and DOM manipulation.
*   **Bootstrap 5**: For a clean, responsive UI.
*   **SortableJS**: A lightweight library for implementing drag-and-drop functionality.

---

## Setup and Installation

Follow these steps to get the project running on your local machine for development and testing.

### Prerequisites
*   Python 3.8+
*   Git
*   (Optional but Recommended) A running Redis server.

### 1. Clone the Repository
git clone https://github.com/your-username/LiveBoard.git
cd LiveBoard
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
daphne liveboard_project.asgi:application

Usage Guide
Create Users: Log in to the Django Admin at /admin/ and create a few user accounts (e.g., user1, user2).
Create a Board: In the admin, create a new "Board" (e.g., "Final Year Project").
Add Members: In the board's admin view, add your newly created users to the "Members" list. Remember to add the owner as a member as well.
Create Lists & Cards: Create a few "Lists" (e.g., "To Do", "In Progress", "Done") and some "Cards" within those lists, all associated with your new board.
Test Collaboration:
Open two different browsers (e.g., Chrome and Firefox).
In Browser A, log in as user1 and navigate to the board's URL (e.g., /board/1/).
In Browser B, log in as user2 and navigate to the same board URL.
Drag a card in Browser A. You should see it move instantly in Browser B!

