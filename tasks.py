from invoke import task

@task
def test(c):
    """Install dependencies."""
    c.run("python3 src/test.py")