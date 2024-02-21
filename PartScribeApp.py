##Inchcape Digital PartScribeApp

import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt6.QtGui import QImage, QPixmap, QImageReader
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlDatabase
from PIL import Image
import traceback
from main import Ui_MainWindow
from login import Ui_dlgLogin
from rename import Ui_Rename

SERVER_NAME = 'az-aue-au-sql-dev-dpp-001.database.windows.net'
DATABASE_NAME = 'epc-subaru'

class Rename(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Rename()
        self.ui.setupUi(self)

        self.ui.btnAddItem.clicked.connect(self.add_item)

        self.ui.btnInputDir.clicked.connect(self.InputDir)

        self.ui.btnOutputDir.clicked.connect(self.OutputDir)

        self.ui.btnCopyRename.clicked.connect(self.CopyandRename)

    def add_item(self):
        row_position = self.ui.tblRename.rowCount()
        self.ui.tblRename.insertRow(row_position)

    def InputDir(self):
        infiledir = QFileDialog.getExistingDirectory(self, 'Select input directory', '/home')
        self.ui.lblInputDir.setText(f'{infiledir}')

    def OutputDir(self):
        outfiledir = QFileDialog.getExistingDirectory(self, 'Select input directory', '/home')
        self.ui.lblOutputDir.setText(f'{outfiledir}')

    def CopyandRename(self):
        src = self.ui.lblInputDir.text()
        dest = self.ui.lblOutputDir.text()

        try:
            if src and dest:
                for row in range(self.ui.tblRename.rowCount()):
                    old_name = self.ui.tblRename.item(row, 0).text()
                    
                    brand_prefix = self.ui.tblRename.item(row, 3).text()[:3].upper()
                    
                    prodid = self.ui.tblRename.item(row, 2).text().upper()
                    
                    imgno = self.ui.tblRename.item(row, 1).text().upper()
                    
                    suffix = 'masterProductCatalog'

                    filetype = os.path.splitext(old_name)[1]

                    new_name = f'{brand_prefix}{prodid}-{imgno}-{suffix}{filetype}'

                    self.ui.tblRename.setItem(row, 4, QTableWidgetItem(new_name))

            if new_name:
                old_path = os.path.join(src, old_name)
                new_path = os.path.join(dest, new_name)

                try:
                    copyfile(old_path, new_path)
                except Exception as e:
                    print(f'Error: {e}')     

        except Exception as exception:
            traceback.print_exc()

class Login(QDialog):
    def __init__(self):
        super().__init__()
        #loadUi("login.py",self)

        self.ui = Ui_dlgLogin()
        self.ui.setupUi(self)

        self.ui.btnSignIn.clicked.connect(self.connectToDB)

    # Connect to SQL server using credentials
    def connectToDB(self):
        USERNAME = self.ui.txtUser.toPlainText()
        PASSWORD = self.ui.txtPassword.text()

        connString = f'DRIVER={{SQL Server}};'\
                f'SERVER={SERVER_NAME};'\
                f'DATABASE={DATABASE_NAME};'\
                f'UID={USERNAME};'\
                f'PWD={PASSWORD}'

        global db
        db = QSqlDatabase.addDatabase('QODBC')
        db.setDatabaseName(connString)

        if db.open():
            self.ui.lblStatus.setText("Sign In Successful")
            self.accept()
            
            # Open main window on successful login
            main_window.show()
            
        else:
            self.ui.lblStatus.setText("Sign In Failed")
            
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        #loadUi("main.py",self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize image property label
        self.ui.lblImgPropHeader.hide()
        
        # Create a status bar
        self.ui.statusBar.showMessage(f'Ready')

        # Open dialog box for image input
        self.ui.btnSelImg.clicked.connect(self.dlgOpen)

        # Open dialog box for folder selection
        self.ui.btnSelDir.clicked.connect(self.dlgDir)

        # Initiate watermark addition
        self.ui.btnSelectWM.clicked.connect(self.dlgOpenWM)

        # Initiate slider
        self.ui.slider_value = 80
        self.ui.sldTransparency.valueChanged.connect(self.update_value)

        # Default button action
        self.ui.btnApplyWM.clicked.connect(self.watermark)

        # Initiate Batch or Single toggle
        self.ui.tbBatch.stateChanged.connect(self.checkbox_changed)

        self.ui.actionRename.triggered.connect(self.show_rename)       

    def show_rename(self):
        rename_screen.show()
   
    def checkbox_changed(self, state):
        if state == 2:  # 2 corresponds to the checked state
            self.ui.btnApplyWM.clicked.disconnect(self.watermark)
            self.ui.btnApplyWM.clicked.connect(self.batch_watermark)
        else:
            self.ui.btnApplyWM.clicked.disconnect(self.batch_watermark)
            self.ui.btnApplyWM.clicked.connect(self.watermark)

    def update_value(self, value):
        # Update the label text and store the value in a variable
        self.ui.lblSlider.setText(f'{value}')
        self.ui.slider_value = value

    def dlgOpen(self):
        global filename, imgfilename
        filepath = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Images (*.png *.jpg *.bmp *.gif)")

        if filepath[0]:
            filename = filepath[0]
            imgfilename = os.path.basename(filename)

            #Display Image Metadata
            image = QImageReader(filename).read()
            self.ui.lblImgPropHeader.show()
            properties_text = f"Product Image\n"
            properties_text += f"File Name: {imgfilename}\n"
            properties_text += f"Size: {image.sizeInBytes()} bytes\n"
            properties_text += f"Width: {image.width()} pixels\n"
            properties_text += f"Height: {image.height()} pixels\n"
            properties_text += f"Format: {filename.split('.')[-1]}\n"

            self.ui.lblImgProp.setText(properties_text)

            # Ensure that the image is within file size limit and within 4k resolution
            self.resize_image()

            # Load resized image in the previewer
            self.loadImage()
            self.ui.lblFile.setText(f'{filename}')
            self.ui.statusBar.showMessage(f'Selected product image: {filename}')

    def dlgOpenWM(self):
        global wmfilename, wmimgfilename
        wmfilename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Images (*.png)")
        wmfilename = wmfilename[0]
        wmimgfilename = os.path.basename(wmfilename)

        #Display Image Metadata
        wmimage = QImageReader(wmfilename).read()
        wm_prop_text = f"Watermark Image\n"
        wm_prop_text += f"File Name: {wmimgfilename}\n"
        wm_prop_text += f"Size: {wmimage.sizeInBytes()} bytes\n"
        wm_prop_text += f"Width: {wmimage.width()} pixels\n"
        wm_prop_text += f"Height: {wmimage.height()} pixels\n"
        wm_prop_text += f"Format: {wmfilename.split('.')[-1]}\n"

        self.ui.lblWmImgProp.setText(wm_prop_text)

        self.ui.lblWM.setText(f'{wmfilename}')
        self.ui.statusBar.showMessage(f'Selected watermark: {wmfilename}')
            
    def dlgDir(self):
        global filedir
        filedir = QFileDialog.getExistingDirectory(self, 'Select Directory', '/home')
        self.ui.lblDir.setText(f'{filedir}')
        self.ui.statusBar.showMessage(f'Selected output directory: {filedir}')

    def loadImage(self):
        image = QImage(f'{filename}_temp.png')

        if image.isNull():
            self.ui.statusBar.showMessage('Error loading image')
            return

        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.ui.lblImage.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.lblImage.setPixmap(scaled_pixmap)
        
        os.remove(f'{filename}_temp.png')
            
    def watermark(self):
        # Ensure that the image is within file size limit and within 4k resolution
        self.resize_image()

        self.resize_watermark()
        
        transparency = (self.ui.slider_value * 255) / 100

        WmPos = self.ui.cbWmPos.currentText()

        # Open the input image
        original_image = Image.open(f'{filename}_temp.png')

        # Open the watermark image
        watermark = Image.open(f'{wmfilename}_temp.png')

        # Define padding values
        horizontal_padding = 50
        vertical_padding = 50

        # Calculate position based on the chosen option
        if WmPos == 'Top, Left':
            position = (horizontal_padding, vertical_padding)
        elif WmPos == 'Top, Center':
            position = (original_image.width // 2 - watermark.width // 2, vertical_padding)
        elif WmPos == 'Top, Right':
            position = (original_image.width - watermark.width - horizontal_padding, vertical_padding)
        elif WmPos == 'Center, Left':
            position = (horizontal_padding, original_image.height // 2 - watermark.height // 2)
        elif WmPos == 'Center':
            position = (original_image.width // 2 - watermark.width // 2, original_image.height // 2 - watermark.height // 2)
        elif WmPos == 'Center, Right':
            position = (original_image.width - watermark.width - horizontal_padding, original_image.height // 2 - watermark.height // 2)
        elif WmPos == 'Bottom, Left':
            position = (horizontal_padding, original_image.height - watermark.height - vertical_padding)
        elif WmPos == 'Bottom, Center':
            position = (original_image.width // 2 - watermark.width // 2, original_image.height - watermark.height - vertical_padding)
        elif WmPos == 'Bottom, Right':
            position = (original_image.width - watermark.width - horizontal_padding, original_image.height - watermark.height - vertical_padding)
        else:
            raise ValueError(f"Invalid position: {position}")

        # Ensure the watermark has an alpha channel (transparency)
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')

        # Adjust the transparency of the watermark
        watermark = watermark.convert('RGBA')

        watermark_with_transparency = Image.new('RGBA', watermark.size)

        for x in range(watermark.width):
            for y in range(watermark.height):
                r, g, b, a = watermark.getpixel((x, y))
                watermark_with_transparency.putpixel((x, y), (r, g, b, int(a * (transparency / 255.0))))

        # Create a transparent layer the same size as the original image
        watermark_layer = Image.new('RGBA', original_image.size, (0, 0, 0, 0))

        # Paste the watermark with transparency onto the transparent layer at the calculated position
        watermark_layer.paste(watermark_with_transparency, position, mask=watermark_with_transparency)

        # Combine the original image with the watermark layer
        watermarked_image = Image.alpha_composite(original_image.convert('RGBA'), watermark_layer)

        # Save the watermarked image
        basename = os.path.splitext(os.path.basename(imgfilename))[0]
        watermarked_image.save(f'{filedir}/{basename}.png')
        self.ui.statusBar.showMessage(f'Image processed and saved to output directory: {filedir}/{basename}.png')

        # Preview image
        image = QImage(f'{filedir}/{basename}.png')
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.ui.lblImage.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.lblImage.setPixmap(scaled_pixmap)

        # Cleanup
        os.remove(f'{filename}_temp.png')
        os.remove(f'{wmfilename}_temp.png')

    def resize_image(self):
        # Open the image
        original_image = Image.open(filename)
        
        # Calculate new dimensions while maintaining the aspect ratio
        global Res
        ImgRes = self.ui.cbRes.currentText()
        if ImgRes == '1200 x 1200':
            Res = (1200, 1200)
        elif ImgRes == '515 x 515':
            Res = (515, 515)
        elif ImgRes == '365 x 246':
            Res = (365, 246)
        elif ImgRes == '300 x 300':
            Res = (300, 300)
        elif ImgRes == '96x 96':
            Res = (96, 96)
        elif ImgRes == '65 x 65':
            Res = (65, 65)
        elif ImgRes == '30 x 30':
            Res = (30, 30)
        else:
            if float(original_image.size[0]) > 3840 or float(original_image.size[1]) > 3840:
                Res = (3840, 2160)
            else:
                Res = (original_image.size[0], original_image.size[1])

        width_percent = Res[0] / float(original_image.size[0])
        height_percent = Res[1] / float(original_image.size[1])
        new_width = int(original_image.size[0] * min(width_percent, height_percent))
        new_height = int(original_image.size[1] * min(width_percent, height_percent))

        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        resized_image.save(f'{filename}_temp.png')

    def resize_watermark(self):
        # Open the image
        watermark_image = Image.open(wmfilename)
        
        # Scale watermark with image dimension while maintaining the aspect ratio
        width_percent = Res[0]*0.2 / float(watermark_image.size[0])

        height_percent = Res[1]*0.2 / float(watermark_image.size[1])
            
        new_width = int(watermark_image.size[0] * min(width_percent, height_percent))
        new_height = int(watermark_image.size[1] * min(width_percent, height_percent))

        # Resize the image
        resized_image = watermark_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        resized_image.save(f'{wmfilename}_temp.png')

    def batch_watermark(self):
        global filename, wmfilename, imgfilename

        filename = self.ui.lblFile.text()
        wmfilename = self.ui.lblWM.text()
        
        input_folder = os.path.dirname(filename)

        # List all files in the input folder
        all_files = os.listdir(input_folder)

        # Filter only image files (you may want to extend this list)
        image_files = [file for file in all_files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        for image_file in image_files:
            filename = os.path.join(input_folder, image_file)
            imgfilename = image_file
            self.watermark()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create instances of LoginScreen and MainWindow
    login_screen = Login()
    main_window = Main()
    rename_screen = Rename()

    # Show the login screen initially
    login_screen.show()

    sys.exit(app.exec())
