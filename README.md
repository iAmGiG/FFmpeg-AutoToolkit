# FFmpeg-AutoToolkit

## Technical Details

---

### Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)

---

## Project Overview

`FFmpeg-AutoToolkit` is a Python-based cross-platform application designed to automate the process of downloading, installing, and utilizing FFmpeg for audio and video processing tasks. The project features both a graphical user interface (GUI) using **PyQt6** and a command-line interface using **absl-py**.

The application supports both **Windows** and **Linux** platforms, providing users with an efficient way to work with FFmpeg without requiring manual installation or setup.

---

## Features

- **Cross-Platform FFmpeg Installation**
  - Automatically detects if FFmpeg is installed on the system.
  - Downloads and installs FFmpeg if it is missing.
  - Supports both Windows and Linux platforms.
  - Allows users to specify a custom FFmpeg path.

- **PyQt6 GUI**
  - Intuitive interface for selecting files, merging audio tracks, and converting video formats.
  - Provides a progress bar for FFmpeg operations.
  - Error handling with informative pop-up messages.

- **Console-Only Version**
  - Provides all features available in the GUI through a console interface.
  - Uses `absl-py` for easy command-line argument parsing.
  - Supports verbose logging and error handling for advanced users.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/FFmpeg-AutoToolkit.git
cd FFmpeg-AutoToolkit
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

For the GUI version:

```bash
python -m ffmpeg_autotoolkit.gui.main_window
```

For the Console version:

```bash
python -m ffmpeg_autotoolkit.console.console_app --help
```
