from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required,current_user, logout_user
import base64
import os
from dotenv import load_dotenv
load_dotenv()
import re
import database_handler as db_handler
import notify as email_service
from photo_scan import initialize_photo_scan_app
from actions import get_action_manager

photo_path = "photo.jpg"
photo_scan_app=initialize_photo_scan_app()

# Setting up Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

# User Authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
# Initializing action manager
action_manager = None


def is_valid_email(email):
    # Regular expression pattern for a more comprehensive email validation
    pattern = r'^[\w\.-]+(\+[\w\.-]+)*@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


@login_manager.user_loader
def load_user(user_id):
  global action_manager
  user = db_handler.get_user_by_id(user_id)
  if(user):
    action_manager = get_action_manager(reporter_name=user.name, reporter_email=user.email)
  return user


# Index Route
@app.route('/')
@app.route('/index')
def index():
  return render_template("home.html")


def show_dashboard(escalated=False):
  plugins=db_handler.get_all_plugins()
  images=db_handler.get_pending_images()
  if images:
    if escalated: 
      images=db_handler.get_escalated_images()
      images=[image.to_dict() for image in images]
      dashboard_name="Escalated images"
    else:  
      images=[image.to_dict() for image in images]
      dashboard_name="Submitted images"
  else:
    images = []
  return render_template('dashboard.html',images=images,dashboard_name=dashboard_name, plugins=plugins, action_manager=action_manager)

@app.route('/dashboard')
@login_required
def dashbboard():
    return show_dashboard()

@app.route('/filter_images', methods=['POST'])
@login_required
def filter_images():
    # Retrieve filter data from the request
    username = request.form.get('username')
    date = request.form.get('date')
    result = request.form.get('result') == 'true'
    escalated = request.form.get('escalated') == 'true'
    # Call the function to get filtered images
    filtered_images = db_handler.get_filtered_images(username, date, result, escalated)
    images = [image.to_dict() for image in filtered_images]
    return jsonify({'images': images})

@app.route('/perform_actions', methods=['POST'])
@login_required
def perform_actions():
    actions=[]
    selected_actions = request.json.get('selected_actions', [])
    for action in selected_actions:
      action_type, number = re.match(r'([a-zA-Z_]+)_(\d+)', action).groups()
      actions.append(action_type)
    image = db_handler.get_image_by_id(int(number))
    # Iterate through selected actions and perform the desired action
    for action_id in actions:
        action_manager.perform_action(action_id, image)
    return jsonify({'success': True}), 200, {'Content-Type': 'application/json'}


@app.route('/submitted_images')
@login_required
def submitted_images():
  return redirect("/dashboard")


@app.route('/escalated_images')
@login_required
def escalated_images():
  return show_dashboard(escalated=True)
  
@app.route('/plugins')
@login_required
def plugins():
  plugins=db_handler.get_all_plugins()
  active_plugins = [plugin for plugin in plugins if plugin.is_registered==True]
  inactive_plugins = [plugin for plugin in plugins if plugin.is_registered==False]
  active_plugins=[plugin.to_dict() for plugin in active_plugins ]
  return render_template('plugins.html',active_plugins=active_plugins,inactive_plugins=inactive_plugins)

@app.route('/apis')
@login_required
def apis():
  apis=db_handler.get_all_apis()
  active_apis = [api for api in apis if api.is_registered==True]
  inactive_apis = [api for api in apis if api.is_registered==False]
  active_apis=[api.to_dict() for api in active_apis ]
  return render_template('apis.html',active_apis=active_apis,inactive_apis=inactive_apis)

@app.route('/dismiss', methods=['POST'])
def dismiss_image():
    image_id = request.form.get('image_id')
    status="Dismissed"
    response_data = {
        "success": True,
        "message": "Image dismissed successfully"
    }
    db_handler.update_image_status(image_id, status)
    return jsonify(response_data)

@app.route('/approve', methods=['POST'])
def approve_image():
    image_id = request.form.get('image_id')
    status="Approved"
    response_data = {
        "success": True,
        "message": "Image approved successfully"
    }
    db_handler.update_image_status(image_id, status)    
    return jsonify(response_data)

