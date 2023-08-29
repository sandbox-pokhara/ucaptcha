import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucaptcha",
    version="1.0.2",
    author="Pradish Bijukchhe",
    author_email="pradishbijukchhe@gmail.com",
    description="Universal captcha solving python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandbox-pokhara/ucaptcha",
    project_urls={
        "Bug Tracker": "https://github.com/sandbox-pokhara/ucaptcha/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_dir={"ucaptcha": "ucaptcha"},
    python_requires=">=3",
    install_requires=["requests"],
)
