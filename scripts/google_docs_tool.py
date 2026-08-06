import sys
import os
import pickle
from googleapiclient.discovery import build

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_doc_with_content(title, content):
    """สร้างไฟล์ Google Doc ใหม่ และใส่เนื้อหาลงไป"""
    if not os.path.exists('token.pickle'):
        raise FileNotFoundError("Error: ไม่พบไฟล์ token.pickle กรุณารัน scripts/authenticate_google.py ก่อนนะคะ")
        
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('docs', 'v1', credentials=creds)

    # 1. สร้างเอกสารเปล่า
    doc = service.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')

    # 2. ใส่เนื้อหาลงในเอกสาร
    requests = [{'insertText': {'location': {'index': 1}, 'text': content}}]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

    return f"https://docs.google.com/document/d/{doc_id}/edit"

if __name__ == "__main__":
    # รับค่าจาก Command Line (ชื่อเรื่อง และ เนื้อหา)
    doc_title = sys.argv[1] if len(sys.argv) > 1 else "สรุปเนื้อหาจาก Canvas"
    doc_content = sys.argv[2] if len(sys.argv) > 2 else "ไม่มีเนื้อหา"
    url = create_doc_with_content(doc_title, doc_content)
    print(f"สร้างเอกสารเรียบร้อยแล้ว: {url}")
