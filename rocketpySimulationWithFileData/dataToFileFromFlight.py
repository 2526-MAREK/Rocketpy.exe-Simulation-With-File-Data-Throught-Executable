import configparser    
import csv
import rocketpy

class dataToFileFromFlight(rocketpy.Flight):
    def saveDataAboutFlightToFileParser(self, iniFile):
        if self.postProcessed is False:
            self.postProcess()

        config = configparser.ConfigParser()

        config['Position'] = {'x' : str(self.x[:, 1]), # [m]
                              'y' : str(self.y[:, 1]),
                              'z' : str(self.z[:, 1])}
        config['Velocity'] = {'vx' : str(self.vx[:, 1]), # [m/s]
                              'vy' : str(self.vy[:, 1]),
                              'vz' : str(self.vz[:, 1])}   
        config['Acceleration'] = {'ax' : str(self.ax[:, 1]), #[m/s^2]
                                  'ay' : str(self.ay[:, 1]),
                                  'az' : str(self.az[:, 1])}    
        config['AttitudeAngleRespectOXY'] = {'Angle' : str(self.attitudeAngle[:, 1])}                                                                                           
        config['LateralAttitudeAngleRespectOZ'] = {'Angle' : str(self.lateralAttitudeAngle[:, 1])}                                                                                           

        with open(iniFile, 'w') as configfile:
            config.write(configfile)
            
        return None

    def saveDataAboutFlightToFileCsv(self, csvFile):
        if self.postProcessed is False:
            self.postProcess()
        header = ['x','y','z','vx','vy','vz',
        'ax','ay','az',
        'AttitudeAngleRespectOXY','LateralAttitudeAngleRespectOZ','time','velocity','acceleration','mach_number']    

        #print(self.timeSteps)            
        #print(len(self.x[:, 1]), len(self.y[:, 1]), 
        # len(self.z[:, 1]),len(self.vx[:, 1]),len(self.vy[:, 1]),
        # len(self.vz[:, 1]),len(self.ax[:, 1]),
        # len(self.ay[:, 1]),len(self.az[:, 1]),len(self.attitudeAngle[:, 1]),
        # len(self.lateralAttitudeAngle[:, 1]))
        with open(csvFile, 'w', newline='') as csvFile:   
            writer = csv.writer(csvFile)
            writer.writerow(header)
            for i in range(len(self.x[:, 1])):
                if i == len(self.x[:, 1])-1:
                    writer.writerow([self.x[:, 1][i],self.y[:, 1][i],
                    self.z[:, 1][i],self.vx[:, 1][i],
                    self.vy[:, 1][i],self.vz[:, 1][i],0,0,0,
                    self.attitudeAngle[:, 1][i],self.lateralAttitudeAngle[:, 1][i],i,self.speed[:, 1][i],0  ,self.MachNumber[:, 1][i]])
                else:
                    writer.writerow([self.x[:, 1][i],self.y[:, 1][i],self.z[:, 1][i],
                    self.vx[:, 1][i],self.vy[:, 1][i],self.vz[:, 1][i],self.ax[:, 1][i],
                    self.ay[:, 1][i],self.az[:, 1][i],self.attitudeAngle[:, 1][i],
                    self.lateralAttitudeAngle[:, 1][i],i ,self.speed[:, 1][i], self.acceleration[:, 1][i]  ,self.MachNumber[:, 1][i]])
    
        return None