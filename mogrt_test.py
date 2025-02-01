import pymiere
import color
from pathlib import Path
from pymiere.objects.premiere_objects import Project

mogrt_path = Path.cwd()/'VW_Text_Caption_MOGRT_9x16_2025.01.mogrt'


app = pymiere.objects.app
project = app.project
sequence = project.activeSequence


# Test inputs to add into the mogrt
test_inputs = { "Text": "Hello World\nthis is a test",
                "Font": "",
                "Size": '50',
                "Faux Bold": "False",
                "Faux Italic": "False",
                "Caps": 1, # 0 = No override. 1 = no caps, 2 = all caps, 3 = small caps
                "Position Offset" : [0,0],
                "Emoji Unicode": "",
                "Emoji Scale Offset": 50,
                'Tilt': 0,
                "Drop Shadow": 2,
                "Tracking Offset": 11,
                "Leading Offset": 0,
                "Text Base Color": "#FFFFFF",
                "Highlight Color" : "#C43EEC",
                "Highlight Scaling": 1,
                "Stroke Width" : 8,
                "Stroke Color": "#000000",
            }

def set_mgt_properties(mgt_clip, settings):

    # Takes properties dict. display_name: value

    # get component hosting modifiable template properties  
    mgt_component = mgt_clip.getMGTComponent()  
    # handle two types, see Note 2 above
    if mgt_component is None:
        # Premiere Pro type, directly use components
        components = mgt_clip.components
    else:
        # After Effects type, everything is hosted by the MGT component
        components = [mgt_component]

    for component in components:
        # iter through MGT properties, display and change values
        for prop in component.properties:
            for key, value in settings.items():
                if prop.displayName.lower() == key.lower():
                    if not "color" in key.lower():
                        print(f"setting value: {key}: {value}")
                        if "position" in key.lower():
                            comp_x = sequence.frameSizeHorizontal
                            comp_y = sequence.frameSizeVertical
                            value = [value[0]/comp_x, value[1]/comp_y]
                        prop.setValue(value, True)
                    else:
                        if type(value) == list and len(value) == 4:
                            pass
                        elif value[0] == "#" and len(value) == 7:
                            value = color.Color(value).hex_to_adobe_argb()
                        elif value.isdigit():
                            value = int(value)
                        prop.setColorValue(int(value[0]), value[1], value[2], value[3], True)
                    # print("done\n\n\n")


mogrt_track_item = sequence.importMGT(str(mogrt_path), 0, 0, 0)

set_mgt_properties(mogrt_track_item, test_inputs)

print("Done")

breakpoint()

