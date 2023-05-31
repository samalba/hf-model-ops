"""Deploy an app to a Hugginface Space"""

import os
import sys
import time
import dagger

from lint import lint
from test import test


def deploy(client: dagger.Client, hf_token: str, hf_space_id: str):
    client = client.pipeline("deploy")

    # get reference to the local project
    src = client.host().directory("./src", exclude=["venv/", ".pytest_cache/"])

    secret_token = client.set_secret("hfAccessToken", hf_token)
    deployer = (
        client.container().from_("ghcr.io/samalba/huggingface-space-deploy:latest@sha256:d043d0088b95d3c6a602637eda38eaac38c94d564b10edabbd617965322f0247")
        .with_directory("/src", src)
        .with_secret_variable("ACCESS_TOKEN", secret_token)
        # uncomment to bypass the cache (deploy every time)
        # .with_env_variable("CACHE_BUSTER", str(time.time()))
        .with_exec([
            "--repo-id", hf_space_id,
            "--timeout", "600",
            "/src"
        ])
    )
    deployer.exit_code()

    print(f"Space is running at: https://{hf_space_id.replace('/', '-')}.hf.space/")


if __name__ == "__main__":
    access_token = os.environ.get("HF_TOKEN")

    if access_token is None:
        print("missing HF_TOKEN in environment")
        sys.exit(1)

    with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Run the lint pipeline
        lint(client)
        # Run the tests
        test(client)
        # Deploy the app to HF
        deploy(client, access_token, "samalba/demo")
