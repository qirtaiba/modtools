import psycopg2
import psycopg2.extras
import os
from psycopg2 import pool
from tables import  User,Image,Invitation,API,Plugin
import json
from datetime import datetime
from dotenv import load_dotenv
import time
load_dotenv()

MAX_TRIES = 5
conn_string = os.environ["DATABASE_URL"]
conn = psycopg2.connect(conn_string)
conn_pool = psycopg2.pool.SimpleConnectionPool(1, 50, conn_string)


def handle_connection(func):
    def wrapper(*args, **kwargs):
        conn = None
        cur = None
        tries = 0
        while tries < MAX_TRIES:
            try:
                conn = conn_pool.getconn()
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                result = func(*args, **kwargs, conn=conn, cur=cur)
                # Keep the connection alive by executing a SELECT 1 query
                cur.execute("SELECT 1;")
                conn.commit()
                conn_pool.putconn(conn)
                return result
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                if conn:
                    conn_pool.putconn(conn, close=True)
                conn = None
                cur = None
                
                # Reconnect to the database, wait for a while, and retry
                time.sleep(1)
                
                tries += 1

        raise Exception("Failed to establish database connection after multiple attempts")
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
        return [User(**row) for row in rows]
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

@handle_connection
def read_table_columns(conn, cur):
    cur.execute("SELECT column_name \
                 FROM information_schema.columns \
                 WHERE table_schema = 'public' \
                 AND table_name = 'images';")
    result = cur.fetchall()  # Fetch all rows
    for row in result:
        print(row)
    conn.commit()

#====================================
@handle_connection
def create_image(user_id, image_url, status,
                 incident_time, reportee_name, reportee_ip_address, username, location,
                 conn, cur):
    try:
        photodna_results = None
        hiveai_results = None
        cur.execute(
            "INSERT INTO images (user_id, image_url, photodna_results, hiveai_results, "
            "status, incident_time, reportee_name, reportee_ip_address, username, "
            "latitude, longitude, altitude, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP) RETURNING id",
            (user_id, image_url, photodna_results, hiveai_results,
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
        return Image(**image_data)
    else:
        return None

@handle_connection
def get_pending_images(conn, cur):
    cur.execute("SELECT * FROM images WHERE status = 'pending'")
    image_data = cur.fetchall()
    if image_data:

        image_list = [Image(**row) for row in image_data]
        return image_list
    else:
        return None

@handle_connection
def get_escalated_images(conn, cur):
    cur.execute("SELECT * FROM images WHERE status = 'Escalate'")
    image_data = cur.fetchall()
    if image_data:
        image_list = [Image(**row) for row in image_data]
        return image_list
    else:
        return None

@handle_connection
def alter_images(conn, cur):
    cur.execute("ALTER TABLE images\
                 ADD COLUMN user_id INTEGER DEFAULT NULL;")
    conn.commit()  # Commit the changes to the database
    print("Column 'user_id' added successfully.")

@handle_connection
def get_all_images(conn, cur):
    cur.execute("SELECT * FROM images")
    rows = cur.fetchall()
    if rows:
        return [Image(**row) for row in rows]
    else:
        return []

@handle_connection
def get_unscanned_images(conn, cur):
    cur.execute("SELECT * FROM images WHERE scan_results= 'none'")
    rows = cur.fetchall()
    if rows:
        return [Image(**row) for row in rows]
    else:
        return []



@handle_connection
def update_image(image_id, user_id, image_url, photodna_results, hiveai_results, status,
                 incident_time, reportee_name, reportee_ip_address, username, location,
                 conn, cur):
    cur.execute(
        "UPDATE images SET user_id = %s, image_url = %s, "
        "photodna_results = %s, hiveai_results = %s, status = %s, updated_at = CURRENT_TIMESTAMP, "
        "incident_time = %s, reportee_name = %s, reportee_ip_address = %s, username = %s, "
        "latitude = %s, longitude = %s, altitude = %s "
        "WHERE id = %s",
        (user_id, image_url, photodna_results, hiveai_results,
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
def update_image_hiveai_scan_results(image_id,scan_results, conn, cur):
    scan_results_json = json.dumps(scan_results)
    cur.execute(
        "UPDATE images SET hiveai_results = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (scan_results_json,image_id)
    )
    conn.commit()

@handle_connection
def update_image_photodna_scan_results(image_id,scan_results, conn, cur):
    scan_results_json = json.dumps(scan_results)
    cur.execute(
        "UPDATE images SET photodna_results = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (scan_results_json,image_id)
    )
    conn.commit()

@handle_connection
def get_filtered_images(username=None, date=None, photodna_results=False, hiveai_results=False, escalated=None, conn=None, cur=None):
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

    if photodna_results:
        where_conditions.append("photodna_results <> ''")

    if hiveai_results:
        where_conditions.append("hiveai_results <> ''")

    # Construct the final SQL query
    sql_query = """
        SELECT * FROM images
        WHERE {}
    """.format(" AND ".join(where_conditions)) if where_conditions else "SELECT * FROM images"
    # Execute the query and retrieve the filtered images
    cur.execute(sql_query)
    filtered_images = [Image(**row) for row in cur.fetchall()]
    # if result:
    #     filtered_images1 = []
    #     for image in filtered_images:
    #         if(len(image.scan_results) > 0 and image.scan_results != '""'):
    #             filtered_images1.append(image)
    return filtered_images

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
        return [Invitation(**row) for row in rows]
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
        return [API(**row) for row in rows]
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
        return [Plugin(**row) for row in rows]
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
def update_images_table_structure(conn=None, cur=None):
    # Remove the scan_results column (if exists) and add new columns for photodna_results and hiveai_results
    cur.execute(
        """
        ALTER TABLE images
        DROP COLUMN "hiveai_result";
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

@handle_connection
def test(image_id, conn=None, cur=None):
    hiveai_result = 'Positive'
    photodna_result = 'MatchFound'

    cur.execute("UPDATE images SET hiveai_results = %s, photodna_results = %s WHERE id = %s",
                (hiveai_result, photodna_result, image_id))
    conn.commit()

if __name__=="__main__":
    #print(get_user_by_email("slepamacka@gmail.com"))
    #location2 = {
    #    "latitude": 40.7128,
    #    "longitude": -74.0060,
    #    "altitude": 1389  # in meters
    #}
    # image_id=create_image(user_id=13, image_url="desinger_pvc.png", status= "pending",
    #             incident_time=None, reportee_name='Mike', reportee_ip_address='192.168.1.1',
    #             username='bike1389', location=location)
    #desinger_image=get_image_by_id(86)
    #print(desinger_image)
    #update_image(desinger_image.id, desinger_image.user_id, desinger_image.image_url, desinger_image.photodna_results, 
    #            desinger_image.hiveai_results, desinger_image.status,
    #            desinger_image.incident_time, desinger_image.reportee_name, desinger_image.reportee_ip_address, desinger_image.username, location2)
    #print(get_image_by_id(86))