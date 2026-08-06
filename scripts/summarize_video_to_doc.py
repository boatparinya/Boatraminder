import os
import sys
import pickle
import io
import tempfile
import subprocess

# Reconfigure stdout for UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ============================
# CONFIG
# ============================
FILE_ID = "1EdX8PNFdH0H-QCHwchykR4NAmQs_SvxI"
DOC_TITLE = "🫁 สรุป: Control of Respiration in Dog"
TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'token.pickle')
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
]

def get_credentials():
    from google.auth.transport.requests import Request
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            creds_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def download_video(creds, file_id, dest_path):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    print("📥 กำลังดาวน์โหลดวิดีโอจาก Google Drive...")
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    with open(dest_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request, chunksize=10*1024*1024)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"   ⬇️  ดาวน์โหลดแล้ว {int(status.progress() * 100)}%")
    print(f"✅ ดาวน์โหลดสำเร็จที่: {dest_path}")

def extract_audio(video_path, audio_path):
    print("🎵 กำลังแยกเสียงจากวิดีโอ...")
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'pcm_s16le',
         '-ar', '16000', '-ac', '1', audio_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("❌ ffmpeg error:", result.stderr[-500:])
        raise RuntimeError("ffmpeg ไม่สามารถแยกเสียงได้ค่ะ")
    print(f"✅ แยกเสียงสำเร็จที่: {audio_path}")

def transcribe_audio(audio_path):
    print("🎙️ กำลังถอดเสียงเป็นข้อความ (Whisper)...")
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="th", verbose=False)
        text = result["text"]
        print(f"✅ ถอดเสียงสำเร็จ ({len(text)} ตัวอักษร)")
        return text
    except ImportError:
        print("⚠️  ไม่พบ whisper กำลังติดตั้ง...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'openai-whisper'], check=True)
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="th", verbose=False)
        return result["text"]

def summarize_with_gemini(transcript_text):
    """ใช้ Google Gemini API สรุปเนื้อหาจาก transcript"""
    print("🤖 กำลังสรุปเนื้อหาด้วย AI...")
    try:
        import google.generativeai as genai
        # ลอง load API key จาก env
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            # อ่านจาก .env
            env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('GEMINI_API_KEY=') or line.startswith('GOOGLE_API_KEY='):
                            api_key = line.strip().split('=', 1)[1]
                            break
        if not api_key:
            raise ValueError("ไม่พบ GEMINI_API_KEY ใน .env")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""คุณเป็นผู้ช่วยสรุปเนื้อหาวิชาการ กรุณาสรุปเนื้อหาต่อไปนี้ให้ครบถ้วน ถูกต้อง และอ่านง่าย
โดยเนื้อหาเป็นเรื่อง "Control of Respiration in Dog" (การควบคุมการหายใจในสุนัข) จากการบรรยายทางสรีรวิทยา

เนื้อหา transcript:
{transcript_text[:15000]}

กรุณาสรุปในรูปแบบต่อไปนี้ (เขียนเป็นภาษาไทย):
1. ภาพรวม (Overview)
2. กลไกการควบคุมการหายใจ (Mechanisms of Respiratory Control)
3. ศูนย์ควบคุมการหายใจในสมอง (Respiratory Centers in the Brain)
4. ปัจจัยที่มีผลต่อการหายใจ (Factors Affecting Respiration)
5. การทดลองในสุนัข (Experiments in Dogs) - ถ้ามีในเนื้อหา
6. สรุปสำคัญ (Key Takeaways)"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"⚠️ Gemini ใช้งานไม่ได้: {e}")
        # Fallback: สรุปแบบ basic จาก transcript
        return create_basic_summary(transcript_text)

def create_basic_summary(text):
    """สร้างสรุปเบื้องต้นจาก transcript โดยตรง"""
    summary = f"""สรุปเนื้อหา: Control of Respiration in Dog
(การควบคุมการหายใจในสุนัข)

=== เนื้อหาจากการบรรยาย ===

{text[:8000]}

=== หมายเหตุ ===
เนื้อหานี้ถอดจากคลิปวิดีโอการบรรยายทางสรีรวิทยา
"""
    return summary

def create_google_doc(creds, title, content):
    from googleapiclient.discovery import build
    print("📄 กำลังสร้าง Google Docs...")
    service = build('docs', 'v1', credentials=creds)

    # สร้างเอกสารเปล่า
    doc = service.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')

    # แบ่ง content เป็น sections สำหรับ formatting
    requests = []
    lines = content.split('\n')
    full_text = content + '\n'

    # Insert ทั้งหมดก่อน
    requests.append({
        'insertText': {
            'location': {'index': 1},
            'text': full_text
        }
    })

    service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()

    url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"✅ สร้าง Google Doc สำเร็จแล้วค่ะ!")
    print(f"🔗 ลิงก์: {url}")
    return url

def main():
    print("=" * 60)
    print("🫁 สรุปคลิป: Control of Respiration in Dog")
    print("=" * 60)

    creds = get_credentials()

    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, 'respiration.mp4')
        audio_path = os.path.join(tmpdir, 'respiration.wav')

        # Step 1: Download video
        download_video(creds, FILE_ID, video_path)

        # Step 2: Extract audio
        extract_audio(video_path, audio_path)

        # Step 3: Transcribe
        transcript = transcribe_audio(audio_path)

        # Step 4: Summarize
        summary = summarize_with_gemini(transcript)

        # Step 5: Create Google Doc
        doc_url = create_google_doc(creds, DOC_TITLE, summary)

    print("\n" + "=" * 60)
    print("🎉 เสร็จสมบูรณ์ค่ะเตง!")
    print(f"📄 Google Doc: {doc_url}")
    print("=" * 60)

if __name__ == '__main__':
    main()
