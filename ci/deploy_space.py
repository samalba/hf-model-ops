"""Deploy an app to a Hugginface Space"""

import os
import sys
import dagger


def deploy(hf_token: str, hf_space_id: str):
    with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory("./src", exclude=["venv/", ".pytest_cache/"])

        secret_token = client.set_secret("hfAccessToken", hf_token)
        deployer = (client.container().from_("samalba/huggingface-space-deploy")
            .with_directory("/src", src)
            .with_secret_variable("HF_TOKEN", secret_token)
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
    deploy(os.environ.get("HF_TOKEN"), "samalba/demo")
