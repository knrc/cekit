import logging
import os
from typing import List

from cekit.builder import Builder
from cekit.tools import run_wrapper

LOGGER = logging.getLogger("cekit")


class OCIBuilder(Builder):
    def common_build(self, build_type: str, cmd: List[str], tagging=True):
        tags: List[str] = self.params.tags
        args: List[str] = self.params.build_args
        generic_args: List[str] = self.params.build_flag

        if tagging and not tags:
            tags = self.generator.get_tags()

        if not self.params.no_squash:
            cmd.append("--squash")

        if self.params.trace:
            cmd += ["--log-level", "debug"]

        if self.params.pull:
            cmd.append("--pull-always")

        if self.params.platform:
            cmd.append("--platform")
            cmd.append(self.params.platform)

        # Custom tags for the container image
        LOGGER.debug("Building image with tags: '{}'".format("', '".join(tags)))

        if tagging:
            cmd.extend(self.get_tag_params(tags))

        if args:
            for arg in args:
                cmd.extend(["--build-arg=" + arg])

        if generic_args:
            for arg in generic_args:
                cmd.extend([arg])

        LOGGER.debug("Building image with command: '{}'".format("' '".join(cmd)))
        LOGGER.info("Building container image...")

        cmd.append(os.path.join(self.target, "image"))

        run_wrapper(cmd, False, f"Could not run {build_type} {cmd}")

        LOGGER.info(
            f"Image built and available under following tags: {', '.join(tags)}"
        )

    def get_tag_params(self, tags: List[str]):
        params: List[str] = []
        for tag in tags:
            cmd.extend(["-t", tag])
        return params
