# Coding Agent Guide (dirsearch GUI)

This repository contains **dirsearch GUI**, a PyQt6-based graphical user interface for the dirsearch web path discovery tool. Use this guide to keep changes aligned with project expectations and development workflows.

## Scope
- These instructions apply to the entire repository.
- If a subdirectory contains its own `AGENTS.md`, that file takes precedence for that subtree.

## Project overview (high-level map)
- **Entrypoint**: `admin.py` is the main GUI application entry point.
- **Core functionality**: Provides a graphical interface for the dirsearch CLI tool, allowing users to configure and execute web path discovery scans.
- **Backend**: Interacts with the original dirsearch tool in `dirsearch-master/` directory.
- **UI**: Built with PyQt6, featuring tabbed parameter configuration and command preview.

## Directory structure (quick map)
- `admin.py`: Main GUI application code
- `dirsearch-master/`: Original dirsearch tool source code
  - `dirsearch.py`: CLI entry point for dirsearch
  - `lib/`: Core application modules (controller, connection, core, parse, report, utils, view)
  - `db/`: Default wordlists and blacklists
  - `config.ini`: Default configuration file
  - `pyinstaller/`: PyInstaller build configuration
  - `sessions/`: Default session storage location
  - `static/`: Static assets (logo images)
  - `tests/`: Test files
  - `.github/workflows/`: CI/CD workflows
- `参数.md`: Parameter documentation
- `ui.md`: UI documentation
- `提示文件.md`: Instruction files

## Code style and architecture
- Prefer **pythonic** code: clear naming, readable structure, and small, testable functions.
- Use **object-oriented design** with PyQt6 for UI components, keeping UI logic separate from business logic.
- Maintain clean separation between GUI components and dirsearch execution.
- Add **comments for edge cases** so behavior is clear to future maintainers.
- Follow PyQt6 best practices for GUI development.

## When you change X, check Y (dependency map)
Use this section to keep side effects aligned and to avoid missing required updates.

### GUI / UI changes
- If you modify the GUI layout or controls:
  - Verify the command preview updates correctly with new parameters
  - Update parameter validation and linking logic if needed
  - Ensure config saving/loading includes new parameters

### dirsearch backend integration
- If you modify how the GUI calls dirsearch:
  - Verify all command-line options are correctly passed through the interface
  - Update the command preview functionality accordingly
  - Test with various parameter combinations to ensure proper execution

### Parameter handling
- If you add or modify parameter inputs:
  - Update the `update_command_preview` method to include the new parameter
  - Add validation logic if required
  - Update config save/load methods to handle the new parameter
  - Update parameter linking logic in `init_parameter_links`

### Configuration handling
- If you modify the config save/load functionality:
  - Update both `save_config` and `load_config` methods
  - Ensure JSON serialization handles new data types correctly
  - Update the data structures used for config persistence

### UI components
- If you add or modify UI elements:
  - Consider updating the styling to maintain visual consistency
  - Add appropriate tooltips and placeholder text
  - Maintain logical grouping of related parameters

### Standalone execution
- If you modify how the tool executes:
  - Ensure the standalone CMD window execution works properly
  - Update error handling if execution method changes
  - Maintain cross-platform compatibility for execution

## Current automation (quick reference)
- **Execution**: Direct Python execution of the admin.py script
- **Build**: No specific build system - runs as a Python script with required dependencies

## Testing guidance
- For UI changes, run the GUI and test parameter modifications to ensure:
  - Command preview updates correctly
  - Parameters are properly passed to dirsearch
  - Config saving/loading works
- For functionality changes, test various parameter combinations
- Verify the standalone CMD window execution works as expected

## Communication checklist (for summaries / PRs)
- What changed and why.
- Any updates to UI functionality or parameters.
- Whether configuration handling was affected.
- Tests executed and their results.