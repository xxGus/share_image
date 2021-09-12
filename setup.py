from setuptools import setup

setup(
    name="share_image",
    packages=["share_image"],
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-restful",
        "mongoengine"
    ],
)
