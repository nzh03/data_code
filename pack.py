from cx_Freeze import setup, Executable

# 创建可执行文件对象
exe = Executable(
    script="UI.py",
    base="Win32GUI",
    target_name="数据职位推荐系统",
)

# cx_Freeze配置选项
options = {
    "build_exe": {
        "packages": ['tkinter','sklearn'],
        "excludes": [],
        "include_files": ['models.pkl'],
        "silent": False,
    }
}

# 运行setup进行打包
setup(
    name="数据职位推荐系统",
    version="1.0",
    description="版权所有，侵权必究@by_nzh",
    options=options,
    executables=[exe]
)
# python pack.py build