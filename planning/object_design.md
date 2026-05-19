# PYuGiOh Object Design

## Cardlist
* runs off of MySQL database for card storage
    - use SQLite for 
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

## Deck
* loaded from a stored txt file with extension .deck
* should be a group of Card objects in some structure (list? list of dicts? tuple of dicts?)
* Attributes
    - cards [array]: list of cards in deck
    - xtra_cards [array]: list of cards in extra deck
    - isSpeed [bool]: denotes whether the deck is for a Speed Duel or not
    - notes [list[str]]: ordered group of comments related to deck
    - isValid [bool]: denotes whether the deck is a valid deck for play
        - follows banlists
        - has correct number of cards in deck and extra deck

## Card
* should have str class that contains a printout of all information related to a card
* should be initialized from a dict passed in from the database
* Class Inheritance
    - Monster Card
    - Trap Card
    - Spell Card
    - Skill Card
* Attributes
    - passcode [str]: id for the card, not unique
    - name [str]: name for card
    - set_code [str]: set code for the card
    - meta_type [str]: enumerated value for the type of card
        - monster
        - spell
        - trap
        - skill
    - type [list[enum]]: list of tags for the card types
    - frame_type [str]: designates the type of frame for the card; possibly derive from type tags?
        - Possible Values
            - normal
            - effect
            - fusion
            - effect pendulum
            - trap
            - spell
            - link
            - xyz
            - synchro
            - ritual
            - skill
            - token
            - fusion pendulum
            - normal pendulum
            - synchro pendulum
            - xyz pendulum
            - ritual pendulum

## Data Structures
### Card Type Enumeration
* Convert string values for card types to a set of enumerated tags
* YGOPRODECK Values
    - 'Spell Card'
    - 'Effect Monster'
    - 'Normal Monster'
    - 'Flip Effect Monster'
    - 'Trap Card'
    - 'Union Effect Monster'
    - 'Fusion Monster'
    - 'Pendulum Effect Monster'
    - 'Link Monster'
    - 'XYZ Monster'
    - 'Synchro Monster'
    - 'Synchro Tuner Monster'
    - 'Tuner Monster'
    - 'Gemini Monster'
    - 'Normal Tuner Monster'
    - 'Spirit Monster'
    - 'Ritual Effect Monster'
    - 'Skill Card'
    - 'Token'
    - 'Pendulum Effect Fusion Monster'
    - 'Ritual Monster'
    - 'Toon Monster'
    - 'Pendulum Normal Monster'
    - 'Synchro Pendulum Effect Monster'
    - 'Pendulum Tuner Effect Monster'
    - 'XYZ Pendulum Effect Monster'
    - 'Pendulum Effect Ritual Monster'
    - 'Pendulum Flip Effect Monster'
* Enumeration Values
    1. Spell
    2. Effect
    3. Normal
    4. Flip
    5. Union
    6. Fusion
    7. Pendulum
    8. XYZ
    9. Synchro
    10. Tuner
    11. Gemini
    12. Spirit
    13. Ritual
    14. Skill
    15. Token
    16. Toon