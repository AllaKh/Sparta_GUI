import VISADriver.VisaInterface as VISAHandel

class cls_GDM_8261A():
    __Instrument=0
    def __init__(self, ControllerID="0", ConnecationType="GPIB",Address="5"):
        global Instrument
        if ConnecationType=="GPIB":
            self.__Instrument = VISAHandel.ConnectToGPIBInstrument(ControllerID, Address)
        else:
            self.__Instrument = VISAHandel.ConnectToLocalLANInstrument(ControllerID, Address)

    def fnIDNInstrument(self):
        return VISAHandel.IDNInstrument(self.__Instrument)

    def fnRSTInstrument(self):
        VISAHandel.WriteSCPICmd(self.__Instrument,"*RST")

    def fnTSTInstrument(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"*TST?")

    def fnGetVoltage(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASURE:VOLTAGE:DC?")

    def fnGetCurrent(self):
        return VISAHandel.QuerySCPICmd(self.__Instrument,"MEASURE:CURRENT:DC?")



if __name__ == '__main__':

    from Equipment import GWINSTEK_GDM8261A_DMM

    dmm11 = GWINSTEK_GDM8261A_DMM.cls_GDM_8261A(ControllerID="0", ConnecationType="GPIB", Address='5')

    print(dmm11.fnGetVoltage())
