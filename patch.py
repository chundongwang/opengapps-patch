import argparse
import logging
from lib.update_binary_patcher import UpdateBinaryPatcher

logger = logging.getLogger('OpenGAppsPatcher')


def parse_args():
    parser = argparse.ArgumentParser(
            description='Patch open gapps to use busybox df instead of '
                        'built-in df to fix issue of genymotion vms. For '
                        'details see https://github.com/opengapps/opengapps/'
                        'commit/968b7795e266fa43317494c2500f80cc72640349')
    parser.add_argument(
            '-i', '--input_zip', type=str, required=True,
            help="Zip file of opengapps to patch. Download from "
                 "http://opengapps.org/?api=5.1&variant=mini&arch=x86"
    )
    parser.add_argument(
            '--keystore', type=str, default="~/.android/debug.keystore",
            help="keystore file to sign archive"
    )
    parser.add_argument(
            '--alias', type=str, default="androiddebugkey",
            help="keystore alias to sign archive"
    )
    parser.add_argument(
            '--storepass', type=str, default="android",
            help="keystore file to sign archive"
    )
    parser.add_argument(
            '-d', '--debug',
            help="debug mode, output debugging info for this program "
                 "and it will be noisy.",
            action="store_const", dest="loglevel", const=logging.DEBUG,
            default=logging.WARNING,
    )
    parser.add_argument(
            '-v', '--verbose',
            help="verbose mode",
            action="store_const", dest="loglevel", const=logging.INFO,
    )

    return parser.parse_args()


def main(args):
    patcher = UpdateBinaryPatcher(zipfile=args.input_zip,
                                  keystore=args.keystore,
                                  alias=args.alias,
                                  storepass=args.storepass)
    patcher.patch()


if __name__ == '__main__':
    args = parse_args()

    FORMAT = '%(asctime)-15s %(levelname)-6s %(name)-20s %(message)s'
    logging.basicConfig(format=FORMAT, level=args.loglevel)

    main(args)