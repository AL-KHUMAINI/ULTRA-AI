[app]
title = ULTRA AI
package.name = ultraai
package.domain = com.ultra.ai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,env
version = 1.0.0
requirements = python3,kivy,urllib3,requests,google-generativeai
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
[buildozer]
log_level = 2
warn_on_root = 1
