import os
import sys
import argparse
import tempfile
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright, Error

# Reconfigure stdout to support UTF-8 (Thai characters) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_default_chrome_user_data_dir():
    """ค้นหาตำแหน่งโฟลเดอร์ Chrome User Data เริ่มต้นบน Windows"""
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        path = Path(local_app_data) / "Google" / "Chrome" / "User Data"
        if path.exists():
            return str(path)
    return None

def run_chrome_automation(action, url, output_path=None, headless=True, user_data_dir=None, profile="Default"):
    """
    ฟังก์ชันหลักในการควบคุม Chrome ด้วย Playwright
    """
    if not user_data_dir:
        user_data_dir = get_default_chrome_user_data_dir()
        
    print(f"[*] เริ่มต้นระบบอัตโนมัติ: Headless={headless}, Action={action}")
    print(f"[*] กำหนดการใช้ User Data Dir: {user_data_dir}")
    print(f"[*] Profile: {profile}")
    
    with sync_playwright() as p:
        browser_context = None
        browser = None
        is_persistent = False
        
        # พยายามเปิด Chrome ด้วย Profile จริงแบบ Persistent Context
        if user_data_dir:
            try:
                # Playwright ต้องการพาธแยกเฉพาะสำหรับ profile (ระบุผ่าน args หรือยึดตามโครงสร้างของ Playwright)
                # สำหรับ launch_persistent_context ใน Playwright:
                # user_data_dir คือโฟลเดอร์หลัก "User Data" และ default profile จะเป็น "Default"
                # หากต้องการใช้ Profile อื่น สามารถระบุได้โดยใช้ user_data_dir ชี้ตรงไปยังโฟลเดอร์อื่น
                # หมายเหตุ: หาก Chrome เปิดอยู่ จะไม่สามารถใช้งานโฟลเดอร์นี้ซ้ำได้ (จะติด Lock)
                browser_context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    channel="chrome",
                    headless=headless,
                    args=[
                        f"--profile-directory={profile}",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage"
                    ]
                )
                is_persistent = True
                print("[+] ล็อกอิน/เชื่อมต่อด้วย Chrome Profile สำเร็จ!")
            except Error as e:
                error_msg = str(e)
                print(f"[!] ไม่สามารถเปิด Chrome Profile จริงได้เนื่องจาก: {error_msg}")
                if "is already running" in error_msg or "lock" in error_msg or "in use" in error_msg.lower():
                    print("[!] สาเหตุ: Chrome ของเตงกำลังทำงานอยู่และล็อกไฟล์ Profile นี้ไว้")
                    print("[*] กำลังลองเชื่อมต่อแบบไม่ใช้ Profile เดิม (สร้าง Temporary Session แทน)...")
                
                # ทำการ fallback ไปเปิด Browser ปกติ (ไม่เชื่อมโยงโปรไฟล์ที่ถูกล็อก)
                try:
                    browser = p.chromium.launch(
                        channel="chrome",
                        headless=headless,
                        args=["--no-sandbox", "--disable-setuid-sandbox"]
                    )
                    browser_context = browser.new_context()
                    print("[+] สร้าง Temporary Chrome Session สำเร็จ (หมายเหตุ: จะไม่มีประวัติการล็อกอินเดิมของเตง)")
                except Error as fallback_err:
                    print(f"[-] ล้มเหลวในการเปิด Chrome (Fallback): {fallback_err}")
                    sys.exit(1)
        else:
            # หากไม่พบโฟลเดอร์ User Data ให้เปิดเบราว์เซอร์ใหม่ธรรมดา
            try:
                browser = p.chromium.launch(
                    channel="chrome",
                    headless=headless,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                browser_context = browser.new_context()
                print("[+] เปิด Temporary Chrome Session (เนื่องจากไม่พบโฟลเดอร์ User Data)")
            except Error as err:
                print(f"[-] ไม่สามารถเริ่มต้น Chrome ได้: {err}")
                sys.exit(1)
                
        try:
            page = browser_context.new_page()
            
            # ปรับปรุง User-Agent เพื่อไม่ให้เว็บตรวจจับว่าเป็นบอท
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            
            print(f"[*] กำลังเดินทางไปยังหน้าเว็บ: {url} ...")
            # โหลดหน้าเว็บและรอจนโหลดเนื้อหาหลักสำเร็จ
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # รอเพิ่มเล็กน้อยเพื่อให้แน่ใจว่า Dynamic JS รันแล้ว
            page.wait_for_timeout(3000)
            
            if action == "get_content":
                # ดึงเนื้อหาข้อความทั้งหมด
                title = page.title()
                text_content = page.locator("body").inner_text()
                print(f"\n=== Title: {title} ===")
                print(f"\n--- Text Content (First 1500 chars) ---\n")
                print(text_content[:1500])
                print(f"\n--------------------------------------\n")
                
                # บันทึกเนื้อหาเต็มลงไฟล์หากมีการกำหนด output_path
                if output_path:
                    output_file = Path(output_path)
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    output_file.write_text(f"Title: {title}\nURL: {url}\n\n{text_content}", encoding="utf-8")
                    print(f"[+] บันทึกเนื้อหาฉบับเต็มลงไฟล์: {output_file.absolute()} สำเร็จ")
                    
            elif action == "screenshot":
                if not output_path:
                    output_path = "screenshot.png"
                
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # ถ่ายภาพหน้าจอแบบเต็มหน้า
                page.screenshot(path=str(output_file), full_page=True)
                print(f"[+] แคปหน้าจอสำเร็จและเซฟไว้ที่: {output_file.absolute()}")
                
        except Exception as run_err:
            print(f"[-] เกิดข้อผิดพลาดขณะทำงานบนหน้าเว็บ: {run_err}")
        finally:
            # ปิดการทำงาน
            if browser_context:
                try:
                    browser_context.close()
                except Exception:
                    pass
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
            print("[*] ปิดระบบอัตโนมัติเรียบร้อย")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gigi's Chrome Automation Tool")
    parser.add_argument("action", choices=["get_content", "screenshot"], help="การทำงาน: get_content (ดึงข้อความ) หรือ screenshot (แคปหน้าจอ)")
    parser.add_argument("url", help="URL ของเว็บไซต์ที่ต้องการเข้าถึง")
    parser.add_argument("--output", "-o", help="พาธสำหรับเซฟผลลัพธ์ (ข้อความ/รูปภาพ)")
    parser.add_argument("--headed", action="store_true", help="เปิดเบราว์เซอร์แบบแสดงหน้าจอ (Default เป็น Headless)")
    parser.add_argument("--profile", default="Default", help="ชื่อโฟลเดอร์ Chrome Profile (Default: Default)")
    parser.add_argument("--user-data-dir", help="พาธเต็มของ Chrome User Data Directory")
    
    args = parser.parse_args()
    
    # กำหนดโหมด headless
    headless = not args.headed
    
    run_chrome_automation(
        action=args.action,
        url=args.url,
        output_path=args.output,
        headless=headless,
        user_data_dir=args.user_data_dir,
        profile=args.profile
    )
