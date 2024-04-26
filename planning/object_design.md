# PYuGiOh Object Design

## Cardlist
* runs off of MySQL database for card storage
* loads from stored json file on start
* 

## Collection
* loads from stored json file with .coll extension when selected
* connects to decks via GUID
* attributes
    - alias [str]: name of collection
    - created [str]: ISO-8601 timestamp of when collection was created
    - modified [str]: ISO-8601 timestamp of when collection was last modified
    - cards [list[dict]]: list of cards in collection
        - key-value pairs
            - 'passcode': passcode of card
            - 'setcode': displays set code of card
            - 
    - size [int]: number of cards in collection
    - note [list[str]]: notes assigned to collection