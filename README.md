# EECE435L Lab 10

Ali Naji's Python CI/CD lab. The project uses Jenkins to install its tools,
check code style, run tests, measure coverage, scan Python code, and deploy a
working copy of the application locally.

Repository: https://github.com/Vortexx-hash/AliNaji-EECE435L-Lab10

## Files

- `app.py`: prints `Hello, World from Ali Naji!`.
- `tests/test_app.py`: four unittest tests, also runnable with pytest.
- `Jenkinsfile_Ali_Naji`: the complete Part 3 and Part 4 pipeline.
- `requirements.txt`: pinned versions of flake8, pytest, coverage, and Bandit.
- `deploy.py`: creates a local release, checks its output, and packages it.
- `Lab10_Report_Ali_Naji.docx`: the lab report with screenshot placeholders.
- `github_link.txt`: repository link for the Moodle submission.
- `docs/JENKINS_STEPS.md`: dashboard settings, screenshots, and submission steps.

## Run locally on Windows

Run these commands from the project directory in PowerShell:

```powershell
python -m venv venv
& ./venv/Scripts/python.exe -m pip install -r requirements.txt
& ./venv/Scripts/python.exe app.py
& ./venv/Scripts/python.exe -m flake8 app.py deploy.py tests
& ./venv/Scripts/python.exe -m pytest -v
& ./venv/Scripts/python.exe -m coverage run --branch --source=app -m pytest
& ./venv/Scripts/python.exe -m coverage report -m --fail-under=100
& ./venv/Scripts/python.exe -m bandit app.py deploy.py
& ./venv/Scripts/python.exe deploy.py
```

On Linux/macOS, use `python3` to create the environment and `venv/bin/python`
for the following commands. Jenkins chooses `bat` or `sh` for its agent.

## Jenkins configuration

The existing job is `Python-CI-CD` at http://localhost:8080/job/Python-CI-CD/.
Use **Pipeline script from SCM**, Git, this repository, branch `*/main`, and
script path **`Jenkinsfile_Ali_Naji`**. The repository is public, so SCM
credentials can remain **none**.

For this Windows machine, use **Build with Parameters** and set:

```text
PYTHON_EXECUTABLE = C:/Users/Public/JenkinsTools/Python310/python.exe
```

This runtime is a copy of the installed Python 3.10.11 standard runtime,
including ensurepip and venv launchers, placed where `jenkins_svc` can read it.
The original Python under AliNaji's private profile returned `Access is denied`
when the service tried to create its environment. The shared copy avoids that
profile restriction. It is machine setup and is not stored in Git.

The parameter defaults to the shared Python path above for this Windows lab.
On another machine, use a Python 3.10+ executable accessible to its Jenkins
agent, or `python3` on Unix.
Each build creates a fresh `venv` and installs the pinned tools.

## Stages and build outputs

1. **Setup** creates the virtual environment and installs dependencies.
2. **Lint** checks the app, deployment script, and tests with flake8.
3. **Test** runs four tests and writes `reports/tests.xml` for Jenkins.
4. **Coverage** reruns the tests under coverage.py, measures the app's lines
   and branches, writes text/XML/HTML reports, and requires 100% coverage.
5. **Security Scan** scans `app.py` and `deploy.py` with Bandit. A finding
   fails the stage. The environment and test assertions are outside the scan.
6. **Deploy** copies the app outside the workspace, executes that copy, checks
   its greeting, records release details, and creates a ZIP artifact.

The pipeline publishes JUnit results and archives `reports/**/*` and
`dist/*.zip` before deleting the checkout and virtual environment. If a check
fails, later stages are skipped. No scan failure is suppressed.

The deployed app needs only Python's standard library. Jenkins releases remain
under `<JENKINS_HOME>/deployments/Python-CI-CD/build-<number>/`, separate from
the cleaned workspace. On this machine that base directory is:

```text
C:\Users\jenkins_svc\AppData\Local\Jenkins\.jenkins\deployments\Python-CI-CD
```

For a manual run, `deploy.py` uses `../deployments/build-local`. An optional
`--target PATH` selects a different destination outside the project. This is a
local command line application deployment; it does not start a web server.

Download the deployment ZIP from a successful build's **Artifacts** section.
Extract it and run `python app.py`. It also contains `release.json`.

## Lab handout adjustments

The sample app returned `Hello, World!`, while the required test expected a
student name. The app and tests now both use `Ali Naji`. The requirements also
include pytest, coverage, and Bandit because the full pipeline runs them.
The example's Unix activation commands were replaced with direct environment
Python calls so the same stages work with a Windows service account.
`deleteDir()` provides workspace cleanup without requiring `cleanWs()`.

The job does not need remote SSH credentials because the lab permits local
deployment. Git, Pipeline, JUnit, and SSH Agent plugins are installed. Stage
View is also installed to help capture the successful stages.

## Submission

Replace all screenshot placeholders in the report using one successful Jenkins
build, save the Word document, and submit it with `Jenkinsfile_Ali_Naji` and
`github_link.txt` as required by Moodle. See `docs/JENKINS_STEPS.md` for the
exact screenshots. Keep `Jenkins_admin.txt` private and outside the repository.

## References

- Lab handout: `lab 10-jenkins.docx`, supplied in the parent workspace.
- Jenkins Windows commands: https://www.jenkins.io/doc/pipeline/tour/running-multiple-steps/
- Jenkins test results and artifacts: https://www.jenkins.io/doc/pipeline/tour/tests-and-artifacts/
- coverage.py: https://coverage.readthedocs.io/
- Bandit: https://bandit.readthedocs.io/
