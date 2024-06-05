#!/usr/bin/env python3
from aws_cdk import (
    aws_ecr as ecr,
    aws_ecr_assets as ecr_assets,
    Stack,
)
import cdk_ecr_deployment as ecrdeploy
import aws_cdk as cdk
from constructs import Construct

class EcrRepositoryStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create the ECR repository
        ecr.Repository(self, 
                       "ConsigFreeswitchMrfRepo",
                       repository_name="consig-freeswitch-mrf")

        freeswitch_image_asset = ecr_assets.DockerImageAsset(self, "Freeswitch",
                                directory="../",  # Path to the directory with Dockerfile
                                platform=ecr_assets.Platform.LINUX_AMD64,
                                build_args={
                                    "BUILD_CPUS": "4",
                                    "TARGETARCH": "x86_64",
                                },
                            )
        
        # Copy from cdk docker image asset to another ECR.
        ecrdeploy.ECRDeployment(self, "FreeswitchImage",
            src=ecrdeploy.DockerImageName(freeswitch_image_asset.image_uri),
            dest=ecrdeploy.DockerImageName(f"{Stack.of(self).account}.dkr.ecr.{Stack.of(self).region}.amazonaws.com/consig-freeswitch-mrf:latest")
        )

app = cdk.App()

#
# Create the core DNS Sub Zones
#
EcrRepositoryStack(app, "FreeSwitchMRF")

app.synth()
