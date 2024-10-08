import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from openai import OpenAI
from project.main import config
from project.utils.processing import TaskManager
from project.utils.crawler import Crawler

db = SQLAlchemy()
bcrypt = Bcrypt()

client = OpenAI(
    base_url=config.SERVE_API,
    api_key='sk-no-api-key'
)

crawler = Crawler()
task_manager = TaskManager(client=client, crawler=crawler)