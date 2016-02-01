# opengapps-patch

## How to use ##
`python patch.py [-v|-d] -i <path/to/opengapps.zip>`
Use `-d` for debug output and `-v` for verbose output.

## Why did I build this ##
With a [fix](https://github.com/opengapps/opengapps/commit/968b7795e266fa43317494c2500f80cc72640349) from [@mfonville](https://github.com/mfonville), all usage of busybox are dropped including the lines to determine if there's enought space for open gapps. However, genymotion come with a non-posix compatible df in its toolkit. So `df -k /system` would return human readable format integers like `518.8M` which isn't expected.

Before genymotion fixed their built-in toolkit, you may use this tool to patch Open GApps zip.