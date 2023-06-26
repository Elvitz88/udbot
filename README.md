# __udbot__
UDBot เป็นซอฟต์แวร์อัตโนมัติที่ออกแบบมาเพื่อทำ Robotic Process Automation (RPA) กับโปรแกรมเฉพาะ เราสร้างบอทด้วย Python และออกแบบมาเพื่อทำงานอย่างรวดเร็วและมีประสิทธิภาพ

## __คำแนะนำในการติดตั้ง__
ทำตามขั้นตอนด้านล่างเพื่อติดตั้งและรัน UDBot:

### __ขั้นตอนที่ 1: clone repository__
clone repository ไปยังเครื่องของคุณ

    https://github.com/Elvitz88/udbot.git

### __ขั้นตอนที่ 2: สร้างไดเรกทอรีที่จำเป็น__
เข้าสู่ Root ของโปรเจ็คและสร้างไดเรกทอรีต่อไปนี้:

    mkdir documents
        cd documents
        mkdir pictures
        mkdir datalog
    mkdir my_function
    mkdir mydb

ไดเรกทอรีเหล่านี้จะเก็บเอกสาร, สคริปต์ฟังก์ชันที่กำหนดเอง, และฐานข้อมูล ตามลำดับ

### __ขั้นตอนที่ 3: สร้าง virtual environment__
สร้าง virtual environment ของ Python เพื่อแยก dependencies ของโปรเจ็ค คุณสามารถทำได้โดยรันคำสั่งต่อไปนี้:

    python -m venv env

ในการเปิดใช้งาน virtual environment, run:

    env\Scripts\activate.bat

### __ขั้นตอนที่ 4: ติดตั้ง dependencies__
ติดตั้ง dependencies ของ Python ที่จำเป็นโดย run:

    pip install -r requirement.txt

การดำเนินการนี้จะติดตั้ง dependencies ทั้งหมดที่แสดงอยู่ในไฟล์ requirements.txt

## __การรัน Bot__
หลังจากติดตั้งเสร็จสิ้น, คุณสามารถรัน UDBot โดยการ execute สคริปต์ Python หลัก (โปรดแทน main_script.py ด้วยชื่อจริงของสคริปต์ของคุณ):

    python main_script.py

## __การทำงานร่วมกัน__
ยินดีต้อนรับการส่ง pull request สำหรับการเปลี่ยนแปลงสำคัญ, โปรดเปิดปัญหาก่อนเพื่อสนทนาเกี่ยวกับสิ่งที่คุณต้องการเปลี่ยน

## __ใบอนุญาต__
UDBot ได้รับใบอนุญาตภายใต้เงื่อนไขของ ใบอนุญาต [MIT](https://choosealicense.com/licenses/mit/)