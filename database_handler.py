import psycopg2
import os
from psycopg2 import pool
from tables import  User,Image,Invitation,API,Plugin
import json
from datetime import datetime

MAX_TRIES = 5

# Create a connection string
conn_string = os.environ["DATABASE_URL"]
# Create an engine
conn = psycopg2.connect(conn_string)
conn_pool = pool.SimpleConnectionPool(1, 20, conn_string)


def handle_connection(func):

  def wrapper(*args, **kwargs):
    conn = None
    cur = None
    tries = 0
    while tries < MAX_TRIES:
      try:
        conn = conn_pool.getconn()
        cur = conn.cursor()
        result = func(*args, **kwargs, conn=conn, cur=cur)
        conn.commit()
        conn_pool.putconn(conn)
        return result
      except (psycopg2.OperationalError, psycopg2.InterfaceError):
        if conn:
          conn_pool.putconn(conn)
        conn = None
        cur = None
        tries += 1
    raise Exception(
      "Failed to establish database connection after multiple attempts")

  return wrapper

@handle_connection
def create_user(name, lastname, email, password, conn, cur, role='moderator'):
    try:
        # Check if the "users" table is empty
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]

        if user_count == 0:
            # If the table is empty, set the role to 'admin'
            role = 'admin'

        # Insert the new user into the "users" table
        cur.execute(
            "INSERT INTO users (name, lastname, email, password, role) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (name, lastname, email, password, role)
        )
        
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except psycopg2.errors.UniqueViolation as e:
        print(f"Error: {e}")
        return None


@handle_connection
def delete_user(user_id, conn, cur):
    cur.execute("DELETE FROM invitation WHERE inviter_user_id = %s", (user_id,))
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

@handle_connection
def get_user_by_email(email, conn, cur):
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_data = cur.fetchone()
    if user_data:
        return User(*user_data)
    else:
        return None

@handle_connection
def get_admin_user(conn, cur):
    cur.execute("SELECT * FROM users WHERE role = 'admin'")
    admin_user_data = cur.fetchone()
    if admin_user_data:
        return User(*admin_user_data)
    else:
        return None


@handle_connection
def get_user_by_id(user_id, conn, cur):
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
        return User(*user_data)
    else:
        return None

@handle_connection
def get_all_users(conn, cur):
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    if rows:
        return [User(*row) for row in rows]
    else:
        return []

@handle_connection
def update_user(user_id, name, lastname, email, password, conn, cur):
    cur.execute(
        "UPDATE users SET name = %s, lastname = %s, email = %s, password = %s WHERE id = %s",
        (name, lastname, email, password, user_id)
    )
    conn.commit()


