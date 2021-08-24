#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import pprint

# 编译控制
CLEAN_FLAG = ARGUMENTS.get('clean', 0)
PACKAGE_FLAG = ARGUMENTS.get('pack', 0)
APP_NAME = ARGUMENTS.get('app_name', '')
if len(APP_NAME):
    PACKAGE_FLAG = 1

# 构造基本信息
ROOT_DIR = Dir('.').srcnode().abspath
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
OUTPUT_LIB_DIR = os.path.join(OUTPUT_DIR, 'lib')
PACK_DIR = os.path.join(OUTPUT_DIR, 'pack')
PACK_LIB_DIR = os.path.join(PACK_DIR, 'lib')
PACK_INC_DIR = os.path.join(PACK_DIR, 'include')

V = {
    'TOP': {
        'ROOT_DIR': ROOT_DIR,
        'OUTPUT_DIR': OUTPUT_DIR,
        'OUTPUT_LIB_DIR': OUTPUT_LIB_DIR,
        'PACK_DIR': PACK_DIR,
        'INC_DIRS': [],
        'LIB_DIRS': [],
        'APP': {
            "APP_NAME": APP_NAME,
        },
    }
}


# 包含子目录SConscript
SConscript("hal/SConscript", variant_dir="output/lib/hal", duplicate=0, exports=V)
SConscript("sdk/SConscript", variant_dir="output/lib/sdk", duplicate=0, exports=V)
SConscript("apps/SConscript", variant_dir="output/bin/app", duplicate=0, exports=V)


# clean
Clean("hal", OUTPUT_DIR)  # 简单粗暴的clean
if CLEAN_FLAG == '1':
    print("===== clean =====")
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    print("----- clean finished -----")


# 打包产物
LIB_DIRS = V['TOP']['LIB_DIRS']
INC_DIRS = V['TOP']['INC_DIRS']
if PACKAGE_FLAG == '1':
    print("===== pack =====")
    shutil.rmtree(PACK_DIR, ignore_errors=True)
    os.makedirs(PACK_DIR)

    os.makedirs(os.path.join(PACK_DIR, 'lib'))  # 库文件打包
    for l in LIB_DIRS:
        shutil.copy(l, PACK_LIB_DIR)

    os.makedirs(os.path.join(PACK_DIR, 'include'))  # 头文件打包
    for i in INC_DIRS:
        if ROOT_DIR+os.sep == i[:len(ROOT_DIR)+1]:
            sub_dir = i[len(ROOT_DIR)+1:]
            pack_inc = os.path.join(PACK_INC_DIR, sub_dir)
            shutil.copytree(i, pack_inc)

    print("----- pack finished -----")


# 输出编译信息
pprint.pprint(V)
