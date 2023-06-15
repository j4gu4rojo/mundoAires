from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import sqlite3
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import smtplib
from email.mime.text import MIMEText







def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        create_table_productos(cursor)
        create_table_motos(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)

def create_table_productos(cursor):
    cursor.execute(
        '''
        CREATE TABLE Productos(
        ID        INT   PRIMARY KEY  NOT NULL,
        Nombre    TEXT               NOT NULL,
        Marca     TEXT               NOT NULL,
        Costo     FLOAT              NOT NULL,
        Almacen   INT                NOT NULL
        )'''
    )
def create_table_motos(cursor):

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Motos(
        ID        INT   PRIMARY KEY  NOT NULL,
        Placa    TEXT               NOT NULL,
        Marca     TEXT               NOT NULL,
        Conductor TEXT              NOT NULL,
        FechaAceite   TEXT      NOT NULL
        )'''
    )

class MessagePopup(Popup):
    pass

class MainWid(ScreenManager):

    def __init__(self,**kwargs):
        super(MainWid,self).__init__()
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH+'/my_database.db'
        self.Login = Login(self)
        self.StartWid = StartWid(self)
        self.DataBaseWid = DataBaseWid(self)
        self.InsertDataWid = BoxLayout()
        self.UpdateDataWid = BoxLayout()
        self.DataBaseWidM = DataBaseWidM(self)
        self.InsertDataWidM = BoxLayout()
        self.UpdateDataWidM = BoxLayout()
        
        
        self.Popup = MessagePopup()
        
        wid = Screen(name='login')
        wid.add_widget(self.Login)
        self.add_widget(wid) 
        wid = Screen(name='start')
        wid.add_widget(self.StartWid)
        self.add_widget(wid)
        wid = Screen(name='database')
        wid.add_widget(self.DataBaseWid)
        self.add_widget(wid)
        wid = Screen(name='insertdata')
        wid.add_widget(self.InsertDataWid)
        self.add_widget(wid)
        wid = Screen(name='updatedata')
        wid.add_widget(self.UpdateDataWid)
        self.add_widget(wid)
        wid = Screen(name='databaseM')
        wid.add_widget(self.DataBaseWidM)
        self.add_widget(wid)
        wid = Screen(name='insertdataM')
        wid.add_widget(self.InsertDataWidM)
        self.add_widget(wid)
        wid = Screen(name='updatedataM')
        wid.add_widget(self.UpdateDataWidM)
        self.add_widget(wid)
        
        self.goto_login()


    def goto_login(self):
        self.current = 'login'
        
    def goto_start(self):
        self.current = 'start'
        
    def goto_database(self):
        self.DataBaseWid.check_memory()
        self.current = 'database'
        
    def goto_insertdata(self):
        self.InsertDataWid.clear_widgets()
        wid = InsertDataWid(self)
        self.InsertDataWid.add_widget(wid)
        self.current = 'insertdata'

    def goto_updatedata(self,data_id):
        self.UpdateDataWid.clear_widgets()
        wid = UpdateDataWid(self,data_id)
        self.UpdateDataWid.add_widget(wid)
        self.current = 'updatedata'

    def goto_databaseM(self):
        self.DataBaseWidM.check_memory()
        self.current = 'databaseM'

    def goto_insertdataM(self):
        self.InsertDataWidM.clear_widgets()
        wid = InsertDataWidM(self)
        self.InsertDataWidM.add_widget(wid)
        self.current = 'insertdataM'

    def goto_updatedataM(self, data_id):
        self.UpdateDataWidM.clear_widgets()
        wid = UpdateDataWidM(self, data_id)
        self.UpdateDataWidM.add_widget(wid)
        self.current = 'updatedataM'
    


class Login(Screen):
    username_input = ObjectProperty()
    password_input = ObjectProperty()
    email_input = ObjectProperty()
    popup = None

    def __init__(self, mainwid, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.mainwid = mainwid

    def login(self):
        dialog = None

        username = self.ids.username_input.text if self.ids.username_input else ""
        password = self.ids.password_input.text if self.ids.password_input else ""

        if username == 'mundo' and password == 'messi':
            self.mainwid.goto_start()
        else:
            self.popup = MDDialog(
                title='Error',
                text='Credenciales incorrectas',
                buttons=[
                    MDFlatButton(
                        text='Cerrar',
                        on_release=self.dismiss_dialog
                    )
                ]
            )
            self.popup.open()
            self.current = 'login'
    
    def show_recovery_dialog(self):
        self.email_input = MDTextField(hint_text='Ingrese su correo electrónico')

        self.popup = MDDialog(
            title='Recuperación de contraseña',
            type='custom',
            content_cls=self.email_input,
            buttons=[
                MDFlatButton(
                    text='Cancelar',
                    on_release=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='Enviar',
                    on_release=lambda x: self.send_recovery_email(self.email_input.text)
                )
            ]
        )
        self.popup.open()

    @staticmethod
    def enviar_correo(remitente, destinatario, asunto, mensaje, correo, contraseña):
        # Configuración del servidor SMTP de Gmail
        servidor_smtp = "smtp.gmail.com"
        puerto_smtp = 587

        # Crear objeto MIMEText con el contenido del correo electrónico
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario

        try:
            # Iniciar una conexión SMTP segura
            server = smtplib.SMTP(servidor_smtp, puerto_smtp)
            server.starttls()
            server.login(correo, contraseña)

            # Enviar el correo electrónico
            server.sendmail(remitente, destinatario, msg.as_string())

            # Cerrar la conexión SMTP
            server.quit()

            return True
        except Exception as e:
            print("Error al enviar el correo electrónico:", str(e))
            return False    

    def send_recovery_email(self, email):
        # Genera una nueva contraseña aleatoria
        import random
        import string
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Aquí debes utilizar el método enviar_correo con los detalles adecuados
        # Asegúrate de tener configurado el servidor SMTP y las credenciales de correo electrónico correctamente

        # Ejemplo de cómo podrías implementar el envío del correo electrónico de recuperación
        subject = "Recuperación de contraseña"
        message = f"Hola,\n\nTu nueva contraseña es: {new_password}\n\nPor favor, inicia sesión con esta nueva contraseña y cambia tu contraseña después de iniciar sesión."
        sender_email = "tu_correo_electronico@gmail.com"  # Reemplaza con tu dirección de correo electrónico
        sender_password = "tu_contraseña"  # Reemplaza con tu contraseña de correo electrónico

        try:
            self.enviar_correo(sender_email, email, subject, message, sender_email, sender_password)
            self.popup = MDDialog(
                title='Correo enviado',
                text='Se ha enviado un correo electrónico de recuperación a la dirección proporcionada.',
                buttons=[
                    MDFlatButton(
                        text='Cerrar',
                        on_release=self.dismiss_dialog
                    )
                ]
            )
            self.popup.open()
        except Exception as e:
            self.popup = MDDialog(
                title='Error',
                text='Ocurrió un error al enviar el correo electrónico de recuperación.',
                buttons=[
                    MDFlatButton(
                        text='Cerrar',
                        on_release=self.dismiss_dialog
                    )
                ]
            )
            self.popup.open()

    def dismiss_dialog(self, instance):
        if self.popup:
            self.popup.dismiss()
        if self.username_input:
            self.username_input.text = ''




class StartWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(StartWid,self).__init__()
        self.mainwid = mainwid
        
    def create_database(self):
        connect_to_database(self.mainwid.DB_PATH)
        self.mainwid.goto_database()
        self.mainwid.goto_databaseM()

    def create_new_product(self):
        self.mainwid.goto_insertdata()

    def create_new_moto(self):
        self.mainwid.goto_insertdataM()

    def back_to_dbw(self):
        self.mainwid.goto_database() 

    def back_to_dbwM(self):
        self.mainwid.goto_databaseM()  

  
    
class DataBaseWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(DataBaseWid,self).__init__()
        self.mainwid = mainwid
        
    def check_memory(self):
        self.ids.container.clear_widgets()
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID, Nombre, Marca, Costo, Almacen from Productos')
        for i in cursor:
            wid = DataWid(self.mainwid)
            r1 = 'ID: '+str(100000000+i[0])[1:9]+'\n'
            r2 = i[1]+', '+i[2]+'\n'
            r3 = 'Precio por unidad: '+'$'+str(i[3])+'\n'
            r4 = 'En almacen: '+str(i[4])
            wid.data_id = str(i[0])
            wid.data = r1+r2+r3+r4
            self.ids.container.add_widget(wid)

        con.close()
        

class UpdateDataWid(BoxLayout):
    def __init__(self,mainwid,data_id,**kwargs):
        super(UpdateDataWid,self).__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        self.check_memory()

    def check_memory(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'select Nombre, Marca, Costo, Almacen from Productos where ID='
        cursor.execute(s+self.data_id)
        for i in cursor:
            self.ids.ti_nombre.text = i[0]
            self.ids.ti_marca.text = i[1]
            self.ids.ti_costo.text = str(i[2])
            self.ids.ti_almacen.text = str(i[3])
        con.close()

    def update_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_nombre.text
        d2 = self.ids.ti_marca.text
        d3 = self.ids.ti_costo.text
        d4 = self.ids.ti_almacen.text
        a1 = (d1,d2,d3,d4)
        s1 = 'UPDATE Productos SET'
        s2 = 'Nombre="%s",Marca="%s",Costo=%s,Almacen=%s' % a1
        s3 = 'WHERE ID=%s' % self.data_id
        try:
            cursor.execute(s1+' '+s2+' '+s3)
            con.commit()
            con.close()
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
            con.close()

    def delete_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from productos where ID='+self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_database()

    def back_to_dbw(self):
        self.mainwid.goto_database()
        
class InsertDataWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(InsertDataWid,self).__init__()
        self.mainwid = mainwid

    def insert_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_id.text
        d2 = self.ids.ti_nombre.text
        d3 = self.ids.ti_marca.text
        d4 = self.ids.ti_costo.text
        d5 = self.ids.ti_almacen.text
        a1 = (d1,d2,d3,d4,d5)
        s1 = 'INSERT INTO Productos(ID, Nombre, Marca, Costo, Almacen)'
        s2 = 'VALUES(%s,"%s","%s",%s,%s)' % a1
        try:
            cursor.execute(s1+' '+s2)
            con.commit()
            con.close()
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.mainwid.goto_database()





     
    
class DataWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(DataWid,self).__init__()
        self.mainwid = mainwid
        
    def update_data(self,data_id):
        self.mainwid.goto_updatedata(data_id)

    def back_to_dbw(self):
        self.mainwid.goto_database()








class DataBaseWidM(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(DataBaseWidM,self).__init__()
        self.mainwid = mainwid
        
    def check_memory(self):
        self.ids.containerM.clear_widgets()
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID, Placa, Marca, Conductor, FechaAceite from Motos')
        
        for i in cursor:
            wid = DataWidM(self.mainwid)
            r1 = 'ID: '+str(100000000+i[0])[1:9]+'\n'
            r2 = i[1]+', '+i[2]+'\n'
            r3 = 'Conductor: '+''+str(i[3])+'\n'
            r4 = 'Fecha: '+str(i[4])
            wid.data_id = str(i[0])
            wid.data = r1+r2+r3+r4
            self.ids.containerM.add_widget(wid)

        con.close()

        
class InsertDataWidM(BoxLayout):

    root = None  # Agregar el atributo root a la clase Ui
    fecha_seleccionada = StringProperty()
    
    def __init__(self,mainwid,**kwargs):
        super(InsertDataWidM,self).__init__()
        self.mainwid = mainwid
    
    def on_date_save(self, instance, value, date_range):
        self.fecha_seleccionada = str(value)

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def insert_dataM(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_idM.text
        d2 = self.ids.ti_placaM.text
        d3 = self.ids.ti_marcaM.text
        d4 = self.ids.ti_conductorM.text
        d5 = self.fecha_seleccionada
        a1 = (d1,d2,d3,d4,d5)
        s1 = 'INSERT INTO Motos(ID, Placa, Marca, Conductor, FechaAceite)'
        s2 = 'VALUES(%s,"%s","%s","%s","%s")' % a1
        try:
            cursor.execute(s1+' '+s2)
            con.commit()
            con.close()
            self.mainwid.goto_databaseM()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
            con.close()

    def back_to_dbwM(self):
        self.mainwid.goto_databaseM()



class DataWidM(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(DataWidM,self).__init__()
        self.mainwid = mainwid
        
    def update_dataM(self,data_id):
        self.mainwid.goto_updatedataM(data_id)

    def back_to_dbwM(self):
        self.mainwid.goto_databaseM()





        
        


class UpdateDataWidM(BoxLayout):

    root = None  # Agregar el atributo root a la clase Ui
    fecha_seleccionada = StringProperty()

    def __init__(self,mainwid,data_id,**kwargs):
        super(UpdateDataWidM,self).__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        self.check_memory()

    def check_memory(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'select Placa, Marca, Conductor, FechaAceite from Motos where ID='
        cursor.execute(s+self.data_id)
        for i in cursor:
            self.ids.ti_placaM.text = i[0]
            self.ids.ti_marcaM.text = i[1]
            self.ids.ti_conductorM.text = str(i[2])
            self.fecha_seleccionada = str(i[3])
        con.close()

    def on_date_save(self, instance, value, date_range):
        self.fecha_seleccionada = str(value)

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def update_dataM(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_placaM.text
        d2 = self.ids.ti_marcaM.text
        d3 = self.ids.ti_conductorM.text
        d4 = self.fecha_seleccionada
        a1 = (d1,d2,d3,d4)
        s1 = 'UPDATE Motos SET'
        s2 = 'Placa="%s",Marca="%s",Conductor="%s",FechaAceite="%s"' % a1
        s3 = 'WHERE ID=%s' % self.data_id
        try:
            cursor.execute(s1+' '+s2+' '+s3)
            con.commit()
            con.close()
            self.mainwid.goto_databaseM()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
            con.close()

    def delete_dataM(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from Motos where ID='+self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_databaseM()

    def back_to_dbwM(self):
        self.mainwid.goto_databaseM()


class MainApp(MDApp):
    def build(self):
        Window.size = (330, 550) 
        self.theme_cls.primary_palette = "LightBlue"
        return MainWid()
        
if __name__ == '__main__':
    MainApp().run()