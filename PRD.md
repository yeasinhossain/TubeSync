# YouTube Metadata Update Tool

## Objective
Develop a GUI-based tool that automates updating video titles, descriptions, and tags on multiple YouTube channels by replacing specific text (e.g., replacing "2024" with "2025"). The tool should be user-friendly for non-technical team members, allowing them to:
1. Replace specific text in metadata.
2. Switch between multiple channels and repeat the process.

---

## Features

### Core Features
1. **Authentication**
   - OAuth 2.0 authentication for secure access to YouTube accounts.
   - Allow switching between multiple YouTube channels by logging into different Google accounts.

2. **Fetch Videos**
   - Retrieve a list of all videos from the authenticated YouTube channel.
   - Fetch metadata, including titles, descriptions, and tags.

3. **Update Metadata**
   - Replace specified text in video titles, descriptions, and tags.
   - Push updated metadata to YouTube using the API.

4. **User Input**
   - Specify:
     - Text to replace.
     - Replacement text.
   - Apply updates selectively based on:
     - Date range.
     - Specific keywords in the title or description.
   - Enable bulk updates for all videos in a channel.

5. **Graphical User Interface (GUI)**
   - Design a user-friendly GUI to:
     - Authenticate and switch between channels.
     - Input replacement parameters (old text and new text).
     - Display a list of videos with preview options for metadata before and after changes.
     - Log and show progress for each update.
     - Export logs for review.

6. **Multi-Channel Support**
   - Allow the user to log out and log in with different Google accounts to manage multiple channels.
   - Save previous channel metadata locally (or in logs) for reference.

7. **Error Handling**
   - Handle API errors, invalid inputs, and connectivity issues gracefully.
   - Provide clear error messages in the GUI.

8. **Logging**
   - Log details of all updates, including:
     - Video ID
     - Old metadata
     - Updated metadata
   - Provide options to export logs in CSV format.

---

## User Flow

1. **Channel Selection**
   - User logs into a Google account via the GUI.
   - The tool fetches a list of videos for the selected YouTube channel.
   - After completing updates, the user can switch to another channel by logging into a different Google account.

2. **Specify Replacement Details**
   - User inputs:
     - Text to be replaced.
     - Replacement text.
   - Optionally filters videos by:
     - Date range.
     - Specific keywords.

3. **Preview and Update**
   - The tool displays a list of videos with:
     - Current titles, descriptions, and tags.
     - A preview of changes after replacement.
   - User reviews and confirms the updates.

4. **Progress and Logs**
   - The tool shows real-time progress during updates.
   - After completion, a log is displayed with an option to export the log file.

---

## Technical Requirements

### Language
- Primary: Python (or as recommended by the AI IDE).

### APIs
- YouTube Data API v3 for video management.

### Authentication
- OAuth 2.0 for secure access to multiple YouTube accounts.

### Libraries (for Python)
- `google-auth`
- `google-auth-oauthlib`
- `google-api-python-client`
- GUI libraries: 
  - `tkinter` (basic GUI)
  - `PyQt` or `PySide2` (for more advanced GUI features).

### Environment
- Local or desktop-based application.

---

## Development Steps

1. **Set Up Google Cloud Project**
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **YouTube Data API v3**.
   - Generate OAuth 2.0 credentials and download the `credentials.json` file.

2. **Set Up Development Environment**
   - Install required dependencies:
     ```bash
     pip install google-auth google-auth-oauthlib google-api-python-client PyQt5
     ```

3. **Design GUI**
   - Create a GUI with the following elements:
     - **Login/Logout Button**: Authenticate and switch between accounts.
     - **Input Fields**: Text to replace and replacement text.
     - **Filters**: Date range and keywords.
     - **Video List**: Display videos with metadata and a preview of changes.
     - **Progress Bar**: Show update progress.
     - **Export Button**: Save logs to CSV.

4. **Implement Authentication**
   - Allow login/logout functionality to switch between YouTube accounts.
   - Save authentication tokens locally for session management.

5. **Fetch Videos**
   - Use the `videos.list` API to retrieve video metadata:
     - Title
     - Description
     - Tags
   - Populate the video list in the GUI.

6. **Replace Metadata**
   - Implement text replacement logic for:
     - Titles
     - Descriptions
     - Tags
   - Allow bulk or selective updates.

7. **Push Updates**
   - Use the `videos.update` API to push metadata changes back to YouTube.

8. **Handle Multi-Channel Support**
   - Enable logout/login to switch accounts.
   - Ensure the tool resets data and logs between sessions.

9. **Logging**
   - Log all updates with video IDs, old metadata, and new metadata.
   - Add an option to export logs as a CSV file.

10. **Testing**
    - Test for:
      - GUI usability.
      - Text replacement accuracy.
      - API quota management.
    - Validate error handling and edge cases.

11. **Deployment**
    - Package as a standalone desktop app using tools like `PyInstaller` or `cx_Freeze`.

---

## Sample GUI Layout

### Main Window
- **Login/Logout Button**: Top-right corner.
- **Input Section**:
  - Old Text: Input field.
  - New Text: Input field.
  - Filters: Date range, keywords.
  - Submit Button.
- **Video List**:
  - Table displaying:
    - Video Title
    - Description
    - Tags
    - Preview of changes.
- **Progress Bar**: Bottom of the window.
- **Export Logs Button**: Below the video list.

---

## Deliverables
- A GUI-based tool for managing YouTube metadata.
- Multi-channel support with seamless account switching.
- Exportable logs of updates for review.

---

## Additional Notes
- **Usability**: Ensure the GUI is simple enough for non-technical users.
- **Scalability**: Allow the tool to handle large video libraries without performance issues.
- **API Quota**: Monitor YouTube API quota usage and notify the user if limits are reached.

---

This PRD should now fully encompass your requirements. Let me know if any further adjustments are needed!