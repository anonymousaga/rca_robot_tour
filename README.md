# [<img src="icon.png" width="40"/>](icon.png)  Robot Coaching Assistant (RCA)

A tool to simulate a robot's path for robot tour in Science Olympiad. \
⚠️You MUST set up `compileCommands` to use this. [How to configure compileCommands](docs/COMPILE_COMMANDS.md)

## Usage
* Select a start point using the grid: \
  <img src="docs/selector_grid.png" width="250"/>
* Paste in or type in your robot's movements, and the path will show up!
* Click `Robot Moving Animation` to get an animation of the path

### Settings
* **Track Size:** size of the robot tour course. 4x4 for 2023-24, 4x5 for 2024-25
* **Starting Dot Offset** (default: 0): How far, in cm, the icon is from the course's edge when starting. Useful when the first move is longer than expected in order to align the center of the robot with the center of the box. For example, my bot travels 32cm instead of 25cm on the first move because the dowel is 7cm in front of the center.
* **Dark Mode for Map:** invert the colors of the map
* **Robot Moving Speed:** the speed of the robot moving animation
* **compileCommands Function:** read [how to configure compileCommands](docs/COMPILE_COMMANDS.md)

### Screenshots
![screenshot_of_map](docs/screenshot1.jpg)
*Map with a robot course*\
&nbsp;\
![screenshot_of_map](docs/screenshot2.jpg)
*Page to enter path*\
&nbsp;\
![screenshot_of_map](docs/screenshot3.jpg)
*Settings of the app*

## Troubleshooting
- **macOS:** `“Robot Coaching Assistant.app” is damaged and can’t be opened.` can be fixed by running this command in terminal:
    ````
    xattr -rd com.apple.quarantine /Applications/Robot\ Coaching\ Assistant.app
    ````




### Building From Source
See [building from source](docs/BUILDING_SRC.md)
