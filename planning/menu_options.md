# PYuGiOh Menu Tree

 * card: submenu for cardlist operations
    - count: print cardlist stats like total count, breakdown by card types, etc.
    - version: print out the version of the cardlist
    - update: pull the newest version of the cardlist using YGOPRODECK API
    - view: navigate to page view of all cards in the cardlist
    - search: nevigate to page view of filtered cardlist based on passed in search terms
 * coll: submenu for collection operations
    - view: navigate to the view menu for the selected collection
    - select: change selected collection; no args will display collections that can be selected
        - name [str]: name of collection to be selected
    - add: add cards to the selected collection
        - code [int]: passcode of the card(s) to be added
        - -quant | -q [int]: quantity of card to be added
        - -setcode | -sc [bool]: takes in setcodes instead of passcodes
        - --set [str]: adds all cards in a set to the collection
    - search: navigate to a filtered view of the selected collection based on entered search terms
    - new: create new collection and select it automatically
        - -o [bool]: override automatic selection, will create new collection without switching to it
        - name [str]: assigns name to new collection
    - alias: change name of collection
        - newname [str]: new name for collection
    - remove: removes cards from collection
        --recursive | -r: overrides recursive remove, will keep 
 * deck: submenu for deck operations
    - view: show the name, notes, and contents of the deck
    - select: change the selected deck; all selectable decks will be printed if no args passed
    - add: add cards to the selected deck
        - --note | -n [str]: list of strings to be added as notes for the file
    - new: create a new deck assigned to the selected collection
    - alias: change name of selected deck
    - assign: assigns a deck to a different collection
    - note: submenu for managing deck notes
        - (no args): print all notes for the selected deck
        - edit: edit an existing note
            - id [int]: index of the note to be added
        - add: attach a new note to the selected deck
        - remove: remove a note from the selected deck
            - id [int]: index of the note to be removed
 * config: submenu for settings and root operations
    - remove: submenu for removing collections or decks
    - default: submenu for setting a collection or deck as default
    - merge: capability for merging collections
    - rainbow: submenu for console color customization (?)
    - user: submenu for user settings and operations