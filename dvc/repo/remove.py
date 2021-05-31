import logging
import typing


from dvc.dvcfile import PipelineFile
from dvc.exceptions import InvalidArgumentError

from . import locked

if typing.TYPE_CHECKING:
    from dvc.repo import Repo

logger = logging.getLogger(__name__)


PARENT_TRACKED_ERROR_MSG = """
    DVC is already tracking '{parent}'
    and can't remove files within that directory.
    You can run 'dvc remove {parent}'
    in order to remove '{child}' and all
    the other files within that directory.
"""


@locked
def remove(self: "Repo", target: str,):
    stages_info = self.stage.collect_granular(target)
    for stage, filter_info in stages_info:

        if isinstance(stage.dvcfile, PipelineFile):
            raise InvalidArgumentError(
                f"'target': {target} is a stage name."
                " in order to remove a stage use 'dvc stage remove'")

        if filter_info is not None:
            if stage.outs[0].path_info != filter_info:
                raise InvalidArgumentError(
                    PARENT_TRACKED_ERROR_MSG.format(
                        parent=stage.outs[0].path_info, child=filter_info
                    )
                )

        stage.remove(remove_outs=False)

    return [x.stage for x in stages_info]
