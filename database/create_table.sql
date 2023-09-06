CREATE TABLE Asset (
    AssetID INTEGER PRIMARY KEY AUTOINCREMENT,
    AssetName TEXT,
    AssetNumber INTEGER,
    AssetVariant TEXT,
    AssetDescription TEXT,
    AssetCategoryID INTEGER REFERENCES AssetCategory(AssetCategoryID),
    AssetAttributeID INTEGER REFERENCES AssetAttribute(AssetAttributeID),
    AssetShapeID INTEGER REFERENCES AssetShape(AssetShapeID),
    AssetImportlistID INTEGER REFERENCES AssetImportlist(AssetImportlistID),
    AssetImageID INTEGER REFERENCES AssetImage(AssetImageID)
);