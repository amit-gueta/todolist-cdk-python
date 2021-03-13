from aws_cdk import core, aws_dynamodb, aws_cognito, aws_lambda, aws_apigateway, aws_apigatewayv2


class TodoListStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        TODOLIST_TABLE_NAME = "todolist"
        TODOLIST_TABLE_PARTITION_KEY = "userId"
        TODOLIST_TABLE_SORT_KEY = "todoId"

        table = aws_dynamodb.Table(self, "Todo",
                                   table_name="todolist",
                                   partition_key=aws_dynamodb.Attribute(
                                       name=TODOLIST_TABLE_PARTITION_KEY, type=aws_dynamodb.AttributeType.STRING),
                                   sort_key=aws_dynamodb.Attribute(
                                       name=TODOLIST_TABLE_SORT_KEY, type=aws_dynamodb.AttributeType.STRING),
                                   removal_policy=core.RemovalPolicy.DESTROY)

        user_pool = aws_cognito.UserPool(self, "todo_list",
                                         self_sign_up_enabled=True,
                                         sign_in_aliases=aws_cognito.SignInAliases(
                                             email=True)
                                         )

        sign_up_lambda_function = aws_lambda.Function(self, "signup",
                                                      runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                      handler="signup.main",
                                                      code=aws_lambda.Code.asset("./lambda"))

        confirm_sign_up_lambda_function = aws_lambda.Function(self, "confirm",
                                                              runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                              handler="confirm.main",
                                                              code=aws_lambda.Code.asset("./lambda"))

        auth_lambda_function = aws_lambda.Function(self, "auth",
                                                   runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                   handler="auth.main",
                                                   code=aws_lambda.Code.asset("./lambda"))

        create_todo_list_lambda_function = aws_lambda.Function(self, "create",
                                                               runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                               handler="lambda/create.main",
                                                               environment=dict(
                                                                   TABLE_NAME=table.table_name
                                                               ),
                                                               code=aws_lambda.Code.from_asset("./lambdas.zip"))

        get_all_todo_lambda_function = aws_lambda.Function(self, "getall",
                                                           runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                           handler="lambda/get_all_todo.main",
                                                           environment=dict(
                                                               TABLE_NAME=table.table_name
                                                           ),
                                                           code=aws_lambda.Code.from_asset(
                                                               "./lambdas.zip")
                                                           )

        table.grant_write_data(create_todo_list_lambda_function)
        table.grant_read_data(get_all_todo_lambda_function)

        api = aws_apigateway.RestApi(self, "todolistRestApi",
                                     rest_api_name="Todolist API",
                                     default_cors_preflight_options={
                                         "allow_origins": aws_apigateway.Cors.ALL_ORIGINS,
                                         "allow_methods": aws_apigateway.Cors.ALL_METHODS,
                                         "allow_headers": ["client-id", "Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key", "X-Amz-Security-Token", "X-Amz-User-Agent"]
                                     }
                                     #  default_cors_preflight_options={
                                     #      "allow_origins": ["*"],
                                     #      "allow_methods": ["GET", "POST", "OPTIONS"],
                                     #      "allow_headers": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key", "X-Amz-Security-Token", "X-Amz-User-Agent"]
                                     #  }
                                     )

        sign_up_lambda_integration = aws_apigateway.LambdaIntegration(
            sign_up_lambda_function)
        api.root.add_resource("signup").add_method(
            "POST", sign_up_lambda_integration)

        confirm_sign_up_lambda_integration = aws_apigateway.LambdaIntegration(
            confirm_sign_up_lambda_function)
        api.root.add_resource("confirm").add_method(
            "POST", confirm_sign_up_lambda_integration)

        auth_lambda_integration = aws_apigateway.LambdaIntegration(
            auth_lambda_function)
        api.root.add_resource("auth").add_method(
            "POST", auth_lambda_integration)

        todolist_api = api.root.add_resource("todolists")
        create_todo_list_lambda_integration = aws_apigateway.LambdaIntegration(
            create_todo_list_lambda_function)
        todolist_api.add_method(
            "POST", create_todo_list_lambda_integration)

        get_all_todo_lambda_integration = aws_apigateway.LambdaIntegration(
            get_all_todo_lambda_function)
        todolist_api.add_method(
            "GET", get_all_todo_lambda_integration)
