import os
import tempfile
import shutil
import logging
from abc import ABCMeta, abstractmethod
from zipfile import ZipFile, ZIP_DEFLATED

logger = logging.getLogger('ZipPatcher')


class ZipPatcher:
    __metaclass__ = ABCMeta

    def __init__(self, zipfile):
        assert os.path.isfile(zipfile)
        self.zipfile = zipfile

    def _read_zip(self, filename):
        with ZipFile(self.zipfile, 'r') as zip_f:
            return zip_f.read(filename)

    def _replace_zip(self, filename, new_content):
        self._remove_from_zip(filename)
        self._add_to_zip(filename, new_content)

    def _remove_from_zip(self, *filenames):
        """
        remove files from the zip if remove_filter_func(filename) returns True
        :param filenames: to be removed files
        :return:
        """
        tempdir = tempfile.mkdtemp()
        try:
            tempzip = os.path.join(tempdir, os.path.split(self.zipfile)[-1])
            logger.debug('copy from {} to {}'.format(self.zipfile, tempzip))
            with ZipFile(self.zipfile, 'r') as zip_src_f:
                with ZipFile(tempzip, 'w') as zip_dst_f:
                    for item in zip_src_f.infolist():
                        if item.filename not in filenames:
                            data = zip_src_f.read(item.filename)
                            zip_dst_f.writestr(item, data)
            logger.debug('move from {} to {}'.format(tempzip, self.zipfile))
            shutil.move(tempzip, self.zipfile)
        finally:
            shutil.rmtree(tempdir)

    def _add_to_zip(self, filename, content):
        """
        Add file to a zip with specified content.
        :param zipfile: target zip file
        :param filename: path of the file to be added
        :param content: content of the file to be added
        :return:
        """
        with ZipFile(self.zipfile, mode='a', compression=ZIP_DEFLATED) as zip_f:
            logger.debug('append {} to {}'.format(filename, self.zipfile))
            zip_f.writestr(filename, content)

    @abstractmethod
    def patch(self):
        raise TypeError('abstract patch method of ZipPatcher')