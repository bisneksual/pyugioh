PYUGIOH_TYPE_VALUES_MONSTER = [
    "Effect Monster",
    "Flip Effect Monster",
    "Flip Tuner Effect Monster",
    "Gemini Monster",
    "Normal Monster",
    "Normal Tuner Monster",
    "Ritual Effect Monster",
    "Ritual Monster",
    "Spirit Monster",
    "Toon Monster",
    "Tuner Monster",
    "Union Effect Monster",
]

PYUGIOH_TYPE_VALUES_PEND_MONSTER = [
    "Pendulum Effect Monster",
    "Pendulum Effect Ritual Monster",
    "Pendulum Flip Effect Monster",
    "Pendulum Normal Monster",
    "Pendulum Tuner Effect Monster",
]

PYUGIOH_TYPE_VALUES_EXTRA = [
    "Fusion Monster",
    "Link Monster",
    "Synchro Monster",
    "Synchro Tuner Monster",
    "XYZ Monster",
]

PYUGIOH_TYPE_VALUES_PEND_EXTRA = [
    "Pendulum Effect Fusion Monster",
    "Synchro Pendulum Effect Monster",
    "XYZ Pendulum Effect Monster",
]

PYUGIOH_PEND_DESC_PATTERN = r'\[ Pendulum Effect \] \\n(?P<p_desc>.+)(?:\\n\\n)\[ Monster Effect \] \\n(?P<m_desc>.+)'
PYUGIOH_XD_MATS_PATTERN = r'(?P<mats>.+)(?:\\r\\n)(?P<desc>.+)' # materials for fusion, synchro, and xyz summoning are included at beginning of monster description and separated by CRLF (\r\n)