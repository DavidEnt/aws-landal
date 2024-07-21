from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as events_targets,
)
from constructs import Construct


class ScheduledLambdaContainerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = _lambda.DockerImageFunction(
            self,
            "LandalLambda",
            code=_lambda.DockerImageCode.from_image_asset("image"),
            memory_size = 512,
            timeout = Duration.seconds(90)
        )

        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["sqs:SendMessage"],
                resources=["*"],
            )
        )

        schedule = events.Rule(
            self,
            "weekly-landal-scraper-trigger",
            targets=[events_targets.LambdaFunction(lambda_function)], # type: ignore
            schedule=events.Schedule.cron(minute="0", hour="21", week_day="1",)
        )