# ModTools: A Content Moderation System

ModTools is a powerful Flask-based web application designed to streamline the process of moderating user-uploaded images. It leverages AI and human verification to ensure that the content remains appropriate for the platform's audience.

## Key Features

### User Authentication
- Secure user authentication using Flask-Login
- Role-based access control (e.g., admin, moderator, user)
- Password hashing with Flask-Bcrypt for enhanced security

### Image Moderation
- Automatic image scanning through integrated services like HiveAI and PhotoDNA
- Manual review options: approve, dismiss, or escalate
- Detailed image metadata (upload time, location, IP address, etc.)

### Plugin Management
- Flexible and extensible plugin architecture
- Easy activation/deactivation of moderation plugins
- Customizable workflow tailored to platform needs

### API Integration
- Seamless integration with external APIs (e.g., image analysis, content moderation)
- Modular design for adding or removing APIs based on requirements

### User Management (Admin)
- Invite, promote, degrade, or remove users
- Granular control over user access and permissions

### Content Submission and Management
- User-friendly interface for submitting images and metadata
- Powerful filtering and sorting capabilities
- Image status tracking (pending, approved, dismissed, escalated)

## Technologies Used

- **Flask**: Python web framework for building the application
- **Flask-Bcrypt**: Hashing user passwords for secure storage
- **Flask-Login**: Handling user authentication sessions
- **dotenv**: Loading environment variables from a `.env` file
- **Regex**: Validating user inputs (e.g., email formats)
- **Base64**: Encoding and decoding images for processing
- **Jinja2**: Templating engine for rendering the frontend
- **smtplib**: Email engine for notifications and alerts
- **psycopg2**: Interacting with the PostgreSQL database

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL (or any other supported database)

### Using Docker (Recommended)

ModTools Image is available on Docker Hub as `qirtaiba/modtools`. You can get it running with the following steps:

1. Pull the Docker image:
   ```
   docker pull qirtaiba/modtools
   ```

2. Create a `.env` file with the required environment variables (see below).

3. Run the Docker container and map the required ports:
   ```
   docker run -d --name modtools -p 8000:8000 -v $(pwd)/.env:/app/.env qirtaiba/modtools
   ```
   This command maps the `.env` file from the current directory to the `/app/.env` path in the container and exposes the application on port `8000` of the host machine.

4. Access the application at `http://localhost:8000`.

### Source installation

1. Clone the repository:
   ```
   git clone https://github.com/qirtaiba/modtools
   ```

2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # For Unix/Linux/MacOS
   venv\Scripts\activate  # For Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file at the root directory and set the required variables (see below.).

5. Initialize the database:
   Run the script provided in `db/create_tables.sql` to set up your database schema.

6. Run the application:
   ```
   flask run --host=0.0.0.0 --port=8000
   ```

7. Access the application at `http://localhost:8000`.

### Environment variables
```
    'SECRET_KEY':     create a secret key for your Flask app
    'PHOTODNA_KEY':   PhotoDNA key, obtained from Microsoft
    'x-user':         NCMEC reporting username, obtained from NCMEC
    'x-pwd':          NCMEC reporting password, obtained from NCMEC
    'HIVEAI_KEY':     your Hive AI key, obtained from Hive AI
    'DATABASE_URL':   connection string to a database like neondb
                      eg. postgres://[username]:[password]@[hostname]/[databasename]
    'BASE_URL':       URL of your website where Modtools Image is hosted
    'EMAIL_SENDER':   SMTP email sender 
    'EMAIL_PASSWORD': SMTP email password
```

### Obtaining the required configuration credentials

* The PhotoDNA credentials can be acquired via https://www.microsoft.com/en-us/photodna/cloudservice.
* To receive the NCMEC credentials for automated report functionality, write an email to espteam@ncmec.org to request the registration form.

## Usage

### Web interface

1. **Login/Register**: First, register as a new user or log in with existing credentials through the provided forms.

2. **Dashboard**: Navigate the dashboard to access moderation features, view submitted or escalated images, and manage plugins or APIs.

3. **Actions**: Perform actions like approve, dismiss, or escalate on submitted images based on moderation needs.

4. **Administration** (for admin users): Manage users and invitations, activate or deactivate plugins and APIs.

### API interface

``/upload`` and ``/upload_images`` endpoints are used to upload images that are later going to be processed.

``/upload`` endpoint takes in the following input arguments 
```
        'Email':               email of the user uploading the the image
        'Password':            password of the user uploading the the image
        'image':               base64 image data or in other words the content of the image
        'metadata':            image metadata
            --> metadata fields         'title': image title,
                                        'extension': extension of the image ex. png jpg
        'reportee_name':       reportee_name,
        'reportee_ip_address': reportee_ip_address
        'location': location
            --> location fields
                                "latitude":  latitude of where the image was taken
                                "longitude": lognitude of where the image was taken
                                "altitude":  altitude of where the image was taken
```

``/upload`` endpoint returns the following JSON response:
```
    'status':         status of the request
    'message':        message describing the ouctome of the upload request
    'image_metadata': metadata of the uploaded images
    'image_id':       image_id of the created image on the server
```

``/upload_images`` takes in the following input arguments
```
            "Email":    email of the user uploading the the image
            "Password": password of the user uploading the the image
            "images":   a list of JSON objects
                --> images fields:
                                "image": base64 image data or in other words the content of the image
                                "metadata": metadata
                                    --> metadata fields
                                          "title":      image title,
                                          "extension":  extension of the image ex. png jpg
                                'reportee_name': reportee_name,
                                'reportee_ip_address': reportee_ip_address,
                                'location': location
                                     --> location fields
                                     "latitude":  latitude of where the image was taken
                                     "longitude": lognitude of where the image was taken
                                     "altitude":  altitude of where the image was taken
```

``/upload_images`` endpoint returns the following object:
```
    'images': a list of  JSON response objects used by /upload
```  

The ``/status/<image_id>`` endpoint is used to view tha status of the uploaded image.

``/status`` endpoint returns a JSON with the following fields
```
            "image_url": url of the image 
            "status":    status of the image on the server for example "pending"
            "photodna_results": photo dna result for the image
            "hiveai_results":   hive ai result for the image
```

## Limitations

Modtools Image is currently in the early stages of development. Many features are missing, undocumented, or incomplete. These include:

* Configuration options for the plugins and APIs are not implemented in the web interface.
* The email alerting plugin, intended to send email alerts when a specified scan result is received, has not been implemented.
* Filtering based on the numerical value of HiveAI score has not been implemented.

Further known limitations will be maintained as Issues in Github.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please raise an issue in the repository's issue tracker.
