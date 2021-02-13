#!/usr/bin/env python3

from aws_cdk import core

from todo_list.todo_list_stack import TodoListStack


app = core.App()
TodoListStack(app, "todo-list", env={'region': 'us-west-2'})

app.synth()
