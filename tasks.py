from invoke import task

@task
def cluster(c):
    """Install dependencies."""
    c.run("python3 src/generate_clusters.py")

@task
def aliases(c):
    """Install dependencies."""
    c.run("python3 src/generate_aliases.py")

@task
def color_function(c):
    """Install dependencies."""
    c.run("python3 src/generate_color_function.py")