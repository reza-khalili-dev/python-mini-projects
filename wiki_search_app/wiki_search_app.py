import wikipedia as wiki
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import scrolledtext, messagebox


wiki.set_lang("fa")

# ساخت پنجره اصلی
app = tb.Window(themename="superhero")
app.title("📚 جستجو در ویکی‌پدیا")
app.geometry("700x520")
app.resizable(False, False)

# عنوان
title_label = tb.Label(app, text="🔍 جستجو در ویکی‌پدیا", font=("Segoe UI", 18, "bold"))
title_label.pack(pady=(14, 6))

# فریم ورودی و دکمه‌ها
top_frame = tb.Frame(app)
top_frame.pack(padx=20, pady=6, fill=X)

entry = tb.Entry(top_frame, font=("Segoe UI", 14), width=42, bootstyle="info")
entry.pack(side=LEFT, padx=(0, 8))
entry.focus_set()

search_btn = tb.Button(top_frame, text="جستجو", width=12, command=lambda: search_wiki(), bootstyle="success")
search_btn.pack(side=LEFT)

clear_btn = tb.Button(top_frame, text="پاک‌سازی", width=10, command=lambda: clear_all(), bootstyle="warning-outline")
clear_btn.pack(side=LEFT, padx=(8,0))

# وضعیت (Status)
status_var = tb.StringVar()
status_var.set("آماده. یک عبارت وارد کنید و Enter را بزنید یا روی جستجو کلیک کنید.")
status_label = tb.Label(app, textvariable=status_var, font=("Segoe UI", 10), anchor="w")
status_label.pack(fill=X, padx=20, pady=(6,0))

# جعبه متن اسکرول‌دار برای نمایش نتیجه
result_box = scrolledtext.ScrolledText(app, wrap='word', font=("Segoe UI", 12), height=18)
result_box.pack(padx=20, pady=12, fill=BOTH, expand=True)
result_box.configure(state='disabled')  # پیش‌فرض غیرقابل ویرایش

# توابع
def set_status(text):
    status_var.set(text)
    app.update_idletasks()

def clear_all():
    entry.delete(0, 'end')
    result_box.configure(state='normal')
    result_box.delete(1.0, "end")
    result_box.configure(state='disabled')
    set_status("پاک شد. عبارت جدید را وارد کنید.")

def search_wiki(event=None):
    word = entry.get().strip()
    if not word:
        messagebox.showwarning("هشدار", "لطفاً یک عبارت وارد کنید.")
        return

    set_status(f"در حال جستجو برای: {word} ...")
    result_box.configure(state='normal')
    result_box.delete(1.0, "end")

    try:
        # sentences را کم/زیاد کن برا خلاصه طولانی‌تر یا کوتاه‌تر
        info = wiki.summary(word, sentences=6)
        result_box.insert("end", info + "\n\n")
        # لینک صفحه (در صورتی که صفحه وجود داشته باشه)
        try:
            page = wiki.page(word)
            if page and page.url:
                result_box.insert("end", f"لینک صفحه: {page.url}")
        except Exception:
            pass

        result_box.configure(state='disabled')
        set_status(f"نتیجه برای «{word}» نمایش داده شد.")
    except wiki.DisambiguationError as e:
        options = e.options[:8]
        msg = "عبارت شما چند معنی دارد. چند پیشنهاد:\n" + "\n".join(options)
        messagebox.showinfo("ابهام در جستجو", msg)
        result_box.insert("end", msg)
        result_box.configure(state='disabled')
        set_status("جستجو ابهام داشت — برای انتخاب دقیق‌تر یکی از پیشنهادات را وارد کنید.")
    except wiki.PageError:
        messagebox.showerror("خطا", "صفحه‌ای با این عنوان پیدا نشد.")
        set_status("صفحه پیدا نشد.")
    except Exception as e:
        messagebox.showerror("خطای شبکه/ناشناخته", str(e))
        set_status("خطا در جستجو — اتصال اینترنت یا مشکل دیگر.")

# اتصال کلید Enter به جستجو
entry.bind("<Return>", lambda event: search_wiki())

# دکمه خروج
exit_btn = tb.Button(app, text="خروج", command=app.destroy, bootstyle="danger-outline")
exit_btn.pack(pady=(6,12))

app.mainloop()
