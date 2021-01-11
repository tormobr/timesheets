import re
import pandas as pd
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

HEADER = '\033[95m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# TOP DATA CORDINATES
first_name = (50, 745)
subject = (220, 745)
birth = (400, 745)
last_name = (50, 700)
month = (220, 700)
hours = (400, 700)

# HOURS DETAIL CORDINATES
meeting = (410, 580)
prep_lab = (410, 550)
lab = (410, 520)
prep_classroom = (410, 490)
classroom = (410, 460)
coms = (410, 430)



# DATE AND SIGNATURE
date = (40, 100)

fd = pd.DataFrame()

def add_oblig():
    pass

def UI(can):
    tot = 0
    print("\n------------------------------------------")
    ans = input(f"\t{HEADER}Use Preset? {OKGREEN}Y{ENDC}/{FAIL}N: {ENDC}")
    if ans not in ["Y", "y", "yes", "Yes", "YES"]:
        can.drawString(*first_name, input(f"\t{HEADER}First Name: {ENDC}"))
        can.drawString(*last_name, input(f"\t{HEADER}Last Name: {ENDC}"))
        can.drawString(*birth, input(f"\t{HEADER}Birth Date: {ENDC}"))
        can.drawString(*subject, input(f"\t{HEADER}Subject: {ENDC}"))
    else:
        can.drawString(*first_name, "Tormod")
        can.drawString(*last_name, "Brændshøi")
        can.drawString(*birth, "16-09-1995")
        can.drawString(*subject, "IN-3000")

    can.drawString(*month, datetime.today().strftime("%B"))



    M = input(f"\t{HEADER}Meeting: {ENDC}")
    can.drawString(*meeting, M)

    P_L = input(f"\t{HEADER}Preperations Lab: {ENDC}")
    can.drawString(*prep_lab, P_L)

    L = input(f"\t{HEADER}Lab: {ENDC}")
    can.drawString(*lab, L)

    P_C = input(f"\t{HEADER}Preperations Class: {ENDC}")
    can.drawString(*prep_classroom, P_C)

    C = input(f"\t{HEADER}Class: {ENDC}")
    can.drawString(*classroom, C)

    CO = input(f"\t{HEADER}Comunication: {ENDC}")
    can.drawString(*coms, CO)

    other_x, other_y = 370, 410
    O = input(f"\t{HEADER}Other (<tag>:<hours>, <tag2>:<hours2>): {ENDC}")
    for item in O.split(","):
        item = re.sub(" ", "", item)
        tag, num = item.split(":")
        tot += float(num)
        can.drawString(other_x, other_y, item)
        other_y -= 15

    try:
        tot += sum(map(float, [M, P_L, L, P_C, C, CO]))
    except ValueError:
        print(f"{FAIL}NOT VALID INPUT{ENDC}")
        exit(0)


    # GRADING
    curr_oblig = (70, 260)
    while True:
        print("------------------------------------------")
        curr_x, curr_y = curr_oblig
        ans = input(f"\t{HEADER}Add Oblig? {OKGREEN}Y{ENDC}/{FAIL}N: {ENDC}")
        if ans not in ["Y", "y", "yes", "Yes", "YES"]:
            break
        nr = input(f"\t\t{HEADER}Oblig Nr: {ENDC}")
        can.drawString(curr_x, curr_y, nr)
        curr_x += 135
        delivery_nr = input(f"\t\t{HEADER}Delivery Nr: {ENDC}")
        can.drawString(curr_x, curr_y, delivery_nr)
        curr_x += 135
        num_obligs = input(f"\t\t{HEADER}Number of Obligs Corrected: {ENDC}")
        can.drawString(curr_x, curr_y, num_obligs)
        curr_x += 135
        H = input(f"\t\t{HEADER}Hours spent: {ENDC}")
        try:
            tot += float(H)
        except ValueError:
            print(f"{FAIL}NOT VALID INPUT{ENDC}")
            exit(0)

        can.drawString(curr_x, curr_y, H)
        curr_x -= 135 * 3
        curr_y -= 30
        curr_oblig = (curr_x, curr_y)

    print("------------------------------------------")

    can.drawString(*date, datetime.today().strftime("%d-%m-%Y"))
    can.drawString(*hours, str(tot))


# Code from stack-overflow
def write_file(packet):
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(PATH, "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # finally, write "output" to a real file
    outputStream = open(f"timeliste_{datetime.today().strftime('%B')}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    print("------------------------------------------")
    print(f"{OKGREEN}File written{ENDC}\n")


def run(PATH):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    UI(can)
    can.save()
    write_file(packet)



if __name__ == "__main__":
    CWD = dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "template.pdf"
    PATH = os.path.join(CWD, filename)
    run(PATH)
