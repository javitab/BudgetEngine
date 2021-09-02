import bbdata as bb
import pprint

def recView():
    print("Listing available collections")
    print(bb.bbdb.list_collection_names())
    col = input("What collection would you like to enter? # ")
    print("Listing all records in %s" % col)
    colDf = bb.convDf(bb.listCollection(col))
    bb.printDf(colDf)
    rec = input("Enter the name of the record you would like to view: # ")
    record = bb.printRecord(col, rec)
    for i in record:
        pprint.pprint(i)
        #bb.printAsDataFrame(i)
    startEdit = input("Would you like to modify this record? (y/n)")
    if (startEdit == 'y'):
        itemToEdit = input("Please enter the name of the item that you would like to edit as listed in record above: # ")
        