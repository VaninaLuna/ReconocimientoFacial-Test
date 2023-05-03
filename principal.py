
#-------Importar librerias -------

from tkinter import *
from tkinter import messagebox as msg
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import database as db

# -------Configuracion colores y letra-------
path = "C:/Users/user/facial_recognition/" # your path
txt_login = "Inicio de Sesión"
txt_register = "Cual sera tu eleccion"

color_white = "#f4f5f4"
color_black = "#101010"
color_green = "#42FF00"
color_grey_transparent = 'grey'

color_black_btn = "#202020"
color_background = "#ADA7A7"

font_label = "Calibri"
size_screen = "800x500"

# colors
color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"

res_bd = {"id": 0, "affected": 0} # database variable

# GENERAL
def getEnter(screen):
    ''' Set an enter inside the screen '''
    Label(screen, text="", bg=color_background).pack()

def printAndShow(screen, text, flag):
    ''' Prints and shows text '''
    if flag:
        print(color_success + text + color_normal)
        screen.destroy()
        msg.showinfo(message=text, title="¡Éxito!")
    else:
        print(color_error + text + color_normal)
        Label(screen, text=text, fg="red", bg=color_background, font=(font_label, 12)).pack()

def configure_screen(screen, text, image_screen):
    ''' Configure global styles '''
    screen.title(text)
    screen.geometry(size_screen)
    screen.configure(bg=color_background)
    
    Label(screen, image=image_screen, bg=color_black, text=f"{text}", fg=color_white, font=(font_label, 18), width="500", height="2").place(relwidth=1, relheight=1) 
    # image=image_screen, 
    # place(relwidth=1, relheight=1) // pack()

def credentials(screen, var, flag):
    ''' Configuration of user input '''
    
    Label(screen, text="Ingrese usuario:", fg=color_white, bg=color_black, font=(font_label, 12)).pack()
    
    entry = Entry(screen, textvariable=var, justify=CENTER, font=(font_label, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)
    
    getEnter(screen)
    frame = Frame(screen)
    frame.pack()
    
    if flag:
        Button(frame, text="Permitir acceso",fg=color_white, bg=color_black_btn, borderwidth=10, font=(font_label, 14), height="2", width="40", command=login_capture).grid(row=20, column=0, padx=0, pady=0, sticky="nsew")        
    else:
        #screen = root
        #screen.grid()
        #screen.rowconfigure(0, weight=1)
        #screen.rowconfigure(1, weight=1)
        #screen.columnconfigure(0, weight=1)
        #screen.columnconfigure(1, weight=1)
        Button(frame, text="Lado Oscuro", fg=color_white, bg=color_black, borderwidth=10,font=(font_label, 14), height="2", width="40", command=register_capture).grid(row=5, column=0, padx=0, pady=0, sticky="nsew")

        Button(frame, text="Lado Luminoso", fg=color_black, bg=color_white, borderwidth=10, font=(font_label, 14), height="2", width="40", command=register_capture).grid(row=5, column=1, padx=0, pady=0, sticky="nsew")
        
    return entry

def face(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1,len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])

# REGISTER #
def register_face_db(img):
    name_user = img.replace(".jpg","").replace(".png","")
    res_bd = db.registerUser(name_user, path + img)

    getEnter(screen1)
    if(res_bd["affected"]):
        printAndShow(screen1, "¡Éxito! Ha sido registrado correctamente", 1)
    else:
        printAndShow(screen1, "¡Error! No ha sido registrado correctamente", 0)
    os.remove(img)

def register_capture():
    cap = cv2.VideoCapture(0)
    user_reg_img = user1.get()
    img = f"{user_reg_img}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Registro Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry1.delete(0, END)
    
    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)
    face(img, faces)
    register_face_db(img)

def register():
    global user1
    global user_entry1
    global screen1

    screen1 = Toplevel(root)
    user1 = StringVar()
        
    configure_screen(screen1, txt_register, bg_image_register)
    user_entry1 = credentials(screen1, user1, 0)

# LOGIN #
def compatibility(img1, img2):
    orb = cv2.ORB_create()

    kpa, dac1 = orb.detectAndCompute(img1, None)
    kpa, dac2 = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(dac1, dac2)

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar)/len(matches)

def login_capture():
    cap = cv2.VideoCapture(0)
    user_login = user2.get()
    img = f"{user_login}_login.jpg"
    img_user = f"{user_login}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry2.delete(0, END)
    
    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)

    face(img, faces)
    getEnter(screen2)

    res_db = db.getUser(user_login, path + img_user)
    if(res_db["affected"]):
        my_files = os.listdir()
        if img_user in my_files:
            face_reg = cv2.imread(img_user, 0)
            face_log = cv2.imread(img, 0)

            comp = compatibility(face_reg, face_log)
            
            if comp >= 0.94:
                print("{}Compatibilidad del {:.1%}{}".format(color_success, float(comp), color_normal))
                printAndShow(screen2, f"Bienvenido, {user_login}", 1)
            else:
                print("{}Compatibilidad del {:.1%}{}".format(color_error, float(comp), color_normal))
                printAndShow(screen2, "¡Error! Incopatibilidad de datos", 0)
            os.remove(img_user)
    
        else:
            printAndShow(screen2, "¡Error! Usuario no encontrado", 0)
    else:
        printAndShow(screen2, "¡Error! Usuario no encontrado", 0)
    os.remove(img)

def login():
    global screen2
    global user2
    global user_entry2

    screen2 = Toplevel(root)
    user2 = StringVar()
    
    #bg_label = Label(root, image=bg_image_login)
    #bg_label.place(relwidth=1, relheight=1)
    
    configure_screen(screen2, txt_login, bg_image_login)
    user_entry2 = credentials(screen2, user2, 1)

root = Tk()

root.geometry(size_screen)
root.title("AVM")
root.configure(bg=color_background)
#Asignar un color al fondo de root (De preferencia un color que no utilices)
root['bg'] = color_grey_transparent
#Configurar el color que va a ser transparente, debe ser el mismo que el color del fondo de root
root.attributes('-transparentcolor', color_grey_transparent)

# Obtener la ruta absoluta de la imagen
image_home = os.path.join(os.getcwd(), "img", "idea2.png")
image_login = os.path.join(os.getcwd(), "img", "idea1.png")
image_register = os.path.join(os.getcwd(), "img", "login2.png")

# Cargar la imagen
bg_image_home = PhotoImage(file=image_home)
bg_image_login = PhotoImage(file=image_login)
bg_image_register = PhotoImage(file=image_register)

# Crear un widget Label con la imagen cargada
bg_label = Label(root, image=bg_image_home)
bg_label.place(relwidth=1, relheight=1)
# bg_label.pack(fill="both", expand=True)

#Mensaje de bienvenida
Label(text="¡Bienvenido!", fg=color_white, bg=color_black, font=(font_label, 20), width="500", height="2").pack()
Label(text="¿Seras digno del ingreso?", fg=color_white, bg=color_grey_transparent, font=(font_label, 20), width="500", height="2").pack()

#Botones de ingreso y registro
getEnter(root)
Button(text=txt_login, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()

getEnter(root)
Button(text=txt_register, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register).pack()

root.mainloop()

