import sqlite3
import os


class CrudDB():
    DATABSE_PATH = os.path.join(os.getcwd(), 'new_assetDB.db')

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

    def __del__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


# if __name__ == '__main__':
#     crud = CrudDB()
#     # print(crud.load_master_table())
