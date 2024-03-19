# **Modtools**: A Content Moderation System

**Modtools** is a Flask-based web application aimed at simplifying the process of moderating user-uploaded images.

Using AI and manual verification, it ensures the content remains appropriate for the platform audience.

The system integrates various APIs for real-time image scanning, supports image status updates, and offers extendable plugin management for scalability.

## **Features**

**User Authentication:**

- Leverages Flask-Login for secure user authentication, ensuring only authorized personnel access the dashboard.

**Image Moderation:** Supports automatic scanning through integrated services like HiveAI and PhotoDNA, alongside manual review options such as approve, dismiss, or escalate.

**Plugin Management:**

- Easily manage active and inactive moderation plugins, enabling a customizable workflow suited to platform needs.

**API Integration:**

- Seamless integration with external APIs, facilitating the addition or removal based on current requirements.

**User Management:**

- Admins can invite, promote, degrade, or remove users, maintaining robust control over who can access the system.

**Content Submission and Management:**

- Users can submit images alongside metadata. Images are either automatically analyzed or manually reviewed, with options to filter based on various criteria.

## **Technologies Used**

- **Flask**
- **Flask-Bcrypt:** For hashing user passwords.
- **Flask-Login:** Handles user authentication sessions.
- **dotenv:** For loading environment variables from a .env file, keeping secrets safe.
- **Regex:** For validation purposes, such as verifying email formats.
- **Base64:** To handle image encoding and decoding, allowing images to be received and processed in various formats.
- **Jinja2:** Templating engine for rendering the frontend.
- **smtplib:** Email engine
- **psycopg2:** For interacting with the database.

## **Installation**

**Clone the Repository**

git clone https://github.com/qirtaiba/modtools

Set Up a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # For Unix/Linux/MacOS
venv\Scripts\activate  # For Windows
Install Dependencies

pip install -r requirements.txt
**Environment Variables**

Create a .env file at the root directory and configure your environment variables:

SECRET_KEY     your secret key for your flask app
PHOTODNA_KEY   photo dna key
x-user         photo dna username
x-pwd          photo dna password
HIVEAI_KEY     Your hive ai key
DATABASE_URL   Connection string to a database like neondb.
BASE_URL       url of your website where your moderation tool is hosted
EMAIL_SENDER   smtp email sender
EMAIL_PASSWORD smtp email password

**Initialize the Database**

Run the script provided in db/create_tables.sql to set up your database schema.

Run the Application

flask run --host=0.0.0.0 --port=8000
Access the application at http://localhost:8000.

**Usage**
Login/Register: First, register as a new user or login with existing credentials through the provided forms.

Dashboard: Navigate the dashboard to access moderation features, view submitted or escalated images, and manage plugins or APIs.

Actions: Perform actions like approve, dismiss, or escalate on submitted images based on moderation needs.

Administration: Admin users have additional capabilities including managing users and invitations, as well as activating or deactivating plugins and APIs.

**Contributing**
Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

**License**
This project is MIT licensed.

**Contact**
For any inquiries, please reach out through the repository's issue tracker.
