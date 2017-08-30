import os
import uranium


def main(build):
    build.packages.install(".", develop=True)


@uranium.task_requires("main")
def test(build):
    """ execute the unit tests. """
    build.packages.install("pytest")
    build.packages.install("pytest-benchmark")
    build.packages.install("pytest-cov")
    build.packages.install("flake8")
    build.packages.install("cattrs")
    build.executables.run([
        "py.test", "--cov", "jsonschema_extractor",
        "jsonschema_extractor/tests",
        "--cov-report", "term-missing"
    ] + build.options.args)


def publish(build):
    """ publish the package itself """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload", "--release"
    ])


def build_docs(build):
    build.packages.install("Babel")
    build.packages.install("Sphinx")
    build.packages.install("sphinx_rtd_theme")
    build.packages.install("sphinxcontrib-programoutput")
    return build.executables.run([
        "sphinx-build", "docs",
        os.path.join("docs", "_build")
    ] + build.options.args)[0]
