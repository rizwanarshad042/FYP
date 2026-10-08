# StockSense FYP Report

LaTeX source for the StockSense Final Year Project report.

## Project files

- `main.tex` is the document entry point.
- `StockSense.cls` contains the report formatting and packages.
- `fypbib.bib` contains the bibliography entries.
- `Figures/` contains all logos, screenshots, diagrams, and sequence diagrams.

## Run locally on Windows

1. Install [Git for Windows](https://git-scm.com/download/win).
2. Install [MiKTeX](https://miktex.org/download) and select the option to install missing packages automatically when prompted.
3. Install [Perl](https://strawberryperl.com/) if `latexmk` is not included with your TeX installation.
4. Open a new PowerShell window in this project folder.
5. Build the report:

   ```powershell
   .\build.ps1
   ```

   This runs LaTeX and BibTeX as needed and creates `main.pdf`. Build output is ignored by Git. The script uses MiKTeX's installation path directly, so it works even when PowerShell has not refreshed its `PATH`.

   If PowerShell blocks local scripts, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\build.ps1
   ```

   If `latexmk` reports that Perl is blocked or unavailable, run the underlying commands directly:

   ```powershell
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```

6. Clean generated files when needed:

   ```powershell
   latexmk -C main.tex
   ```

You can also install the VS Code extension **LaTeX Workshop**, open `main.tex`, and use its build command.

## Collaborate through GitHub

One group member should create an empty GitHub repository, then run these commands from this folder:

```powershell
git init
git add .
git commit -m "Add StockSense FYP report"
git branch -M main
git remote add origin https://github.com/<github-username>/<repository-name>.git
git push -u origin main
```

Replace the remote URL with the repository URL from GitHub. Each group member can then clone it:

```powershell
git clone https://github.com/<github-username>/<repository-name>.git
cd <repository-name>
```

For each new change, use a branch and pull request:

```powershell
git switch -c update-introduction
git add main.tex Figures/
git commit -m "Update introduction"
git push -u origin update-introduction
```

Open a pull request on GitHub and merge it after another group member reviews it. Before starting new work, update your local copy:

```powershell
git switch main
git pull
```

Do not edit the same section at the same time without coordinating first; LaTeX files are text files and conflicting edits may need manual resolution.

## GitHub access

GitHub no longer accepts account passwords for Git over HTTPS. When prompted for a password, use a GitHub Personal Access Token, or configure SSH and use the SSH repository URL instead.
