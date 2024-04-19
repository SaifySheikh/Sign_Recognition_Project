---

# Sign Language to Text Converter

Welcome to the Sign Language to Text Converter project! This application utilizes a convolutional neural network (CNN) to recognize hand signs and translate them into text in real-time. Whether you're learning sign language or need assistance communicating with individuals who are deaf or hard of hearing, this tool aims to bridge the gap by providing accurate and efficient sign language recognition.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Contributing](#contributing)
6. [License](#license)

## Getting Started

To get started with the Sign Language to Text Converter, follow the installation instructions below.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/SaifySheikh/Sign_Recognition_Project.git
```

2. Navigate to the project directory:

```bash
cd Sign_Recognition_Project
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure you have MongoDB installed and running on your system. This application uses MongoDB to store suggestions for the sign language words.

## Usage

1. Run the `realtimedetection.py` script:

```bash
python realtimedetection.py
```

2. Once the application is running, you will see a real-time video feed from your webcam. Perform sign language gestures in front of the camera, and the application will recognize and display the corresponding text on the screen.

3. As you sign, the application will also provide suggestions for completing words or phrases based on the signs you've made. These suggestions are fetched from a MongoDB database.

4. Use the audio button to hear the recognized text spoken aloud.

## Features

- Real-time sign language recognition using a CNN.
- Integration with MongoDB for storing and retrieving suggestions.
- Audio playback of recognized text.
- User-friendly interface with suggestions for completing words or phrases.

## Contributing

Contributions to the Sign Language to Text Converter project are welcome! If you encounter any bugs or have suggestions for improvements, please open an issue on GitHub or submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to expand upon each section with more detailed instructions, screenshots, or additional information as needed. Happy coding!
