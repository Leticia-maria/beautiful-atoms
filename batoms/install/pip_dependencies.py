import sys
import subprocess
import importlib
from bpy.types import Operator
from bpy.props import (StringProperty,
                       )

dependencies = {"ase": "ase",
                "scikit-image": "skimage",
                }


def has_pip():
    # check pip exist or not
    return not subprocess.call([sys.executable, "-m", "pip", "--version"])

def has_module(modname):
    try:
        module = importlib.import_module(modname)
        return True
    except ImportError:
        return False

def install_pip():
    # if not exist
    cmd = [sys.executable, "-m", "ensurepip", "--upgrade"]
    subprocess.call(cmd)
    # upgrade
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    subprocess.call(cmd)
    if not has_pip():
        print("pip cannot be installed, please install pip manually.")

def install_wheel():
    cmd = [sys.executable, "-m", "pip", "install", "wheel"]


def install_module(package, modname):
    if not has_module(modname):
        if not has_pip():
            install_pip()
        cmd = [sys.executable, "-m", "pip",
                "install", "--upgrade", package]
        subprocess.call(cmd)
        print("package {0} installed.".format(package))
    # else:
        # print("package {0} installed.".format(package))
    return has_module(modname)

def install():
    for package, modname in dependencies.items():
        install_module(package, modname)



class BatomsInstallPackage(Operator):
    bl_idname = "batoms.pip_install_package"
    bl_label = "pip install"
    bl_description = ("Install pip dependencies")


    package: StringProperty(
        name="package", default='ase',
        description="package name")
    
    modname: StringProperty(
        name="modname", default='ase',
        description="module name")

    def execute(self, context):
        if not has_pip():
            install_pip()
        install_module(self.package, self.modname)
        if not has_module(self.modname):
            self.report({"WARNING"}, "Cannot install package: {}".format(self.package))
            return {"CANCELLED"}
        self.report({"INFO"}, "Install package {} successfully!".format(self.package))
        return {"FINISHED"}


classes = [
    BatomsInstallPackage,
]

def register_class():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    

def unregister_class():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    