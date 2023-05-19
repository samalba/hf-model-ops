"""Run tests for multiple Python versions concurrently."""

import sys
import anyio
import dagger


async def test():
    versions = ["3.10", "3.11"]

    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory("./tests", exclude=["venv/", ".pytest_cache/", ".git/"])

        python_cache = client.cache_volume("python")

        async def test_version(version: str):
            python = (
                client.container().from_(f"python:{version}-slim-buster")
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
            await python.exit_code()

            print(f"Tests for Python {version} succeeded!")

        # when this block exits, all tasks will be awaited (i.e., executed)
        async with anyio.create_task_group() as tg:
            for version in versions:
                tg.start_soon(test_version, version)

    print("All tasks have finished")


if __name__ == "__main__":
    anyio.run(test)