@app.route('/escalate', methods=['POST'])
def escalate_image():
    image_id = request.form.get('image_id')
    status="Escalate"
    response_data = {
        "success": True,
        "message": "Image escalated successfully"
    }
    db_handler.update_image_status(image_id, status)    
    return jsonify(response_data)


@app.route('/invite', methods=['POST'])
@login_required
def invite():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if is_valid_email(email):
           invitation_status="invitation sent successfully!"
           invitation_id=db_handler.create_invitation(email, current_user.id)
           email_service.welcome_new_user(email)
        else:
           invitation_status="email submitted invalid!"
          
        users=db_handler.get_all_users()
        
        users=[user.to_dict() for user in users]
        return render_template('manage_users.html',
                               users=users,
                               invitation_status=invitation_status)
    
    return "Invalid request method" 

@app.route('/activate_api/<id>')
@login_required
def activate_api(id):
  db_handler.update_api_status(id,"TRUE") 
  return redirect("/apis")

@app.route('/delete_api/<id>')
@login_required
def delete_api(id):
  db_handler.update_api_status(id,"FALSE") 
  return redirect("/apis")

@app.route('/activate_plugin/<id>')
@login_required
def activate_plugin(id):
  db_handler.update_plugin_status(plugin_id=id, is_registered=True) 
  return redirect("/plugins")

@app.route('/delete_plugin/<id>')
@login_required
def delete_plugins(id):
  db_handler.update_plugin_status(plugin_id=id, is_registered=False)
  return redirect("/plugins")

@app.route('/kick/<user_id>')
@login_required
def kick(user_id):
  db_handler.delete_user(user_id) 
  users=db_handler.get_all_users()
  users=[user.to_dict() for user in users]
  return render_template('manage_users.html',users=users)

@app.route('/promote/<user_id>')
@login_required
def promote(user_id):
  db_handler.promote_user(user_id) 
  users=db_handler.get_all_users()
  users=[user.to_dict() for user in users]
  return render_template('manage_users.html',users=users)

@app.route('/degrade/<user_id>')
@login_required
def degrade(user_id):
  db_handler.degrade_user(user_id) 
  users=db_handler.get_all_users()
  users=[user.to_dict() for user in users]
  return render_template('manage_users.html',users=users)
  
@app.route('/manage_users')
@login_required
def manage_users():
  users=db_handler.get_all_users()
  users=[user.to_dict() for user in users]
  return render_template('manage_users.html',users=users)


def token_valid(token):
  if token != "123454676868":
    return False
  return True

@app.route('/scan')
@login_required
def scan():
   images=db_handler.get_unscanned_images()
   for image in images:
         analysis_results=photo_scan_app.scan_photo("http://127.0.0.1:7000/static/img/"+image.image_url)
         print(analysis_results)
         #TODO neka logika da se upakuje u novi zapis
         result_string=""
         for result in analysis_results:
          if result[0]==True:
            result_string+=result[1]+", " 
         scan_results=str(result_string.strip(", "))
         db_handler.update_image_scan_results(image.id,scan_results)
   return redirect("dashboard")

@app.route('/status/<image_id>', methods=["GET"])
def get_image_status(image_id):
    image = db_handler.get_image_by_id(image_id)
    if image:
        return jsonify({
            "image_url": image.image_url,
            "status": image.status,
            "scan_result": image.scan_results
        }),200
    else:
        return jsonify({"message": "No image with that id found."}), 404
      
