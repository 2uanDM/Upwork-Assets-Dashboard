from PIL import Image
import sys
import os
sys.path.append(os.getcwd())


class ImageResize():
    temp_folder_dir = os.path.join(os.getcwd(), '.temp')
    asset_pictures_dir = os.path.join(os.getcwd(), 'asset_pictures')
    MASTER_TABLE_HEIGHT = 63
    MEDIA_FRAME_HEIGHT = 130

    def fit_master_table(self, asset_id: int, asset_name: str, image_name: str):
        """
        Resize the image to fit the master table
        Args:
            asset_id (int): Example: 1
            asset_name (str): Example: 'Asset 1'
            image_name (str): Example: 'image.png'
        """
        image_dir = os.path.join(self.asset_pictures_dir, f'{asset_id}_{asset_name}', f'{image_name}')
        # Load the image
        image = Image.open(image_dir)
        # Get the width and height of the image
        width, height = image.size
        # Get the ratio of the image
        ratio = width / height
        # Resize the image that the height is MASTER_TABLE_HEIGHT
        image = image.resize((int(self.MASTER_TABLE_HEIGHT * ratio), self.MASTER_TABLE_HEIGHT))
        # Save the image to the temp folder
        temp_asset_image_folder = os.path.join(self.temp_folder_dir, f'{asset_id}_{asset_name}')

        if not os.path.exists(temp_asset_image_folder):
            os.mkdir(temp_asset_image_folder)

        image.save(os.path.join(temp_asset_image_folder, f'{image_name}^mastertable.png'))

    def fit_media_frame(self, asset_id: int, asset_name: str, image_name: str):
        """
        Resize the image to fit the media frame
        Args:
            asset_id (int): Example: 1
            asset_name (str): Example: 'Asset 1'
            image_name (str): Example: 'image.png'
        """
        image_dir = os.path.join(self.asset_pictures_dir, f'{asset_id}_{asset_name}', f'{image_name}')
        # Load the image
        image = Image.open(image_dir)
        # Get the width and height of the image
        width, height = image.size
        # Get the ratio of the image
        ratio = width / height
        # Resize the image that the height is MASTER_TABLE_HEIGHT
        image = image.resize((int(self.MEDIA_FRAME_HEIGHT * ratio), self.MEDIA_FRAME_HEIGHT))
        # Save the image to the temp folder
        temp_asset_image_folder = os.path.join(self.temp_folder_dir, f'{asset_id}_{asset_name}')

        if not os.path.exists(temp_asset_image_folder):
            os.mkdir(temp_asset_image_folder)

        image.save(os.path.join(temp_asset_image_folder, f'{image_name}^mediaframe.png'))


# if __name__ == "__main__":
#     image_resize = ImageResize()
#     image_resize.fit_master_table(1, 'Laptop', 'spinner.jpg')
