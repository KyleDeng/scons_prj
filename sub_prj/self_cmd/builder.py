import os
from SCons.Script import (
    DefaultEnvironment,
    Environment,
    Glob,
    VariantDir,
)

env: Environment = DefaultEnvironment()

ROOT = os.getcwd()  # run cmd path
OUTPUT_DIR = os.path.join(ROOT, ".output")
SOURCE_DIR = OUTPUT_DIR  # VariantDir 避免.o生成在源码路径
OUTPUT_LIBS_DIR = os.path.join(OUTPUT_DIR, "libs")
OUTPUT_OBJS_DIR = os.path.join(OUTPUT_DIR, "objs")
OUTPUT_BIN_DIR = os.path.join(OUTPUT_DIR, "bin")

VariantDir(OUTPUT_DIR, ".", duplicate=0)

# sdk
sdk_lib = os.path.join(OUTPUT_LIBS_DIR, "libsdk.a")
sdk_src = Glob(f'{os.path.join(SOURCE_DIR, "sdk", "src")}/*.c')
sdk_inc = os.path.join(SOURCE_DIR, "sdk", "include")
sdk_target = env.Library(
    target=sdk_lib,
    source=sdk_src,
    CPPPATH=sdk_inc,
)
env.Alias("sdk", sdk_target)

# app
app_lib = os.path.join(OUTPUT_LIBS_DIR, "libapp.a")
app_src = Glob(f'{os.path.join(SOURCE_DIR, "app")}/*.c')
app_target = env.Library(
    target=app_lib,
    source=app_src,
    CPPPATH=sdk_inc,
)
env.Alias("app", app_target)

# bin
bin_name = os.path.join(OUTPUT_BIN_DIR, "myapp")
bin_target = env.Program(
    target=bin_name,
    source=[],
    LIBS=["app", "sdk"],
    LIBPATH=OUTPUT_LIBS_DIR,
)
env.Alias("bin", bin_target)


# run
def run_action(target, source, env):
    print("========= RUN =========")
    os.system(f"{source[0]}")
    print("--------- RUN END ---------")


run_target = env.Command('run', [bin_name], run_action)


# help
def help_action(target, source, env):
    note = '''
    Use:
    scons -Q -f ./builder.py [command] [-c]

    Command:
    sdk
    app
    run
    help
'''
    print(note)


help_target = env.Command("help", [], help_action)


env.Default(bin_target)
