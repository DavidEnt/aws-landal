#!/usr/bin/env python3
import aws_cdk as cdk
from scheduled_lambda import ScheduledLambdaContainerStack

app = cdk.App()
ScheduledLambdaContainerStack(
    app,
    "LandalStats",
)
app.synth()
