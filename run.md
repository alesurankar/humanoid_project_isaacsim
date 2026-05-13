
from pathlib import Path
ROOT = Path(r"C:/Users/proje/Desktop/alesurankar/scripts/humanoid_project_isaacsim")

# immediate move
exec(open(ROOT / "scripts" / "_1_joint_move.py").read())

# smooth move
exec(open(ROOT / "scripts" / "_2_smoth_joint_move.py").read())

# read json
exec(open(ROOT / "scripts" / "_3_read_json.py").read())

# dynamic json player
exec(open(ROOT / "scripts" / "live_json_player.py").read())

# json file modifier
python C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\scripts\json_modifier.py