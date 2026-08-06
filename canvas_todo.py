import os
import sys
from canvasapi import Canvas
from dotenv import load_dotenv

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

API_URL = os.getenv("CANVAS_API_URL")
API_KEY = os.getenv("CANVAS_API_KEY")

canvas = Canvas(API_URL, API_KEY)

def get_todo_tasks():
    """ดึงรายการการบ้านหรือกำหนดการส่งงานที่กำลังจะถึง"""
    todos = canvas.get_todo_items()

    result = []
    for item in todos:
        assignment = getattr(item, 'assignment', None)
        if assignment and isinstance(assignment, dict):
            name = assignment.get('name', 'ไม่มีชื่อ')
            due_at = assignment.get('due_at', 'ไม่มีกำหนดส่ง')
            context_name = getattr(item, 'context_name', 'ไม่ระบุวิชา')
            result.append(f"- [{context_name}] {name} (ส่งวันที่: {due_at})")
        elif getattr(item, 'quiz', None):
            quiz = item.quiz
            name = quiz.get('title', 'ไม่มีชื่อ')
            due_at = quiz.get('due_at', 'ไม่มีกำหนดส่ง')
            context_name = getattr(item, 'context_name', 'ไม่ระบุวิชา')
            result.append(f"- [{context_name}] [Quiz] {name} (ส่งวันที่: {due_at})")
        else:
            html_url = getattr(item, 'html_url', '#')
            context_name = getattr(item, 'context_name', 'ไม่ระบุวิชา')
            result.append(f"- [{context_name}] งานอื่น ๆ: {html_url}")

    return "\n".join(result) if result else "ไม่มีการบ้านค้างส่งในขณะนี้"

if __name__ == "__main__":
    print(get_todo_tasks())
