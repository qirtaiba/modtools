from flask_login import UserMixin


class User(UserMixin):

  def __init__(self, id, name, lastname, email, password, created_at=None, role='moderator'):
    self.id = id
    self.role = role
    self.name = name
    self.lastname = lastname
    self.email = email
    self.password = password
    self.created_at = created_at

  def to_dict(self):
    created_at_formatted = self.created_at.strftime('%d/%m/%y %H:%M:%S')
    return {
      "id": self.id,
      "role": self.role,
      "name": self.name,
      "lastname": self.lastname,
      "email": self.email,
      "password": self.password,
      "created_at": created_at_formatted
    }

  def __str__(self):
    return f"User(id={self.id}, role={self.role}, name='{self.name}', lastname='{self.lastname}', email='{self.email}', password='{self.password}', created_at='{self.created_at}')"


from datetime import datetime

class Image:
    def __init__(self, id, user_id, image_url, photodna_results=None, hiveai_results=None, status='pending',
                 created_at=None, updated_at=None, incident_time=None,
                 reportee_name=None, reportee_ip_address=None, username=None,
                 latitude=None, longitude=None, altitude=None):
        self.id = id
        self.user_id = user_id
        self.image_url = image_url
        self.photodna_results = photodna_results
        self.hiveai_results = hiveai_results
        self.status = status
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.incident_time = incident_time
        self.reportee_name = reportee_name
        self.reportee_ip_address = reportee_ip_address
        self.username = username
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def to_dict(self):
        created_at_formatted = self.created_at
        updated_at_formatted = self.updated_at
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "photodna_results": self.photodna_results,
            "hiveai_results": self.hiveai_results,
            "status": self.status,
            "created_at": created_at_formatted,
            "updated_at": updated_at_formatted,
            "incident_time": self.incident_time,
            "reportee_name": self.reportee_name,
            "reportee_ip_address": self.reportee_ip_address,
            "username": self.username,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude
        }

    def __str__(self):
        return (
            f"Image(id={self.id}, user_id={self.user_id}, image_url='{self.image_url}', "
            f"photodna_results={self.photodna_results}, hiveai_results={self.hiveai_results},"
            f"status='{self.status}', created_at='{self.created_at}', "
            f"updated_at='{self.updated_at}', incident_time='{self.incident_time}', "
            f"reportee_name='{self.reportee_name}', reportee_ip_address='{self.reportee_ip_address}', "
            f"username='{self.username}', latitude='{self.latitude}', "
            f"longitude='{self.longitude}', altitude='{self.altitude}')"
        )



class Invitation:
    def __init__(self, id, invitee_email, inviter_user_id, created_at=None):
        self.id = id
        self.invitee_email = invitee_email
        self.inviter_user_id = inviter_user_id
        self.created_at = created_at

    def to_dict(self):
        created_at_formatted = self.created_at.strftime('%d/%m/%y %H:%M:%S') if self.created_at else None
        return {
            "id": self.id,
            "invitee_email": self.invitee_email,
            "inviter_user_id": self.inviter_user_id,
            "created_at": created_at_formatted
        }

    def __str__(self):
        return f"Invitation(id={self.id}, invitee_email='{self.invitee_email}', inviter_user_id={self.inviter_user_id}, created_at='{self.created_at}')"


class Plugin:

    def __init__(self, id, name, about, is_registered, action_id):
        self.id = id
        self.name = name
        self.about = about
        self.is_registered = is_registered
        self.action_id = action_id

    def __str__(self):
        return f"Plugin(id={self.id}, name='{self.name}', about='{self.about}', is_registered={self.is_registered}, action_id={self.action_id})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'is_registered': self.is_registered,
            'action_id': self.action_id
        }


class API:

    def __init__(self, id, name, about,is_registered=True):
        self.id = id
        self.name = name
        self.about = about
        self.is_registered = is_registered

    def __str__(self):
        return f"API(id={self.id}, name='{self.name}', about='{self.about}', is_registered={self.is_registered})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'is_registered': self.is_registered
        }