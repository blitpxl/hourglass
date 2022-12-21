import PyInstaller.__main__ as build
import subprocess

# compile resources into python file to be embedded into the executable
subprocess.run("pyrcc5 hourglass/res/res.qrc -o hourglass/res/generated/resources.py")


# build hourglass
build.run(
    [
        "hourglass/hourglass.py",
        "--noconfirm",
        "--noconsole",
        "--name=hourglass",
        "--icon=hourglass.ico",
        "--workpath=pyinstaller/build",
        "--specpath=pyinstaller/spec",
        "--distpath=pyinstaller/dist"
    ]
)


# build hourglass-configurator
build.run(
    [
        "hourglass/hourglass-configurator.py",
        "--noconfirm",
        "--noconsole",
        "--name=hourglass-configurator",
        "--icon=hourglass.ico",
        "--uac-admin",
        "--workpath=pyinstaller/build",
        "--specpath=pyinstaller/spec",
        "--distpath=pyinstaller/dist"
    ]
)
