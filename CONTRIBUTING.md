# Contributing to Qtile-Con

First off, thank you for considering contributing to **Qtile-Con**! Open-source projects thrive on community collaboration, feedback, and passion.

---

## 💖 Community Spirit: Be Kind

We want this project to be a welcoming, inclusive, and friendly environment for everyone, regardless of experience level, background, or identity.

- **Be kind and respectful**: Treat others with empathy and patience. We are all learning and building together.
- **Be constructive**: Provide thoughtful, helpful, and courteous feedback when reviewing code or discussing issues.
- **Be welcoming**: Help newcomers feel at home and encourage questions.
- **Assume good intent**: Most contributions are made with the best intentions. Approach misunderstandings with grace and open communication.

---

## How Can I Contribute?

### 1. Reporting Bugs
- Check the [Issue Tracker](https://github.com/Opposum0112/Qtile-con/issues) first to see if your bug has already been reported.
- When filing a new issue, include:
  - Your host operating system and distribution (e.g. Parrot OS, Arch, Fedora, Void, FreeBSD).
  - Qtile version (`qtile --version`).
  - Clear steps to reproduce the bug.
  - Relevant logs or output from `~/.config/qtile/scripts/check-config` or `~/.local/share/qtile/qtile.log`.

### 2. Suggesting Enhancements & New Features
- Open an issue tagged `enhancement` describing the idea.
- Outline why the feature would be beneficial and how it fits within the modular, lean architecture of Qtile-Con.

### 3. Submitting Code Contributions

1. **Fork and Clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/Qtile-con.git
   cd Qtile-con
   ```

2. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **Follow Project Architectural Standards**:
   - **Maintain Lean Memory (< 800 MB)**: Do not add persistent heavy background daemons or memory-hogging processes to `scripts/autostart`. The idle memory footprint should remain light (~150 MB baseline).
   - **Multi-Distro Compatibility**: Changes to `install.sh` or `uninstall.sh` must remain OS-aware and support all 8 target ecosystems (`apt`, `pacman`, `dnf`, `zypper`, `eopkg`, `xbps`, `pkg`, `emerge`).
   - **Unified PATH Resolution**: Always use standard script wrappers (`qtile-run`, `qtile-action`) or resolve tools via `$PATH` rather than hardcoding personal system paths.
   - **Privacy & Sanitization**: Never commit personal usernames, private IP addresses (`192.168.*`, `10.*`), or secret credentials.

4. **Verify Tests & Syntax**:
   - Ensure shell scripts are error-free:
     ```bash
     bash -n install.sh uninstall.sh scripts/*
     ```
   - Validate Qtile configuration and types:
     ```bash
     ./scripts/check-config
     ```
   - Run the master test suite:
     ```bash
     python3 -m unittest discover -s tests -v
     ```
   - **Note on Test Suite Size**: Keep the test suite compact and unified (**strictly no more than 10 total tests**). If adding new test coverage, integrate it into the existing comprehensive test categories in `tests/test_suite.py`.

5. **Commit with Clear Messages**:
   - Write clear, concise, and descriptive commit messages summarizing what changed and why.

6. **Submit a Pull Request**:
   - Push your branch to GitHub and open a Pull Request against the `main` branch.
   - Provide a brief summary of the changes and confirm all validation checks pass.

### 🤖 AI-Assisted Contributions
Contributions generated with or assisted by AI models are welcome! However, contributors are responsible for reviewing, testing, understanding, and validating any AI-generated code to ensure it meets our quality, safety, and architectural standards.

---

## Acknowledgements

A heartfelt thank you to:
- The **[Qtile Community](https://qtile.org)**, core maintainers, and contributors for building an incredible, hackable tiling window manager.
- The global **Open Source and Linux Community** whose collective tooling, libraries, and philosophies make projects like Qtile-Con possible.
- Everyone who tests, files issues, suggests improvements, or contributes code.

Thank you for helping make Qtile-Con better for everyone!

