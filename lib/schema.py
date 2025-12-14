YGODECKSCHEMA = """
$schema: https://json-schema.org/draft-07/schema#
description: A Yu-Gi-Oh! deck to be saved by Pyugioh
properties:
  deck:
    additionalProperties: false
    properties:
      cards:
        description: A list of the cards in the deck based on the different zones
          available
        properties:
          extra:
            description: A list of cards in the Extra Deck zone
            type: array
          main:
            description: A list of cards in the Main Deck zone
            items:
              anyOf:
              - exclusiveMinimum: 0
                type: integer
              - type: string
              - additionalProperties:
                  minimum: 1
                  type: integer
                type: object
            type: array
          side:
            description: A list of cards in the Side Deck zone
            type: array
          skill:
            description: A list of Skill Cards to be used with the deck
            type: array
        type: object
      coll-id:
        description: A stored UUID that connects the real deck to a collection to
          be validated against.
        type: string
      comments:
        description: A place to store certain notes or reminders regarding the deck
        type: string
      fantasy:
        description: An indicator of whether the deck is a real or fantasy deck
        type: boolean
      game:
        description: The designator for the game that the deck is meant for
        type: string
      name:
        description: The name assigned to the deck by the user
        type: string
    required:
    - game
    - name
    - fantasy
    - cards
    type: object
required:
- deck
title: YGODeck
"""