"""Run tests for multiple Python versions concurrently."""

import sys
import dagger

version = "3.11"

def lint():
    with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory("./src", exclude=["venv/", ".pytest_cache/", ".git/"])

        python_cache = client.cache_volume("python")

        python = (
            client.container().from_(f"python:{version}-slim-buster")
            # mount cloned repository into image
            .with_directory("/src", src)
            # set current working directory for next commands
            .with_workdir("/src")
            .with_mounted_cache("/cache", python_cache)
            .with_env_variable("XDG_CACHE_HOME", "/cache")
            # install test dependencies
            .with_exec(["pip", "install", "flake8"])
            # run linter
            .with_exec(["flake8"])
        )

        # execute the linter
        python.exit_code()
        print("Linter passed!")


if __name__ == "__main__":
    lint()
