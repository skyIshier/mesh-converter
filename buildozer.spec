[app]

# 应用名称（显示在手机上的名字）
title = 光遇Mesh转换器

# 源代码所在目录（. 表示当前目录）
source.dir = .

# 包名（唯一标识，通常使用反向域名格式）
package.name = meshconverter
package.domain = org.example

# 版本号
version = 0.1

# 需要的 Python 模块（kivy 和 lz4 必须）
requirements = python3,kivy,lz4

# 要包含的源码文件扩展名（.py 文件必须包含，其他资源文件根据需要添加）
source.include_exts = py,png,jpg,kv,atlas

# 入口文件（你的 Kivy 应用主文件）
source.main = main.py

# 图标文件（可选，留空则使用默认图标）
# icon.filename = %(source.dir)s/icon.png

# Android 权限（读写存储权限必须）
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.build_tools_version = 34.0.0

# 是否显示控制台（调试用建议设为 True，正式版可改为 False）
android.console = False

# 目标 Android API 级别（30 对应 Android 11，可根据需要调整）
android.api = 30
android.minapi = 21

# NDK 版本（buildozer 会自动下载）
android.ndk = 23b

# SDK 版本（通常与 api 一致）
android.sdk = 30

# 是否启用 AndroidX（推荐启用）
android.use_sdl2 = True
android.allow_backup = True
android.gradle_dependencies = ''

# 其他可选配置（一般保持默认即可）
# android.add_src = 
# android.add_libs_arch = 
# android.archs = armeabi-v7a, arm64-v8a

[buildozer]

# 日志级别（0 最安静，2 最详细）
log_level = 2

# 警告如果以 root 身份运行
warn_on_root = 1

# 在构建前自动更新 requirements 中的模块
# pre_build_commands = 
