# تلگرام اسپمر
![Telegram Spammer](preview.png)
تلگرام اسپمر ابزاری است که شما را در اسپم کردن و کارهای دیگر در تلگرام کمک میکند.

# نصب
بعد از کلون کردن باید کتابخانه های پایتون را نصب کنید.

```bash
pip3 install -r requirements.txt
```

سپس باید دستور زیر را اجرا کنید کنید.

```bash
python3 setup.py build_ext --inplace
```

بعد از نصب کتابخانه ها ابتدا باید در سایت [My Telegram](https://my.telegram.org/auth) وارد شوید و احراز هویت کنید.
سپس وارد قسمت API Development شوید فیلد ها را پر کنید.

سپس با دستور `python3 run.py conf` میتوانید وارد تنظیمات برنامه شوید. بعد از بازکردن تنظیمات گزینه ها را شخصی سازی کنید:

```ini
[auth]
api_id = Your API ID
api_hash = Your API Hash
client_count = Your Accounts Count

# پروکسی اختیاری است.
[proxy]
addr = Your Proxy Address
port = Your Proxy Port

[client0]
phone = Your Phone Number
name = Name

.....
```

# بروزرسانی

برای بروزرسانی تلگرام اسپمر اسکریپت `update.sh` را اجرا کنید.

```bash
bash update.sh
```

## ارسال پیام متنی

ابتدا یک فایل از پیام هایی که میخواهید ارسال کنید درست کنید.

سپس در برنامه با استفاده از دستور زیر میتوانید پیام انبوه ارسال کنید.

```bash
python3 run.py sendtext target count file
```

> target: تارگت  
> count: تعداد پیام هایی که میخواهید ارسال  
> file: فایلی که پیام ها را در ان نوشتید  

## عضو/لفت دادن از گروه یا کانال

```bash
python3 run.py join ChatID ClientNumber private
```

> ChatID: آیدی چتی که میخواهید در آن عضو شوید.  
> ClientNumber: شماره اکانتی که میخواهید با آن عضو شوید.  
> private: اگر چت خصوصی باشد از این گزینه استفاده کنید در غیر اینصورت از public استفاده کنید.  

```bash
python3 run.py leave ChatID ClientNumber
```

> ChatID: آیدی چتی که میخواهید از‌ آن لفت بدهید.  
> ClientNumber: شماره اکانتی که میخواهید با آن لفت بدهید.  

## ریپورت

```bash
python3 run.py report target count type
```

> target: یوزرنیمی که قصد ریپورت آن را دارید.  
> count: تعداد ریپورت.  
> type: انواع ریپورت عبارتند از: port, spam, copyright, childabuse, violence and geoirrelevant.  

## بلاک/آنبلاک

```bash
python3 run.py block ID ClientNumber
```

> ID: آیدی کسی که میخواهید بلاک کنید.  
> ClientNumber: شماره اکانتی که میخواهید با آن بلاک کنید.  

```bash
python3 run.py unblock ID ClientNumber
```

> ID: آیدی کسی که میخواهید آنبلاک کنید.  
> ClientNumber: شماره اکانتی که میخواهید با آن آنبلاک کنید.   

## فوروارد

```bash
python3 run.py forward from to count
```

> from: چتی که میخواهید پیام ها را از آن فوروارد کنید.  
> to: چتی که میخواهید پیام ها را به آن ارسال کنید.  
> count: تعداد پیام ها.  

# مشارکت

برای مشارکت در این پروژه از طرق pull requests اقدام کنید یا به [آیدی](https://t.me/BraveProgrammer) من در تلگرام پیام بدهید.

# حمایت مالی

Bitcoin: 1GKiThh6AaAj8Y1TEbwgC6cvrD82UyWDFk
