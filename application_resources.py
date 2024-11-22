import os

class IconPaths:
    PENCIL_ICON="assets/pencil_icon.png"
    PLAY_ICON="assets/play_icon.png"
    PAUSE_ICON="assets/pause_icon.png"
    DELETE_ICON="assets/delete_icon.png"
    EYE_OPEN_ICON="assets/eye_icon.png"

class JsonFiles:
    SUBJECT_CODE_REFERENCE="json_files/subjects.json"

class ApplicationPaths:
    DATABASE_PATH=os.getenv("APPDATA")+"\\OnlineExaminator"
    QUESTION_PAPER_DIR=os.path.join(DATABASE_PATH, "question_papers")
    USER_CREDENTIALS_FILE=os.path.join(DATABASE_PATH, "users.json")
    RESULT_DIR=os.path.join(DATABASE_PATH, "results")

class PrintingLayoutPaths:
    RESULT_LAYOUT="assets/HTML_PrintLayout/ResultLayout/result_page.html"