@handle_connection
def promote_user(user_id, conn, cur):
    try:
        cur.execute(
            "UPDATE users SET role = 'admin' WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@handle_connection
def degrade_user(user_id, conn, cur):
    try:
        cur.execute(
            "UPDATE users SET role = 'moderator' WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@handle_connection
def drop_users_table(conn, cur):
  cur.execute("DROP TABLE IF EXISTS users")
  conn.commit()

#====================================

@handle_connection
def create_image(user_id, image_url, scan_results, status,
                 incident_time, reportee_name, reportee_ip_address, username, location,
                 conn, cur):
    try:
        cur.execute(
            "INSERT INTO images (user_id, image_url, scan_results, "
            "status, incident_time, reportee_name, reportee_ip_address, username, "
            "latitude, longitude, altitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (user_id, image_url, scan_results,
             status, incident_time, reportee_name, reportee_ip_address, username, 
             location.get("latitude", ""), location.get("longitude", ""),
             location.get("altitude", ""))
        )
        image_id = cur.fetchone()[0]
        conn.commit()
        return image_id
    except psycopg2.errors.UniqueViolation as e:
        print(f"Error: {e}")
        return None

@handle_connection
def delete_image(image_id, conn, cur):
    cur.execute("DELETE FROM images WHERE id = %s", (image_id,))
    conn.commit()

@handle_connection
def get_image_by_id(image_id, conn, cur):
    cur.execute("SELECT * FROM images WHERE id = %s", (image_id,))
    image_data = cur.fetchone()
    if image_data:
        return Image(*image_data)
    else:
        return None

@handle_connection
def get_pending_images(conn, cur):
    cur.execute("SELECT * FROM images WHERE status = 'pending'")
    image_data = cur.fetchall()
    if image_data:
        image_list = [Image(*row) for row in image_data]
        return image_list
    else:
        return None

@handle_connection
def get_escalated_images(conn, cur):
          cur.execute("SELECT * FROM images WHERE status = 'Escalate'")
          image_data = cur.fetchall()
          if image_data:
              image_list = [Image(*row) for row in image_data]
              return image_list
          else:
              return None

@handle_connection
def get_all_images(conn, cur):
    cur.execute("SELECT * FROM images")
    rows = cur.fetchall()
    if rows:
        return [Image(*row) for row in rows]
    else:
        return []

@handle_connection
def get_unscanned_images(conn, cur):
    cur.execute("SELECT * FROM images WHERE scan_results= 'none'")
    rows = cur.fetchall()
    if rows:
        return [Image(*row) for row in rows]
    else:
        return []



@handle_connection
def update_image(image_id, user_id, image_url, scan_results, status,
                 incident_time, reportee_name, reportee_ip_address, username, location,
                 conn, cur):
    cur.execute(
        "UPDATE images SET user_id = %s, image_url = %s, "
        "scan_results = %s, status = %s, updated_at = CURRENT_TIMESTAMP, "
        "incident_time = %s, reportee_name = %s, reportee_ip_address = %s, username = %s, "
        "latitude = %s, longitude = %s, altitude = %s "
        "WHERE id = %s",
        (user_id, image_url, scan_results,
         status, incident_time, reportee_name, reportee_ip_address, username, 
         location.get("latitude", ""), location.get("longitude", ""),
         location.get("altitude", ""), image_id)
    )
    conn.commit()

@handle_connection
def update_image_status(image_id, status, conn, cur):
    cur.execute(
        "UPDATE images SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (status, image_id)
    )
    conn.commit()

@handle_connection
def update_image_scan_results(image_id,scan_results, conn, cur):
    scan_results_json = json.dumps(scan_results)
    cur.execute(
        "UPDATE images SET scan_results = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (scan_results_json,image_id)
    )
    conn.commit()

@handle_connection
def get_filtered_images(username=None, date=None, result=False, escalated=None, conn=None, cur=None):
    # Build the WHERE clause based on the provided filters
    where_conditions = []

    if username:
        where_conditions.append(f"username = '{username}'")

    if date:
        try:
            # Attempt to parse the date in 'dd/mm/yyyy' format
            date_obj = datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            # If parsing fails, try 'yyyy-mm-dd' format
            date_obj = datetime.strptime(date, '%Y-%m-%d')

        formatted_date = date_obj.strftime('%Y-%m-%d')
        where_conditions.append(f"created_at::date = '{formatted_date}'::date")

    if escalated:
        where_conditions.append("status = 'escalated'")

    if result:
        where_conditions.append("scan_results <> ''")

    # Construct the final SQL query
    sql_query = """
        SELECT * FROM images
        WHERE {}
    """.format(" AND ".join(where_conditions)) if where_conditions else "SELECT * FROM images"
    # Execute the query and retrieve the filtered images
    cur.execute(sql_query)
    filtered_images = [Image(*row) for row in cur.fetchall()]
    if result:
        filtered_images1 = []
        for image in filtered_images:
            if(len(image.scan_results) > 0 and image.scan_results != '""'):
                filtered_images1.append(image)
    return filtered_images1

#====================================

@handle_connection
def create_invitation(invitee_email, inviter_user_id, conn, cur):
    try:
        cur.execute(
            "INSERT INTO invitation (invitee_email, inviter_user_id) VALUES (%s, %s) RETURNING id",
            (invitee_email, inviter_user_id)
        )
        invitation_id = cur.fetchone()[0]
        conn.commit()
        return invitation_id
    except psycopg2.errors.UniqueViolation as e:
        print(f"Error: {e}")
        return None

@handle_connection
def delete_invitation(invitation_id, conn, cur):
    cur.execute("DELETE FROM invitation WHERE id = %s", (invitation_id,))
    conn.commit()

@handle_connection
def get_invitation_by_id(invitation_id, conn, cur):
    cur.execute("SELECT * FROM invitation WHERE id = %s", (invitation_id,))
    invitation_data = cur.fetchone()
    if invitation_data:
        return Invitation(*invitation_data)
    else:
        return None

@handle_connection
def get_invitation_by_email(invitee_email, conn, cur):
    cur.execute("SELECT * FROM invitation WHERE invitee_email = %s", (invitee_email,))
    invitation_data = cur.fetchone()
    if invitation_data:
        return Invitation(*invitation_data)
    else:
        return None

@handle_connection
def get_all_invitations(conn, cur):
    cur.execute("SELECT * FROM invitation")
    rows = cur.fetchall()
    if rows:
        return [Invitation(*row) for row in rows]
    else:
        return []

@handle_connection
def update_invitation(invitation_id, invitee_email, inviter_user_id, conn, cur):
    cur.execute(
        "UPDATE invitation SET invitee_email = %s, inviter_user_id = %s WHERE id = %s",
        (invitee_email, inviter_user_id, invitation_id)
    )
    conn.commit()

#===================================

@handle_connection
def create_api(name, about, is_registered=True, conn=None, cur=None):
    cur.execute(
        "INSERT INTO apis (name,about ,is_registered) VALUES (%s, %s, %s) RETURNING id",
        (name, about, is_registered)
    )
    api_id = cur.fetchone()[0]
    conn.commit()
    return api_id

@handle_connection
def delete_api(api_id, conn=None, cur=None):
    cur.execute("DELETE FROM apis WHERE id = %s", (api_id,))
    conn.commit()

@handle_connection
def get_api_by_id(api_id, conn=None, cur=None):
    cur.execute("SELECT * FROM apis WHERE id = %s", (api_id,))
    api_data = cur.fetchone()
    if api_data:
        return API(*api_data)
    else:
        return None

@handle_connection
def get_all_apis(conn=None, cur=None):
    cur.execute("SELECT * FROM apis")
    rows = cur.fetchall()
    if rows:
        return [API(*row) for row in rows]
    else:
        return []

@handle_connection
def update_api(api_id, name, is_registered, conn=None, cur=None):
    cur.execute(
        "UPDATE apis SET name = %s, is_registered = %s WHERE id = %s",
        (name, is_registered, api_id)
    )
    conn.commit()

@handle_connection
def update_api_status(api_id, is_registered, conn=None, cur=None):
    cur.execute(
        "UPDATE apis SET  is_registered = %s WHERE id = %s",
        ( is_registered, api_id)
    )
    conn.commit()

#=================== Plugin

@handle_connection
def create_plugin(name, about, action_id, is_registered=True, conn=None, cur=None):
    cur.execute(
        "INSERT INTO plugins (name, about, is_registered, action_id) VALUES (%s, %s, %s, %s) RETURNING id",
        (name, about, is_registered, action_id)
    )
    plugin_id = cur.fetchone()[0]
    conn.commit()
    return plugin_id

@handle_connection
def delete_plugin(plugin_id, conn=None, cur=None):
    cur.execute("DELETE FROM plugins WHERE id = %s", (plugin_id,))
    conn.commit()

@handle_connection
def get_plugin_by_id(plugin_id, conn=None, cur=None):
    cur.execute("SELECT * FROM plugins WHERE id = %s", (plugin_id,))
    plugin_data = cur.fetchone()
    if plugin_data:
        return Plugin(*plugin_data)
    else:
        return None

@handle_connection
def get_all_plugins(conn=None, cur=None):
    cur.execute("SELECT * FROM plugins")
    rows = cur.fetchall()
    if rows:
        return [Plugin(*row) for row in rows]
    else:
        return []

@handle_connection
def update_plugin(plugin_id, name, is_registered, action_id, conn=None, cur=None):
    cur.execute(
        "UPDATE plugins SET name = %s, is_registered = %s, action_id = %s WHERE id = %s",
        (name, is_registered, action_id, plugin_id)
    )
    conn.commit()

@handle_connection
def update_plugin_status(plugin_id, is_registered, conn=None, cur=None):
    cur.execute(
        "UPDATE plugins SET is_registered = %s WHERE id = %s",
        ( is_registered, plugin_id)
    )
    conn.commit()

@handle_connection
def bla(conn=None, cur=None):
    cur.execute(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'images';"
    )
    columns = cur.fetchall()
    print(columns)
    conn.commit()

@handle_connection
def add_columns_to_images(conn=None, cur=None):
    # Add new columns to the images table
    cur.execute(
        """
        ALTER TABLE images
        ADD COLUMN "incident_time" timestamp,
        ADD COLUMN "reportee_name" varchar(255),
        ADD COLUMN "reportee_ip_address" varchar(16),
        ADD COLUMN "username" varchar(50),
        ADD COLUMN "latitude" varchar(50),
        ADD COLUMN "longitude" varchar(50),
        ADD COLUMN "altitude" varchar(50);
        """
    )
    conn.commit()

@handle_connection
def remove_columns_from_images(conn=None, cur=None):
    cur.execute(
        """
        ALTER TABLE images
        DROP COLUMN "metadata";
        """
    )
    conn.commit()

# remove_columns_from_images()
# add_columns_to_images()
# bla()


def test_image_operations():
    # Replace the following with your own test data
    test_user_id = 1
    test_image_url = "example.com/image.jpg"
    test_metadata = {"key": "value"}
    test_scan_results = {"result": "clean"}
    test_status = "pending"

    # Test create_image function
    image_id = create_image(test_user_id, test_image_url, test_metadata, test_scan_results, test_status)
    assert image_id is not None

    # Test get_image_by_id function
    image = get_image_by_id(image_id)
    assert image is not None
    assert image.user_id == test_user_id
    assert image.image_url == test_image_url
    assert image.metadata == test_metadata
    assert image.scan_results == test_scan_results
    assert image.status == test_status

    # Test update_image function
    updated_user_id = 2
    updated_image_url = "example.com/updated.jpg"
    updated_metadata = {"key": "updated_value"}
    updated_scan_results = {"result": "updated_clean"}
    updated_status = "approved"
    update_image(image_id, updated_user_id, updated_image_url, updated_metadata, updated_scan_results, updated_status)
    
    updated_image = get_image_by_id(image_id)
    assert updated_image is not None
    assert updated_image.user_id == updated_user_id
    assert updated_image.image_url == updated_image_url
    assert updated_image.metadata == updated_metadata
    assert updated_image.scan_results == updated_scan_results
    assert updated_image.status == updated_status

    # Test get_all_images function
    all_images = get_all_images()
    assert len(all_images) > 0

    # Test delete_image function
    delete_image(image_id)
    deleted_image = get_image_by_id(image_id)
    assert deleted_image is None

def test_invitation_crud_methods():
    # Create an invitation
    invitation_id = create_invitation("invitee@example.com", 4)
    assert invitation_id is not None

    # Get the created invitation by ID
    created_invitation = get_invitation_by_id(invitation_id)
    assert created_invitation is not None
    assert created_invitation.invitee_email == "invitee@example.com"
    assert created_invitation.inviter_user_id == 4

    # Update the invitation
    update_invitation(invitation_id, "updated@example.com", 4)
    updated_invitation = get_invitation_by_id(invitation_id)
    assert updated_invitation.invitee_email == "updated@example.com"
    assert updated_invitation.inviter_user_id == 4

    # Get all invitations
    all_invitations = get_all_invitations()
    assert len(all_invitations) >= 1

    # Delete the invitation
    delete_invitation(invitation_id)
    deleted_invitation = get_invitation_by_id(invitation_id)
    assert deleted_invitation is None

            
def test_api_functions():
    # Test create_api
    api_id = create_api("Test API", "This is a test API", True)
    assert isinstance(api_id, int)

    # Test get_api_by_id
    api = get_api_by_id(api_id)
    assert isinstance(api, API)
    assert api.name == "Test API"
    assert api.about == "This is a test API"
    assert api.is_registered == True

    # Test update_api
    update_api(api_id, "Updated API", False)
    updated_api = get_api_by_id(api_id)
    assert updated_api.name == "Updated API"
    assert updated_api.is_registered == False

    # Test update_api_status
    update_api_status(api_id, True)
    updated_status_api = get_api_by_id(api_id)
    assert updated_status_api.is_registered == True

    # Test get_all_apis
    apis = get_all_apis()
    assert len(apis) >= 1
    assert isinstance(apis[0], API)

    # Test delete_api
    delete_api(api_id)
    deleted_api = get_api_by_id(api_id)
    assert deleted_api is None

def test_plugin_functions():
    # Test create_plugin
    plugin_id = create_plugin("Test Plugin", "This is a test plugin", True)
    assert isinstance(plugin_id, int)

    # Test get_plugin_by_id
    plugin = get_plugin_by_id(plugin_id)
    assert isinstance(plugin, Plugin)
    assert plugin.name == "Test Plugin"
    assert plugin.about == "This is a test plugin"
    assert plugin.is_registered == True

    # Test update_plugin
    update_plugin(plugin_id, "Updated Plugin", False)
    updated_plugin = get_plugin_by_id(plugin_id)
    assert updated_plugin.name == "Updated Plugin"
    assert updated_plugin.is_registered == False

    # Test update_plugin_status
    update_plugin_status(plugin_id, True)
    updated_status_plugin = get_plugin_by_id(plugin_id)
    assert updated_status_plugin.is_registered == True

    # Test get_all_plugins
    plugins = get_all_plugins()
    assert len(plugins) >= 1
    assert isinstance(plugins[0], Plugin)

    # Test delete_plugin
    delete_plugin(plugin_id)
    deleted_plugin = get_plugin_by_id(plugin_id)
    assert deleted_plugin is None