[app]

# Application title
title = ULTRA AI

# Package name
package.name = ultraai

# Package domain (needed for android packaging)
package.domain = org.ultraai

# Source code location
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,json,db

# Application version
version = 1.0.0

# Application requirements
requirements = python3,kivy==2.3.0,requests==2.31.0,google-generativeai==0.8.3,pillow==10.2.0,python-dotenv==1.0.1,urllib3,chardet,idna,certifi,openssl

# Orientation
orientation = portrait

# Fullscreen setting
fullscreen = 0

# Android permissions required
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android API targeting
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1
