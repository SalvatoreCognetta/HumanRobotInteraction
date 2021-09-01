# Human-Pepper™ Interaction: Your MoMA assistant 

This project was developed during the 2020 Human-Robot interaction (HRI) course held by [Prof. Iocchi](https://sites.google.com/a/dis.uniroma1.it/iocchi/home) at [Sapienza University of Rome](https://www.uniroma1.it/).

The project was intended to be deployed on the real [Pepper™ robot](https://www.softbankrobotics.com/emea/it/pepper), but due to COVID-19 emergency, it has been developed in a remote fashion using [MODIM](https://bitbucket.org/mtlazaro/modim/src/master/), [NaoQI](http://doc.aldebaran.com/2-5/index_dev_guide.html).

The purpose of this HRI application is to help the user find useful information about the Museum of Modern Art thanks to a Pepper™ robot.

## Summary

  - [Getting Started](#getting-started)
  - [Runing the tests](#running-the-tests)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes. 

### Prerequisites

- (tested) Ubuntu 18.04 or newer or (not tested) other Linux distribution
- Python3

### Installing

You can find installation notes on the environment to emulate Pepper™ robot
in [docker folder](https://github.com/giabb/human-pepper-interaction/tree/main/docker/README.md).

## Running the tests

You can find instructions on running all the tests you want both in [docker folder](https://github.com/giabb/human-pepper-interaction/tree/main/docker/README.md) 
and in [this video](https://github.com/giabb/human-pepper-interaction/blob/main/demo.mp4). 
Some scripts shown in the video are not present in this folder because they are just some scripts to simplify the sintax of [pepper-tools](https://bitbucket.org/mtlazaro/pepper_tools/src/master/).

If you want to change the behaviour of Pepper™, you can edit the files in [action folder](https://github.com/giabb/human-pepper-interaction/tree/main/src/actions/)
and the [Python script](https://github.com/giabb/human-pepper-interaction/tree/main/src/scripts/start.py)

## Authors

- **Giovanbattista Abbate** - [giabb](https://github.com/giabb)
- **Mario Fiorino**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- **Prof. Luca Iocchi** - *Provided Pepper™ environment* - [personal site](https://sites.google.com/a/dis.uniroma1.it/iocchi/home)
- **Billie Thompson** - *Provided README Template* - [PurpleBooth](https://github.com/PurpleBooth)
