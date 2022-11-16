import logging

from pip._internal.cli.base_command import Command
from pip._internal.operations.check import (
    check_package_set, create_package_set_from_installed,
)

logger = logging.getLogger(__name__)


class CheckCommand(Command):
    """Verify installed packages have compatible dependencies."""
    name = 'check'
    usage = """
      %prog [options]"""
    summary = 'Verify installed packages have compatible dependencies.'

    def run(self, options, args):
        package_set, parsing_probs = create_package_set_from_installed()
        missing, conflicting = check_package_set(package_set)

        for project_name in missing:
            version = package_set[project_name].version
            for dependency in missing[project_name]:
                logger.info(
                    "%s %s requires %s, which is not installed.",
                    project_name, version, dependency[0],
                )

        for project_name in conflicting:
            version = package_set[project_name].version
            for dep_name, dep_version, req in conflicting[project_name]:
                logger.info(
                    "%s %s has requirement %s, but you have %s %s.",
                    project_name, version, req, dep_name, dep_version,
                )

        if missing or conflicting or parsing_probs:
            return 1
        else:
            logger.info("No broken requirements found.")