import unittest
from unittest.mock import patch, Mock
from utils.qr_code_utils import QrCode

class TestQrCode(unittest.TestCase):

    @patch('utils.qr_code_utils.ImageTk.PhotoImage')
    @patch('utils.qr_code_utils.tk.Toplevel')
    @patch('utils.qr_code_utils.tk.Label')
    @patch('utils.qr_code_utils.qrcode')
    def test_show_qr_code(self, mock_qrcode, mock_label, mock_toplevel, mock_photimage):
        mock_qr_instance = Mock()
        mock_qrcode.QRCode.return_value = mock_qr_instance

        mock_img_instance = Mock()
        mock_photimage.return_value = mock_img_instance

        mock_toplevel_instance = Mock()
        mock_toplevel.return_value = mock_toplevel_instance

        mock_label_instance = Mock()
        mock_label.return_value = mock_label_instance

        mock_qrcode.constants.ERROR_CORRECT_L = 1

        test_url = "https://example.com"
        QrCode.show_qr_code(test_url)

        mock_qrcode.QRCode.assert_called_once_with(
            version=1,
            error_correction=mock_qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4
        )
        mock_qr_instance.add_data.assert_called_once_with(test_url)
        mock_qr_instance.make.assert_called_once_with(fit=True)
        mock_qr_instance.make_image.assert_called_once_with(fill_color="black", back_color="white")

        mock_photimage.assert_called_once_with(mock_qr_instance.make_image())

        mock_toplevel.assert_called_once()
        mock_toplevel_instance.title.assert_called_once_with("QR Code")
        mock_toplevel_instance.geometry.assert_called_once_with("600x600")

        mock_label.assert_called_once_with(mock_toplevel_instance, image=mock_img_instance)
        mock_label_instance.pack.assert_called_once()
        self.assertEqual(mock_label_instance.image, mock_img_instance)

        mock_toplevel_instance.mainloop.assert_called_once()

if __name__ == "__main__":
    unittest.main()
