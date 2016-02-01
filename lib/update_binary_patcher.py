import logging
from subprocess import check_output, check_call, CalledProcessError
from lib.zip_patcher import ZipPatcher

logger = logging.getLogger('UpdateBinaryPatcher')
TARGET_FILE = 'META-INF/com/google/android/update-binary'
TARGET_LINE = 'df=$(df -k /system | tail -n 1);'
PATCHED_LINE = 'df=$(busybox df -k /system | tail -n 1);'
JARSIGN_FILES = ['META-INF/MANIFEST.MF',
                 'META-INF/CERT.SF',
                 'META-INF/CERT.RSA']


class UpdateBinaryPatcher(ZipPatcher):

    def __init__(self, zipfile, keystore, alias, storepass):
        super(UpdateBinaryPatcher, self).__init__(zipfile)
        self.keystore = keystore
        self.alias = alias
        self.storepass = storepass

    def patch(self):
        # remove signed files
        self._remove_from_zip(*JARSIGN_FILES)

        # patch update-binary
        script_content = self._read_zip(TARGET_FILE)
        script_content = script_content.replace(TARGET_LINE, PATCHED_LINE)
        self._replace_zip(filename=TARGET_FILE, new_content=script_content)

        # sign again
        try:
            output = self._sign_zip()
            logger.info('signed the zip with output: {}'.format(output))
            exitcode = self._verify_signature()
            logger.info('verified the zip with exitcode: {}'.format(exitcode))
        except OSError as e:
            logger.error('Cannot sign the zip again. Please make sure you '
                         'have jarsigner installed (mostly part of java '
                         'installation.')
        except CalledProcessError as e:
            logger.error('Cannot sign the patched zip. jarsigner exit with '
                         '{}, output: \n{}'.format(e.returncode, e.output))

    def _sign_zip(self):
        return check_output(
            'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 '
            '-keystore {keystore} {target} {alias} -storepass {storepass}'
                .format(keystore=self.keystore,
                        alias=self.alias,
                        storepass=self.storepass,
                        target=self.zipfile)
                .split()
        )

    def _verify_signature(self):
        return check_call(
            'jarsigner -verify -verbose -certs {target}'
                .format(target=self.zipfile)
                .split()
        )