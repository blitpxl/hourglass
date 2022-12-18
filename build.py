import PyInstaller.__main__ as build

build.run(
    [
        "hourglass/hourglass.py",
        "--noconsole",
        "--name=HourGlass",
        "--icon=hourglass.ico",
    ]
)


build.run(
    [
        "hourglass/hourglass-configurator.py",
        "--noconsole",
        "--name=HourGlass-Configurator",
        "--icon=hourglass.ico",
        "--uac-admin"
    ]
)
