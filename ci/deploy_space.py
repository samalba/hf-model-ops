"""Deploy an app to a Hugginface Space"""

import os
import sys
import time
import dagger

from lint import lint
from test import test


def deploy(hf_token: str, hf_space_id: str):
    with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory("./src", exclude=["venv/", ".pytest_cache/"])

        secret_token = client.set_secret("hfAccessToken", hf_token)
        deployer = (client.container().from_("samalba/huggingface-space-deploy")
            .with_directory("/src", src)
            .with_secret_variable("HF_TOKEN", secret_token)
            .with_env_variable("CACHE_BUSTER", str(time.time()))
            .with_exec([
                "--repo-id", hf_space_id,
                "--access-token", hf_token,
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

    # Run the lint pipeline
    lint()
    # Run the tests
    test()
    # Deploy the app to HF
    deploy(access_token, "samalba/demo")
