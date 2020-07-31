# from . import db
#
#
# class user(db.Model):
#
#     __tablename__ = 'user'
#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )
#     username = db.Column(
#         db.String(64),
#         index=False,
#         unique=True,
#         nullable=False
#     )
#     password = db.Column(
#         db.String(64),
#         index=False,
#         unique=False,
#         nullable=False
#     )
#     email = db.Column(
#         db.String(80),
#         index=True,
#         unique=True,
#         nullable=False
#     )
#     admin = db.Column(
#         db.Boolean,
#         index=False,
#         unique=False,
#         nullable=False
#     )
#
#     def __repr__(self):
#         return '<user {}>'.format(self.username)
#
# class user(db.Model):
#
#     __tablename__ = 'req'
#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )
#     user_id = db.Column(
#         db.Integer,
#         foreign_key=True
#     )
#     created = db.Column(
#         db.DateTime,
#         index=False,
#         unique=False,
#         nullable=False
#     )
#     req_date = db.Column(
#         db.String(64),
#         index=False,
#         unique=True,
#         nullable=False
#     )
#     req_time = db.Column(
#         db.String(64),
#         index=False,
#         unique=False,
#         nullable=False
#     )
#     location = db.Column(
#         db.String(80),
#         index=True,
#         unique=True,
#         nullable=False
#     )
#     priority = db.Column(
#         db.Integer(80),
#         index=True,
#         unique=True,
#         nullable=False
#     )
#     capacity = db.Column(
#         db.Integer(80),
#         index=True,
#         unique=True,
#         nullable=False
#     )
#
#     def __repr__(self):
#         return '<req {}>'.format(self.id)
