from django.db import models
from auth_.models import *


class Task(models.Model):
    name = models.CharField(max_length=50)
    user_id = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    process_id = models.IntegerField()
    # Process Variable =
	# Task Variable =
	# Case Variable =
	# Process Instance ID =
	# Process Instance Business Key =
	# Process Definition ID =
	# Process Definition Key =
	# Process Definition Name =
	# Execution ID =
	# Case Instance ID =
	# Case Instance Business Key =
	# Case Definition ID =
	# Case Definition Key =
	# Case Definition Name =
	# Case Execution ID =
	# Assignee =
	# Owner =
	# Candidate Group =
	# Candidate User =
	# Involved User =
	# Task Definition Key =
	# Name =
	# Description =
	# Priority =
	# Due date =
	# Follow-up date =
	# Created =
	# Delegation State =
	# Tenant ID =
	# Without Tenant ID =