import json
import sqlite3
import os

with open(os.path.join(os.getcwd(), 'configuration', 'application.json'), "r") as f:
    config = json.load(f)


class CrudDB():
    DATABSE_PATH = os.path.join(os.getcwd(), f'{config["database_name"]}.db')

    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.DATABSE_PATH)
        self.cursor = self.conn.cursor()
        self.conn.execute('PRAGMA foreign_keys = ON;')

    def get_category_id(self, category_name: str) -> int:
        return self.cursor.execute(f"""
            select AssetCategoryID
            from AssetCategory
            where CategoryName = '{category_name}';
        """).fetchone()[0]

    def get_asset_id(self, asset_number: int, asset_name: str, asset_category_name: str) -> int:
        """
        Get the asset id from the database
        Args:
            asset_number (int)
            asset_name (str)
            asset_category_name (str)

        Returns:
            int: The asset id
        """
        return self.cursor.execute(f"""
            select AssetID
            from Asset
            where 1 = 1
            and AssetNumber = {asset_number}
            and AssetName = '{asset_name}'
            and AssetCategoryID = (
                select AssetCategoryID
                from AssetCategory
                where CategoryName = '{asset_category_name}'
            );
        """).fetchone()[0]

    def get_list_of_asset_categories(self) -> list:
        """
        Return a list of asset categories
        """
        return [category[0] for category in self.cursor.execute("SELECT CategoryName FROM AssetCategory").fetchall()]

    def get_list_of_image_categories(self) -> list:
        """
        Return a list of image categories
        """
        return [category[0] for category in self.cursor.execute("SELECT CategoryName FROM ImageCategory").fetchall()]

    def get_list_of_asset_images(self, asset_number: int, asset_name: str, asset_category_name: str) -> list:
        # Get the AssetID of the asset
        asset_id: int = self.get_asset_id(asset_number, asset_name, asset_category_name)
        return [image[0] for image in self.cursor.execute(f"""
            select ImageFileName
            from AssetImage
            where AssetID = {asset_id};
        """).fetchall()]

    def load_master_table(self) -> dict:
        """
        return {

            "total_assets": The total number of assets in the database

            "total_pages":  The total number of pages in the database

            "data":  The data to be displayed in the table. List of tuples (AssetNumber, AssetName, CategoryName)
        }
        """
        # Count the number of assets in the database
        total_assets = self.cursor.execute("SELECT COUNT(*) FROM Asset").fetchall()[0][0]

        # Since the table can hold maximum 10 rows, we have to count the number of pages
        if total_assets == 0:
            total_pages = 1
            return {
                "total_assets": total_assets,
                "total_pages": total_pages,
                "data": [],
            }
        else:
            total_pages = total_assets // 10 + 1 if (total_assets %
                                                     10 != 0 or total_assets == 0) else total_assets // 10

            all_assets = self.cursor.execute("""
            SELECT AssetNumber, AssetName, ac.CategoryName
            FROM Asset AS a
            JOIN AssetCategory AS ac
            ON a.AssetCategoryID = ac.AssetCategoryID
            ORDER BY AssetNumber
            """).fetchall()

            return {
                "total_assets": total_assets,
                "total_pages": total_pages,
                "data": all_assets,
            }

    def load_asset_detail_table(self, asset_number: int, asset_name: str, asset_category_name: str) -> tuple:
        """
        Call whenever click on a row in master tabel to query the detail of that asset
        Args:
            asset_number (int)
            asset_name (str)
            asset_category (str)

        Returns:
            tuple: (AssetVariant, AssetDescription, ImportlistHeader, Importlist_2ndRow, Importlist_3ndRow)
        """
        asset_id = self.get_asset_id(asset_number, asset_name, asset_category_name)

        command = self.cursor.execute(f"""
            select 
                    a.AssetVariant,
                    a.AssetDescription,
                    ImportlistHeader,
                    Importlist_2ndRow,
                    Importlist_3ndRow
            from Asset as a 
            join AssetImportList as ail 
                on ail.AssetID = a.AssetID
            where a.AssetID = {asset_id};                                
                                      """)
        return command.fetchone()

    def create_new_asset(self) -> bool:

        # Get the smallest available AssetCategoryID
        asset_category_id: int = self.cursor.execute("""
            select AssetCategoryID
            from AssetCategory
            order by AssetCategoryID
            limit 1;
            """).fetchone()[0]

        # Insert a new row into Asset table
        operation = self.cursor.execute(f"""
            insert into Asset (AssetNumber, AssetName, AssetVariant, AssetDescription, AssetCategoryID)
            values (9999999, 'example', 'example', 'example', {asset_category_id});
                            """)
        if operation.rowcount == 0:
            return False

        # Get the AssetID of the newly created row
        asset_id = self.cursor.execute("select last_insert_rowid()").fetchone()[0]

        # Insert a new row into AssetImportList table
        operation = self.cursor.execute(f"""
            insert into AssetImportList ('AssetID',ImportlistHeader, Importlist_2ndRow, Importlist_3ndRow)
            values ({asset_id},'', '', '');
                            """)
        if operation.rowcount == 0:
            return False

        self.conn.commit()
        return True

    def create_new_image(self,
                         asset_number: int,
                         asset_name: str,
                         asset_category_name: str,
                         image_file_name: str,
                         image_category_name: str) -> bool:
        # Get the AssetID of the asset
        asset_id: int = self.get_asset_id(asset_number, asset_name, asset_category_name)

        # Get the ImageCategoryID of the image category
        image_category_id: int = self.cursor.execute(f"""
            select ImageCategoryID
            from ImageCategory
            where CategoryName = '{image_category_name}';
        """).fetchone()[0]

        # Insert a new row into AssetImage table
        operation = self.cursor.execute(f"""
            insert into AssetImage (AssetID, ImageFileName, ImageCategoryID)
            values ({asset_id}, '{image_file_name}', {image_category_id});
        """)
        if operation.rowcount == 0:
            return False

        self.conn.commit()
        return True

    def update_asset_table(self,
                           asset_id: int,
                           asset_number: int,
                           asset_name: str,
                           asset_variant: str,
                           asset_category_id: int,
                           asset_description: str,
                           ) -> bool:
        operation = self.cursor.execute(f"""
            update Asset 
            set 
                AssetName = '{asset_name}', 
                AssetNumber = {asset_number},
                AssetVariant = '{asset_variant}',
                AssetDescription = '{asset_description}',
                AssetCategoryID = {asset_category_id}
            where AssetID = {asset_id};                    
                                        """)

        # Check if the operation is successful
        if operation.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def update_asset_import_list(self,
                                 asset_id: int,
                                 import_list_header: str,
                                 import_list_2nd_row: str,
                                 import_list_3nd_row: str) -> bool:

        opearation = self.cursor.execute(f"""
            update AssetImportList 
            set 
                ImportlistHeader = '{import_list_header}',
                Importlist_2ndRow = '{import_list_2nd_row}',
                Importlist_3ndRow = '{import_list_3nd_row}'
            where AssetID = {asset_id};
                                         """)

        # Check if the operation is successful
        if opearation.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def delete_asset(self, asset_number: int, asset_name: str, asset_category_name: str) -> bool:
        """
        Delete an asset from the database
        Args:
            asset_number (int)
            asset_name (str)
            asset_category_name (str)

        Returns:
            None
        """
        asset_id = self.get_asset_id(asset_number, asset_name, asset_category_name)

        operation = self.cursor.execute(f"""
            delete from Asset
            where AssetID = {asset_id};
        """)

        # Check if the operation is successful
        if operation.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def __del__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    crud = CrudDB()
    # print(crud.load_master_table())
    crud.test()
