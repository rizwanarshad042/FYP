# StockSense FYP Report

LaTeX source for the StockSense Final Year Project report.

## Files to know

- `main.tex` is the document entry point. Edit this file for report content.
- `StockSense.cls` contains the report layout, packages, headings, and citation configuration.
- `fypbib.bib` contains the bibliography records.
- `build.ps1` builds the final PDF on Windows.
- `latexmkrc` contains the optional `latexmk` configuration.

Generated files such as `.aux`, `.bbl`, `.blg`, `.lof`, `.log`, `.lot`, `.out`, `.toc`, and `.pdf` are build output. Do not edit them manually.

## Windows setup

Each group member needs the following software:

1. [Git for Windows](https://git-scm.com/download/win) for downloading the repository and sharing changes.
2. [MiKTeX](https://miktex.org/download) for compiling LaTeX. During installation, allow MiKTeX to install missing packages automatically.
3. [Visual Studio Code](https://code.visualstudio.com/) or another text editor.
4. The optional **LaTeX Workshop** VS Code extension for editing and previewing LaTeX.

The included build script uses the default per-user MiKTeX path:

```text
C:\Users\<your-user>\AppData\Local\Programs\MiKTeX\miktex\bin\x64
```

If MiKTeX was installed somewhere else, edit the `$miktexBin` value in `build.ps1` or use the direct commands below.

## Download the project

Open PowerShell and run:

```powershell
git clone https://github.com/<github-username>/<repository-name>.git
cd <repository-name>
code .
```

Replace the URL and folder name with the values for the group's GitHub repository. In VS Code, open `main.tex` to edit the report.

## Build the PDF

From the project folder, run:

```powershell
.\build.ps1
```

The script runs `pdflatex`, BibTeX, and two additional LaTeX passes. The final report is written to:

```text
F26-131.pdf
```

Open that PDF to review the report. Multiple LaTeX passes are required so that the table of contents, list of figures, list of tables, cross-references, and bibliography are updated correctly.

### If PowerShell blocks the script

Allow scripts only for the current PowerShell session, then run the build again:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build.ps1
```

### Direct build commands

If the script cannot find MiKTeX, run these commands after confirming that `pdflatex` and `bibtex` are available in your `PATH`:

```powershell
pdflatex -jobname=F26-131 -interaction=nonstopmode -file-line-error main.tex
bibtex F26-131
pdflatex -jobname=F26-131 -interaction=nonstopmode -file-line-error main.tex
pdflatex -jobname=F26-131 -interaction=nonstopmode -file-line-error main.tex
```

If BibTeX reports missing packages or fonts, open MiKTeX Console, install pending updates, and run the build again.

## Editing workflow

1. Pull the latest version before editing:

   ```powershell
   git switch main
   git pull
   ```

2. Create a branch for your change:

   ```powershell
   git switch -c update-literature-review
   ```

3. Edit `main.tex`, `fypbib.bib`, `StockSense.cls`, or files under `Figures/`.
4. Build the PDF and check the log for errors or unresolved references.
5. Review the generated `F26-131.pdf` before sharing the change.
6. Commit and push the source changes:

   ```powershell
   git status
   git add main.tex fypbib.bib StockSense.cls Figures/
   git commit -m "Update literature review"
   git push -u origin update-literature-review
   ```

7. Open a pull request on GitHub. Ask another group member to review it before merging.

Do not edit the same section at the same time without coordinating. LaTeX is plain text, so overlapping edits can create merge conflicts. Resolve conflicts in source files, then rebuild the PDF; never resolve conflicts by manually editing generated `.aux`, `.bbl`, or `.toc` files.

## Cleaning build output

To remove the auxiliary files created by `latexmk`, run:

```powershell
latexmk -C main.tex
```

The build script uses the `F26-131` job name, so remove its generated files only when needed and do not delete source files such as `main.tex`, `StockSense.cls`, `fypbib.bib`, or anything under `Figures/`.

## GitHub authentication

GitHub does not accept account passwords for Git over HTTPS. Use a GitHub Personal Access Token when Git asks for a password, or configure SSH and use the SSH repository URL instead.
