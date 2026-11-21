# Jenkins dashboard and report screenshots

The job has been configured to load `Jenkinsfile_Ali_Naji` from this repository's
`main` branch. Jenkins is running at http://localhost:8080/ as `jenkins_svc`.

## Run the latest repository version

1. Open http://localhost:8080/job/Python-CI-CD/ and sign in if needed.
2. If the configuration page from the supplied screenshot is still open,
   refresh it before saving. It was open before the saved job was completed.
3. Under **Configure > Pipeline**, the settings should be:
   - Definition: **Pipeline script from SCM**.
   - SCM: **Git**.
   - Repository URL: `https://github.com/Vortexx-hash/AliNaji-EECE435L-Lab10.git`.
   - Credentials: **none**, since this repository is public.
   - Branch Specifier: `*/main`.
   - Script Path: **`Jenkinsfile_Ali_Naji`**, with the exact name and capitalization.
   - Lightweight checkout: enabled.
4. Click **Build with Parameters**. Set `PYTHON_EXECUTABLE` to
   `C:/Users/Public/JenkinsTools/Python310/python.exe` and click **Build**.
   This is also the final Jenkinsfile's default value.
5. Open the new build and its **Console Output**. The six stages are Setup,
   Lint, Test, Coverage, Security Scan, and Deploy. Check `Finished: SUCCESS`.
6. Open **Test Result** for the four tests. Open **Artifacts** for the saved
   reports and `dist/ali-naji-lab10.zip`. Jenkins removes the workspace after
   saving these files; that cleanup is expected.

No webhook is required for a manual build. Pushing a commit alone does not
trigger this job automatically. If automatic builds are wanted later, enable
**Poll SCM** with a schedule such as `H/5 * * * *`. A GitHub webhook needs an
address GitHub can reach; `localhost:8080` is only available on this computer.

## Replace the four report placeholders

Use the same successful build number for all four screenshots. In Word, delete
each placeholder paragraph and insert the matching image in that position.
Keep the caption underneath it. Use **In Line with Text** and fit the image
within the page margins. Each placeholder has room for a wide screenshot.

1. **S1 Pipeline success**: the job's Stage View showing all six stages green
   and the successful build number. If Stage View needs a page reload after
   plugin installation, refresh the dashboard. The build page and Pipeline
   Steps view can also show the stage outcomes.
2. **S2 Tests and coverage**: Console Output around `4 passed` and the
   `coverage report` table showing `100%`. The Jenkins Test Result page can be
   included as an additional image if the console needs two captures.
3. **S3 Security scan**: open the successful build's archived
   `reports/bandit.txt`. Capture `No issues identified` and the zero issue
   counts. The JSON artifact records the same scan results.
4. **S4 Deployment**: Console Output near the end showing the release path,
   `Deployment smoke test: PASS`, `Hello, World from Ali Naji!`, and
   `Finished: SUCCESS`.

Optional evidence: a configuration screenshot with repository URL, `*/main`,
and `Jenkinsfile_Ali_Naji`. Keep credentials, tokens, and passwords out of all
screenshots. Installation screenshots are not necessary for the brief report
unless the instructor asks for them.

## Submission

- Finish the screenshot placeholders in `Lab10_Report_Ali_Naji.docx`.
- Submit the report and `Jenkinsfile_Ali_Naji` for Part 4.
- Submit `github_link.txt` for the GitHub link requested in Part 3.
- The repository also contains the source, tests, and saved build evidence.
- After inserting images, commit and push the updated report if the GitHub
  copy should include the screenshots:

```powershell
git add Lab10_Report_Ali_Naji.docx
git commit -m "Add Jenkins screenshots to lab report"
git push
```

The SSH Agent plugin is installed, but this local deployment needs no SSH key,
remote host, or extra Jenkins credential. Stage View was also installed.
