import json



def generate_manifest(track, output_path):
    with open(output_path, "w") as f:
        json.dump(track.__dict__, f, indent=2)
