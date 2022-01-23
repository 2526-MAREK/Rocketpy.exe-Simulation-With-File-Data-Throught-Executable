from rocketpy import Environment, Rocket, SolidMotor, Flight
from dataFromParser import dataFromParser
from dataToFileFromFlight import dataToFileFromFlight

Data = dataFromParser()

Data.openFileParser('input.ini')

from netCDF4 import Dataset

Env = Environment(
    railLength=Data.Config.getfloat("Environment", "railLength"), 
    latitude=Data.Config.getfloat("Environment", "latitude"),
    longitude=Data.Config.getfloat("Environment", "longitude"),
    elevation=Data.Config.getfloat("Environment", "elevation"),
    date=(Data.Config.getint("Environment", "year"),Data.Config.getint("Environment", "month"),Data.Config.getint("Environment", 
    "day"),Data.Config.getint("Environment", "hourToDateInEnvironment")) # Tomorrow's date in year, month, day, hour UTC format
) 

import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=Data.Config.getint("toMethodsOfClassEnvironment", "days"))

Env.setDate((tomorrow.year, tomorrow.month, tomorrow.day, Data.Config.getint("toMethodsOfClassEnvironment", "hourToSetDate"))) # Hour given in UTC time

Env.setAtmosphericModel(type=Data.Config.get("toMethodsOfClassEnvironment",'type'), 
                        pressure=None,
                        temperature=Data.Config.getfloat("toMethodsOfClassEnvironment",'temperature'),
                        wind_u=[(Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_u1'), 
                        Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_u2')), (Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_u3'),
                         Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_u4')), 
                         (Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_u5'), Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_u6'))],
                        wind_v=[(Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_v1'), 
                        Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_v2')), (Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_v3'),
                         Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_v4')), 
                         (Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_v5'), Data.Config.getfloat("toMethodsOfClassEnvironment",'wind_v6'))])

motor = SolidMotor(
    thrustSource=Data.Config.get("SolidMotor",'thrustSource'), #Config
    burnOut=Data.Config.getfloat("SolidMotor", "burnOut"),
    grainNumber=Data.Config.getint("SolidMotor", "grainNumber"),
    grainSeparation=Data.Config.getfloat("SolidMotor", "grainSeparation"),
    grainDensity=Data.Config.getint("SolidMotor", "grainDensity"),
    grainOuterRadius=Data.Config.getfloat("SolidMotor", "grainOuterRadius"),
    grainInitialInnerRadius=Data.Config.getfloat("SolidMotor", "grainInitialInnerRadius"),
    grainInitialHeight=Data.Config.getfloat("SolidMotor", "grainInitialHeight"),
    nozzleRadius=Data.Config.getfloat("SolidMotor", "nozzleRadius"),
    throatRadius=Data.Config.getfloat("SolidMotor", "throatRadius"),
    interpolationMethod=Data.Config.get("SolidMotor", "interpolationMethod")
)

R4S = Rocket(
    motor=motor,
    radius=Data.Config.getfloat("Rocket", "radius"),
    mass=Data.Config.getfloat("Rocket", "mass"),
    inertiaI=Data.Config.getfloat("Rocket", "inertiaI"),
    inertiaZ=Data.Config.getfloat("Rocket", "inertiaZ"),
    distanceRocketNozzle=Data.Config.getfloat("Rocket", "distanceRocketNozzle"),
    distanceRocketPropellant=Data.Config.getfloat("Rocket", "distanceRocketPropellant"),
    powerOffDrag=Data.Config.get("Rocket", "powerOffDrag"),
    powerOnDrag=Data.Config.get("Rocket", "powerOnDrag")
)

R4S.setRailButtons([Data.Config.getfloat("toMethodsOfClassRocketSetRailButtons", "RailButtons1"), Data.Config.getfloat("toMethodsOfClassRocketSetRailButtons", "RailButtons2")])

NoseCone = R4S.addNose(length=Data.Config.getfloat("toMethodsOfClassRocketAddNose", "lengthToNose"), kind=Data.Config.get("toMethodsOfClassRocketAddNose", "kindToNose"),
 distanceToCM=Data.Config.getfloat("toMethodsOfClassRocketAddNose", "distanceToCMToNose"))

FinSet = R4S.addFins(Data.Config.getint("toMethodsOfClassRocketAddFins", "numberOfFins"), span=Data.Config.getfloat("toMethodsOfClassRocketAddFins", "span"), 
rootChord=Data.Config.getfloat("toMethodsOfClassRocketAddFins", "rootChord"), tipChord=Data.Config.getfloat("toMethodsOfClassRocketAddFins", "tipChord"), 
distanceToCM=Data.Config.getfloat("toMethodsOfClassRocketAddFins", "distanceToCMToFins"))

#Tail = R4S.addTail(topRadius=Data.Config.getfloat("toMethodsOfClassRocketAddTail", "topRadius"), bottomRadius=Data.Config.getfloat("toMethodsOfClassRocketAddTail", 
# "bottomRadius"), length=Data.Config.getfloat("toMethodsOfClassRocketAddTail", "lengthToTail"), distanceToCM=Data.Config.getfloat("toMethodsOfClassRocketAddTail", "distanceToCMToTail"))

def drogueTrigger(p, y):
    return True if y[Data.Config.getint("definitionOfParachutes", "vz1")] < Data.Config.getint("definitionOfParachutes", "activateDrogueParachutesWhenVz") else False
 # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.

def mainTrigger(p, y):
    return True if y[Data.Config.getint("definitionOfParachutes", 
    "vz2")] < Data.Config.getint("definitionOfParachutes", "activateMainParachutesWhenVz") and y[Data.Config.getint("definitionOfParachutes", "z")] < Data.Config.getint("definitionOfParachutes",
     "activateMainParachutesWhenWhenZ") else False
# p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).

Main = R4S.addParachute(Data.Config.get("addParachuteMain", "NameOfParachutes1"),
                            CdS=Data.Config.getfloat("addParachuteMain", "CdSToMainParachute"),
                            trigger=mainTrigger, 
                            samplingRate=Data.Config.getfloat("addParachuteMain", "samplingRateToMainParachute"),
                            lag=Data.Config.getfloat("addParachuteMain", "lagToMainParachute"),
                            noise=(Data.Config.getfloat("addParachuteMain", "noise1ToMainParachute"), Data.Config.getfloat("addParachuteMain", "noise2ToMainParachute"),
                             Data.Config.getfloat("addParachuteMain", "noise3ToMainParachute")))

Drogue = R4S.addParachute(Data.Config.get("addParachuteDrogue", "NameOfParachutes2"),
                              CdS=Data.Config.getfloat("addParachuteDrogue", "CdSToDrogueParachute"),
                              trigger=drogueTrigger, 
                              samplingRate=Data.Config.getfloat("addParachuteDrogue", "samplingRateToDrogueParachute"),
                              lag=Data.Config.getfloat("addParachuteDrogue", "lagToDrogueParachute"),
                              noise=(Data.Config.getfloat("addParachuteDrogue", "noise1ToDrogueParachute"),
                               Data.Config.getfloat("addParachuteDrogue", "noise2ToDrogueParachute"), Data.Config.getfloat("addParachuteDrogue", "noise3ToDrogueParachute")))

TestFlight = dataToFileFromFlight(rocket=R4S, environment=Env, inclination=Data.Config.getfloat("toConstructorOfClassFlight", "inclination"), heading=Data.Config.getfloat("toConstructorOfClassFlight", "heading"))

#TestFlight.saveDataAboutFlightToFileParser("dataFromRocketpyToSimulator.ini")
TestFlight.saveDataAboutFlightToFileCsv("output.csv")
TestFlight.plot3dTrajectory()

