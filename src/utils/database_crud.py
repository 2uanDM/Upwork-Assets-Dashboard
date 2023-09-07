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
            total_pages = total_assets // 10 + 1 if total_assets % 10 != 0 else total_assets // 10

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
        command = self.cursor.execute(f"""
            select 
                    a.AssetVariant,
                    a.AssetDescription,
                    ImportlistHeader,
                    Importlist_2ndRow,
                    Importlist_3ndRow
            from Asset as a 
            join AssetCategory as ac 
                on ac.AssetCategoryID = a.AssetCategoryID
            join AssetImportList as ail 
                on ail.AssetImportListID = a.AssetImportListID
            where 1 = 1 
            and a.AssetNumber = {asset_number}
            and a.AssetName = '{asset_name}'
            and ac.CategoryName = '{asset_category_name}';                                  
                                      """)
        return command.fetchone()

    def delete_asset(self, asset_number: int, asset_name: str, asset_category_name: str) -> None:
        """
        Delete an asset from the database
        Args:
            asset_number (int)
            asset_name (str)
            asset_category_name (str)

        Returns:
            None
        """
        operation = self.cursor.execute(f"""
            delete from Asset
            where 1 = 1
            and AssetNumber = {asset_number}
            and AssetName = '{asset_name}'
            and AssetCategoryID = (
                select AssetCategoryID
                from AssetCategory
                where CategoryName = '{asset_category_name}'
            );
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


# if __name__ == '__main__':
#     crud = CrudDB()
#     # print(crud.load_master_table())
#     print(crud.load_asset_detail_table(1103, 'Pencil Sharpener', 'Office Supplies'))
