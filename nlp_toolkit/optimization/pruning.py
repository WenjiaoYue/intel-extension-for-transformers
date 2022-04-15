from enum import Enum
from neural_compressor.conf.config import Pruner as INCPruner
from neural_compressor.pruners import PRUNERS
from typing import Dict, List


class PruningMode(Enum):
    BASICMAGNITUDE = "basic_magnitude"
    PATTERNLOCK = "pattern_lock"
    GROUPLASSO = "group_lasso"


SUPPORTED_PRUNING_MODE = set([approach.name for approach in PruningMode])


class Pruner(INCPruner):
    def __init__(self, epoch_range: List=None, initial_sparsity_ratio: float=None,
                 target_sparsity_ratio: float=None, update_frequency: int=1,
                 prune_type: str='BasicMagnitude', method: str='per_tensor',
                 names: List=[], parameters: Dict=None):
        if epoch_range is not None:
            assert len(epoch_range) == 2, "Please set the epoch_range as [start_epoch, end_epoch]"
            self.start_epoch = epoch_range[0]
            self.end_epoch = epoch_range[1]
        else:
            self.start_epoch = None
            self.end_epoch = None
        self.update_frequency = update_frequency
        self.target_sparsity = target_sparsity_ratio
        self.initial_sparsity = initial_sparsity_ratio
        self.update_frequency = update_frequency
        assert prune_type.upper() in SUPPORTED_PRUNING_MODE, \
            "prune_type only support {}!".format(
                [mode.lower() for mode in SUPPORTED_PRUNING_MODE]
            )
        self.prune_type = PruningMode[prune_type.upper()].value
        self.method = method
        self.names= names
        self.parameters = parameters


