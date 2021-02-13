import json
import pytest

from aws_cdk import core
from todo-list.todo_list_stack import TodoListStack


def get_template():
    app = core.App()
    TodoListStack(app, "todo-list")
    return json.dumps(app.synth().get_stack("todo-list").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
