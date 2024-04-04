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

``SECRET_KEY``
    Create a secret key for your Flask app  
``PHOTODNA_KEY``
    PhotoDNA key, obtained from Microsoft  
``x-user``
    NCMEC reporting username, obtained from NCMEC  
``x-pwd``
    NCMEC reporting password, obtained from NCMEC  
``HIVEAI_KEY``
    Your Hive AI key, obtained from Hive AI  
``DATABASE_URL``
    Connection string to a database like neondb  
``BASE_URL``
    URL of your website where Modtools Image is hosted  
``EMAIL_SENDER``
    SMTP email sender  
``EMAIL_PASSWORD``
    SMTP email password  

## Usage

1. **Login/Register**: First, register as a new user or log in with existing credentials through the provided forms.

2. **Dashboard**: Navigate the dashboard to access moderation features, view submitted or escalated images, and manage plugins or APIs.

3. **Actions**: Perform actions like approve, dismiss, or escalate on submitted images based on moderation needs.

4. **Administration** (for admin users): Manage users and invitations, activate or deactivate plugins and APIs.

## Limitations

Modtools Image is currently in the early stages of development. Many features are missing, undocumented, or incomplete. These include:

* Configuration options for the plugins and APIs are not implemented in the web interface.
* The JSON API for submitting images and querying their status is undocumented.
* The email alerting plugin, intended to send email alerts when a specified scan result is received, has not been implemented.
* Filtering based on the numerical value of HiveAI score has not been implemented.

Further known limitations will be maintained as Issues in Github.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please raise an issue in the repository's issue tracker.


## API for submitting images, reading their status and making a report action

## About the HiveAI API JSON object
    The object returned by the HiveAI API represents the analysis result of a photo. It contains information about the status of the analysis and the output of the analysis. The response field contains an array of analysis results for each image provided. Each analysis result contains information about the classes detected in the image and the corresponding scores.

    The check_for_bad_classes function in the HiveAI_Plugin class checks for harmful classes in the analysis results. It compares the detected classes with a predefined list of harmful classes and a threshold score. If any harmful classes are found with a score equal to or higher than the threshold, the function returns True and the list of harmful classes. Otherwise, it returns False and None.

    Example of content HiveAI based filter check for are:
                "yes_nsfw",
                "yes_suggestive",
                "yes_female_underwear",
                "yes_male_underwear",
                "yes_sex_toy",
                "yes_female_nudity",
                "yes_male_nudity",
                "yes_female_swimwear",
                "yes_male_shirtless",
                "yes_gun_in_hand",
                "yes_culinary_knife_in_hand",
                "yes_knife_in_hand",
                "yes_pills",
                "yes_smoking",

## About the PhotoDNA scan API JSON object

    The analyze_photo function in the PhotoDNA_Plugin class performs the API request to the PhotoDNA service. It uses the provided image URL to request a matching analysis. The returned JSON response is then checked to determine if a match was found. If a match is found (if scan_result["IsMatch"]), the function returns a dictionary object indicating the plugin name (PhotoDNA) and that a match was found. If no match is found, it returns a dictionary object indicating the plugin name and that no match was found.

    The initialize_photo_scan_app function initializes the PhotoScanApp class and registers the HiveAI_Plugin and PhotoDNA_Plugin instances as plugins. It returns the initialized PhotoScanApp object.

## About the PhotoDNA report action API JSON object
    The PhotoDNA_report_action class is an action class specifically for reporting violations using the PhotoDNA service. It requires a reporter name and email address for initialization. The perform_action method takes image data as input. It reads the image file specified by the image URL, encodes it in base64 format, and sends a request to the PhotoDNA service to report the violation. The request includes various metadata such as the reporter's information, incident time, reportee information, and violation content.
        "OrgName":Organization submitting the image
        "ReporterName": Name of the reporter of the image
        "ReporterEmail": Email of the reporter
        "IncidentTime": Time the image was submitted 
        "ReporteeName": Name of the person being reported
        "ReporteeIPAddress":IP adress of the person being reported
        "ViolationContentCollection": [
                    {
                    "Name":Name of the image being submitted
                    "Value":base64 encoded value of the image being submitted
                    "Location":{ 
                                 "Latitude":Latitude of where the image was taken,
                                 "Longitude":Longitude of where the image was taken,
                                 "Altitude": Alittude of where the image was taken },
                    "UploadIpAddress": IP adress of where the image was uploaded,
                    "UploadDateTime": Date and time image was uploaded,
                    }
                    ],

    Headers of this request hold following key values obtained at :
            "Ocp-Apim-Subscription-Key": PhotoDNA api key
            "x-user": username on the PhotoDNA platform
            "x-pwd":  password on the PhotoDNA platform
    
    The get_server_ip in actions.py function retrieves the IP address of the server where the code is running by obtaining the hostname and resolving it to the IP address.
