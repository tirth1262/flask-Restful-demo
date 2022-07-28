from flask import Blueprint
from office_management.users.resources import (Login, Profile,
                                               Register, OfficialInformation,
                                               PersonalInfo, UpdatePassword, RefreshToken)

users = Blueprint("users", __name__)

users.add_url_rule("/login", view_func=Login.as_view("login"))
users.add_url_rule("/profile", view_func=Profile.as_view("profile"))
users.add_url_rule("/register", view_func=Register.as_view("register"))
users.add_url_rule("/profile/official_info", view_func=OfficialInformation.as_view("official-profile"))
users.add_url_rule("/profile/personal_info", view_func=PersonalInfo.as_view("personal-profile"))
users.add_url_rule("/profile/update_password", view_func=UpdatePassword.as_view("update-password"))
users.add_url_rule("/refresh", view_func=RefreshToken.as_view("refresh"))