@app.route('/upload', methods=['GET', 'POST'])
def upload():
  try:
    access_token = request.headers.get('Authorization')
    if not access_token:
      return jsonify({
        'status': 'error',
        'message': 'Access token missing'
      }), 401

    if not token_valid(access_token):
      return jsonify({
        'status': 'error',
        'message': 'Access token invalid'
      }), 401
    user_id = 1
    scan_results = {"result": "none"}
    status = "pending"
    data = request.get_json()
    base64_image_data = data.get("image")
    metadata = data.get('metadata')
    
    if base64_image_data and metadata:
      image_data = base64.b64decode(base64_image_data)
      file_extension = metadata.get("extension", "jpg")
      file_name = f"{metadata['title'].replace(' ', '_')}.{file_extension}"
      image_path = os.path.join("", file_name)
      
      with open(image_path, "wb") as image_file:
        image_file.write(image_data)
        
        image_id = db_handler.create_image(user_id, image_path, metadata,
                                           scan_results, status)

    response = {
      'status': 'success',
      'message': 'Image and metadata received',
      'image_metadata': metadata,
      'image_id':image_id
    }
    return jsonify(response), 200

  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 400


@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
  return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  return render_template('register.html')


@app.route('/forgot_password')
def forgot_password():
  return render_template('forgot_password.html')


@app.route('/logout_user', methods=['GET', 'POST'])
@login_required
def logout_users():
  logout_user()
  user_name = ""
  session['user_name'] = user_name
  return redirect('/login')


@app.route('/login_user', methods=['GET', 'POST'])
def login_users():
  if request.method == 'POST':
    email = request.form.get('exampleInputEmail')
    password = request.form.get('exampleInputPassword')
    user = db_handler.get_user_by_email(email)
    if (user and bcrypt.check_password_hash(user.password, password)):
      login_user(user)
      user_name = f"{user.name} {user.lastname}"
      session['user_name'] = user_name
      return redirect('/dashboard')
    elif (not user):
      flash("No acount with this email registred! Please Sign Up!", "error")
      return redirect('/login')
    else:
      flash("Wrong password! Please try again!", "error")
      return redirect('/login')

  return render_template('login.html')


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
  if request.method == 'POST':
    # Get form data
    name = request.form.get('exampleFirstName')
    lastname = request.form.get('exampleLastName')
    email = request.form.get('exampleInputEmail')
    if not db_handler.get_invitation_by_email(email):
      if len(db_handler.get_all_users())!=0:
        flash("Email is not invited, please ask for invite first.",
            "error")
        return redirect('/register')
    password = request.form.get('exampleInputPassword')
    repeat_password = request.form.get('exampleRepeatPassword')
    # Check if password and repeat_password match
    if password != repeat_password:
      flash("Password and Repeat Password do not match. Please try again.",
            "error")
      return redirect('/register')
    # Check if email is already registered
    if db_handler.get_user_by_email(email):
      flash("Email already registered. Please use a different email.", "error")
      return redirect('/register')
    # Hash the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Add new user to the database
    db_handler.create_user(name, lastname, email, hashed_password)

    return redirect('/login')

  return render_template('register.html')

# db_handler.add_column()

# Custom filter function
def add_strong_tag(text):
  # Use regular expression to match any text before ":" until a new line character
  # Not perfect because sometimes bot can make statements with ":"
  formatted_text = re.sub(r'([^:\n]+:)', r'<br><strong>\1</strong>', text)
  return formatted_text


# Add the filter to Jinja2 environment
app.jinja_env.filters['add_strong_tag'] = add_strong_tag

@app.route('/update_or_create_image', methods=['POST'])
def update_or_create_image():
    try:
        data = request.json
        image_id = data.get('image_id')
        user_id = data.get('user_id')
        image_url = data.get('image_url')
        scan_results = data.get('scan_results')
        status = data.get('status')
        incident_time = data.get('incident_time')
        reportee_name = data.get('reportee_name')
        reportee_ip_address = data.get('reportee_ip_address')
        username = data.get('username')
        location = data.get('location')

        if image_id:
            # If image_id is provided, update the existing image
            db_handler.update_image(image_id, user_id, image_url,
                          scan_results, status, incident_time,
                          reportee_name, reportee_ip_address,username, location)
        else:
            # If no image_id is provided, create a new image
            db_handler.create_image(user_id, image_url,
                                         scan_results, status, incident_time,
                                         reportee_name, reportee_ip_address,username,  location)

        return jsonify({'success': True, 'image_id': image_id})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Run the Flask app
if __name__ == '__main__':
  #from waitress import serve
  app.run(host="0.0.0.0", port=7000)
