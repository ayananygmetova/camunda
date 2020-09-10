from django.db import models
from auth_.models import *


class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=150)
    
    name = models.CharField(max_length=50)
    assignee = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    process_id = models.CharField(max_length=150)
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
	# taskDefinitionKey =
	# Name =
	# Description =
	# Priority =
	# Due date =
	# Follow-up date =
	# Created =
	# Delegation State =
	# Tenant ID =
	# Without Tenant ID =