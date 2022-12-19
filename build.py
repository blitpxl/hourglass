import PyInstaller.__main__ as build
import subprocess

# compile resources into python file to be embedded into the executable
subprocess.run("pyrcc5 hourglass/res/res.qrc -o hourglass/res/generated/resources.py")


build.run(
    [
        "hourglass/hourglass.py",
        "--noconsole",
        "--name=HourGlass",
        "--icon=hourglass.ico",
        "--workpath=pyinstaller/build",
        "--specpath=pyinstaller/spec",
        "--distpath=pyinstaller/dist"
    ]
)


build.run(
    [
        "hourglass/hourglass-configurator.py",
        "--noconsole",
        "--name=HourGlass-Configurator",
        "--icon=hourglass.ico",
        "--uac-admin",
        "--workpath=pyinstaller/build",
        "--specpath=pyinstaller/spec",
        "--distpath=pyinstaller/dist"
    ]
)
