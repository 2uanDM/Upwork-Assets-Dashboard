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

    def check_if_asset_attribute_exists(self,
                                        asset_id: int,
                                        attribute_order_number: int,
                                        attribute_name: str,
                                        data_type_name: str,
                                        attribute_remark: str) -> bool:
        count: int = self.cursor.execute(f"""
            select count(*)
            from AssetAttribute as aa
            join DataType as dt 
            on aa.DataTypeID = dt.DataTypeID
            where 1 = 1
            and aa.AssetID = {asset_id}
            and aa.AttributeOrderNumber = {attribute_order_number}
            and aa.AttributeName = '{attribute_name}'
            and dt.DataTypeName = '{data_type_name}'
            and aa.AttributeRemark = '{attribute_remark}';
            """).fetchone()[0]

        if count == 0:
            return False
        else:
            return True

    def get_asset_name_frome_asset_id(self, asset_id: int) -> str:
        return self.cursor.execute(f"""
            select AssetName
            from Asset
            where AssetID = {asset_id};
        """).fetchone()[0]

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

    def get_list_of_data_types(self) -> list:
        """
        Return a list of data types
        """
        return [data_type[0] for data_type in self.cursor.execute("SELECT DataTypeName FROM DataType").fetchall()]

    def get_list_of_image_categories(self) -> list:
        """
        Return a list of image categories
        """
        return [category[0] for category in self.cursor.execute("SELECT CategoryName FROM ImageCategory").fetchall()]

    def get_list_of_asset_images(self, asset_id: int) -> list:
        # Get the AssetID of the asset
        return [image[0] for image in self.cursor.execute(f"""
            select ImageFileName
            from AssetImage
            where AssetID = {asset_id};
        """).fetchall()]

    def get_asset_image_category_name(self, asset_id: int, image_name: str) -> str:
        return self.cursor.execute(f"""
            select ic.CategoryName
            from AssetImage as ai
            join ImageCategory as ic
            on ai.ImageCategoryID = ic.ImageCategoryID
            where ai.AssetID = {asset_id} and ai.ImageFileName = '{image_name}';
        """).fetchone()[0]

    def get_list_of_shape_types(self) -> list:
        return [x[0] for x in self.cursor.execute(f"select TypeName from ShapeType;").fetchall()]

    def load_all_assets_data(self) -> dict:
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

    def load_asset_attribute_table(self, asset_id: int) -> list:
        return self.cursor.execute(f"""
            select AttributeOrderNumber, AttributeName, DataTypeName, AttributeRemark
            from AssetAttribute as aa
            join DataType as dt
                on aa.DataTypeID = dt.DataTypeID
            where aa.AssetID = {asset_id}
            """).fetchall()

    def load_asset_shape_table(self, asset_id: int) -> list:
        return self.cursor.execute(f"""
            select AssetShapeID, TypeName, ShapeDescription
            from AssetShape as ash
            join ShapeType as st
                on ash.ShapeTypeID = st.ShapeTypeID
            where ash.AssetID = {asset_id};
            """).fetchall()

    def create_new_asset(self) -> bool:

        # Get the smallest available AssetCategoryID
        asset_category_id: int = self.cursor.execute("""
            select AssetCategoryID
            from AssetCategory
            order by AssetCategoryID
            limit 1;
            """).fetchone()[0]

        # Get the biggest AssetNumber
        asset_number: int = self.cursor.execute("""
            select AssetNumber
            from Asset
            order by AssetNumber desc
            limit 1;
            """).fetchone()[0]

        # Insert a new row into Asset table
        operation = self.cursor.execute(f"""
            insert into Asset (AssetNumber, AssetName, AssetVariant, AssetDescription, AssetCategoryID)
            values ({asset_number + 111}, 'example{asset_number + 111}', 'example{asset_number + 111}', 'example{asset_number + 111}', {asset_category_id});
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
                         asset_id: int,
                         image_file_name: str,
                         image_category_name: str) -> bool:
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

    def create_new_attribute(self, asset_id: int) -> bool:
        # Get the biggest AttributeOrderNumber of the asset
        attribute_order_number: int = self.cursor.execute(f"""
            select max(AttributeOrderNumber)
            from AssetAttribute
            where AssetID = {asset_id};
        """).fetchone()[0]

        if attribute_order_number is None:
            attribute_order_number = 1
        else:
            attribute_order_number += 1

        operation = self.cursor.execute(f"""
            insert into AssetAttribute (AssetID, AttributeOrderNumber, AttributeName, DataTypeID, AttributeRemark)
            values ({asset_id}, {attribute_order_number}, '', 1, '');
        """)
        if operation.rowcount == 0:
            return False

        self.conn.commit()
        return True

    def create_new_shape(self, asset_id: int) -> bool:
        # Get the smallest ShapeTypeID
        shape_type_id: int = self.cursor.execute(f"""
            select ShapeTypeID
            from ShapeType
            order by ShapeTypeID
            limit 1;
        """).fetchone()[0]

        if shape_type_id is None:
            shape_type_id = 1

        operation = self.cursor.execute(f"""
            insert into AssetShape (AssetID, ShapeTypeID, ShapeDescription)
            values ({asset_id}, {shape_type_id}, 'Example Description');
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

    def update_asset_attribute(self, asset_id: int, new_attributes: list) -> bool:
        """
        Update the AssetAttribute of an asset in the database
        Args:
            asset_id (int): The AssetID of the asset to be updated in the database
            new_attributes (list): A list of tuple (AttributeOrderNumber, AttributeName, DataTypeName, AttributeRemark)

        Returns:
            bool: The result of the operation: True if successful, False otherwise
        """

        # Delete all the attributes of the asset
        operation = self.cursor.execute(f"""
            delete from AssetAttribute
            where AssetID = {asset_id};
        """)

        # Check if the operation is successful
        if operation.rowcount == 0:
            return False

        # Insert the new attributes
        for new_att in new_attributes:
            new_att_order_number = new_att[0]
            new_att_name = new_att[1]
            new_att_data_type_name = new_att[2]
            new_att_remark = new_att[3]

            operation = self.cursor.execute(f"""
                insert into AssetAttribute (AssetID, AttributeOrderNumber, AttributeName, DataTypeID, AttributeRemark)
                values (
                    {asset_id},
                    {new_att_order_number},
                    '{new_att_name}',
                    (select DataTypeID from DataType where DataTypeName = '{new_att_data_type_name}'),
                    '{new_att_remark}'
                );
                                            """)

            # Check if the operation is successful
            if operation.rowcount == 0:
                return False

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

    def delete_asset_attribute(self, asset_id: int, row_data: tuple) -> bool:
        """
        Delete an attribute from the database of an asset
        Args:
            asset_id (int): The AssetID of the asset to be deleted
            row_data (list): The data of the row to be deleted (AttributeOrderNumber: int, AttributeName: str, DataTypeName: str, AttributeRemark: str)

        Returns:
            bool: True if the operation is successful, False otherwise
        """

        operation = self.cursor.execute(f"""
            delete from AssetAttribute
            where 1 = 1
            and AssetID = {asset_id}
            and AttributeOrderNumber = {row_data[0]}
            and AttributeName = '{row_data[1]}'
            and AttributeRemark = '{row_data[3]}'
            and DataTypeID = (
                select DataTypeID
                from DataType
                where DataTypeName = '{row_data[2]}'
            );
        """)

        # Check if the operation is successful
        if operation.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def delete_asset_image(self, asset_id: int, asset_image_name: str) -> bool:
        """
        Delete an image from the database
        Args:
            asset_id (int)
            asset_image_name (str)

        Returns:
            True if the operation is successful, False otherwise
        """
        operation = self.cursor.execute(f"""
            delete from AssetImage
            where AssetID = {asset_id} and ImageFileName = '{asset_image_name}';
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
    print(crud.get_list_of_shape_types())
