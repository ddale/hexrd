import logging
import multiprocessing as mp
import os

from .config import Config, Parameter
from .detector import Detector
#from .findorientations import FindOrientations
#from .fitgrains import FitGrains
#from .imageseries import ImageSeries
#from .material import Material
#from .utils import null
from .validators import is_str, path_exists


logger = logging.getLogger('hexrd.config')



def set_multiproc(key, val):
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        val = val.lower()
        if val in ['all', 'half']:
            return val
    raise RuntimeError(
        'invalid value specified for "%s": %s' % (key, val)
        )



def get_multiproc(key, multiproc):
    ncpus = mp.cpu_count()
    if multiproc == 'all':
        return ncpus
    elif multiproc == 'half':
        temp = ncpus / 2
        return temp if temp else 1
    elif isinstance(multiproc, int):
        if multiproc >= 0:
            if multiproc > ncpus:
                logger.warning(
                    'Resuested %s processes, %d available, using %d',
                    multiproc, ncpus, ncpus
                    )
                return ncpus
            return multiproc if multiproc else 1
        else:
            temp = ncpus + multiproc
            if temp < 1:
                logger.warning(
                    'Cannot use less than 1 process, requested %d of %d'
                    ' available. Defaulting to 1',
                    temp, ncpus
                    )
                return 1
            return temp
    else:
        temp = ncpus - 1
        logger.warning(
            "Invalid value %s for multiprocessing, defaulting to %d"
            " of %d available",
            multiproc, temp, ncpus
            )
        return temp



class Root(Config):


    analysis_name = Parameter(
        'analysis_name', is_str, is_str, default='analysis'
        )


    @property
    def detector(self):
        return Detector(self)


    @property
    def find_orientations(self):
        return FindOrientations(self)


    @property
    def fit_grains(self):
        return FitGrains(self)


    @property
    def image_series(self):
        return Imageseries(self)


    @property
    def material(self):
        return Material(self)


    multiprocessing = Parameter(
        'multiprocessing', get_multiproc, set_multiproc, default=-1
        )


    working_dir = Parameter(
        'working_dir', path_exists, path_exists, default=os.getcwd()
        )
