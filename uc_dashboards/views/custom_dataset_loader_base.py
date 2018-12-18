from abc import abstractmethod, ABCMeta
from typing import Sequence, Any

from xf.uc_dashboards.models.dataset import DataSet


class XFCustomDataSetLoaderBase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_dataset(self, dataset: DataSet, request, **kwargs) -> Sequence[Any]:
        pass
