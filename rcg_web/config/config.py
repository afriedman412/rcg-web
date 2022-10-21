import os
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# bright green: #1fd362
# dark green: #047c2c
# purple: #533b53
# orange: #f09933
# red: #ff1e00
# grey: #585858

COLORS = {
    "Male": "#a1c3d1",
    "Female": "#f09933",
    "Non-Binary": "#816f88"
}

