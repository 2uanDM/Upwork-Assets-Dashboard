CREATE TRIGGER delete_asset_list BEFORE DELETE ON Asset FOR EACH ROW BEGIN
DELETE FROM AssetImportList
WHERE AssetImportListID = OLD.AssetImportListID;
END;