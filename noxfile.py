import nox

@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def test(session):
    session.install("waelstow==0.11.1")
    session.run("./load_tests.py", external=True)
