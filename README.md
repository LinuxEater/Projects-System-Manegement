# Freelas Manager

Freelas Manager is a comprehensive web application built with Django, designed to streamline the workflow of freelancers. It provides a user-friendly interface to manage clients, projects, invoices, and payments, helping you stay organized and focused on your work.

## About

This project was developed to address the common challenges faced by freelancers in managing their administrative tasks. With Freelas Manager, you can easily track project progress, monitor financial transactions, and maintain a clear overview of your client relationships. The application is built on the robust Django framework, ensuring security, scalability, and ease of use.

## Features

*   **Client Management:** Add, edit, and view client details, including contact information and project history.
*   **Project Management:** Create and manage projects with detailed information such as title, description, start and end dates, value, and status (Pending, In Progress, Completed).
*   **Invoice Tracking:** Generate and manage invoices for your projects, with status tracking (Pending, Sent, Late, Paid).
*   **Payment Recording:** Keep a record of payments received for each invoice, ensuring your financial records are always up-to-date.
*   **Dashboard:** A central dashboard to visualize your projects, clients, and financial status at a glance.
*   **User Authentication:** A secure user authentication system to protect your data.
*   **Image Uploads:** The ability to upload images for both clients and projects, allowing for a more visual and organized presentation of your work.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.x
*   Pip

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your_username/freelas_manager.git
    ```
2.  **Navigate to the project directory:**
    ```sh
    cd freelas_manager
    ```
3.  **Create and activate a virtual environment:**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```
4.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
5.  **Apply the database migrations:**
    ```sh
    python manage.py migrate
    ```
6.  **Create a superuser to access the admin panel:**
    ```sh
    python manage.py createsuperuser
    ```
7.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`. You can access the admin panel at `http://127.0.0.1:8000/admin/`.

## Database

This project uses SQLite as the default database, which is a lightweight and easy-to-use option for development. If you need a more robust database for production, you can easily configure the project to work with other databases such as PostgreSQL, MySQL, or Oracle. To do so, you will need to update the `DATABASES` setting in the `freelas_manager/settings.py` file.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your_email@example.com

Project Link: [https://github.com/your_username/freelas_manager](httpss://github.com/your_username/freelas_manager)
