import os
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import messagebox as m
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as font

import stego.hover as ho
import stego.text as txt
import stego.audio as aud
import stego.database as db
import stego.image as image_

root = Tk()
root.title('Steno')
root.config(bg='#000000')
root.resizable(True, True)
root.wm_iconbitmap('images/snap.ico')

# centering the main window
root_h, root_w = 300, 400
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x_coor = int((s_w / 2) - (root_w / 2))
y_coor = int((s_h / 2) - (root_h / 2))
root.geometry("{}x{}+{}+{}".format(root_w, root_h, x_coor, y_coor))

# defining the fonts used and images
bos = ('Bookman Old Style', 10)
bos_big = ('Bookman Old Style', 20)
img = PhotoImage(file="images/noshow.png").subsample(4, 4)
img2 = PhotoImage(file="images/show.png").subsample(4, 4)
img3 = PhotoImage(file="images/dots.png").subsample(3, 3)
myFont = font.Font(family='Helvetica')


def text_steno():
    """The text steganography function this includes both encoding and decoding"""
    win = Toplevel(master=root, bg='#c0ed98')
    win.title('Text Steno')
    win.geometry('480x410')
    win.wm_iconbitmap('images/snap.ico')
    win_label = Label(win, text='Text-Steganography', font=bos_big, bg='#c0ed98', fg='#1046b3', justify='center')
    win_label.place(x=5, y=4)

    def encode():
        """encoding function for text files"""
        global choice_button, infile_loc
        outfile_loc, m_or_f = '', ''

        size_label = Label(win, text='Select File:', font=bos, bg='#c0ed98', fg='#f20713')
        size_label.place(x=5, y=45)
        es = Entry(win, width=50, font=bos)
        es.place(x=7, y=65)

        def browse():
            """Opens a prompt for selecting files"""
            global infile_loc
            infile_loc = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File to DECODE',
                                         filetypes=[('Text files', '.txt')], defaultextension='.txt')
            es.delete(0, END)
            es.insert(0, infile_loc)
            size_label.config(text='Selected File:')

        se_bu = Button(win, text='Browse', bg='#8ed925', font=myFont, command=browse, relief='ridge')
        se_bu.place(x=411, y=61)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        # TODO add a widget where user will be able to see contents of their chosen file

        ch_lb = Label(win, text='Select what you want to hide', bg='#c0ed98', fg='#1046b3', font=bos)
        ch_lb.place(x=5, y=85)
        select = StringVar(win)
        style = ttk.Style(master=win)
        style.configure('C.TRadiobutton', font=bos, background='#c0ed98', foreground='#1046b3')

        message_ch = ttk.Radiobutton(win, text='Hide a Message', value="1", variable=select, style='C.TRadiobutton')
        message_ch.place(x=5, y=105)

        choice_file = ttk.Radiobutton(win, text='Hide a File', value="2", variable=select, style='C.TRadiobutton')
        choice_file.place(x=5, y=130)

        password_ = Entry(win, width=20, show='*', font=bos, state=DISABLED)
        password_.place(x=10, y=185)

        def choice():
            """Here the user's choice is evaluated & accordingly work is done"""
            global choice_button
            if select.get() == "1":
                """If the user chooses to enter a message a text prompt is opened"""
                message = Toplevel(master=win)
                message.title('Enter Message')
                message.resizable(False, False)
                message.wm_iconbitmap('images/snap.ico')
                lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=bos)
                lm.pack(side=TOP, fill=BOTH)
                ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
                t = st.ScrolledText(message)
                t.config(font=bos)
                t.pack()

                def click(event=None):
                    """Here we collect whatever message the user entered"""
                    global m_or_f
                    message.withdraw()
                    m_or_f = t.get("1.0", "end-1c")
                    # after getting message we allow the user to enter password
                    password_.config(state=NORMAL)
                    password_.focus()

                bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg='yellow', font=myFont)
                bm.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
                message.bind('<Control-b>', click)
                choice_button.config(state=DISABLED)
                refresh.config(state=NORMAL)

            elif select.get() == "2":
                """If user chooses to encode a file then select file prompt opens up"""
                global m_or_f
                m.showinfo('Procedure', 'Select the file which contains\nthe data you want to encode.')
                m_or_f = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File',
                                         filetypes=[('Text files', '.txt')], defaultextension='.txt')
                choice_button.config(state=DISABLED)
                refresh.config(state=NORMAL)
                password_.config(state=NORMAL)
                password_.focus()

        choice_button = Button(win, text='Select', command=choice, bg='#08d0fc', font=myFont, relief='ridge')
        choice_button.place(x=152, y=122)
        ho.CreateToolTip(choice_button, 'Opens a prompt according\nto your chosen option.')

        def process():
            """Here the password's eyes show & hide functions are carried out"""
            if password_["state"] == ACTIVE or password_['state'] == NORMAL:
                if password_["show"] == '*':
                    password_.config(show="")
                    pass_button.config(image=img2)
                elif password_["show"] == "":
                    password_.config(show='*')
                    pass_button.config(image=img)

        pass_label = Label(win, text='Set password:', font=bos, bg='#c0ed98', fg='#1046b3')
        pass_label.place(x=10, y=155)

        pass_button = Button(win, image=img, relief='ridge', bg='#36f5eb', command=process, font=myFont)
        pass_button.place(x=195, y=180)
        ho.CreateToolTip(pass_button, 'Show/ Hide password')
        success = Label(win, bg='#c0ed98', font=bos, fg='red')
        success.place(x=20, y=280)

        def execute():
            """Main function which checks the requirements and encodes data accordingly"""
            global outfile_loc, m_or_f
            m.showinfo('Procedure', 'Where would you like the encoded file to be saved?\n'
                                    'Select the path in the next window.')
            outfile_loc = asksaveasfilename(title='Save your encoded file as', filetypes=[('Text File', '.txt')],
                                            defaultextension='.txt', initialdir=os.getcwd(), parent=win)
            if password_.get() != '' and infile_loc != '' and outfile_loc != '' and m_or_f != '' and es.get() != '':
                if select.get() == '1':
                    try:
                        txt.encode(passwd=password_.get(), infile=es.get(), outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password_.get(), infile=infile_loc, outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                elif select.get() == '2':
                    try:
                        txt.encode(passwd=password_.get(), infile=es.get(), outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file\n{} in\n{}'.format(m_or_f, outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password_.get(), infile=infile_loc, outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file\n{} in\n{}'.format(m_or_f, outfile_loc))
            else:
                m.showerror('ERROR', 'Something went wrong\ntry again.')

        main = Button(win, text='Hide Data', command=execute, bg='#eba823', relief='ridge', font=bos)
        main.place(x=20, y=250)
        ho.CreateToolTip(main, 'Checks everything\nthen encodes the data')

        # TODO show contents of file after encoding[optional]

        def refresh():
            """If the user wants to again choose the options"""
            if choice_button['state'] == DISABLED:
                choice_button.config(state=NORMAL)

        refresh = Button(win, text='Refresh', command=refresh, state=DISABLED, relief='ridge', font=myFont, bg='#fca903')
        refresh.place(x=360, y=122)
        ho.CreateToolTip(refresh, 'Refreshes Page')

    def decode():
        """Decoding function for text files"""
        global file_loc
        dec = Toplevel(master=root, bg='#c0ed98')
        dec.title('Text Steno-DECODE')
        dec.geometry('480x250')
        dec.wm_iconbitmap('images/snap.ico')
        dec_label = Label(dec, text='Text -Steganography[DECODE]', font=bos_big, bg='#c0ed98', fg='#1046b3')
        dec_label.place(x=5, y=4)
        info_label = Label(dec, text='Select File:', font=bos, bg='#c0ed98', fg='#f20713')
        info_label.place(x=5, y=60)
        file_ent = Entry(master=dec, width=50, font=bos)
        file_ent.place(x=7, y=85)

        def browse():
            """Opens a prompt for selecting files"""
            global file_loc
            file_loc = askopenfilename(parent=dec, initialdir=os.getcwd(), title='Select File to DECODE',
                                       filetypes=[('Text files', '.txt')], defaultextension='.txt')
            file_ent.delete(0, END)
            file_ent.insert(0, file_loc)
            info_label.config(text='Selected File:')

        se_bu = Button(dec, text='Browse', bg='#8ed925', font=bos, command=browse, relief='ridge')
        se_bu.place(x=410, y=82)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        pass_lb = Label(dec, text='Enter password:', bg='#c0ed98', fg='#1046b3', font=bos)
        pass_lb.place(x=5, y=110)
        pass_ent = Entry(dec, width=20, font=bos, show='*')
        pass_ent.place(x=7, y=135)
        pass_ent.focus()

        def show():
            """Here the password's eyes show & hide functions are carried out"""
            if pass_ent["state"] == ACTIVE or pass_ent['state'] == NORMAL:
                if pass_ent["show"] == '*':
                    pass_ent.config(show="")
                    pass_bu.config(image=img2)
                elif pass_ent["show"] == "":
                    pass_ent.config(show='*')
                    pass_bu.config(image=img)

        pass_bu = Button(dec, image=img, command=show, bg='#36f5eb', relief='ridge')
        pass_bu.place(x=190, y=130)
        ho.CreateToolTip(pass_bu, 'Show/ Hide password')

        def work(event=None):
            """Here after collecting the requirements decoding is carried out"""
            global data
            try:
                data = txt.decode(passwd=pass_ent.get(), file=file_ent.get())
            except FileNotFoundError:
                data = txt.decode(passwd=pass_ent.get(), file=file_loc)
            finally:
                text_win = Toplevel(dec)
                text_win.title('Decoded Message')
                text_win.resizable(False, False)
                text_win.wm_iconbitmap('images/snap.ico')
                show_lb = Label(text_win, text='The message hidden in the selected file:',
                                bg='yellow', fg='red', font=bos)
                show_lb.pack(side=TOP, fill=BOTH)
                ho.CreateToolTip(show_lb, "Can't understand what's decoded\nthen your password is WRONG")
                show_text = st.ScrolledText(text_win)
                show_text.pack()
                show_text.tag_configure('beauty', font=bos)
                show_text.insert(INSERT, data, 'beauty')
                show_text.config(state=DISABLED)
                show_bu = Button(text_win, text='Exit', bg='yellow', fg='red',
                                 command=text_win.destroy, font=bos)
                show_bu.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(show_bu, 'Closes the window')

        def forgotten():
            global path
            foo = Toplevel(dec, bg='#93ed87')
            foo.title('Forgot Password')
            foo.geometry('420x300')
            foo.wm_iconbitmap('images/snap.ico')
            f_lb = Label(foo, text='Forgot Password Recovery', font=bos_big, fg='#214a22', bg='#93ed87')
            f_lb.place(x=5, y=5)
            uname_lb = Label(foo, text='Enter Admin username:', bg='#93ed87', fg='#214a22', font=bos).place(x=5, y=50)
            uname_ent = Entry(foo, font=bos, width=20)
            uname_ent.place(x=180, y=50)
            pwd_lb = Label(foo, text='Enter Admin Password:', bg='#93ed87', fg='#214a22', font=bos).place(x=5, y=80)
            pwd_ent = Entry(foo, font=bos, width=20, show='*')
            pwd_ent.place(x=180, y=80)
            file2 = Label(foo, text='Enter file Path:', bg='#93ed87', fg='#214a22', font=bos).place(x=5, y=110)
            file_new = Entry(foo, font=bos, width=51)
            file_new.place(x=5, y=140)

            def browse_txt():
                """Opens a prompt for selecting files"""
                global path
                path = askopenfilename(parent=foo, initialdir=os.getcwd(), title='Select File to DECODE',
                                       filetypes=[('Text files', '.txt')], defaultextension='.txt')
                file_new.delete(0, END)
                file_new.insert(0, path)

            def check(event=None):
                dt = db.main_work(uname_ent.get(), pwd_ent.get(), path)
                if len(dt) < 2:
                    show_label.config(text=dt[0], font=bos_big)
                else:
                    dt1, dt2 = dt
                    state = 'Hi {} the password for the\nchosen file is:- {}'.format(dt1, dt2[0])
                    show_label.config(text=state, font=bos)

            def show_txt():
                """Here the password's eyes show & hide functions are carried out"""
                if pwd_ent["state"] == ACTIVE or pwd_ent['state'] == NORMAL:
                    if pwd_ent["show"] == '*':
                        pwd_ent.config(show="")
                        pass_bu2.config(image=img2)
                    elif pwd_ent["show"] == "":
                        pwd_ent.config(show='*')
                        pass_bu2.config(image=img)

            pass_bu2 = Button(foo, image=img, command=show_txt, bg='#36f5eb', relief='ridge')
            pass_bu2.place(x=350, y=70)
            ho.CreateToolTip(pass_bu, 'Show/ Hide password')

            fo_br = Button(foo, text='Browse', font=bos, fg='#f53a1d', command=browse_txt, relief='flat', bg='#ffcc9c')
            fo_br.place(x=354, y=161)
            ho.CreateToolTip(fo_br, 'Browse & select files')
            check2 = Button(foo, text='Check & Retrieve', font=bos, bg='#47f5a7', fg='#2200fc', command=check)
            check2.place(x=25, y=200)
            ho.CreateToolTip(check2, 'Checks everything & gives password')
            show_label = Label(foo, text='', bg='#93ed87', fg='#f53a1d', font=bos_big)
            show_label.place(x=10, y=230)
            foo.bind('<Return>', check)

        decode_main = Button(dec, text='Decode', relief='ridge', bg='#00fc69', font=bos, command=work)
        decode_main.place(x=10, y=190)
        ho.CreateToolTip(decode_main, 'Checks the requirements then\nshows the decoded data.')
        forgot = Button(dec, text='Forgot Password', relief='ridge', bg='#fa8a20', font=bos, command=forgotten)
        forgot.place(x=150, y=200)
        ho.CreateToolTip(forgot, 'This helps you retrieve\nforgotten if you have admin account.')
        exit_dec = Button(dec, text='Exit', bg='#f53a1d', font=bos, relief='ridge',
                          command=dec.destroy)
        exit_dec.place(x=360, y=200)
        ho.CreateToolTip(exit_dec, 'Closes the window')
        dec.bind('<Return>', work)

    encoding = Button(win, text='Encode data', command=encode, relief='ridge', font=bos, bg='#f00c58')
    encoding.place(x=40, y=360)
    ho.CreateToolTip(encoding, 'Encoding data function')
    decoding = Button(win, text="Decode data", command=decode, relief='ridge', font=bos, bg='#6b0cf0')
    decoding.place(x=180, y=360)
    ho.CreateToolTip(decoding, "Decoding data function")
    exit_win = Button(win, text='Exit', bg='#eb3131', font=bos, relief='ridge', command=win.destroy)
    exit_win.place(x=360, y=360)
    ho.CreateToolTip(exit_win, 'Closes the window')


def image_steno():
    """Image steganography function"""
    img_win = Toplevel(master=root, bg='#edaa82')
    img_win.title('Image steno')
    img_win.geometry('515x260')
    img_win.wm_iconbitmap('images/snap.ico')
    im_lb = Label(img_win, text='Image-Steganography', bg='#edaa82', fg='#fa05bd', font=bos_big)
    im_lb.place(x=10, y=10)

    def em_img():
        """Image steganography functions"""
        global file, mess
        select_lb = Label(img_win, text='Select File:', font=bos, bg='#edaa82', fg='#fa05bd')
        select_lb.place(x=5, y=50)
        file_im = Entry(img_win, width=55, font=bos, relief='ridge')
        file_im.place(x=7, y=75)
        file_im.place(x=7, y=75)
        file_im.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=img_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                   filetypes=[('Image files', '.png')], defaultextension='.png')
            file_im.delete(0, END)
            file_im.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(img_win, text='Browse', bg='#8ed925', font=bos, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(img_win)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/snap.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=bos)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=bos)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg='yellow', font=bos)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(img_win, command=pan, text='Enter Message', font=bos, bg='#94f748')
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(img_win, bg='#edaa82', font=bos)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then embeds the data in image file"""
            global file, mess
            m.showinfo('Procedure', 'Where would you like the embedded file to be saved?\n'
                                    'Select the path in the next window.')
            out = asksaveasfilename(title='Save your embedded file as', filetypes=[('Image files', '.png')],
                                    defaultextension='.png', initialdir=os.getcwd(), parent=img_win)
            if mess != '' and file != '' and file_im.get() != '' and out != '':
                try:
                    image_.encrypt_image(img_path=file, message=mess, new_path=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
                except FileNotFoundError:
                    image_.encrypt_image(img_path=file_im.get(), message=mess, new_path=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(img_win, text='Embed Message', bg='#f79205', font=bos, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and embeds your data')

    def ex_img():
        """Data extracting function of audio steno"""
        global ex_file
        ex_win = Toplevel(root, bg='#edaa82')
        ex_win.title('Image Steno-EXTRACT')
        ex_win.geometry('515x310')
        ex_win.wm_iconbitmap('images/snap.ico')
        ex_lb = Label(ex_win, text='Image -Steganography[EXTRACT]', bg='#edaa82', fg='#fa05bd', font=bos_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=bos, bg='#edaa82', fg='#fa0505')
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=bos, relief='ridge')
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                      filetypes=[('Image files', '.png')], defaultextension='.png')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg='#8ed925', font=bos, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = image_.decrypt_image(img_path=ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=bos, fg='#f50c81', bg='#edaa82').place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=bos)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', bg='#f79205', font=bos, command=extract_data)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=bos, bg='#f23f3f', fg='#e1f719', command=ex_win.destroy)
        qu_bu.place(x=467, y=278)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(img_win, text='Embed', font=bos, bg='#05ff82', fg='#0569ff', command=em_img)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Embeds data in image file')
    bu_ex = Button(img_win, text='Extract', font=bos, bg='#acff05', fg='#fa029b', command=ex_img)
    bu_ex.place(x=260, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from image file')
    qubu = Button(img_win, text='Exit', font=bos, bg='#f23f3f', fg='#e1f719', command=img_win.destroy)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')


def audio_steno():
    """Audio steganography functions"""
    aud_win = Toplevel(master=root, bg='#c3f0fa')
    aud_win.title('Audio Steno')
    aud_win.geometry('515x260')
    aud_win.wm_iconbitmap('images/snap.ico')
    au_lb = Label(aud_win, text='Audio-Steganography', bg='#c3f0fa', fg='#fa05bd', font=bos_big)
    au_lb.place(x=10, y=10)

    def em_aud():
        """Audio steno's embedding function"""
        global file, mess
        select_lb = Label(aud_win, text='Select File:', font=bos, bg='#c3f0fa', fg='#fa0505')
        select_lb.place(x=5, y=50)
        file_au = Entry(aud_win, width=55, font=bos, relief='ridge')
        file_au.place(x=7, y=75)
        file_au.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=aud_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                   filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_au.delete(0, END)
            file_au.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(aud_win, text='Browse', bg='#8ed925', font=bos, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(aud_win)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/snap.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=bos)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=bos)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg='yellow', font=bos)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(aud_win, command=pan, text='Enter Message', font=bos, bg='#94f748')
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(aud_win, bg='#c3f0fa', font=bos)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then embeds the data in audio file"""
            global file, mess
            m.showinfo('Procedure', 'Where would you like the embedded file to be saved?\n'
                                    'Select the path in the next window.')
            out = asksaveasfilename(title='Save your embedded file as', filetypes=[('Audio File', '.wav')],
                                    defaultextension='.wav', initialdir=os.getcwd(), parent=aud_win)
            if mess != '' and file != '' and file_au.get() != '' and out != '':
                try:
                    aud.embed(infile=file, message=mess, outfile=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
                except FileNotFoundError:
                    aud.embed(infile=file_au.get(), message=mess, outfile=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(aud_win, text='Embed Message', bg='#f79205', font=bos, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and embeds your data')

    def ex_aud():
        """Data extracting function of audio steno"""
        global ex_file
        ex_win = Toplevel(root, bg='#c3f0fa')
        ex_win.title('Audio Steno-EXTRACT')
        ex_win.geometry('515x310')
        ex_win.wm_iconbitmap('images/snap.ico')
        ex_lb = Label(ex_win, text='Audio -Steganography[EXTRACT]', bg='#c3f0fa', fg='#fa05bd', font=bos_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=bos, bg='#c3f0fa', fg='#fa0505')
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=bos, relief='ridge')
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                      filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg='#8ed925', font=bos, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = aud.extract(ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=bos, fg='#f50c81', bg='#c3f0fa').place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=bos)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', bg='#f79205', font=bos, command=extract_data)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=bos, bg='#f23f3f', fg='#e1f719', command=ex_win.destroy)
        qu_bu.place(x=467, y=278)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(aud_win, text='Embed', font=bos, bg='#05ff82', fg='#0569ff', command=em_aud)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Embeds data in audio file')
    bu_ex = Button(aud_win, text='Extract', font=bos, bg='#acff05', fg='#fa029b', command=ex_aud)
    bu_ex.place(x=230, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from audio file')
    qubu = Button(aud_win, text='Exit', font=bos, bg='#f23f3f', fg='#e1f719', command=aud_win.destroy)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')


def password():
    ps = Toplevel(root, bg='#88b1f2')
    ps.geometry('400x300+800+200')
    ps.wm_iconbitmap('images/snap.ico')
    ps_lb = Label(ps, text='User Login[backup]', font=bos_big, bg='#88b1f2', fg='#5c1841')
    ps_lb.place(x=5, y=5)
    ps_name_lb = Label(ps, text='Enter name:', bg='#88b1f2', fg='#5c1841', font=bos).place(x=5, y=50)
    ps_name_entry = Entry(ps, width=30, font=bos)
    ps_name_entry.place(x=100, y=50)
    ps_username_lb = Label(ps, text='Enter\nusername:', bg='#88b1f2', fg='#5c1841', font=bos).place(x=9, y=80)
    ps_username_entry = Entry(ps, width=30, font=bos)
    ps_username_entry.place(x=100, y=100)
    ps_pass = Label(ps, text='Enter\npassword:', bg='#88b1f2', fg='#5c1841', font=bos).place(x=9, y=130)
    ps_pass_entry = Entry(ps, width=25, font=bos, show='*')
    ps_pass_entry.place(x=100, y=150)

    def ok_done(event=None):
        db.new(ps_name_entry.get(), ps_username_entry.get(), ps_pass_entry.get())
        suc_lb.config(text='Done!!')

    ps_button = Button(ps, text='Done', font=bos, command=ok_done, fg='#e08f1d')
    ps_button.place(x=350, y=250)
    suc_lb = Label(ps, text='', font=bos_big, bg='#88b1f2', fg='#5c1841')
    suc_lb.place(x=150, y=200)

    def show():
        """Here the password's eyes show & hide functions are carried out"""
        if ps_pass_entry["show"] == '*':
            ps_pass_entry.config(show="")
            pass_bu.config(image=img2)
        elif ps_pass_entry["show"] == "":
            ps_pass_entry.config(show='*')
            pass_bu.config(image=img)

    pass_bu = Button(ps, image=img, command=show, bg='#36f5eb', relief='ridge')
    pass_bu.place(x=310, y=140)
    ho.CreateToolTip(pass_bu, 'Show/ Hide password')
    ho.CreateToolTip(ps_button, 'Sets up your admin account')
    ps.bind('<Return>', ok_done)


lb = Label(root, text="Stego Software", font=('Bookman Old Style', 20), bg='#000000', fg='#ffffff')
lb.place(x=18, y=20)

text = Button(root, text='Text\nSteganography', relief='flat', bg='#ffffff', command=text_steno, font=bos)
text.place(x=35, y=250)
ho.CreateToolTip(text, 'Click here\nto hide your\ndata in a text file')

image = Button(root, text='Image\nSteganography', relief='flat', bg='#ffffff', command=image_steno, font=bos)
image.place(x=145, y=250)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')

audio = Button(root, text='Audio\nSteganography', relief='flat', bg='#ffffff', command=audio_steno, font=bos)
audio.place(x=255, y=250)
ho.CreateToolTip(audio, 'Click here\nto hide data in\n an audio file.')

uni = Button(root, image=img3, relief='flat', bg='#ffffff', command=password)
uni.place(x=370, y=0)
ho.CreateToolTip(uni, 'Here you can create\nadmin account to\nretrieve forgotten passwords later.')

root.mainloop()
db.close()
