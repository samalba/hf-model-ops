"""Run tests for multiple Python versions concurrently."""

import sys
import dagger


def test():
    versions = ["3.10", "3.11"]

    with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        client = client.pipeline("test")

        # get reference to the local project
        src = client.host().directory("./tests", exclude=["venv/", ".pytest_cache/", ".git/"])

        python_cache = client.cache_volume("python")

        def test_version(version: str):
            python = (
                client.pipeline(f"python-{version}")
                .container().from_(f"python:{version}-slim-buster")
                # mount cloned repository into image
                .with_directory("/src", src)
                # set current working directory for next commands
                .with_workdir("/src")
                # cache for transformers and pip
                .with_mounted_cache("/cache", python_cache)
                .with_env_variable("TRANSFORMERS_CACHE", "/cache/hub")
                .with_env_variable("XDG_CACHE_HOME", "/cache")
                # install test dependencies
                .with_exec(["pip", "install", "-r", "requirements.txt"])
                # run tests
                .with_exec(["pytest"])
            )

            print(f"Starting tests for Python {version}")

            # execute
            python.exit_code()

            print(f"Tests for Python {version} succeeded!")

        for version in versions:
            test_version(version)

    print("All tasks have finished")


if __name__ == "__main__":
    test()
