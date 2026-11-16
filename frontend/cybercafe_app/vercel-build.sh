#!/bin/sh
set -e

git clone --depth 1 --branch stable https://github.com/flutter/flutter.git /tmp/flutter

/tmp/flutter/bin/flutter config --enable-web
/tmp/flutter/bin/flutter pub get
/tmp/flutter/bin/flutter build web --release
