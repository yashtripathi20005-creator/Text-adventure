"""
Story data for the text adventure game.
Each node represents a scene with text, actions, and possible effects.
"""

story_data = {
    'start': {
        'id': 'start',
        'title': 'The Mysterious Island',
        'text': """You wake up on a strange island with no memory of how you got here.
        The sun is warm, and you hear birds singing in the nearby forest.
        To the north, you see a dense jungle. To the east, there's a beach.
        A worn path leads south toward a mountain.""",
        'actions': {
            'go_north': {
                'message': 'You push through the thick vegetation and enter the jungle...',
                'next': 'jungle'
            },
            'go_east': {
                'message': 'You walk across the sandy beach, feeling the warm sand between your toes...',
                'next': 'beach'
            },
            'go_south': {
                'message': 'You follow the path toward the mountain...',
                'next': 'mountain_path'
            },
            'inspect': {
                'message': 'You look around. You notice a glint of metal in the sand near your feet.',
                'next': 'start',
                'effects': {
                    'add_item': 'rusty_key'
                }
            }
        }
    },
    
    'jungle': {
        'id': 'jungle',
        'title': 'The Dense Jungle',
        'text': """The jungle is dark and humid. Vines hang from every tree.
        You can hear strange animal calls in the distance.
        There's an old temple covered in moss to your left, and a path continuing north.""",
        'actions': {
            'go_north': {
                'message': 'You push deeper into the jungle...',
                'next': 'jungle_deep'
            },
            'enter_temple': {
                'message': 'You approach the ancient temple. The stone door is heavy but opens with a groan...',
                'next': 'temple',
                'condition': {'has_item': 'rusty_key'}
            },
            'go_back': {
                'message': 'You return to the starting area.',
                'next': 'start'
            },
            'search': {
                'message': 'You search the area and find a sturdy branch that could be used as a weapon.',
                'effects': {'add_item': 'sturdy_branch'},
                'next': 'jungle'
            }
        }
    },
    
    'beach': {
        'id': 'beach',
        'title': 'The Sandy Beach',
        'text': """The beach stretches along the coastline as far as you can see.
        Waves gently lap at the shore. You see a small cave in the cliff face.
        A rowboat is pulled up on the sand, but it has a hole in it.""",
        'actions': {
            'enter_cave': {
                'message': 'You enter the dark cave. It\'s cool and damp inside...',
                'next': 'cave'
            },
            'examine_boat': {
                'message': 'You examine the rowboat. There\'s a repair kit inside!',
                'effects': {'add_item': 'repair_kit'},
                'next': 'beach'
            },
            'go_back': {
                'message': 'You walk back toward the center of the island.',
                'next': 'start'
            }
        }
    },
    
    'mountain_path': {
        'id': 'mountain_path',
        'title': 'The Mountain Path',
        'text': """The path winds upward through rocky terrain.
        The air gets thinner as you climb. You see an old cabin ahead.
        A narrow ledge leads around the mountain.""",
        'actions': {
            'enter_cabin': {
                'message': 'You approach the cabin. The door creaks open...',
                'next': 'cabin'
            },
            'take_ledge': {
                'message': 'You carefully edge along the narrow ledge...',
                'next': 'ledge',
                'condition': {'has_item': 'sturdy_branch'}
            },
            'go_back': {
                'message': 'You descend back to the starting area.',
                'next': 'start'
            }
        }
    },
    
    'temple': {
        'id': 'temple',
        'title': 'The Ancient Temple',
        'text': """Inside the temple, you find a treasure chest!
        The walls are covered in ancient hieroglyphs.
        A golden amulet sits on an altar in the center of the room.""",
        'actions': {
            'open_chest': {
                'message': 'You open the chest and find a golden coin!',
                'effects': {'add_item': 'golden_coin'},
                'next': 'temple'
            },
            'take_amulet': {
                'message': 'You take the golden amulet. Suddenly, the ground begins to shake!',
                'effects': {'add_item': 'golden_amulet'},
                'next': 'temple_exit'
            },
            'go_back': {
                'message': 'You leave the temple and return to the jungle.',
                'next': 'jungle'
            }
        }
    },
    
    'temple_exit': {
        'id': 'temple_exit',
        'title': 'The Temple Collapses!',
        'text': """The temple collapses around you as you flee!
        You barely escape with your life, clutching the golden amulet.
        You hear a voice in your head: "Return the amulet to the volcano..." """,
        'actions': {
            'go_volcano': {
                'message': 'You feel compelled to go to the volcano...',
                'next': 'volcano'
            }
        }
    },
    
    'cave': {
        'id': 'cave',
        'title': 'The Dark Cave',
        'text': """The cave is deep and dark. You hear water dripping somewhere.
        You feel something brush against your leg - it\'s a friendly cat!
        The cat seems to want you to follow it deeper into the cave.""",
        'actions': {
            'follow_cat': {
                'message': 'You follow the cat through winding tunnels...',
                'next': 'cave_depth'
            },
            'go_back': {
                'message': 'You leave the cave and return to the beach.',
                'next': 'beach'
            }
        }
    },
    
    'cave_depth': {
        'id': 'cave_depth',
        'title': 'The Deep Cave',
        'text': """The cat leads you to an underground lake.
        The water is crystal clear, and you can see ancient ruins beneath the surface.
        A boat is tied to a dock nearby.""",
        'actions': {
            'take_boat': {
                'message': 'You untie the boat and push off into the underground lake...',
                'next': 'underground_river',
                'condition': {'has_item': 'repair_kit'}
            },
            'go_back': {
                'message': 'You follow the cat back to the cave entrance.',
                'next': 'cave'
            }
        }
    },
    
    'underground_river': {
        'id': 'underground_river',
        'title': 'The Underground River',
        'text': """You float down the underground river. The current is strong!
        You see a light ahead - it\'s the exit! You emerge in a hidden valley.
        In the center of the valley is the volcano.""",
        'actions': {
            'enter_volcano': {
                'message': 'You approach the volcano. The heat is intense...',
                'next': 'volcano'
            }
        }
    },
    
    'cabin': {
        'id': 'cabin',
        'title': 'The Mountain Cabin',
        'text': """The cabin is cozy and warm. A fire crackles in the fireplace.
        You find a diary on the table. It tells of a treasure hidden on the island.
        The diary mentions a key that can unlock the temple.""",
        'actions': {
            'read_diary': {
                'message': 'You read more of the diary. It says: "The key is buried near the old oak tree at the beach."',
                'next': 'cabin'
            },
            'search_cabin': {
                'message': 'You search the cabin and find a compass!',
                'effects': {'add_item': 'compass'},
                'next': 'cabin'
            },
            'go_back': {
                'message': 'You leave the cabin and return to the mountain path.',
                'next': 'mountain_path'
            }
        }
    },
    
    'ledge': {
        'id': 'ledge',
        'title': 'The Narrow Ledge',
        'text': """You carefully balance on the ledge. Using your branch as a walking stick, you make it across.
        You find a hidden alcove with a treasure chest!""",
        'actions': {
            'open_chest': {
                'message': 'You open the chest and find a magical ring!',
                'effects': {'add_item': 'magical_ring'},
                'next': 'mountain_path'
            }
        }
    },
    
    'volcano': {
        'id': 'volcano',
        'title': 'The Volcano Summit',
        'text': """You stand at the edge of the volcano. Lava bubbles below.
        The golden amulet glows brightly in your hand.
        You must decide what to do with it...""",
        'actions': {
            'throw_amulet': {
                'message': 'You throw the amulet into the volcano. The ground shakes violently!
                The volcano erupts, but you escape just in time.
                The island is saved! You are hailed as a hero!
                YOU WIN! 🎉',
                'next': 'win',
                'condition': {'has_item': 'golden_amulet'},
                'effects': {'remove_item': 'golden_amulet'}
            },
            'keep_amulet': {
                'message': 'You decide to keep the amulet. A dark shadow falls over the island.
                The volcano erupts, destroying everything.
                GAME OVER! 💀',
                'next': 'game_over'
            }
        }
    },
    
    'win': {
        'id': 'win',
        'title': '🏆 VICTORY! 🏆',
        'text': """Congratulations! You have saved the island and its inhabitants.
        Your bravery and wisdom will be remembered forever.
        You found the golden amulet and made the right choice.
        Thank you for playing!""",
        'game_over': True,
        'actions': {
            'restart': {
                'message': 'Starting a new game...',
                'next': 'start'
            }
        }
    },
    
    'game_over': {
        'id': 'game_over',
        'title': '💀 GAME OVER 💀',
        'text': """Unfortunately, your journey has come to an end.
        But every ending is a new beginning!
        Would you like to try again?""",
        'game_over': True,
        'actions': {
            'restart': {
                'message': 'Starting a new game...',
                'next': 'start'
            }
        }
    },
    
    'jungle_deep': {
        'id': 'jungle_deep',
        'title': 'The Deep Jungle',
        'text': """You venture deep into the jungle. The canopy blocks out most of the sunlight.
        You discover an ancient stone circle. In the center, there\'s a pedestal with a glowing orb.""",
        'actions': {
            'take_orb': {
                'message': 'You take the glowing orb. It pulses with warmth in your hands.',
                'effects': {'add_item': 'glowing_orb'},
                'next': 'jungle_deep'
            },
            'go_back': {
                'message': 'You return to the main jungle area.',
                'next': 'jungle'
            }
        }
    }
}
